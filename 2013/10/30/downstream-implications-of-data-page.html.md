---
author: Josh Williams
gh_issue_number: 870
tags: postgres, sysadmin
title: Downstream Implications of Data Page Checksums
---



Now that Postgres 9.3 is all the rage, page checksums are starting to see use in production. It’s not enabled by default during initdb, so you may want to double check the options used when you upgraded.

What? You have already upgraded to 9.3, right? No? Oh well, when you do get around to updating, keep an eye out for initdb’s --data-checksums option, or just -k. To give the feature a try on my development desktop, after the initdb I created a table and loaded in some text data. Small text strings are being cast from integers so we can more easily see it in the on-disk structure. You’ll see why in a moment. The table was loaded with a good amount of data, at least more than my shared_buffers setting:

```nohighlight
postgres=# CREATE TABLE filler (txt TEXT PRIMARY KEY);
CREATE TABLE
postgres=# INSERT INTO filler SELECT generate_series::text FROM generate_series(-10000000,10000000);
INSERT 0 20000001
postgres=# \dt+
List of relations
 Schema |  Name  | Type  |  Owner   |  Size  | Description
--------+--------+-------+----------+--------+-------------
 public | filler | table | postgres | 761 MB |
(1 row)
```

There. Maybe a little more than I needed, but it works. My storage (on this desktop) is so much slower than the processor, of course, I certainly didn’t notice any difference in performance with checksums on. But on your nice and speedy server you might see the performance hit. Anyway, now to find the file on disk...

```nohighlight
postgres=# SELECT relfilenode FROM pg_class WHERE relname = 'filler';
 relfilenode
-------------
       16390
(1 row)

postgres@endpoint:~/9.3$ dd bs=8192 count=1 skip=10 if=main/base/12066/16390 of=block
1+0 records in
1+0 records out
8192 bytes (8.2 kB) copied, 0.0161733 s, 507 kB/s
```

That relfilenode (plus the “postgres” database oid of 12066) corresponds to base/12066/16390, so I’ve taken a copy of the 10th page in that file. And then introduced some “silent” corruption, such as some that might be seen if I had a scary storage driver, or a cosmic ray hit the disk platter and flipped a bit:

```nohighlight
postgres@endpoint:~/9.3$ sed -iorig 's/9998000/9999000/' block

postgres@endpoint:~/9.3$ diff -u <(hexdump -C block) <(hexdump -C blockorig)
--- /dev/fd/63    2013-10-18 16:35:22.963860942 -0400
+++ /dev/fd/62    2013-10-18 16:35:22.963860942 -0400
@@ -134,7 +134,7 @@
 00000850  98 00 01 00 02 09 18 00  13 2d 39 39 39 37 39 39  |.........-999799|
 00000860  39 00 00 00 00 00 00 00  02 00 00 00 00 00 00 00  |9...............|
 00000870  00 00 00 00 00 00 0a 00  97 00 01 00 02 09 18 00  |................|
-00000880  13 2d 39 39 39 39 30 30  30 00 00 00 00 00 00 00  |.-9999000.......|
+00000880  13 2d 39 39 39 38 30 30  30 00 00 00 00 00 00 00  |.-9998000.......|
 00000890  02 00 00 00 00 00 00 00  00 00 00 00 00 00 0a 00  |................|
 000008a0  96 00 01 00 02 09 18 00  13 2d 39 39 39 38 30 30  |.........-999800|
 000008b0  31 00 00 00 00 00 00 00  02 00 00 00 00 00 00 00  |1...............|
```

Yep, definitely right in the middle of a column value. Normal Postgres wouldn’t have noticed at all, and that incorrect value could creep into queries that are expecting something different. Inject that corrupt page back into the heap table...

```nohighlight
postgres@endpoint:~/9.3$ dd bs=8192 count=1 seek=10 of=main/base/12066/16390 if=block
1+0 records in
1+0 records out
8192 bytes (8.2 kB) copied, 0.000384083 s, 21.3 MB/s

postgres=# SELECT count(*) FROM filler;
WARNING:  page verification failed, calculated checksum 14493 but expected 26981
ERROR:  invalid page in block 10 of relation base/12066/16390
```

... And our checksum-checking Postgres catches it, just as it’s supposed to. And, obviously, we can’t modify anything on that page either, as Postgres would need to read it into the shared buffer before any tuples there could be modified.

```nohighlight
postgres=# UPDATE filler SET txt ='Postgres Rules!' WHERE txt = '-9997999';
WARNING:  page verification failed, calculated checksum 14493 but expected 26981
ERROR:  invalid page in block 10 of relation base/12066/16390
```

The inability to even try to modify the corrupted data is what got me thinking about replicas. Assuming we’re protecting against silent disk corruption (rather than Postgres bugs,) nothing corrupted has made it into the WAL stream. So, naturally, the replica is fine.

```nohighlight
postgres@endpoint:~/9.3$ psql -p 5439
psql (9.3.1)
Type "help" for help.
```
```nohighlight
postgres=# SELECT ctid, * FROM filler WHERE txt IN ('-9997998', '-9997999', '-9998000', '-9998001');
   ctid   |   txt
----------+----------
 (10,153) | -9997998
 (10,152) | -9997999
 (10,151) | -9998000
 (10,150) | -9998001
(4 rows)
```

You’d probably be tempted to fail over to the replica at this point, which would be the Right thing to do. You are, after all, starting to see odd and (presumably) unexplained corruption in the on-disk state. You would be wise to switch off that hardware as soon as you can and investigate.

But Halloween is right around the corner, so lets given to some Mad Scientist tendencies! And remember, only try this at home.

```nohighlight
postgres@endpoint:~/9.3$ dd bs=8192 count=1 skip=10 if=replica/base/12066/16390 seek=10 of=main/base/12066/16390
1+0 records in
1+0 records out
8192 bytes (8.2 kB) copied, 0.000295787 s, 27.7 MB/s
```

With one assumption—that the replica is caught up to the point where the primary first saw the page as corrupted—the replica should be guaranteed to have an up-to-date copy of the page, even if other things on the master are changing and the replica’s lagging behind.

Above, we did a direct copy from the replica’s version of that page back to the master...

```nohighlight
postgres@endpoint:~/9.3$ psql -p 5435
psql (9.3.1)
Type "help" for help.

postgres=# SELECT ctid, * FROM filler WHERE txt IN ('-9997998', '-9997999', '-9998000', '-9998001');
   ctid   |   txt
----------+----------
 (10,150) | -9998001
 (10,151) | -9998000
 (10,152) | -9997999
 (10,153) | -9997998
(4 rows)

postgres=# UPDATE filler SET txt ='Postgres Rules!' WHERE txt = '-9997999';
UPDATE 1
```

Voila! Corruption fixed without even having to take the database down.


