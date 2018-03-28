---
author: Greg Sabino Mullane
gh_issue_number: 1090
tags: database, postgres
title: Postgres custom casts and pg_dump
---



We recently upgraded a client from Postgres 
[version 8.3](https://www.postgresql.org/docs/current/static/release-8-3.html) to [version 9.4](https://www.postgresql.org/docs/current/static/release-9-4.html). Yes, that is quite the jump! In the process, I was reminded about the old implicit cast issue. A major change of Postgres 8.3 was the removal of some of the built-in [casts](https://www.postgresql.org/docs/current/static/sql-createcast.html), meaning that many applications that worked fine on Postgres 8.2 and earlier started throwing errors. The correct response to fixing such things is to adjust the underlying application and its SQL. Sometimes this meant a big code difference. This is not always possible because of the size and/or complexity of the code, or simply the sheer inability to change it for various other reasons. Thus, another solution was to add some of the casts back in. However, this has its own drawback, as seen below.

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2015/02/10/postgres-custom-casts-and-pgdump/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" id="rqgqiaqdaliu2rcuvcocuwdazfpyynogiahcxh3f4tcwrz3rzmoeffepr47gh4sdgu27buhpuxn3glanpqprx4qv2tumhy34umm7qtzlbr2eopluomihrr3evhmip7lsv2tcf767ylzzcdhjgn4rtoczrmqo7fmzrcvuxrqtqe4qgqgncz6q" src="/blog/2015/02/10/postgres-custom-casts-and-pgdump/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/dKfNnR">Image</a> by <a href="https://www.flickr.com/photos/teaem/">Tarek Mohamed</a></small></div>

While this may seem a little academic, given how old 8.3 is, we still see that version in the field. Indeed, we have more than a few clients running versions even older than that! While [pg_upgrade](https://www.postgresql.org/docs/current/static/pgupgrade.html) is the preferred method for upgrading between major versions (even upgrading from 8.3), its use is not always possible. For the client in this story, in addition to some system catalog corruption, we wanted to move to using [data checksums](https://www.postgresql.org/docs/current/static/app-initdb.html#APP-INITDB-DATA-CHECKSUMS). A logical dump via pg_dump was therefore a better choice.

The implicit casts can be added back in via a two-step approach of adding a support function, and then a new cast that uses that function to bind two data types. The canonical list of “missing” casts can be found at [this blog post by Peter Eisentraut](http://petereisentraut.blogspot.com/2008/03/readding-implicit-casts-in-postgresql.html). The first rule of adding back in implicit casts is “don’t do it, fix your code instead”. The second rule is “only add the bare minimum needed to get your application working”. The basic format for re-adding the casts is:

```
create function pg_catalog.text(int) returns text immutable language sql as $$select textin(int4out($1))$$

create cast (int as text) with function pg_catalog.text(int) as implicit
```

Once we got the pg_dump and import working from version 8.3 to 9.4, some old but familiar errors started popping up that looked like this:

```
ERROR:  operator does not exist: text = bigint at character 32
HINT: No operator matches the given name and argument type(s). You might need to
add explicit casts.
```

This was quickly fixed by applying the FUNCTION and CAST from above, but why did we have to apply it twice (the original, and after the migration)? The reason is that pg_dump does *NOT* dump custom casts. Yes, this is a bit surprising as pg_dump is supposed to write out a complete logical dump of the database, but casts are a specific exception. Not all casts are ignored by pg_dump—only if both sides of the cast are built-in data types, and everything is in the pg_catalog namespace. It would be nice if this were fixed someday, such that *any* user-created objects are dumped, regardless of their namespace.

There is a way around this, however, and that is to create the function and cast in another namespace. When this is done, pg_dump *WILL* dump the casts. The drawback is that you must ensure the function and schema are available to everyone. By default, functions are available to everyone, so unless you go crazy with REVOKE commands, you should be fine. The nice thing about pg_catalog is that the schema is not likely to get dropped :). Being able to dump the added casts has another advantage: creating copies of the database via pg_dump for QA or testing will always work.

So, there is a hard choice when creating custom casts (and this applies to all custom casts, not just the ones to fix the 8.3 implicit cast mess). You can either create your casts inside of pg_catalog, which ensures they are available to all users, but cannot be pg_dumped. Thus, you will need to reapply them anytime you make a copy of the database via a pg_dump (including backups!). Or, you can create them in another schema (e.g. "public"), which means that the function must be executable to everyone, but that you can pg_dump them. I really dislike pg_dump breaking its contract, and lean towards the public schema solution when possible.

Here’s a demonstration of the problem and each solution. This is using a Postgres 9.4 instance, and a very simple query to illustrate the problem, using the TEXT datatype and the INT datatype. First, let’s create a brand new database and demonstrate the issue:

```
psql -c 'drop database if exists casting_test'
NOTICE:  database "casting_test" does not exist, skipping
DROP DATABASE

psql -c 'create database casting_test'
CREATE DATABASE

psql casting_test -xtc 'select 123::text = 123::int'
ERROR:  operator does not exist: text = integer
LINE 1: select 123::text = 123::int
                                 ^
HINT:  No operator matches the given name and argument type(s). You might need to add explicit type casts.
```

Now we will fix it by creating a new cast and a supporting function for it. The error disappears. We also confirm that copying the database by using CREATE DATABASE .. TEMPLATE copies our new casts as well:

```
psql casting_test -c 'create function pg_catalog.text(int) returns text immutable language sql as $$select textin(int4out($1))$$'
CREATE FUNCTION

psql casting_test -c 'create cast (int as text) with function pg_catalog.text(int) as implicit'
CREATE CAST

psql casting_test -xtc 'select 123::text = 123::int'
 ?column? | t

psql -c 'create database clone template casting_test'
CREATE DATABASE

psql clone -xtc 'select 123::text = 123::int'
 ?column? | t
```

Now let’s see how pg_dump fails us:

```
psql -qc 'drop database if exists casting_test2'
psql -qc 'create database casting_test2'
pg_dump casting_test | psql -q casting_test2
psql casting_test2 -xtc 'select 123::text = 123::int'
ERROR:  operator does not exist: text = integer
LINE 1: select 123::text = 123::int
                                 ^
HINT:  No operator matches the given name and argument type(s). You might need to add explicit type casts.
```

Now let’s try it again, this time by putting things into the **public** schema:

```
psql -qc 'drop database if exists casting_test'
psql -qc 'create database casting_test'
psql casting_test -xtc 'select 123::text = 123::int'
ERROR:  operator does not exist: text = integer
LINE 1: select 123::text = 123::int
                                 ^
HINT:  No operator matches the given name and argument type(s). You might need to add explicit type casts.
psql casting_test -c 'create function public.text(int) returns text immutable language sql as $$select textin(int4out($1))$$'
CREATE FUNCTION

psql casting_test -c 'create cast (int as text) with function public.text(int) as implicit'
CREATE CAST

psql casting_test -xtc 'select 123::text = 123::int'
 ?column? | t

psql -qc 'drop database if exists casting_test2'
psql -qc 'create database casting_test2'
pg_dump casting_test | psql -q casting_test2
psql casting_test2 -xtc 'select 123::text = 123::int'
 ?column? | t
```

So why does it succeed the second time when using the public schema? By creating the function in a “non-pg” namespace, pg_dump will now dump it and the cast that uses it. This rule is set out in the file src/bin/pg_dump/pg_dump.c, with a source code comment stating:

```
/*
* As per discussion we dump casts if one or more of the underlying
* objects (the conversion function and the data types) are not
* builtin AND if all of the non-builtin objects namespaces are
* included in the dump. Builtin meaning, the namespace name does not
* start with "pg_".
*/
```

The moral of the story here is to avoid re-adding the implicit casts if at all possible, for it causes a ripple effect of woes. If you do add them, add only the ones you really need, only add them to the databases that need them, and consider using the public schema, not pg_catalog, for the new function. Remember that you can only fix this per database, so any new databases that get created or used by your application will need them applied. As a final blow against using them, the string concatenation operator will probably start giving you new errors if you try to combine any of the data type combinations used in your custom casts!


