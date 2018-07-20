---
author: Greg Sabino Mullane
gh_issue_number: 255
tags: database, open-source, perl, postgres
title: Splitting Postgres pg_dump into pre and post data files
---



I’ve just released a small Perl script that has helped me solve a specific problem with Postgres dump files. When you use **pg_dump** or **pg_dumpall**, it outputs things in the following order, per database:

1. schema creation commands (e.g. CREATE TABLE)1. data loading command (e.g. COPY tablename FROM STDIN)1. post-data schema commands (e.g. CREATE INDEX)

The problem is that using the --schema-only flag outputs the first and third sections into a single file. Hence, if you load the file and then load a separate --data-only dump, it can be very slow as all the constraints, indexes, and triggers are already in place. The **split_postgres_dump** script breaks the dump file into two segments, a “pre” and a “post”. (It doesn’t handle a file with a data section yet, only a --schema-only version)

Why would you need to do this instead of just using a full dump? Some reasons I’ve found include:

- When you need to load the data more than once, such as debugging a data load error.
- When you want to stop after the data load step (which you can’t do with a full dump)
- When you need to make adjustments to the schema before the data is loaded (seen quite a bit on [major version upgrades](/blog/2010/01/11/postgres-upgrades-ten-problems-and))

Usage is simply ./split_postgres_dump.pl yourdumpfile.pg, which will then create two new files, yourdumpfile.pg.pre and yourdumpfile.pg.post. It doesn’t produce perfectly formatted files, but it gets the job done!

It’s a small script, so it has no bug tracker, git repo, etc. but it does have a small wiki page at 
[https://bucardo.org/wiki/Split_postgres_dump](https://bucardo.org/wiki/Split_postgres_dump) from which you can download the latest version.

Future versions of pg_dump will allow you to break things into pre and post data sections with flags, but until then, I hope somebody finds this script useful.

**Update:** There is now a git repo: 
git clone git://bucardo.org/split_postgres_dump.git


