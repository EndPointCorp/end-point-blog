---
author: Jon Jensen
title: 10,000 databases on a PostgreSQL cluster
github_issue_number: 74
tags:
- database
- postgres
date: 2008-11-10
---

One of our clients wanted confirmation that PostgreSQL will have no problem handling 1000 or 2000 databases on a single database cluster. I remember testing some years ago, probably on Postgres 7.2 or 7.3, creating 1000 or so databases and finding that it worked fine. But that was a long time ago, the software has changed, and I thought I should make sure my old experiment results still stand.

There’s a [PostgreSQL FAQ question](https://wiki.postgresql.org/wiki/FAQ#item4.4), “What is the maximum size for a row, a table, and a database?” but no mention of the maximum number (or more importantly, maximum *practical* number) of databases per cluster. So I threw together a test script to create 10,000 databases, each with between (randomly) 1-5 tables with 2 columns each (INTEGER and TEXT), each getting randomly between 1-10 inserts with random data up to 100 or so characters in the TEXT field.

I ran the test on PostgreSQL 8.1, the default that ships with Red Hat Enterprise Linux 5 (x86_64). The hardware was a desktop-class HP with an Intel Core 2 @ 1.86 GHz that wasn’t always idle.

The short answer: Postgres 8.1 handles 10,000 databases just fine. \l in psql generates a long list of databases, of course, but returns quickly enough. Ad-hoc concurrency testing was fine. Running queries, inserts, etc. on a handpicked group of the various play databases worked fine, including while new databases were being created. During the creation process, the last database creates seemed about as fast the first. It took 2.75 hours to run.

This all is hardly a big surprise, but maybe by documenting it I’ll save someone the bother of running your own test in the future.

**Addendum:** The actual limit on this platform is probably 31995 databases, because each database occupies a subdirectory in data/base/ and the ext3 filesystem has a limit of 31998 sub-directories per one directory, stemming from its limit of 32000 links per inode. The other 5 would be ., .., template0, template1, and postgres. [(Thanks, Wikipedia.)](https://en.wikipedia.org/wiki/Ext3#Functionality)
