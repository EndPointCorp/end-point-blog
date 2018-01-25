---
author: Greg Sabino Mullane
gh_issue_number: 1092
tags: database, open-source, postgres
title: Postgres pg_dump implicit cast problem patched!
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2015/02/16/postgres-pgdump-implicit-cast-problem/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/02/16/postgres-pgdump-implicit-cast-problem/image-0.jpeg"/></a><br/><small>(image of <a href="https://flic.kr/p/nZScqT">brain coral</a> by <a href="https://www.flickr.com/photos/laradanielle/">Lara Danielle</a>)</small></div>

One of the many reasons I love Postgres is the responsiveness of the developers. Last week I [posted an article](/blog/2015/02/10/postgres-custom-casts-and-pgdump) about the dangers of reinstating some implicit data type casts. Foremost among the dangers was the fact that [pg_dump](https://www.postgresql.org/docs/current/static/app-pgdump.html) will not dump user-created casts in the pg_catalog schema. Tom Lane (eximious Postgres hacker) read this and fixed it up—the very same day! So in git head (which will become Postgres version 9.5 someday) we no longer need to worry about custom casts disappearing with a pg_dump and reload. These same-day fixes are not an unusual thing for the Postgres project.

For due diligence, let’s make sure that the casts now survive a pg_dump and reload into a new database via [psql](https://www.postgresql.org/docs/current/static/app-psql.html):

```
psql -qc 'drop database if exists casting_test'
psql -qc 'create database casting_test'
psql casting_test -xtc 'select 123::text = 123::int'
ERROR:  operator does not exist: text = integer
LINE 1: select 123::text = 123::int
                                 ^
HINT:  No operator matches the given name and argument type(s). You might need to add explicit type casts.
```

```
psql casting_test -c 'create function pg_catalog.text(int) returns text immutable language sql as $$select textin(int4out($1))$$'
CREATE FUNCTION

psql casting_test -c 'create cast (int as text) with function pg_catalog.text(int) as implicit'
CREATE CAST

psql casting_test -xtc 'select 123::text = 123::int'
 ?column? | t

psql -qc 'drop database if exists casting_test2'
psql -qc 'create database casting_test2'
pg_dump casting_test | psql -q casting_test2
psql casting_test2 -xtc 'select 123::text = 123::int'
 ?column? | t
```

Yay, it works! Thanks, Tom, for commit [9feefedf9e92066fa6609d1e1e17b4892d81716f](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commitdiff;h=9feefedf9e92066fa6609d1e1e17b4892d81716f)). The fix even got back-patches, which means it will appear in Postgres version 9.5, but also versions 9.4.2, 9.3.7, 9.2.11, 9.1.16, and 9.0.20. However, does this mean that pg_dump is logically complete, or are there similar dangers lurking like eels below the water in the source code for pg_dump? You will be happy to learn that I could find no other exceptions inside of src/bin/pg_dump/pg_dump.c. While there are still many place in the code where an object can be excluded, it’s all done for valid and expected reasons, such as not dumping a table if the schema it is in is not being dumped as well.


