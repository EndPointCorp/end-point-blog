---
author: Greg Sabino Mullane
title: Detecting table rewrites with the ctid column
github_issue_number: 726
tags:
- database
- postgres
date: 2012-11-26
---



<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/11/detecting-table-rewrites-with-ctid/image-0-big.jpeg" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="320" src="/blog/2012/11/detecting-table-rewrites-with-ctid/image-0.jpeg" width="180"/></a></div>

 

In a  [recent article](/blog/2012/11/postgres-alter-column-problems-and/), I mentioned that changing the column definition of a  Postgres table will sometimes cause a full table rewrite, but sometimes  it will not. The rewrite depends on both the nature of the change and the  version of Postgres you are using. So how can you tell for sure if changing  a large table will do a rewrite or not? I'll show one method using the internal system column **ctid**. 

Naturally, you do not want to perform this test using your actual table.  In this example, we will create a simple dummy table. As long as the  column types are the same as your real table, you can determine if the  change will do a table rewrite on your version of PostgreSQL.

The aforementioned ctid column represents the physical location of the  table's row on disk. This is one of the rare cases in which this  column can be useful. The ctid value consists of two numbers: the first is  the "page" that the row resides in, and the second number is the slot in  that page where it resides. To make things confusing, the page numbering  starts at 0, while the slot starts at 1, which is why the very first row  is always at ctid (0,1). However, the only important information for this  example is determining if the ctid for the rows has changed or now (which  indicates that the physical on-disk data has changed, even if the data  inside of it has not!).

Let's create a very simple example table and see what the  ctids look like. When Postgres updates a row, it actually marks the  current row as deleted and inserts a new row. Thus, there is a "dead"  row that needs to be eventually cleaned out. (this is the way Postgres  implements  [MVCC](http://en.wikipedia.org/wiki/Multiversion_concurrency_control) - there are others). The primary way this cleanup  happens is through the use of VACUUM FULL, so we'll use that command to force  the table to rewrite itself (and thus 'reset' the ctids as you will see): 

```
postgres=# DROP TABLE IF EXISTS babies;
DROP TABLE

postgres=# CREATE TABLE babies (gender VARCHAR(10), births INTEGER);
CREATE TABLE

postgres=# INSERT INTO babies VALUES ('Girl', 1), ('Boy', 1);
INSERT 0 2

-- Note: the ctid column is never included as part of '*'
postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
-------+--------+--------
 (0,1) | Girl   |      1
 (0,2) | Boy    |      1
(2 rows)

-- Here comes Ivy, another girl:
postgres=# UPDATE babies SET births = births+1 WHERE gender = 'Girl';
UPDATE 1

-- Note that we have a new ctid: slot 3 of page 0
-- The old row at (0,1) is still there, but it is deleted and not visible
postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
-------+--------+--------
 (0,2) | Boy    |      1
 (0,3) | Girl   |      2
(2 rows)

-- The vacuum full removes the dead rows and moves the live rows to the front:
postgres=# VACUUM FULL babies;
VACUUM

-- We are back to the original slots, although the data is reversed:
postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
-------+--------+--------
 (0,1) | Boy    |      1
 (0,2) | Girl   |      2
(2 rows)
```

That's what a table rewrite will look like - all the dead rows will be removed,  and the rows will be rewritten starting at page 0, adding slots until a new page is  needed. We know from the previous article and the fine documentation that Postgres  version 9.1 is smarter about avoiding table rewrites. Let's try changing the column  definition of the table above on version 8.4 and see what happens. Note that we do an  update first so that we have at least one dead row.

```
postgres=# SELECT substring(version() from $$\d+\.\d+$$);
 substring 
-----------
 8.4

postgres=# DROP TABLE IF EXISTS babies;
DROP TABLE

postgres=# CREATE TABLE babies (gender VARCHAR(10), births INTEGER);
CREATE TABLE

postgres=# INSERT INTO babies VALUES ('Girl', 1), ('Boy', 1);
INSERT 0 2

-- No real data change, but does write new rows to disk:
postgres=# UPDATE babies SET gender = gender;
UPDATE 2

postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
-------+--------+--------
 (0,3) | Girl   |      1
 (0,4) | Boy    |      1
(2 rows)

-- Change the VARCHAR(32) to a TEXT:
postgres=# ALTER TABLE babies ALTER COLUMN gender TYPE TEXT;
ALTER TABLE

postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
-------+--------+--------
 (0,1) | Girl   |      1
 (0,2) | Boy    |      1
(2 rows)
```

We can see from the above that changing from VARCHAR to TEXT in  version 8.4 of Postgres does indeed rewrite the table. Now let's see  how version 9.1 performs:

```
postgres=# SELECT substring(version() from $$\d+\.\d+$$);
 substring 
-----------
 9.1

postgres=# DROP TABLE IF EXISTS babies;
DROP TABLe

postgres=# CREATE TABLE babies (gender VARCHAR(10), births INTEGER);
CREATE TABLe

postgres=# INSERT INTO babies VALUES ('Girl', 1), ('Boy', 1);
INSERT 0 2

-- No real data change, but does write new rows to disk:
postgres=# UPDATE babies SET gender = gender;
UPDATE 2

postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
-------+--------+--------
 (0,3) | Girl   |      1
 (0,4) | Boy    |      1
(2 rows)

-- Change the VARCHAR(32) to a TEXT:
postgres=# ALTER TABLE babies ALTER COLUMN gender TYPE TEXT;
ALTER TABLE

postgres=# SELECT ctid, * FROM babies;
 ctid  | gender | births 
 -------+--------+--------
 (0,3) | Girl   |      1
 (0,4) | Boy    |      1
(2 rows)
```

We confirmed that the ALTER TABLE in this particular case does *not* perform  a table rewrite when using version 9.1, as we suspected. We tell this by seeing  that the ctids stayed the same. We could further verify by doing a vacuum full and  showing that there were indeed dead rows that had been left untouched by the  ALTER TABLE.

Note that this small example works because nothing else is vacuuming the table,  as it is too small and transient for autovacuum to care about it. VACUUM FULL is  one of three ways a table can get rewritten; besides ALTER TABLE, the other way  is with the CLUSTER command. We go through all the trouble above because an ALTER  TABLE is the only one of the three that *may* rewrite the table - the other two  are guaranteed to do so.

This is just one example of the things you can do by viewing the ctid column. It is always nice to know beforehand if a table rewrite is going to occur, as it can be the difference between a query that runs in milliseconds versus hours!


