---
author: Greg Sabino Mullane
gh_issue_number: 722
tags: database, postgres, sql
title: Postgres alter column problems and solutions
---



<div class="separator" style="clear: both; text-align: center; float:right">
<a href="/blog/2012/11/09/postgres-alter-column-problems-and/image-0-big.jpeg" imageanchor="1" style="clear:right; margin-left:1em; margin-bottom:1em"><img border="0" height="240" src="/blog/2012/11/09/postgres-alter-column-problems-and/image-0.jpeg" width="320"/></a>
<br/><a href="http://www.flickr.com/photos/ell-r-brown/7611437386/">Image</a> from Flickr user <a href="http://www.flickr.com/photos/ell-r-brown/">ell brown</a></div>

A common situation for database-backed applications is the need to change the attributes of a column. One can change the data type, or more commonly, only the size limitation, e.g. VARCHAR(32) gets changed to VARCHAR(42). There are a few ways to accomplish this in PostgreSQL, from a straightforward ALTER COLUMN, to replacing VARCHAR with TEXT (plus a table constraint), to some advanced system catalog hacking.

The most common example of such a change is expanding a 
VARCHAR declaration to allow more characters. For example, 
your “checksum” column was based on 
[MD5](http://en.wikipedia.org/wiki/MD5) (at 32 characters), and 
now needs to be based on 
[Keccak](http://en.wikipedia.org/wiki/Keccak) (Keccak is pronounced “catch-ack”)  (at 64 characters)
In other words, you need a column in your table to change from VARCHAR(32) to VARCHAR(64). 
The canonical approach is to do this:

```
ALTER TABLE foobar ALTER COLUMN checksum TYPE VARCHAR(64);
```

This approach works fine, but it has two huge and interrelated problems: 
locking and time. This approach locks the table for as long as the 
command takes to run. And by lock, we are talking a heavy 
[“access exclusive” lock](http://www.postgresql.org/docs/current/static/explicit-locking.html#LOCKING-TABLES) which shuts everything else out of the table. If your table is small, 
this is not an issue. If your table has a lot of data, however, this brings 
us to the second issue: table rewrite. The above command will cause Postgres 
to rewrite every single row of the table, which can be a very expensive operation 
(both in terms of disk I/O and wall clock time). So, a simple ALTER COLUMN 
solution usually comes at a very high cost for large tables. Luckily, there are 
workarounds for this problem.

First, some good news: as of version 9.2, there are many operations that 
will no longer require a full table rewrite. Going from VARCHAR(32) to 
VARCHAR(64) is one of those operations! Thus, if you are lucky enough to 
be using version 9.2 or higher of Postgres, you can simply run the ALTER TABLE 
and have it return almost instantly. From the release notes:

> 
> 
> *
> Reduce need to rebuild tables and indexes for certain ALTER TABLE ... ALTER COLUMN TYPE operations (Noah Misch)*
> 
> *
> *
> 
> *Increasing the length limit for a varchar or varbit column, or removing the limit altogether, no longer requires a table rewrite. Similarly, increasing the allowable precision of a numeric column, or changing a column from constrained numeric to unconstrained numeric, no longer requires a table rewrite. Table rewrites are also avoided in similar cases involving the interval, timestamp, and timestamptz types.*
> 
> 
> 

However, if you are not yet on version 9.2, or are making an operation not covered above (such as shrinking the 
size limit of a VARCHAR), your only option to avoid a full table rewrite is the system catalog change below. However, 
before you jump down there, consider a different option: abandoning VARCHAR altogether.

In the Postgres world, there are few differences between the VARCHAR and TEXT data types. The latter can 
be thought of as an unbounded VARCHAR, or if you like, a VARCHAR(999999999999). You may also add a 
[check constraint](http://www.postgresql.org/docs/current/static/ddl-constraints.html) to a table to emulate the limit of a VARCHAR. For example, to convert 
a VARCHAR(32) column named “checksum” to a TEXT column:

```
ALTER TABLE foobar ALTER COLUMN checksum TYPE text;
ALTER TABLE foobar ADD CONSTRAINT checksum_length
  CHECK (LENGTH(checksum) <= 32);
```

The data type change suffers from the same full table rewrite problem as before, but if you are using 
version 9.1 or newer of Postgres, the change from VARCHAR to TEXT does *not* do a table rewrite.
The creation of the check constraint, however, will scan all of the existing table rows to make sure they 
meet the condition. While not as costly as a full table rewrite, scanning every single row in a large table will still be expensive. Luckily, version 9.2 
of Postgres comes to the rescue again with the addition of the NOT VALID phrase to the check constraint 
clause. Thus, in newer versions you can avoid the scan entirely by writing:

```
ALTER TABLE foobar ADD CONSTRAINT checksum_length
  CHECK (LENGTH(checksum) <= 32) NOT VALID;
```

This is a one-time exception for the constraint, and only applies as the constraint is 
being created. In other words, despite the name, the constraint is very much valid 
after it is created. If you want to validate all the rows that you skipped at a later 
time, you can use the ALTER TABLE .. VALIDATE CONSTRAINT 
command. This has the double advantage of allowing the 
check to be delayed until a better time, and taking a much lighter lock on the table than the 
ALTER TABLE .. ADD CONSTRAINT does.

So why would you go through the trouble of switching from your VARCHAR(32) to a 
TEXT column with a CHECK constraint? There are at least three good reasons.

First, if you are running Postgres 9.2 or better, this means you can change the constraint 
requirements on the fly, without a table scan - even for the “non-optimal” situations 
such as going from 64 characters down to 32. Just drop the old constraint, and add a new 
one with the NOT VALID clause thrown on it.

Second, the check constraint gives a better error message, and a clearer indication 
that the limitation was constructed with some thought behind it. Compare these messages:

```
postgres=# CREATE TABLE river( checksum VARCHAR(4) );
CREATE TABLE

postgres=# INSERT INTO river VALUES ('abcde');
ERROR:  value too long for type character varying(4)

postgres=# CREATE TABLE river( checksum TEXT,
postgres-#   CONSTRAINT checksum_length CHECK (LENGTH(checksum) <= 4) );
CREATE TABLE

postgres=# INSERT INTO river VALUES ('abcde');
ERROR:  new row for relation "river" violates check constraint "checksum_length"
DETAIL:  Failing row contains (abcde).
```

Third, and most important, you are no longer limited to a single column attribute (maximum length). 
You can use the constraint to check for many other things as well: minimum size, actual content, 
regex matching, you name it. As a good example, if we are are truly storing checksums, we probably 
want the hexadecimal Keccak checksums to be *exactly* 64 characters, and not just a maximum length 
of 64 characters. So, to illustrate the above point about switching constraints on 
the fly, you could change the VARCHAR(32) to a TEXT and enforce a strict 64 character limit with:

 

```
BEGIN;

ALTER TABLE foobar DROP CONSTRAINT checksum_length;

ALTER TABLE foobar ADD CONSTRAINT checksum_length
  CHECK (LENGTH(checksum) = 64) NOT VALID;

COMMIT;
```

We just introduced a minimum *and* a maximum, something old VARCHAR could not do. 
We can constrain it further, as we should only be allowing hexadecimal characters to be stored.
Thus, we can also reject and characters other than 0123456789abcdef 
from being added:

```
BEGIN;

ALTER TABLE foobar DROP CONSTRAINT checksum_length;

ALTER TABLE foobar ADD CONSTRAINT checksum_valid
  CHECK ( LENGTH(checksum) = 64 AND checksum ~ '^[a-f0-9]*$' ) NOT VALID;

COMMIT;
```

Since we have already added a regex check, we can reduce the size 
of the CHECK with a small hit in clarity like so:

```
BEGIN;

ALTER TABLE foobar DROP CONSTRAINT checksum_length;

ALTER TABLE foobar ADD CONSTRAINT checksum_valid
  CHECK ( checksum ~ '^[a-f0-9]{64}$' ) NOT VALID;

COMMIT;
```

<div class="separator" style="clear: both; text-align: center; float:right">
<a href="/blog/2012/11/09/postgres-alter-column-problems-and/image-1-big.jpeg" imageanchor="1" style="clear:right; margin-left:1em; margin-bottom:1em"><img border="0" height="240" src="/blog/2012/11/09/postgres-alter-column-problems-and/image-1.jpeg" width="320"/></a><br/><a href="http://www.flickr.com/photos/loozrboy/4471483367/">Image</a> from Flickr user <a href="http://www.flickr.com/photos/loozrboy/">loozrboy</a></div>

Back to the other problem, however: how can we avoid a table rewrite when going from 
VARCHAR(64) to VARCHAR(32), or when stuck on an older version of Postgres that always insists 
on a table rewrite? The answer is the system catalogs. Please note that any updating to the 
system catalogs should be done very, very carefully. This is one of the few types of update 
I will publicly mention and condone. Do not apply this lesson to any other system table 
or column, as there may be serious unintended consequences.

So, what does it mean to have VARCHAR(32) vs. VARCHAR(64)? As it turns out, there is 
no difference in the way the actual table data is written. The length limit of a VARCHAR 
is simply an implicit check constraint, after all, and as such, it is quite easy to 
change.

Let’s create a table and look at some of the important fields in the system 
table **pg_attribute**. In these examples we will use Postgres 8.4, but 
other versions should look very similar - this part of the system catalog 
rarely changes.

```
postgres=# CREATE TABLE foobar ( checksum VARCHAR(32) );
CREATE TABLE

postgres=# \x
Expanded display is on.

postgres=# SELECT attname, atttypid::regtype, atttypmod FROM pg_attribute 
postgres=#  WHERE attrelid = 'foobar'::regclass AND attname = 'checksum';
-[ RECORD 1 ]----------------
attname   | checksum
atttypid  | character varying
atttypmod | 36
```

The important column is **atttypmod**. It indicates the legal length of this varchar column 
(whose full legal name is “character varying”, but everyone calls it varchar). In the case of 
Postgres, there is also 4 characters of overhead. So VARCHAR(32) shows up as 36 in the 
atttypmod column. Thus, if we want to change it to a VARCHAR(64), we add 4 to 64 and get a number of 68.
Before we do this change, however, we need to make sure that nothing else will be affected. There are 
other dependencies to consider, such as views and foreign keys, that you need to keep in mind before 
making this change. What you should do is carefully check all the dependencies this table has:

```
postgres=# SELECT c.relname||':'||objid AS dependency, deptype
postgres-#   FROM pg_depend d JOIN pg_class c ON (c.oid=d.classid)
postgres-#   WHERE refobjid = 'foobar'::regclass;
  dependency   | deptype 
---------------+---------
 pg_type:16419 | i
```

We can see in the above that the only dependency is an entry in the pg_type table - which is a normal 
thing for all tables and will not cause any issues. Any other entries, however, should give you pause 
before doing a manual update of pg_attribute. You can use the information returned by the first column 
of the above query to see exactly what is referencing the table. For example, let’s make that column 
unique, as well as adding a view that uses the table, and then see the effects on the pg_depend table:

```
postgres=# CREATE UNIQUE INDEX jack ON foobar(checksum);
CREATE INDEX

postgres=# CREATE VIEW martha AS SELECT * FROM foobar;
CREATE VIEW

postgres=# SELECT c.relname||':'||objid AS dependency, deptype
postgres-#   FROM pg_depend d JOIN pg_class c ON (c.oid=d.classid)
postgres-#   WHERE refobjid = 'foobar'::regclass;
   dependency     | deptype 
------------------+---------
 pg_type:16419    | i
 pg_class:16420   | a
 pg_rewrite:16424 | n
```

The “i”, “a”, and “n” stand for internal, auto, and normal. They are not too important in this context, but more 
details can be found in [the docs on the pg_depend table](http://www.postgresql.org/docs/8.4/static/catalog-pg-depend.html). The first column shows us the system table and oid of the dependency, so 
we can look them up and see what they are:

```
postgres=# SELECT typname FROM pg_type WHERE oid = 16419;
 typname 
---------
 foobar

postgres=# SELECT relname, relkind FROM pg_class WHERE oid = 16420;
 relname | relkind 
---------+---------
 jack    | i

-- Views require a little redirection as they are implemented via the rules system
postgres=# SELECT relname,relkind FROM pg_class WHERE oid = 
postgres-#   (SELECT ev_class FROM pg_rewrite WHERE oid = 16424);
 relname | relkind 
---------+---------
 martha  | v

postgres=# \d martha
              View "public.martha"
  Column  |         Type          | Modifiers 
----------+-----------------------+-----------
 checksum | character varying(32) | 
View definition:
 SELECT foobar.checksum
   FROM foobar;
```

So what does all that tell us? It tells us we should look carefully at the index and the view to make 
sure they will not be affected by the change. In this case, a simple index on the column will not be 
affected by changing the length, so it (along with the pg_type entry) can be ignored. The view, however, 
should be recreated so that it records the actual column size.

We are now ready to make the actual change. This would be an excellent time to make a backup of 
your database. This procedure should be done very carefully - if you are unsure about any of 
the entries in pg_depend, do not proceed.

First, we are going to start a transaction, lock the table, and drop the view. Then we are going 
to change the length of the varchar directly, recreate the view, and commit! Here we go:

```
postgres=# SELECT c.relname||':'||objid AS dependency, deptype
postgres-#   FROM pg_depend d JOIN pg_class c ON (c.oid=d.classid)
postgres-#   WHERE refobjid = 'foobar'::regclass;
   dependency     | deptype 
------------------+---------
 pg_type:16419    | i
 pg_class:16420   | a
 pg_rewrite:16424 | n

postgres=# \d foobar
            Table "public.foobar"
  Column  |         Type          | Modifiers 
----------+-----------------------+-----------
 checksum | character varying(32) | 
Indexes:
    "jack" UNIQUE, btree (checksum)

postgres=# \d martha
            View "public.martha"
  Column  |         Type          | Modifiers 
----------+-----------------------+-----------
 checksum | character varying(32) | 
View definition:
 SELECT foobar.checksum
   FROM foobar;
postgres=# BEGIN;
BEGIN

postgres=# DROP VIEW martha;
DROP VIEW

postgres=# LOCK TABLE pg_attribute IN EXCLUSIVE MODE;
LOCK TABLE

postgres=# UPDATE pg_attribute SET atttypmod = 68
postgres-#   WHERE attrelid = 'foobar'::regclass AND attname = 'checksum';
UPDATE 1

postgres=# COMMIT;
COMMIT
```

Verify the changes and check out the pg_depend entries:

```
postgres=# \d foobar
            Table "public.foobar"
  Column  |         Type          | Modifiers 
----------+-----------------------+-----------
 checksum | character varying(64) | 
Indexes:
    "jack" UNIQUE, btree (checksum)

postgres=# CREATE VIEW martha AS SELECT * FROM foobar;
CREATE VIEW

postgres=# \d martha
            View "public.martha"
  Column  |         Type          | Modifiers 
----------+-----------------------+-----------
 checksum | character varying(64) | 
View definition:
 SELECT foobar.checksum
   FROM foobar;

postgres=# SELECT c.relname||':'||objid AS dependency, deptype
postgres-#   FROM pg_depend d JOIN pg_class c ON (c.oid=d.classid)
postgres-#   WHERE refobjid = 'foobar'::regclass;
    dependency    | deptype 
------------------+---------
 pg_type:16419    | i
 pg_class:16420   | a
 pg_rewrite:16428 | n
```

Success. Both the table and the view are showing the new VARCHAR size, but the data in the table was 
not rewritten. Note how the final row returned by the pg_depend query changed: we dropped the view 
and created a new one, resulting in a new row in both pg_class and pg_rewrite, and thus a new 
OID shown in the pg_rewrite table.

Hopefully this is not something you ever have to perform. The new features of 9.1 and 9.2 that 
prevent table rewrites and table scanning should go a long way towards that.


