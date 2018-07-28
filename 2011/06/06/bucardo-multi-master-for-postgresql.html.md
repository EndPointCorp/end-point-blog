---
author: Greg Sabino Mullane
gh_issue_number: 463
tags: bucardo, database, open-source, perl, postgres, sql
title: Bucardo multi-master for PostgreSQL
---

[](bucardo-multi-master-for-postgresql/image-0-big.jpeg)

<a href="/blog/2011/06/06/bucardo-multi-master-for-postgresql/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5615207357803360962" src="/blog/2011/06/06/bucardo-multi-master-for-postgresql/image-0.jpeg"/></a>

The original Bucardo

The next version of [Bucardo](https://bucardo.org/Bucardo/), a replication system for [Postgres](https://www.postgresql.org/), is almost complete. The scope of the changes required a major version bump, so this Bucardo will start at version 5.0.0. Much of the innards was rewritten, with the following goals:

 

### Multi-master support

Where “multi” means “as many as you want”! There are no more pushdelta (master to slaves) or swap (master to master) syncs: there is simply one sync where you tell it which databases to use, and what role they play. See examples below.

### Ease of use

The **bucardo** program (previously known as ‘bucardo_ctl’) has been greatly improved, making all the administrative tasks such as adding tables, creating syncs, etc. much easier.

### Performance

Much of the underlying architecture was improved, and sometimes rewritten, to make things go much faster. Most striking is the difference between the old multi-master “swap syncs” and the new method, which has been described as “orders of magnitudes” faster by early testers. We use async database calls whenever possible, and no longer have the bottleneck of a single large bucardo_delta table.

### Improved logging

Not only are more details provided, there is now the ability to control how verbose the logs are. Just set the log_level parameter to terse, normal, verbose, or debug. Those who had busy systems, which was the equivalent of a ‘debug’ firehose, will really appreciate this.

### Different targets

Who says your slave (target) databases need to be Postgres? In addition to the ability to write text SQL files (for say, shipping to a different system), you can have Bucardo push to other systems as well. Stay tuned for more details on this. (Update: there is a [blog post about using MongoDB as a target](/blog/2011/06/12/mongodb-replication-from-postgres-using))

-----------

This new version is not quite at beta yet, but you can try out a demo of multi-master on Postgres quie easily. Let’s see if we can do it in ten steps.

#### I. Download all prerequisites

To run Bucardo, you will need a Postgres database (obviously), the DBIx::Safe module, the DBI and DBD::Pg modules, and (for the purposes of this demo) the pgbench utility. Systems vary, but on aptitude-based systems, one can grab all of the above like this:

```bash
aptitude install postgresql-server \
perl-DBIx-Safe \
perl-DBD-Pg \
postgresql-contrib
```

#### II. Grab the latest Bucardo

```bash
git clone git://bucardo.org/bucardo.git
```

#### III. Install the program

```bash
cd bucardo
perl Makefile.PL
make
sudo make install
```

You can ignore any errors that come up about ExtUtils::MakeMaker not being recent.

#### IV. Setup an instance of Bucardo

This step assumes there is a running Postgres available to connect to.

```bash
sudo mkdir /var/run/bucardo
sudo chown $USER /var/run/bucardo
bucardo install
```

#### V. Use the pgbench program to create some test tables

```bash
psql -c 'CREATE DATABASE btest1'
pgbench -i btest1
psql -c 'CREATE DATABASE btest2 TEMPLATE btest1'
psql -c 'CREATE DATABASE btest3 TEMPLATE btest1'
psql -c 'CREATE DATABASE btest4 TEMPLATE btest1'
psql -c 'CREATE DATABASE btest5 TEMPLATE btest1'
```

#### VI. Tell Bucardo about the databases and tables you are going to use

```bash
bucardo add db t1 dbname=btest1
bucardo add db t2 dbname=btest2
bucardo add db t3 dbname=btest3
bucardo add db t4 dbname=btest4
bucardo add db t5 dbname=btest5
bucardo list dbs

bucardo add table pgbench_accounts pgbench_branches pgbench_tellers herd=therd
bucardo list tables
```

A herd is simply a logical grouping of tables. We did not add the other pgbench table, pgbench_history, because it has no primary key or unique index.

#### VII. Group the databases together and set their roles

```bash
bucardo add dbgroup tgroup t1:source t2:source t3:source t4:source t5:target
```

We’ve grouped all five databases together, and made four of them masters (aka source), and one of them a slave (aka target). You can any combination of master and slaves you want, as long as there is at least one master.

#### VII. Create the Bucardo sync

```bash
bucardo add sync foobar herd=therd dbs=tgroup ping=false
```

Here we simply create a new sync, which is a controllable replication event, telling it which tables we want to replicate, and which databases we are going to use. We also set ping to false, which means that we will not create triggers to automatically fire off replication on any changes, but will do it manually. In a real world scenario, you generally do want those triggers, or want to set Bucardo to check periodically.

#### VIII. Start up Bucardo

```bash
bucardo start
```

If all went well, you should see some information in the log.bucardo file in the current directory.

#### IX. Make a bunch of changes on all the source databases.

```bash
pgbench -t 10000 btest1
pgbench -t 10000 btest2
pgbench -t 10000 btest3
pgbench -t 10000 btest4
```

Here, we’ve told pgbench to run ten thousand transactions against each of the first four databases. Triggers on these tables have captured the changes.

#### X. Kick off the sync and watch the fun.

```bash
bucardo kick foobar
```

You can now tail the log.bucardo file to see the fun, or simply run:

```bash
bucardo status
```

...to see what it is doing, and the final counts when we are done. Don’t forget to stop Bucardo when you are done testing:

```bash
bucardo stop
```

The output of bucardo status, after the sync has completed, should look like this:

```sql
bucardo status
Name     State    Last good    Time    Last I/D/C           Last bad    Time
========+========+============+=======+====================+===========+=======
foobar | Good   | 17:58:37   | 3m2s  | 131836/131836/4785 | none      |
```

Here we see that this syncs has never failed (“Last bad”), the time of day of the last good run, how long ago it was from right now (3 minutes and 2 seconds), as well as details of the last successful run. Last I/D/C stands for number of inserts, deletes, and collisions across all databases for this syncs. This is just an overview of all syncs at a high level, but we can also give status an argument of a sync name to see more details like so:

```bash
bucardo status foobar
Last good                       : Jun 02, 2011 17:57:47 (time to run: 42s)
Rows deleted/inserted/conflicts : 131,836 / 131,836 / 4,785
Sync name                       : foobar
Current state                   : Good
Source herd/database            : therd / t1
Tables in sync                  : 3
Status                          : active
Check time                      : none
Overdue time                    : 00:00:00
Expired time                    : 00:00:00
Stayalive/Kidsalive             : yes / yes
Rebuild index                   : 0
Ping                            : no
Onetimecopy                     : 0
Post-copy analyze               : Yes
Last error:                     :
```

This gives us a little more information about the sync itself, as well as another important metric, how long the sync itself took to run, in this case, 42 seconds. That particular metric might make its way back to the overall “status” view above. Try things out and [help us find bugs](https://github.com/bucardo/bucardo/issues) and improve Bucardo!


