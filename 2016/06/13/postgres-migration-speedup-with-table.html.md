---
author: Greg Sabino Mullane
gh_issue_number: 1236
tags: postgres
title: Postgres migration speedup with table change analysis
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2016/06/13/postgres-migration-speedup-with-table/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/06/13/postgres-migration-speedup-with-table/image-0.jpeg"/></a><br/><small>(A Unicode rabbit face 🐰 will never be as cute <br/>as this real bunny. <a href="https://flic.kr/p/6stdw2">Photo</a> by <a href="https://www.flickr.com/photos/wsimmons/">Wade Simmons</a>)</small></div>

One of our clients recently reached out to us for help in upgrading their 
[Postgres](https://www.postgresql.org/) database. The use of 
the [pg_upgrade program](https://www.postgresql.org/docs/current/static/pgupgrade.html)
was not an option, primarily because the client was also taking 
the opportunity to change from their SQL_ASCII encoding to UTF-8. (If any 
of your databases, gentle reader, are still SQL_ASCII, please do the same!). 
Naturally, we also took advantage of the lack of pg_upgrade to enable 
the use of data checksums, another action we highly recommend. Although there were 
plenty of wrinkles, and stories to be told about this migration/upgrade, I wanted 
to focus on one particular problem we had: how to detect if a table has changed.

We needed to know if any applications were modifying certain tables because the 
speed of the migration was very important. If we could assert that no changes 
were made, there were some shortcuts available that would greatly speed things up.
Initial testing showed that the migration was taking over eight hours, a time 
unacceptable to the client (no worries, we eventually reduced the time to 
under an hour!).

Looking closer, we found that over half that time was spent converting a single 
small (50MB) table from SQL_ASCII to UTF-8. How this conversion was performed is 
a story for another day, but suffice to say the table had some really, really messy bytes inside of it; 
the conversion program had to struggle mightily. When you are converting a database 
to a new encoding, it is imperative to examine every byte and make sure it gets changed 
to a format that Postgres will accept as valid UTF-8, or the entire table import will fail with an error 
similar to this:

```
ERROR:  invalid byte sequence for encoding "UTF8": 0xf4 0xa5 0xa3 0xa5
```

Looking closer at the data in the table showed that it might - just might! - be a 
historical table. In other words, it no longer receives updates, just selects. 
We really wanted this to be true, for it meant we could dump the whole table, convert it, 
and simply load the converted table into the new database (which took only a 
few seconds!). First, however, we had to confirm that the table was not changing.

Detecting changes may be done in several ways. For all of them, you can 
never prove that the table shall not change at some point in the future, but 
you can prove that it has not changed over a certain period of time. How you 
go about doing that depends on what kind of access you have. If you do not 
have super-user access, you could add a simple trigger to the table that updates 
another table when a update, insert, or delete is performed. Then, checking 
in on the second table will indicate if any changes have been made.

A better solution is to simply look at the underlying file that makes up the 
table. To do this, you need be a Postgres 
[superuser](https://www.postgresql.org/docs/current/static/role-attributes.html) 
or have access to the underlying operating system.
Basically, we will trust the operating system's 
information on when the table was last changed to determine if the table 
itself has changed. Although not foolproof, it is an excellent solution. Let's 
illustrate it here. First: create a test table and add some rows:

```
$ psql
greg=# CREATE TABLE catbox AS SELECT 8675309::INT AS id FROM generate_series(1,1000);
SELECT 1000
```

Now we can use the 
[pg_stat_file() function](https://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADMIN-GENFILE), 
which returns some basic information about a file on disk. With the help of the pg_relation_filepath() function, we can see when 
the table was last modified:

```
greg=# select * from pg_stat_file( pg_relation_filepath('catbox') ) \x\g
Expanded display is on.
-[ RECORD 1 ]+-----------------------
size         | 40960
access       | 2015-11-08 22:36:00-04
modification | 2015-11-08 22:36:00-04
change       | 2015-11-08 22:36:00-04
creation     | 
isdir        | f

```

Next we will revisit the table after some time (e.g. 24 hours) 
and see if the "modification" timestamp is the same. If it is, then the 
table has not been modified either. Unfortunately, the possibility of 
a false positive is possible due to [VACUUM](https://www.postgresql.org/docs/current/static/sql-vacuum.html), 
which may change things on disk but does NOT change the data itself. (A regular VACUUM *may* modify the file, and a 
VACUUM FULL *always* modifies it).

```
greg=# select * from pg_stat_file( pg_relation_filepath('catbox') ) \x\g

-[ RECORD 1 ]+-----------------------
size         | 40960
access       | 2015-11-08 22:36:00-04
modification | 2015-11-08 22:36:00-04
change       | 2015-11-08 22:36:00-04
creation     | 
isdir        | f

greg=# vacuum catbox;
VACUUM

greg=# select * from pg_stat_file( pg_relation_filepath('catbox') );

2016-06-09 22:53:24-04
-[ RECORD 1 ]+-----------------------
size         | 40960
access       | 2015-11-08 22:36:00-04
modification | 2015-11-08 22:40:14-04
change       | 2015-11-08 22:40:14-04
creation     | 
isdir        | f
```

A second (and more foolproof) method is to simply generate a checksum of the 
entire table. This is a fairly straightforward approach; just pump the output 
of [pg_dump](https://www.postgresql.org/docs/current/static/app-pgdump.html) 
to a checksum program:

```
$ pg_dump -t catbox --data-only | sha1sum
6f724565656f455072736e44646c207472536e61  -
```

The advantage here is that even a VACUUM FULL will not change the checksum. 
However, because pg_dump does no ORDER BY when dumping out the table, 
it is possible for the rows to be returned in a different order. To work 
around that, issue a VACUUM FULL yourself before taking the checksum. As 
before, come back later (e.g. 24 hours) and re-run the command. If the checksums 
match, then the table has not changed (and is probably no longer updated by 
the application). By using this method, we were able to verify that the 
large, SQL_ASCII byte-soup table was indeed not being updated, and 
thus we took it out of the direct migration.

Of course, that table needed to be part of the new database, but we simply dumped the table, 
ran the conversion program on it, and (four hours later), had a complete dump of the 
table that loads extremely fast into the new database.

That solved only one of the problems, however; another table was also slowing 
down the migration. Although it did not have the SQL_ASCII conversion 
issue, it was a large table, and took a large percentage of the remaining 
migration time. A quick look at this table showed it had a "creation_time"  
column as well as a 
[SERIAL primary key](www.neilconway.org/docs/sequences/), and was obviously being updated quite often. 
Close examination showed that it was possible this was an append-only 
table, such that older rows were never updated. This called for a similar 
approach: could we prove that a large chunk of the table was not changing? 
If we could, we could pre-populate the new database and copy over only the 
most recent rows during the migration, saving a good bit of time.

The previous tricks would not work for this situation, because the underlying file would 
change constantly as seen by pg_stat_file(), and a pg_dump checksum would 
change on every insert. We needed to analyze a slice of the table - in this particular case, 
we wanted to see about checksumming all rows except those created in 
the last week. As a primary key lookup is very fast, we used the "creation_time" 
column to determine an approximate primary key to start with. Then it was simply 
a matter of feeding all those rows into the sha1sum program:

```
greg=# CREATE TABLE catbox2 (id SERIAL PRIMARY KEY, creation_time TIMESTAMPTZ);
CREATE TABLE
greg=# INSERT INTO catbox2(creation_time) select now() - '1 year'::interval + (x* '1 hour'::interval) from generate_series(1,24*365) x;
INSERT 0 8760

greg=# select * from catbox2 where creation_time > now()-'1 week'::interval order by 1 limit 1
  id  |         creation_time         
------+-------------------------------
 8617 | 2016-06-11 10:51:00.101971-08

$ psql -Atc "select * from catbox2 where id < 8617 order by 1" | sha1sum
456272656d65486e6f203139353120506173733f  -

## Add some rows to emulate the append-only nature of this table:
greg=# insert into catbox2(creation_time) select now() from generate_series(1,1000)
INSERT 0 1000

## Checksums should still be identical:
$ psql -Atc "select * from catbox2 where id < 8617 order by 1" | sha1sum
456272656d65486e6f203139353120506173733f  -
```

Despite the large size of this table (around 10 GB), this command did not take 
that long to run. A week later, we ran the same 
commands, and got the same checksum! Thus, we were able to prove that the 
table was mostly append-only - or at least enough for our use case. We 
copied over the "old" rows, then copied over the rest of the rows during 
the critical production migration window.

In the future, this client will able to take advantage of pg_upgrade, 
but getting to UTF-8 and data checksums was absolutely worth the high one-time cost. 
There were several other tricks used to speed up the final migration, but 
being able to remove the UTF-8 conversion of the first table, and being able 
to pre-copy 99% of the second table accounted for the lion's share of the 
final speed improvements.


