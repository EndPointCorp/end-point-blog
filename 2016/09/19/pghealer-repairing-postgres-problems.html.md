---
author: Greg Sabino Mullane
gh_issue_number: 1255
tags: postgres
title: 'pg_healer: repairing Postgres problems automatically'
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2016/09/19/pghealer-repairing-postgres-problems/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/09/19/pghealer-repairing-postgres-problems/image-0.jpeg"/></a><br/><small>(<a href="https://flic.kr/p/6r7La7">Photograph</a> by <a href="https://www.flickr.com/photos/computerhotline/">Thomas Bresson</a>)</small></div>

Sometimes, [the elephant](http://www.postgres.org) gets hurt—inducing database errors! 
Data corruption is a fact of life in working with computers, and Postgres is not immune. 
With the addition of the “data checksums” feature, detecting such corruption is now 
much easier. But detection is not enough—what happens after the corruption is detected? What if 
Postgres could fix the problem all by itself—what if we could give the elephant a  mutant healing power?!?

Now we can. I wrote an extension named pg_healer that does just that—detects 
corruption issues, and automatically repairs them. Let’s see how it works with a demonstration. 
For this, we will be purposefully corrupting the “pgbench_branches” table, part of 
the venerable [pgbench utility](https://wiki.postgresql.org/wiki/Pgbench).

For the initial setup, we will create a new Postgres cluster and install the pgbench schema. 
The all-important checksum feature needs to be enabled when we initdb, and we will use 
a non-standard port for testing:

```
$ initdb --data-checksums dojo
The files belonging to this database system will be owned by user "greg".
...
Data page checksums are enabled.

creating directory dojo ... ok
creating subdirectories ... ok
...
$ echo port=9999 >> dojo/postgresql.conf
$ pg_ctl start -D dojo -l log.dojo.txt
server starting
$ createdb -p 9999 $USER
$ pgbench -p 9999 -i
NOTICE:  table "pgbench_history" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_branches" does not exist, skipping
creating tables...
100000 of 100000 tuples (100%) done (elapsed 0.35 s, remaining 0.00 s)
vacuum...
set primary keys...
done.
```

Next, we install the pg_healer extension. As it needs to access some low-level hooks, we 
need to load it on startup, by adding a line to the postgresql.conf file:

```
$ git clone git://github.com/turnstep/pg_healer.git
Cloning into 'pg_healer'...
$ cd pg_healer
$ make install
gcc -Wall -Wmissing-prototypes ... -c -o pg_healer.o pg_healer.c
gcc -Wall -Wmissing-prototypes ... -shared -o pg_healer.so pg_healer.o
...
$ echo "shared_preload_libraries = 'pg_healer'" >> dojo/postgresql.conf
$ pg_ctl restart -D dojo -l log.dojo.txt
waiting for server to shut down.... done
server stopped
server starting
## Make sure the extension has loaded cleanly.
## If it did not, the log file would complain
$ tail -2 log.dojo.txt
LOG:  database system is ready to accept connections
LOG:  autovacuum launcher started
```

Now for the fun part. We want to purposefully corrupt the file containing the data 
for the pgbench_branches file, in simulation of a failing hard drive or other really 
serious problem. The type of problem that normally causes the DBA to get paged in the 
middle of the night. Before we do that, we want to take a peek at the contents of 
that table, and then find out which actual disk files contain the table:

```
$ psql -p 9999 -c "select * from pgbench_branches"
 bid | bbalance | filler 
-----+----------+--------
   1 |        0 | 
(1 row)

$ psql -p 9999 -Atc "select format('%s/%s',
  current_setting('data_directory'),
  pg_relation_filepath('pgbench_branches'))"
/home/greg/pg_healer/dojo/base/16384/198461

## That file is too cumbersome to keep typing out, so:
$ ln -s /home/greg/pg_healer/dojo/base/16384/198461 myrelfile
```

Let’s throw a deadly shuriken right into the middle of it!

```
## Here is what the file looks like in its original uncorrupted form
## (checksum is in red):
$ xxd -a -g1 -u myrelfile
00000000: 00 00 00 00 30 69 BC 37 74 66 04 00 1C 00 E0 1F  ....0i.7tf......
00000010: 00 20 04 20 00 00 00 00 E0 9F 40 00 00 00 00 00  . . ......@.....
00000020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
*
00001fe0: F7 0B 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00001ff0: 01 00 03 00 01 09 18 03 01 00 00 00 00 00 00 00  ................

## Good ol' dd is the right tool for the job here:
$ echo -n "Shuriken!" | dd conv=notrunc oflag=seek_bytes seek=4000 bs=9 count=1 of=myrelfile
1+0 records in
1+0 records out
9 bytes (9 B) copied, 0.000156565 s, 57.5 kB/s

## Take a peek inside the file to make sure the shuriken got embedded deeply:
$ xxd -a -g1 -u myrelfile
00000000: 00 00 00 00 30 69 BC 37 74 66 04 00 1C 00 E0 1F  ....0i.7tf......
00000010: 00 20 04 20 00 00 00 00 E0 9F 40 00 00 00 00 00  . . ......@.....
00000020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
*
00000fa0: 53 68 75 72 69 6B 65 6E 21 00 00 00 00 00 00 00  Shuriken!.......
00000fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
*
00001fe0: F7 0B 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00001ff0: 01 00 03 00 01 09 18 03 01 00 00 00 00 00 00 00  ................
```

<div class="separator" style="margin: 0 1em 1em 3em; clear: both; float:right; text-align: center;"><a href="/blog/2016/09/19/pghealer-repairing-postgres-problems/image-1.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/09/19/pghealer-repairing-postgres-problems/image-1.jpeg"/></a><br/><small><a href="https://flic.kr/p/uoCuk">These shurikens</a> are not so deadly, but quite yummy!<br/>(photograph by <a href="https://www.flickr.com/photos/karviainen/">kahvikisu</a>)</small></div>
<br>

Now that we’ve messed up the file, watch closely at what happens when we try to 
read from it. We are going to do this three times. The first time, the table will 
still be in the shared buffer cache, and thus will show no error. The second time, 
the table will be read from the disk and throw an error. At this point, pg_healer 
will see the error and repair it. The final read will pull from the completely 
healed table:

```
$ psql -p 9999 -c "select * from pgbench_branches"
 bid | bbalance | filler 
-----+----------+--------
   1 |        0 | 
(1 row)

## This will force the table out of shared_buffers, so that the next
## time it is accessed, Postgres must read from the disk:
$ psql -p 9999 -qtc "select pg_healer_remove_from_buffer('pgbench_branches')"

$ psql -p 9999 -c "select * from pgbench_branches"
WARNING:  page verification failed, calculated checksum 9478 but expected 26228
INFO:  File has been healed: base/16384/198461 (intrinsic healing)
ERROR:  invalid page in block 0 of relation base/16384/198461

## Mutant healing power was activated. Observe:
$ psql -p 9999 -c "select * from pgbench_accounts"
 bid | bbalance | filler 
-----+----------+--------
   1 |        0 | 
(1 row)
```

The corruption we created before changed the “free space” of the Postgres “page” structure. 
There are multiple ways pg_healer can fix things: this demonstrates one of the 
“intrinsic” fixes, which require no external knowledge to fix. Corruption can occur anywhere 
on the page, of course, including inside your data (as opposed to the meta-data or free space). 
One of the methods of fixing this is for pg_healer to use another copy of the table to try 
and repair the original table.

While eventually pg_healer will be able to reach out to replicas for a copy of the 
(non-corrupted) table data it needs, a simpler method is to simply create a good copy inside the 
data directory. There is a helper function that does just that, by copying the important 
files to a new directory. Details on how this is kept refreshed will be covered later; 
for now, let’s see it in action and observe how it can help Postgres heal itself from 
more serious corruption problems:

```
$ psql -p 9999 -c 'create extension pg_healer'
CREATE EXTENSION
$ psql -p 9999 -qc 'checkpoint'
$ psql -p 9999 -c 'select pg_healer_cauldron()'
```

Rather than free space, let’s corrupt something a little more important: the line pointers, 
which indicate where, inside the page, that each tuple (aka table row) is located. Extremely critical information, 
that is about to get blown away with another deadly shuriken!

```
$ echo -n "Shuriken!" | dd conv=notrunc oflag=seek_bytes seek=20 bs=9 count=1 of=myrelfile
1+0 records in
1+0 records out
9 bytes (9 B) copied, 9.3577e-05 s, 96.2 kB/s
$ xxd -a -g1 -u myrelfile
00000000: 00 00 00 00 30 69 BC 37 74 66 04 00 1C 00 E0 1F  ....0i.7tf......
00000010: 00 20 04 20 53 68 75 72 69 6B 65 6E 21 00 00 00  . . Shuriken!...
00000020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
*
00001fe0: F7 0B 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00001ff0: 01 00 03 00 01 09 18 03 01 00 00 00 00 00 00 00  ................

$ psql -p 9999 -qtc "select pg_healer_remove_from_buffer('pgbench_branches')"

$ psql -p 9999 -c "select * from pgbench_branches"
WARNING:  page verification failed, calculated checksum 8393 but expected 26228
INFO:  File has been healed: base/16384/198461 (external checksum match)
ERROR:  invalid page in block 0 of relation base/16384/198461

$ psql -p 9999 -c "select * from pgbench_branches"
 bid | bbalance | filler 
-----+----------+--------
   1 |        0 | 
(1 row)

## Has the shuriken really been removed?
$ xxd -a -g1 -u myrelfile
00000000: 00 00 00 00 30 69 BC 37 74 66 04 00 1C 00 E0 1F  ....0i.7tf......
00000010: 00 20 04 20 00 00 00 00 E0 9F 40 00 00 00 00 00  . . ......@.....
00000020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
*
00001fe0: F7 0B 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00001ff0: 01 00 03 00 01 09 18 03 01 00 00 00 00 00 00 00  ................
```

Once again, pg_healer has repaired the file. This time, however, it reached out 
to a version of the file outside the data directory, copied the old page data 
to the new page data, and then used the checksum to confirm that the changes 
were correct. This method only works, however, if the original file and the 
copy have the same checksum—which means that no changes have been made since 
the copy was made via pg_healer_cauldron(). As this is not always possible, there 
is a third method pg_healer can use, which is to examine things row by row and 
to try and repair the damage.

For this final demo, we are going to change the table by adding a new row, which 
ensures that the checksums against the copy will no longer match. After that, we 
are going to add some corruption to one of the table rows (aka tuples), and see if 
pg_healer is able to repair the table:

```
$ psql -p 9999 -qtc 'insert into pgbench_branches values (2,12345)'
$ psql -p 9999 -qc 'checkpoint'

## Throw a shuriken right into an active row!
$ echo -n "Shuriken!" | dd conv=notrunc oflag=seek_bytes seek=8180 bs=9 count=1 of=myrelfile
1+0 records in
1+0 records out
9 bytes (9 B) copied, 0.000110317 s, 81.6 kB/s

## If you look close, you will notice the checksum (in red) has also changed:
$ xxd -a -g1 -u myrelfile
00000000: 00 00 00 00 70 B0 8E 38 A4 8E 00 00 20 00 C0 1F  ....p..8.... ...
00000010: 00 20 04 20 00 00 00 00 E0 9F 40 00 C0 9F 40 00  . . ......@...@.
00000020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
*
00001fc0: 05 0C 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00001fd0: 02 00 03 00 01 08 18 03 02 00 00 00 39 30 00 00  ............90..
00001fe0: F7 0B 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00001ff0: 01 00 03 00 53 68 75 72 69 6B 65 6E 21 00 00 00  ....Shuriken!...

$ psql -p 9999 -qtc "select pg_healer_remove_from_buffer('pgbench_branches')"

$ psql -p 9999 -c "select * from pgbench_branches"
WARNING:  page verification failed, calculated checksum 56115 but expected 36516
INFO:  File has been healed: base/16384/198461 (external tuple healing)
ERROR:  invalid page in block 0 of relation base/16384/198461

$ psql -p 9999 -c "select * from pgbench_branches"
 bid | bbalance | filler 
-----+----------+--------
   1 |        0 | 
   2 |    12345 | 
(2 rows)
```

There are still some rough edges, but for a proof of concept it works quite nicely. While 
reacting to corruption errors as they appear is nice, in the future I would like it to 
be more proactive, and run as a background process that scans the database for any problems 
and fixes them. Ideally, it should be able to handle a wider class of table corruption 
problems, as well as problems in indexes, free space maps, system catalogs, etc.
Please jump in and lend a hand—the project is on github as [pg_healer](https://github.com/turnstep/pg_healer). 

Data corruption is a fact of life DBAs must confront, be it from failing hard drives, cosmic rays, 
or other reason. While the detection of such errors was greatly improved in Postgres 9.3 with the 
--data-checksums argument to initdb (which ought to default on!), it’s time to not just detect, but heal!


