---
author: Josh Williams
title: Tracking Down Database Corruption With psql
github_issue_number: 313
tags:
- postgres
date: 2010-06-01
---

I love broken Postgres. Really. Well, not nearly as much as I love the usual working Postgres, but it’s still a fantastic learning opportunity. A crash can expose a slice of the inner workings you wouldn’t normally see in any typical case. And, assuming you have the resources to poke at it, that can provide some valuable insight without lots and lots of studying internals (still on my TODO list.)

As a member of the PostgreSQL support team at End Point a number of diverse situations tend to cross my desk. So imagine my excitement when I get an email containing a bit of log output that would normally make a DBA tremble in fear:

```nohighlight
LOG:  server process (PID 10023) was terminated by signal 11
LOG:  terminating any other active server processes
FATAL:  the database system is in recovery mode
LOG:  all server processes terminated; reinitializing
```

Oops, signal 11 is SIGSEGV, Segmentation Fault. Really not supposed to happen, especially in day to day activities. That’ll cause Postgres to drop all of its current sessions and restart itself, as the log lines indicate. That crash was in response to a specific query their application was running, which essentially runs a process on a column across an entire table. Upon running pg_dump they received a different error:

```nohighlight
ERROR:  invalid memory alloc request size 2667865904
STATEMENT:  COPY public.different_table (etc, etc) TO stdout
```

Different, but still very annoying and in the way of their data. So we have (at least) two areas of corruption. But therein lies the bigger problem: Neither of these messages give us any clues about where in these potentially very large tables it’s encountering a problem.

Yes, my hope is that the corruption is not widespread. I know this database tends to not see a whole lot of churn, relatively speaking, and that they look at most if not all the data rather frequently. So the expectation is that it was caught not long after the disk controller or some memory or something went bad, and that whatever’s wrong is isolated to a handful of pages.

Our good and trusty psql command line client to the rescue! One of the options available in psql is FETCH_COUNT, which if set will wrap a SELECT query in a cursor then automatically and repeatedly fetch the specified number of rows from it. This option is there primarily to allow psql to show the results of large queries without having to dedicate so much memory up front. But in this case it lets us see the output of a table scan as it happens:

```sql
testdb=# \set FETCH_COUNT 1
testdb=# \pset pager off
Pager usage is off.
testdb=# SELECT ctid, * FROM gs;
 ctid  | generate_series
-------+-----------------
 (0,1) |               0
 (0,2) |               1
(scroll, scroll, scroll...)
```

(You did start that in a screen session, right? No need to have it send all the data over to your terminal, especially if you’re working remotely. Set screen to watch for the output to go idle, Ctrl-A, _ keys by default, and switch to a different window. Oh, and this of course isn’t the client’s database, but one where I’ve intentionally introduced some corruption.)

We select the system column ctid to tell us the page where the problem occurs. Or more specifically, the page and positions leading up to the problem:

```nohighlight
 (439,226) |           99878
 (439,227) |           99879
server closed the connection unexpectedly
        This probably means the server terminated abnormally
        before or while processing the request.
The connection to the server was lost. Attempting reset: Failed.
:|!>?
```

Yup, there it is. Some point after item pointer 227 on page 439, which probably actually means page 440. At this point we can reconnect, and possibly through a bit of trial and error narrow down the affected area a little more. But for now let’s run with page 440 being suspect; let’s take a closer look. And it here it should be noted that if you’re going to try anything, shut down Postgres and take a file-level backup of the data directory. Anyway, first we need to find the underlying file for our table...

```sql
testdb=# select oid from pg_database where datname = 'testdb';
  oid
-------
 16393
(1 row)

testdb=#* select relfilenode from pg_class where relname = 'gs';
 relfilenode
-------------
       16394
(1 row)

testdb=#* \q
demo:~/p82$ dd if=data/base/16393/16394 bs=8192 skip=440 count=1 | hexdump -C | less
...
000001f0  00 91 40 00 e0 90 40 00  00 00 00 00 00 00 00 00  |..@...@.........|
00000200  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001000  1f 8b 08 08 00 00 00 00  02 03 70 6f 73 74 67 72  |..........postgr|
00001010  65 73 71 6c 2d 39 2e 30  62 65 74 61 31 2e 74 61  |esql-9.0beta1.ta|
00001020  72 00 ec 7d 69 63 1b b7  d1 f0 f3 55 fb 2b 50 8a  |r..}ic.....U.+P.|
00001030  2d 25 96 87 24 5f 89 14  a6 a5 25 5a 56 4b 1d 8f  |-%..$_....%ZVK..|
00001040  28 27 4e 2d 87 5a 91 2b  6a 6b 72 97 d9 25 75 c4  |('N-.Z.+jkr..%u.|
00001050  f6 fb db df 39 00 2c b0  bb a4 28 5b 71 d2 3e 76  |....9.,...([q.>v|
00001060  1b 11 8b 63 30 b8 06 83  c1 60 66 1c c6 93 41 e4  |...c0....`f...A.|
...
```

Huh, so through perhaps either a kernel bug, a disk controller problem, or bizarre action on the part of a sysadmin, the last bit of our table has been overwritten by the 9.0beta1 tarball distribution. Incidentally this is not one of the recommended ways of upgrading your database.

With a corrupt page identified, if it’s fairly clear the invalid data covers most or all of the page it’s probably not too likely we’ll be able to recover any rows from it. Our best bet is to “zero out” the page so that Postgres will skip over it and let us pull the rest of the data from the table. We can use `dd` to seek to the corrupt block in the table and write out an 8k block of zero-bytes in its place. Shut down Postgres (just to make sure it doesn’t re-overwrite your work later) and note the conv=notrunc that’ll keep dd from truncating the rest of the table.

```nohighlight
demo:~/p82$ dd if=/dev/zero of=data/base/16393/16394 bs=8192 seek=440 count=1 conv=notrunc
1+0 records in
1+0 records out
8192 bytes (8.2 kB) copied, 0.000141498 s, 57.9 MB/s
demo:~/p82$ dd if=data/base/16393/16394 bs=8192 skip=440 count=1 | hexdump -C
1+0 records in
1+0 records out
8192 bytes (8.2 kB) copied, 0.000147993 s, 55.4 MB/s
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00002000
```

Cool, it’s now an empty, uninitialized page that Postgres should be fine skipping right over. Let’s test it, start Postgres back up and run psql again...

```sql
testdb=# select count(*) from gs;
 count
-------
 99880
(1 row)
```

No crash, hurray! We’ve clearly lost some rows from the table, but that should now allow us to rescue any of the surrounding data. As always it’s worth dumping out all the data you can, running initdb, and loading it back in. You never know what else might have been affected in the original database. This is of course no substitute for a real backup, but if you’re in a pinch at least there is some hope. For now, PostgreSQL is happy again!
