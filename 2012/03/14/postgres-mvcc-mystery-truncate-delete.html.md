---
author: Greg Sabino Mullane
gh_issue_number: 566
tags: bucardo, database, postgres
title: The Mystery of The Zombie Postgres Row
---



<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/03/14/postgres-mvcc-mystery-truncate-delete/image-0-big.png" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="320" src="/blog/2012/03/14/postgres-mvcc-mystery-truncate-delete/image-0.png" width="250"/></a></div>

Being a PostgreSQL DBA is always full of new challenges and mysteries. Tracking them 
down is one of the best parts of the job. Presented below is an error message we received one day 
via [tail_n_mail](https://bucardo.org/tail_n_mail/) from one of our client’s production servers.
See if you can figure out what was going on as I walk through it. This is from a “read only” database that acts as a [Bucardo]() target (aka slave), and as such, the only write activity should be from Bucardo.

```error
 05:46:11 [85]: ERROR: duplicate key value violates unique constraint "foobar_id"
 05:46:11 [85]: CONTEXT: COPY foobar, line 1: "12345#011...
```

Okay, so there was a unique violation during a COPY. Seems harmless enough. However, 
this should never happen, as Bucardo always deletes the rows it is about to add in with the COPY command. Sure enough, going to the logs showed the delete right above it:

```error
 05:45:51 [85]: LOG: statement: DELETE FROM public.foobar WHERE id IN (12345)
 05:46:11 [85]: ERROR: duplicate key value violates unique constraint "foobar_id"
 05:46:11 [85]: CONTEXT: COPY foobar, line 1: "12345#011...
```

How weird. Although we killed the row, it seems to have resurrected, and shambled like a zombie into our b-tree index, preventing a new row from being added. At this point, I double checked that the correct schema was being used (it was), that there were no rules or triggers, no quoting problems, no index corruption, and that “id” was indeed the first column in the table. I also confirmed that there were plenty of occurrences of 
the exact same DELETE/COPY pattern—​with the same id!—​that had run without any error at all, both before and after this error. If you are familiar with Postgres’ default MVCC mode, you might make a guess what is going on. Inside the postgresql.conf 
file there is a setting named ‘default_transaction_isolation’, which is almost always 
set to **read committed**. Further discussion of what this mode does can be found 
in [the online documentation](https://www.postgresql.org/docs/current/static/transaction-iso.html), but the short version is that while in this mode, 
another transaction could have added row 12345 and committed after we did the DELETE, 
but before we ran the COPY. A great theory that fits the facts, except that Bucardo always 
sets the isolation level manually to avoid just such problems. Scanning back for the previous command for that PID revealed:

```error
 05:45:51 [85]: LOG: statement: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE
 05:45:51 [85]: LOG: statement: DELETE FROM public.foobar WHERE id IN (12345)
 05:46:11 [85]: ERROR: duplicate key value violates unique constraint "foobar_id"
 05:46:11 [85]: CONTEXT: COPY foobar, line 1: "12345#011...
```

So that rules out any effects of read committed isolation mode. We have Postgres set to the strictest 
interpretation of MVCC it knows, SERIALIZABLE. (As this was on Postgres 8.3, it was not a 
[“true” serializable mode](/blog/2011/09/28/postgresql-allows-for-different),
 but that does not matter here.) What else could be going on? If you look at the timestamps, you will note 
that there is actually quite a large gap between the DELETE and the COPY error, despite it simply deleting and 
adding a single row (I have changed the table and data names, but it was actually a single row). So something 
else must be happening to that table.

Anyone guess what the problem is yet? After all, “when you have eliminated the impossible, 
whatever remains, however improbable, must be the truth”. In this case, the truth must be that 
Postgres’ MVCC was not working, and the database was not as [ACID](https://en.wikipedia.org/wiki/ACID) as advertised. Postgres does use 
[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control), but has two (that I know of) exceptions: the system tables, and the TRUNCATE command. I knew in 
this case nothing was directly manipulating the system tables, so that only left truncate. Sure enough, 
grepping through the logs found that something had truncated the table right around the same time, and then added a 
bunch of rows back in. As truncate is *not* MVCC-safe, this explains our mystery completely. It’s a 
bit of a race condition, to be sure, but it can and does happen. Here’s some more logs showing 
the complete sequence of events for two separate processes, which I have labeled A and B:

```error
A 05:45:47 [44]: LOG: statement: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE
A 05:45:47 [44]: LOG: statement: TRUNCATE TABLE public.foobar
A 05:45:47 [44]: LOG: statement: COPY public.foobar FROM STDIN
B 05:45:51 [85]: LOG: statement: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE
B 05:45:51 [85]: LOG: statement: DELETE FROM public.foobar WHERE id IN (12345)
A 05:46:11 [44]: LOG: duration: 24039.243 ms
A 05:46:11 [44]: LOG: statement: commit
B 05:46:11 [85]: LOG: duration: 19884.284 ms
B 05:46:11 [85]: LOG: statement: COPY public.foobar FROM STDIN
B 05:46:11 [85]: ERROR: duplicate key value violates unique constraint "foobar_id"
B 05:46:11 [85]: CONTEXT: COPY foobar, line 1: "12345#011...
```

So despite transaction B doing the correct thing, it still got tripped up by transaction A, 
which did a truncate, added some rows back in (including row 12345), and committed. If process A had done a 
DELETE instead of a TRUNCATE, the COPY still would have failed, but with a better error message:

```error
ERROR: could not serialize access due to concurrent update
```

Why does this truncate problem happen? Truncate, while extraordinarily handy, can be real tricky to implement properly 
in MVCC without some severe tradeoffs. A DELETE in Postgres actually leaves the row on disk, but changes 
its visibility information. Only after all other transactions that may need to access the old row have ended can 
the row truly be removed on disk (usually via the autovacuum daemon). Truncate, however, does not walk through 
all the rows and add visibility information: 
as the name implies, it truncates the table by removing all rows, period.

So when we did the truncate, process A was able to add row 12345 back in: it had no idea that the row was “in use” by transaction B. Similarly, B had no idea that something had added the row back in. No idea, that is, until it tried to add the row and the unique index prevented it! There appears to be 
[some work](http://www.postgresql-archive.org/RFC-Making-TRUNCATE-more-quot-MVCC-safe-quot-td5470710.html) on making truncate more MVCC friendly in future versions.

Here is a sample script demonstrating the problem:

```perl
#!perl

use strict;
use warnings;
use DBI;
use Time::HiRes; ## so we can reliably sleep less than one second

## Connect and create a test table, populate it:
my $dbh = DBI->connect('dbi:Pg', 'postgres', '', {AutoCommit=>0});
$dbh->do('DROP TABLE foobar');
$dbh->do('CREATE TABLE foobar(a INT UNIQUE)');
$dbh->do('INSERT INTO foobar VALUES (42)');
$dbh->commit();
$dbh->disconnect();

## Fork, then have one process truncate, and the other delete+insert
if (fork) {
  my $dbhA = DBI->connect('dbi:Pg', 'postgres', '', {AutoCommit=>0});
  $dbhA->do('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE');
  $dbhA->do('TRUNCATE TABLE foobar');          ## 1
  sleep 0.3;                                   ## Wait for B to delete
  $dbhA->do('INSERT INTO foobar VALUES (42)'); ## 2
  $dbhA->commit();                             ## 2
}
else {
  my $dbhB = DBI->connect('dbi:Pg', 'postgres', '', {AutoCommit=>0});
  $dbhB->do('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE');
  sleep 0.3;                                   ## Wait for A to truncate
  $dbhB->do('DELETE FROM foobar');             ## 3
  $dbhB->do('INSERT INTO foobar VALUES (42)'); ## 3
}
```

Running the above gives us:

```error
 ERROR:  duplicate key value violates unique constraint "foobar_a_key"
 DETAIL:  Key (a)=(42) already exists
```

This should not happen, of course, as process B did a delete of the entire table 
before trying an INSERT, and was in SERIALIZABLE mode. If we switch out the TRUNCATE 
with a DELETE, we get a completely different (and arguably better) error message:

```error
 ERROR:  could not serialize access due to concurrent update 
```

However, it we try it with a DELETE on PostgreSQL version 9.1 or better, which 
features a brand new true serializable mode, we see yet another error message:

```error
 ERROR:  could not serialize access due to read/write dependencies among transactions
 DETAIL:  Reason code: Canceled on identification as a pivot, during write.
 HINT:  The transaction might succeed if retried
```

This doesn’t really give us a whole lot more information, and the “detail” line is fairly arcane, but 
it does give a pretty nice “hint”, because in this particular case, the transaction *would* succeed if 
it were tried again. More specifically, B would DELETE the new row added by process A, and then safely 
add the row back in without running into any unique violations.

So the morals of the mystery are to be very careful when using truncate, and to realize that everything 
has exceptions, even the supposed sacred visibility walls of MVCC in Postgres.


