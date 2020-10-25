---
author: Greg Sabino Mullane
gh_issue_number: 1231
tags: bucardo, postgres, database
title: Bucardo replication workarounds for extremely large Postgres updates
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2016/05/31/bucardo-replication-workarounds-for/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/05/31/bucardo-replication-workarounds-for/image-0.jpeg"/></a><br/><small>(<a href="https://flic.kr/p/iiRxFT">photograph</a> by <a href="https://www.flickr.com/photos/pagedooley/">Kevin Dooley</a>)</small></div>

[Bucardo](https://bucardo.org/) is very good at replicating data among 
[Postgres](https://www.postgresql.org/) databases 
(as well as replicating to other things, such as 
[MariaDB](http://mariadb.org), Oracle, and 
[Redis](http://redis.io)!). 
However, sometimes you need to work outside the normal flow 
of trigger-based replication systems such as Bucardo. One such scenario 
is when many changes need to be made to your replicated tables. And by a lot, I mean many millions of rows. When this 
happens, it may be faster and easier to find an alternate way to replicate those 
changes.

When a change is made to a table that is being replicated by Bucardo, a 
trigger fires and stores the primary key of the row that was changed into 
a “delta” table. Then the Bucardo daemon comes along, gathers a list of all rows that 
were changed since the last time it checked, and pushes those rows to 
the other databases in the sync (a named replication set). Although all of this is 
done in a fast and efficient manner, there is a bit of overhead that 
adds up when (for example), updating 650 million rows in one 
transaction.

The first and best solution is to simply hand-apply all the changes 
yourself to every database you are replicating to. By disabling the 
Bucardo triggers first, you can prevent Bucardo from even knowing, or caring, 
that the changes have been made.

To demonstrate this, let’s have Bucardo replicate among five 
[pgbench](https://www.postgresql.org/docs/current/static/pgbench.html) databases, 
called A, B, C, D, and E. Databases A, B, and C will be sources; D and E are just targets. Our replication looks like this: ( A <=> B <=> C ) => (D, E). First, we create all the databases and populate them:

```
## Create a new cluster for this test, and use port 5950 to minimize impact
$ initdb --data-checksums btest
$ echo port=5950 >> btest/postgresql.conf
$ pg_ctl start -D btest -l logfile

## Create the main database and install the pg_bench schema into it
$ export PGPORT=5950
$ createdb alpha
$ pgbench alpha -i --foreign-keys

## Replicated tables need a primary key, so we need to modify things a little:
$ psql alpha -c 'alter table pgbench_history add column hid serial primary key'

## Create the other four databases as exact copies of the first one:
$ for dbname in beta gamma delta epsilon; do createdb $dbname -T alpha; done
```

Now that those are done, let’s install Bucardo, teach it about these 
databases, and create a sync to replicate among them as described above.

```
$ bucardo install --batch
$ bucardo add dbs A,B,C,D,E dbname=alpha,beta,gamma,delta,epsilon dbport=5950
$ bucardo add sync fiveway tables=all dbs=A:source,B:source,C:source,D:target,E:target

## Tweak a few default locations to make our tests easier:
$ echo -e "logdest=.\npiddir=." > .bucardorc
```

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/05/31/bucardo-replication-workarounds-for/image-1.png" id="gtsm.com/bucardo_fiveway.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/05/31/bucardo-replication-workarounds-for/image-1.png"/></a></div>

At this point, we have five databases all ready to go, and Bucardo is setup to 
replicate among them. Let’s do a quick test to make sure everything is working as 
it should.

```
$ bucardo start
Checking for existing processes
Starting Bucardo

$ for db in alpha beta gamma delta epsilon; do psql $db -Atc "select '$db',sum(abalance) from pgbench_accounts";done | tr "\n" " "
alpha|0 beta|0 gamma|0 delta|0 epsilon|0

$ pgbench alpha
starting vacuum...end.
transaction type: TPC-B (sort of)
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
number of transactions per client: 10
number of transactions actually processed: 10/10
latency average: 0.000 ms
tps = 60.847066 (including connections establishing)
tps = 62.877481 (excluding connections establishing)

$ for db in alpha beta gamma delta epsilon; do psql $db -Atc "select '$db',sum(abalance) from pgbench_accounts";done | tr "\n" " "
alpha|6576 beta|6576 gamma|6576 delta|6576 epsilon|6576

$ pgbench beta
starting vacuum...end.
...
tps = 60.728681 (including connections establishing)
tps = 62.689074 (excluding connections establishing)
$ for db in alpha beta gamma delta epsilon; do psql $db -Atc "select '$db',sum(abalance) from pgbench_accounts";done | tr "\n" " "
alpha|7065 beta|7065 gamma|7065 delta|7065 epsilon|7065
```

Let’s imagine that the bank discovered a huge financial error, and needed to increase the balance of 
every account created in the last two years by 20 dollars. Let’s further imagine that this involved 
650 million customers. That UPDATE will take a very long time, but will suffer even more because 
each update will also fire a Bucardo trigger, which in turn will write to another “delta” table. Then, Bucardo 
will have to read in 650 million rows from the delta table, and (on every other database in the sync) 
apply those changes by deleting 650 million rows then COPYing over the correct values. This is 
one situation where you want to sidestep your replication and handle things yourself. There are 
three solutions to this. The easiest, as mentioned, is to simply do all the changes yourself and 
prevent Bucardo from worrying about it.

The basic plan is to apply the updates on all the databases in the syncs at once, while using 
the session_replication_role feature to prevent the triggers from firing. Of course, this will 
prevent *all* of the triggers on the table from firing. If there are some non-Bucardo triggers 
that must fire during this update, you might wish to temporarily set them as ALWAYS triggers. 

### Solution one: manual copy

```
## First, stop Bucardo. Although not necessary, the databases are going to be busy enough
## that we don't need to worry about Bucardo at the moment.
$ bucardo stop
Creating ./fullstopbucardo ... Done

## In real-life, this query should get run in parallel across all databases,
## which would be on different servers:
$ QUERY='UPDATE pgbench_accounts SET abalance = abalance + 25 WHERE aid > 78657769;'

$ for db in alpha beta gamma delta epsilon; do psql $db -Atc "SET session_replication_role='replica'; $QUERY"; done | tr "\n" " "
UPDATE 83848570 UPDATE 83848570 UPDATE 83848570 UPDATE 83848570 UPDATE 83848570 

## For good measure, confirm Bucardo did not try to replicate all those rows:
$ bucardo kick fiveway
Kicked sync fiveway

$ grep Totals log.bucardo
(11144) [Mon May 16 23:08:57 2016] KID (fiveway) Totals: deletes=36 inserts=28 conflicts=0
(11144) [Mon May 16 23:09:02 2016] KID (fiveway) Totals: deletes=38 inserts=29 conflicts=0
(11144) [Mon May 16 23:09:22 2016] KID (fiveway) Totals: deletes=34 inserts=27 conflicts=0
(11144) [Tue May 16 23:15:08 2016] KID (fiveway) Totals: deletes=10 inserts=7 conflicts=0
(11144) [Tue May 16 23:59:00 2016] KID (fiveway) Totals: deletes=126 inserts=73 conflicts=0
```

### Solution two: truncate the delta

As a second solution, what about the event involving a junior DBA who made all those updates on one 
of the source databases without disabling triggers? When this happens, you would probably find that 
your databases are all backed up and waiting for Bucardo to handle the giant replication 
job. If the rows that have changed constitute most of the total rows in the table, 
your best bet is to simply copy the entire table. You will also need to stop the Bucardo daemon, 
and prevent it from trying to replicate those rows when it starts up by cleaning out the 
delta table. As a first step, stop the main Bucardo daemon, and then forcibly stop any active 
Bucardo processes:

```
$ bucardo stop
Creating ./fullstopbucardo ... Done

$ pkill -15 Bucardo
```

Now to clean out the delta table. In this example, the junior DBA updated the “beta”
database, so we look there. We may go ahead and truncate it because we are going to 
copy the entire table after that point.

```
# The delta tables follow a simple format. Make sure it is the correct one
$ psql beta -Atc 'select count(*) from bucardo.delta_public_pgbench_accounts'
650000000
## Yes, this must be the one!

## Truncates are dangerous; be extra careful from this point forward
$ psql beta -Atc 'truncate table bucardo.delta_public_pgbench_accounts'
```

The delta table will continue to accumulate changes as applications update the 
table, but that is okay—​we got rid of the 650 million rows. Now we know 
that beta has the canonical information, and we need to get it to all the 
others. As before, we use session_replication_role. However, we also need 
to ensure that nobody else will try to add rows before our COPY gets 
in there, so if you have active source databases, pause your applications. 
Or simply shut them out for a while via pg_hba.conf! Once that is done, 
we can copy the data until all databases are identical to “beta”:

```
$ ( echo "SET session_replication_role='replica'; TRUNCATE TABLE pgbench_accounts; " ; pg_dump beta --section=data -t pgbench_accounts ) | psql alpha -1 --set ON_ERROR_STOP=on
SET
ERROR:  cannot truncate a table referenced in a foreign key constraint
DETAIL:  Table "pgbench_history" references "pgbench_accounts".
HINT:  Truncate table "pgbench_history" at the same time, or use TRUNCATE ... CASCADE.
```

Aha! Note that we used the --foreign-keys option when creating the pgbench tables above. 
We will need to remove the foreign key, or simply copy both tables together. Let’s 
do the latter:

```
$ ( echo "SET session_replication_role='replica'; TRUNCATE TABLE pgbench_accounts, pgbench_history; " ; pg_dump beta --section=data -t pgbench_accounts \
  -t pgbench_history) | psql alpha -1 --set ON_ERROR_STOP=on
SET
TRUNCATE TABLE
SET
SET
SET
SET
SET
SET
SET
SET
COPY 100000
COPY 10
 setval 
--------
     30
(1 row)
## Do the same for the other databases:
$ for db in gamma delta epsilon; do \
 ( echo "SET session_replication_role='replica'; TRUNCATE TABLE pgbench_accounts, pgbench_history; " ; pg_dump $db --section=data -t pgbench_accounts \
  -t pgbench_history) | psql alpha -1 --set ON_ERROR_STOP=on ; done
```

Note: if your tables have a lot of constraints or indexes, you may want to disable those 
to speed up the COPY. Or even turn fsync off. But that's the topic of another post.

### Solution three: delta excision

Our final solution is a variant on the last one. As before, the junior DBA has done a mass 
update of one of the databases involved in the Bucardo sync. But this time, you decide it 
should be easier to simply remove the deltas and apply the changes manually. As before, 
we shut down Bucardo. Then we determine the timestamp of the mass change by checking the 
delta table closely:

```
$ psql beta -Atc 'select txntime, count(*) from bucardo.delta_public_pgbench_accounts group by 1 order by 2 desc limit 3'
2016-05-26 23:23:27.252352-04|65826965
2016-05-26 23:23:22.460731-04|80
2016-05-07 23:20:46.325105-04|73
2016-05-26 23:23:33.501002-04|69
```

Now we want to carefully excise those deltas. With that many rows, it is quicker to save/truncate/copy than 
to do a delete:

```
$ psql beta
beta=# BEGIN;
BEGIN
## To prevent anyone from firing the triggers that write to our delta table
beta=#LOCK TABLE pgbench_accounts;
LOCK TABLE
## Copy all the delta rows we want to save:
beta=# CREATE TEMP TABLE bucardo_store_deltas AS SELECT * FROM bucardo.delta_public_pgbench_accounts WHERE txntime <> '2016-05-07 23:20:46.325105-04';
SELECT 1885
beta=# TRUNCATE TABLE bucardo.delta_public_pgbench_accounts;
TRUNCATE TABLE
## Repopulate the delta table with our saved edits
beta=# INSERT INTO bucardo.delta_public_pgbench_accounts SELECT * FROM bucardo_store_deltas;
INSERT 0 1885
## This will remove the temp table
beta=# COMMIT;
COMMIT
```

Now that the deltas are removed, we want to emulate what caused them on all the other servers. Note that 
this query is a contrived one that may lend itself to concurrency issues. If you go this route, make 
sure your query will produce the exact same results on all the servers.

```
## As in the first solution above, this should ideally run in parallel
$ QUERY='UPDATE pgbench_accounts SET abalance = abalance + 25 WHERE aid > 78657769;'

## Unlike before, we do NOT run this against beta
$ for db in alpha gamma delta epsilon; do psql $db -Atc "SET session_replication_role='replica'; $QUERY"; done | tr "\n" " "
UPDATE 837265 UPDATE 837265 UPDATE 837265 UPDATE 837265 UPDATE 837265 

## Now we can start Bucardo up again
$ bucardo start
Checking for existing processes
Starting Bucardo
```

That concludes the solutions for when you have to make a LOT of changes to your database. How do you know 
how much is enough to worry about the solutions presented here? Generally, you can simply let 
Bucardo run—​you will know when everything crawls to a halt that perhaps trying to insert 
465 million rows at once was a bad idea. :)
