---
author: Greg Sabino Mullane
gh_issue_number: 974
tags: database, dbdpg, postgres
title: Custom plans prepared statements in PostgreSQL 9.2
---

<div class="separator" style="clear: both; float: right; padding-bottom: 1em; text-align: center;"><a href="/blog/2014/04/28/custom-plans-prepared-statements-in/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/04/28/custom-plans-prepared-statements-in/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/4XWBSV">Image</a> by Flickr user <a href="https://www.flickr.com/photos/brettneilson/">Brett Neilson</a></small>
</div>

Someone was having an issue on the #postgresql channel with a query running very fast in psql, but very slow when using [DBD::Pg](http://search.cpan.org/dist/DBD-Pg/Pg.pm). The reason for this, of course, is that DBD::Pg (and most other clients) uses [prepared statements](https://www.postgresql.org/docs/current/static/sql-prepare.html) in the background. Because Postgres cannot know in advance what parameters a statement will be called with, it needs to devise the most generic plan possible that will be usable with all potential parameters. This is the primary reason DBD::Pg has the variable **pg_server_prepare**. By setting that to 0, you can tell DBD::Pg to avoid using prepared statements and thus not incur the “generic plan” penalty. However, that trick will not be needed much longer for most people: version 9.2 of Postgres added a great feature. From the [release notes](https://www.postgresql.org/docs/devel/static/release-9-2.html):

> Allow the planner to generate custom plans for specific parameter values even when using prepared statements.

Because the original IRC question involved a LIKE clause, let’s use one in our example as well. The system table **pg_class** makes a nice sample table: it’s available everywhere, and it has a text field that has a basic B-tree index. Before we jump into the prepared statements, let’s see the three cases of LIKE queries we want to try out: no wildcards, a trailing wildcard, and a leading wildcard. The relname column of the pg_class table is used in the index pg_class_relname_nsp_index. Yes, there is a touch of Hungarian notation in those system catalogs! (Technically relname is type “name”, not type “text”, but they are identical as far as this example goes).

The first case is a LIKE with no wildcards. When Postgres sees this, it converts it to a simple equality clause, as if the LIKE was an equal sign. Thus, it is able to quite easily use the B-tree index:

```plaintext
test# EXPLAIN SELECT 1 FROM pg_class WHERE relname LIKE 'foobar'
                          QUERY PLAN                                           
--------------------------------------------------------------
 Index Only Scan using pg_class_relname_nsp_index on pg_class
   Index Cond: (relname = 'foobar'::name)
   Filter: (relname ~~ 'foobar'::text)
```

Now consider the case in which we only know the first part of the word, so we put a wildcard on the end:

```plaintext
test# EXPLAIN SELECT 1 FROM pg_class WHERE relname LIKE 'foo%'
                             QUERY PLAN                                           
----------------------------------------------------------------------
 Index Only Scan using pg_class_relname_nsp_index on pg_class
   Index Cond: ((relname >= 'foo'::name) AND (relname < 'fop'::name))
   Filter: (relname ~~ 'foo%'::text)
```

As we know how the string starts, there is no problem in using the index. Notice how Postgres is smart enough to change the **foo%** into a range check for anything between **foo** and **fop**!

Finally, the most interesting one: the case where we only know the end of the relname, so the wildcard goes in the front:

```plaintext
test# EXPLAIN SELECT 1 FROM pg_class WHERE relname LIKE '%bar'
             QUERY PLAN                        
-------------------------------------
 Seq Scan on pg_class
   Filter: (relname ~~ '%bar'::text)
```

In this case, Postgres falls back to a sequential scan of the main table, and does not use the index at all, for it offers no gain. The B-tree is useless, and the entire table must be walked through (this can be worked around by clever use of a reverse clause)

So those are the three potential variations of LIKE. When a prepared statement is created, the argument is unknown and left as a placeholder. In other words, Postgres does not know in advance if we are going to search for ‘foobar’, ‘foo%’, ‘%bar’, or something else. Watch what happens when we create a basic prepared statement based on the queries above:

```plaintext
test# PREPARE zz(TEXT) AS SELECT 1 FROM pg_class WHERE relname LIKE $1
PREPARE
```

The $1 is the parameter that will be passed to this statement when it is executed. Because Postgres has no way of knowing what will be passed in, it must create a plan that can work with all possible inputs. This means using a sequential scan, for as we’ve seen above, a wildcard at the start of the input requires one. All the examples using indexes can safely fall back to a sequential scan as well. We can use EXPLAIN EXECUTE to see the plan in action:

```plaintext
test# EXPLAIN EXECUTE zz('%bar');
         QUERY PLAN                        
---------------------------
 Seq Scan on pg_class
   Filter: (relname ~~ $1)
```

As expected, this plan is the only one available for the query given, as the index cannot be used with a leading wildcard. Now for the fun part. Let’s put the wildcard on the end, and see what happens on Postgres version 9,1:

```plaintext
test# SELECT substring(version() from '(.+?) on');
PostgreSQL 9.1.13
# EXPLAIN EXECUTE zz('foo%');
         QUERY PLAN                        
---------------------------
 Seq Scan on pg_class
   Filter: (relname ~~ $1)
```

That’s really not a good plan! It gets worse:

```plaintext
# EXPLAIN EXECUTE zz('foobar');
         QUERY PLAN                        
---------------------------
 Seq Scan on pg_class
   Filter: (relname ~~ $1)
```

Before version 9.2, the prepared statement’s plan was locked in place. This was the cause of many woes, and the reason why programs and functions were “slow” but [the same queries were fast on the command line](/blog/2008/12/11/why-is-my-function-slow). Enter Tom Lane’s [commit](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commitdiff;h=e6faf910d75027bdce7cd0f2033db4e912592bcc) from September 2011:

> Redesign the plancache mechanism for more flexibility and efficiency.
>
> Rewrite plancache.c so that a "cached plan" (which is rather a misnomer at this point) can support generation of custom, parameter-value-dependent plans, and can make an intelligent choice between using custom plans and the traditional generic-plan approach.  The specific choice algorithm implemented here can probably be improved in future, but this commit is all about getting the mechanism in place, not the policy.

Yes, you read that correctly—​new plans can be generated to match the parameters! (In case you were wondering, things have been improved since this commit, as hoped for in the last sentence.) Let’s see what happens when we run the exact same prepared statements above, but on Postgres version 9.3:

```plaintext
# SELECT substring(version() from '(.+?) on');
PostgreSQL 9.3.4
test# EXPLAIN EXECUTE zz('%bar');
             QUERY PLAN                        
-------------------------------------
 Seq Scan on pg_class
   Filter: (relname ~~ '%bar'::text)

test# EXPLAIN EXECUTE zz('foo%');
                              QUERY PLAN                        
----------------------------------------------------------------------
 Index Only Scan using pg_class_relname_nsp_index on pg_class
   Index Cond: ((relname >= 'foo'::name) AND (relname < 'fop'::name))
   Filter: (relname ~~ 'foo%'::text)

test# EXPLAIN EXECUTE zz('foobar');
                       QUERY PLAN                        
--------------------------------------------------------------
 Index Only Scan using pg_class_relname_nsp_index on pg_class
   Index Cond: (relname = 'foobar'::name)
   Filter: (relname ~~ 'foobar'::text)
```

Tada! We have three different plans for the same prepared statement, If you look close, you will see that even the first plan is now a “custom” one, as it has the exact parameter string rather than just $1 as before. The moral of the story: don’t settle for anything less than version 9.2 of Postgres!
