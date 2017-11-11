---
author: Greg Sabino Mullane
gh_issue_number: 1261
tags: postgres
title: Postgres schema differences and views
---



<div class="separator" style="clear: both; text-align: center; float:right"><a href="/blog/2016/10/14/postgres-schema-differences-and-views/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/10/14/postgres-schema-differences-and-views/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/Atz88c
">(Photo</a> by <a href="https://www.flickr.com/photos/miwok/">Philippe Vieux-Jeanton</a>)</small></div>

Comparing the schemas of two or more different [Postgres](https://www.postgresql.org/) databases is a common 
task, but can be tricky when those databases are running different versions 
of Postgres. The quick and canonical way to compare schemas is by using the 
exact same [pg_dump program](https://www.postgresql.org/docs/current/static/app-pgdump.html) to query each database via the --schema-only option. 
This works great, but there are some gotchas, especially when dumping [database views](https://www.postgresql.org/docs/current/static/sql-createview.html).

### BACKGROUND

First some background as to how this issue was discovered. We have a client that is in the 
process of upgrading from Postgres 9.2 to the Postgres 9.6 (the latest version as of this writing). 
Using the [pg_upgrade program](https://www.postgresql.org/docs/current/static/pgupgrade.html) was not an option, because not only are 
[data checksums](http://blog.endpoint.com/2015/12/postgres-checksum-performance-impact.html) going to be enabled, but the encoding is being moved to UTF-8. A number of 
factors, especially the UTF-8 change, meant that the typical upgrade 
process of **pg_dump old_database | psql new_database** was not possible. 
Thus, we have a very custom program that carefully migrates pieces over, 
performing some transformations along the way.

### PROBLEM

As a final sanity check, we wanted to make sure the final schema for the upgraded 
9.6 database was as identical as possible to the current production 9.2 database schema. 
When comparing the pg_dump outputs, we quickly encountered a problem with the way 
that views were represented. Version 9.2 uses a very bare-bones, single-line output, while 
9.6 uses a multi-line pretty printed version. Needless to say, this meant that 
*none* of the views matched when trying to diff the pg_dump outputs.

The problem stems from the system function pg_get_viewdef(), which is used by 
pg_dump to give a human-readable and Postgres-parseable version of the view. 
To demonstrate the problem and the solution, let's create a simple view on 
a 9.2 and a 9.6 database, then compare the differences via pg_dump:

```
$ psql -p 5920 vtest -c \
'create view gregtest as select count(*) from pg_class where reltuples = 0'
CREATE VIEW
$ psql -p 5960 vtest -c \
'create view gregtest as select count(*) from pg_class where reltuples = 0'
CREATE VIEW
$ diff -u &lt;(pg_dump vtest -x -p 5920 --schema-only) &lt;(pg_dump vtest -x -p 5960 --schema-only)

--- /dev/fd/70          2016-09-29 12:34:56.019700912 -0400
+++ /dev/fd/72          2016-09-29 12:34:56.019720902 -0400
@@ -2,7 +2,7 @@
 -- PostgreSQL database dump
 --
 
--- Dumped from database version 9.2.18
+-- Dumped from database version 9.6.0
 -- Dumped by pg_dump version 9.6.0
 
 SET statement_timeout = 0;
@@ -35,22 +35,14 @@
 --
 
 CREATE VIEW gregtest AS
-SELECT count(*) AS count FROM pg_class WHERE (pg_class.reltuples = (0)::double precision);
+ SELECT count(*) AS count
+   FROM pg_class
+  WHERE (pg_class.reltuples = (0)::double precision);
 

```

The only difference other than the server version is the view, which does not match at all as 
far as the diff utility is concerned. (For purposes of this article, the minor ways in which schema 
grants are done have been removed from the output).

As mentioned before, the culprit is the pg_get_viewdef() function. Its job is to present 
the inner guts of a view in a sane, readable fashion. There are basically two adjustments 
it can make to this output: adding more parens, and adding indentation via whitespace. In 
recent versions, and despite what the docs allude to, the indentation (aka pretty printing) 
can NOT be disabled, and thus there is no simple way to get a 9.6 server to output a viewdef 
in a single line the way 9.2 does by default. To further muddy the waters, there are five 
versions of the pg_get_viewdef function, each taking different arguments:

1. by view name
1. by view name and a boolean argument
1. by OID
1. by OID and a boolean argument
1. by OID with integer argument

In Postgres 9.2, the pg_get_viewdef(text,boolean) version will 
toggle indentation on and off, and we can see the default is no indentation:

```
$ psql vtest -p 5920 -Atc "select pg_get_viewdef('gregtest')"
 SELECT count(*) AS count FROM pg_class WHERE (pg_class.reltuples = (0)::double precision);

$ psql vtest -p 5920 -Atc "select pg_get_viewdef('gregtest',false)"
 SELECT count(*) AS count FROM pg_class WHERE (pg_class.reltuples = (0)::double precision);

$ psql vtest -p 5920 -Atc "select pg_get_viewdef('gregtest',true)"
 SELECT count(*) AS count                        +
   FROM pg_class                                 +
  WHERE pg_class.reltuples = 0::double precision;
```

In Postgres 9.6 however, you are always stuck with the pretty indentation - regardless of 
which of the five function variations you choose, and what arguments you give them! Here's 
the same function calls as above in version 9.6:

```
$ psql vtest -p 5960 -Atc "select pg_get_viewdef('gregtest')"
  SELECT count(*) AS count
   FROM pg_class
  WHERE (pg_class.reltuples = (0)::double precision);

$ psql vtest -p 5960 -Atc "select pg_get_viewdef('gregtest',false)"
  SELECT count(*) AS count
   FROM pg_class
  WHERE (pg_class.reltuples = (0)::double precision);

$ psql vtest -p 5960 -Atc "select pg_get_viewdef('gregtest',true)"
  SELECT count(*) AS count
   FROM pg_class
  WHERE pg_class.reltuples = 0::double precision;
```

### SOLUTIONS

When I first ran into this problem, the three solutions that popped into my mind were:

1. Write a script to transform and normalize the schema output
1. Modify the Postgres source code such that ***pg_get_viewdef*** changes its behavior
1. Have pg_dump call ***pg_get_viewdef*** in a way that creates identical output

My original instinct was that a quick Perl script would be the overall easiest route. And while I 
eventually did get one working, it was a real pain to "un-pretty" the output, especially the 
whitespace and use of parens. A brute-force approach of simply removing all parens, 
brackets, and extra whitespace from the rule and view definitions almost did the trick, but the resulting 
output was quite uglyhard to read, and their was still some lingering whitespace problems.

Approach two, hacking the Postgres source code, is actually fairly easy. At some point, the Postgres 
source code was changed such that all indenting is forced "on". A single character change to 
the file src/backend/utils/adt/ruleutils.c did the trick:

```
- #define PRETTYFLAG_INDENT    2
+ #define PRETTYFLAG_INDENT    0
```

Although this solution will clear up the indentation and whitespace, the parenthesis are still 
different, and not as easily solved. Overall, not a great solution.

The third solution was to modify the pg_dump source code. In particular, it 
uses the pg_get_viewdef(oid) form of the function. By switching that to 
the pg_get_viewdef(oid,integer) form of the function, and giving it an 
argument of 0, both 9.2 and 9.5 output the same thing:

```
$ psql vtest -p 5920 -tc "select pg_get_viewdef('gregtest'::regclass, 0)"
  SELECT count(*) AS count                        +
    FROM pg_class                                 +
   WHERE pg_class.reltuples &gt; 0::double precision;

$ psql vtest -p 5960 -tc "select pg_get_viewdef('gregtest'::regclass, 0)"
  SELECT count(*) AS count                        +
    FROM pg_class                                 +
   WHERE pg_class.reltuples &gt; 0::double precision;
```

This modified version will produce the same schema in our test database:

```
$ diff -u &lt;(pg_dump vtest -x -p 5920 --schema-only) &lt;(pg_dump vtest -x -p 5960 --schema-only)

--- /dev/fd/80               2016-09-29 12:34:56.019801980 -0400
+++ /dev/fd/88               2016-09-29 12:34:56.019881988 -0400
@@ -2,7 +2,7 @@
 -- PostgreSQL database dump
 --
 
--- Dumped from database version 9.2.18
+-- Dumped from database version 9.6.0
 -- Dumped by pg_dump version 9.6.0
 
 SET statement_timeout = 0;
```

The best solution, as pointed out by my colleague David Christensen, is to simply make Postgres do all the heavy lifting 
with some import/export magic. At the end of the day, the output of pg_dump is not only human readble, but designed 
to be parseable by Postgres. Thus, we can feed the old 9.2 schema into a 9.6 temporary database, then turn around and 
dump it. That way, we have the same pg_get_viewdef() calls for both of the schemas. 
Here it is on our example databases:

```
$ createdb -p 5960 vtest92

$ pg_dump vtest -p 5920 | psql -q -p 5960 vtest92

$ diff -s -u &lt;(pg_dump vtest92 -x -p 5960 --schema-only) &lt;(pg_dump vtest -x -p 5960 --schema-only)
Files /dev/fd/63 and /dev/fd/62 are identical
```

### CONCLUSION

Trying to compare schemas across versions can be difficult, so it's best not to try. Dumping 
and recreating schemas is a cheap operation, so simply dump them both into the same backend, 
then do the comparison.


