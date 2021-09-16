---
author: Greg Sabino Mullane
title: Disabling Postgres constraints for pg_dump
github_issue_number: 1243
tags:
- postgres
date: 2016-07-13
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2016/07/disabling-postgres-constraints-for/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" height="214" id="jA0EBAMChzm+tKZB3H1gyTmVfCRHS4otffhMjrBmP9+8cv7edF+qqTG1SnC7KYRpMDHK8xT+Wlq8Qnv0JM23KZ5BBFn6NeMLcjo==wAGQ" src="/blog/2016/07/disabling-postgres-constraints-for/image-0.jpeg" width="320"/></a><br/><small><a href="https://flic.kr/p/ieEvjB">Photo</a> by <a href="https://www.flickr.com/photos/joceykinghorn/">Jocelyn Kinghorn</a></small></div>

Constraints in [Postgres](https://www.postgresql.org/) are very powerful and versatile: 
not only are foreign keys, primary keys, and column uniqueness done internally 
via constraints, but you may create your own quite easily (at both the column and table 
level). Most of the time constraints are simply set and forget, but there is one time 
constraints may become a problem: copying the database using the 
[pg_dump program](https://www.postgresql.org/docs/current/static/app-pgdump.html).

The issue is that constraints are usually added *before* the data is copied to the 
new table via the [COPY command](https://www.postgresql.org/docs/current/static/sql-copy.html). This means the constraint fires for each added row, 
to make sure that the row passes the conditions of the constraint. If the data is 
not valid, however, the COPY will fail, and you will not be able to load the output 
of your pg_dump into a new database. Further, there may be a non-trivial performance 
hit doing all that validation. Preventing the constraint from firing may provide 
a significant speed boost, especially for very large tables with non-trivial 
constraints.

Let’s explore one way to work around the problem of pg_dump failing to work 
because some of the data is not valid according to the logic of the constraints.
While it would be quicker to make some of these changes on the production 
system itself, corporate inertia, red tape, and the usual DBA paranoia 
means a better way is to modify a copy of the database instead.

For this example, we will first create a sample “production” database and give it a simple constraint. 
This constraint is based on a function, to both emulate a specific real-world example we came across 
for a client recently, and to allow us to easily create a database in which the data is invalid 
with regards to the constraint:

```
dropdb test_prod; createdb test_prod
pgbench test_prod -i -n
creating tables...
100000 of 100000 tuples (100%) done (elapsed 0.82 s, remaining 0.00 s)
set primary keys...
done.
psql test_prod -c 'create function valid_account(int) returns bool language sql immutable as $$ SELECT $1 > 0$$;'
CREATE FUNCTION
psql test_prod -c 'alter table pgbench_accounts add constraint good_aid check ( valid_account(aid) )'
ALTER TABLE
```

Note that the constraint was added without any problem, as all of the values in the aid column 
satisfy the function, as each one is greater than zero. Let’s tweak the function, such that it no 
longer represents a valid, up to date constraint on the table in question:

```
## Verify that the constraint is working—​we should get an error:
psql test_prod -c 'update pgbench_accounts set aid = -1 where aid = 1'
ERROR:  new row for relation "pgbench_accounts" violates check constraint "good_aid"
DETAIL:  Failing row contains (-1, 1, 0,                                         ...).

## Modify the function to disallow account ids under 100. No error is produced!
psql test_prod -c 'create or replace function valid_account(int) returns bool language sql volatile as $$ SELECT $1 > 99$$'
CREATE FUNCTION

## The error is tripped only when we violate it afresh:
psql test_prod -c 'update pgbench_accounts SET aid=125 WHERE aid=125'
UPDATE 1
psql test_prod -c 'update pgbench_accounts SET aid=88 WHERE aid=88'
ERROR:  new row for relation "pgbench_accounts" violates check constraint "good_aid"
DETAIL:  Failing row contains (88, 1, 0,                                         ...).
```

The volatility was changed from IMMUTABLE to VOLATILE simply to demonstrate that a function called 
by a constraint is not bound to any particular volatility, although it *should* always be IMMUTABLE. In 
this example, it is a moot point, as our function can be immutable and still be “invalid” for some rows 
in the table. Owing to our function changing its logic, we now have a situation in which a regular pg_dump cannot be done:

```
dropdb test_upgraded; createdb test_upgraded
pg_dump test_prod | psql test_upgraded -q
ERROR:  new row for relation "pgbench_accounts" violates check constraint "good_aid"
DETAIL:  Failing row contains (1, 1, 0,                                          ...).
CONTEXT:  COPY pgbench_accounts, line 1: "1             1   0          "
## Ruh roh!
```

Time for a workaround. When a constraint is created, it may be declared as NOT VALID, which simply means 
that it makes no promises about the *existing* data in the table, but will start constraining any data 
changed from that point forward. Of particular importance is the fact that pg_dump can dump things into 
three sections, “pre-data”, “data”, and “post-data”. When a normal constraint is dumped, it will go into 
the pre-data section, and cause the problems seen above when the data is loaded. However, a constraint that 
has been declared NOT VALID will appear in the post-data section, which will allow the data to load, as it 
will not be declared until after the “data” section has been loaded in. Thus, our workaround will be to 
move constraints from the pre-data to the post-data section. First, let’s confirm the state of things by 
making some dumps from the production database:

```
pg_dump test_prod --section=pre-data -x -f test_prod.pre.sql
pg_dump test_prod --section=post-data -x -f test_prod.post.sql
## Confirm that the constraint is in the "pre" section:
grep good_aid test*sql
test_prod.pre.sql:    CONSTRAINT good_aid CHECK (valid_account(aid))
```

There are a few ways around this constraint issue, but here is one that I like as 
it makes no changes at all to production, and produces valid SQL files that may be 
used over and over.

```
dropdb test_upgraded; createdb test_upgraded
## Note that --schema-only is basically the combination of pre-data and post-data
pg_dump test_prod --schema-only | psql test_upgraded -q
## Save a copy so we can restore these to the way we found them later:
psql test_upgraded -c "select format('update pg_constraint set convalidated=true where conname=%L and connamespace::regnamespace::text=%L;', \
  conname, nspname) from pg_constraint c join pg_namespace n on (n.oid=c.connamespace) \
  where contype ='c' and convalidated" -t -o restore_constraints.sql
## Yes, we are updating the system catalogs. <a href="https://www.google.com/doodles/douglas-adams-61st-birthday">Don't Panic!</a>
psql test_upgraded -c "update pg_constraint set convalidated=false where contype='c' and convalidated"
UPDATE 3
## Why 3? The information_schema "schema" has two harmless constraints
pg_dump test_upgraded --section=pre-data -x -o test_upgraded.pre.sql
pg_dump test_upgraded --section=post-data -x -o test_upgraded.post.sql
## Verify that the constraint has been moved to the "post" section:
grep good test*sql
test_prod.pre.sql:    CONSTRAINT good_aid CHECK (valid_account(aid))
test_upgraded.post.sql:-- Name: good_aid; Type: CHECK CONSTRAINT; Schema: public; Owner: greg
test_upgraded.post.sql:    ADD CONSTRAINT good_aid CHECK (valid_account(aid)) NOT VALID;
```

```
## Two diffs to show the inline (pre) versus ALTER TABLE (post) constraint creations:
$ diff -u1 test_prod.pre.sql test_upgraded.pre.sql 
--- test_prod.pre.sql        2016-07-04 00:10:06.676766984 -0400
+++ test_upgraded.pre.sql    2016-07-04 00:11:07.978728477 -0400
@@ -54,4 +54,3 @@
     abalance integer,
-    filler character(84),
-    CONSTRAINT good_aid CHECK (valid_account(aid))
+    filler character(84)
 )

$ diff -u1 test_prod.post.sql test_upgraded.post.sql 
--- test_prod.post.sql        2016-07-04 00:11:48.683838577 -0400
+++ test_upgraded.post.sql    2016-07-04 00:11.57.265797869 -0400
@@ -17,2 +17,10 @@
 
+--
+-- Name: good_aid; Type: CHECK CONSTRAINT; Schema: public; Owner: greg
+--
+
+ALTER TABLE pgbench_accounts
+    ADD CONSTRAINT good_aid CHECK (valid_account(aid)) NOT VALID;
+
+
 SET default_tablespace = '';
```

Now we can simply sandwich our data load between the new pre and post files, and avoid 
having the constraints interfere with the data load portion at all:

```
dropdb test_upgraded; createdb test_upgraded
psql test_upgraded -q -f test_upgraded.pre.sql
pg_dump test_prod --section=data | psql test_upgraded -q
psql test_upgraded -q -f test_upgraded.post.sql
## As the final touch, make all the constraints we changed exactly how each were before:
psql test_upgraded -f restore_constraints.sql
```

A final sanity check is always a good idea, to make sure the two databases are identical, 
despite our [system catalog](https://www.postgresql.org/docs/current/static/catalogs.html) tweaking:

```
diff -s <(pg_dump test_prod) <(pg_dump test_upgraded)
Files /dev/fd/63 and /dev/fd/62 are identical
```

Although we declared a goal of having the upgraded database match production as closely as possible, 
you can always not apply that final restore_constraints.sql file and leave the constraints as 
NOT VALID, which is a better reflection of the reality of things. It also means you will not 
have to go through this rigmarole again, as those constraints shall forevermore be put into 
the post-data section when doing a pg_dump (unless someone runs the ALTER TABLE ... VALIDATE CONSTRAINT ...
command!).

While there is no direct way to disable constraints when loading data, using this pre-data to 
post-data trick can not only boost data load times, but get you out of a potential jam when 
your data is invalid!
