---
author: Szymon Lipiński
gh_issue_number: 851
tags: postgres
title: PostgreSQL 9.3 Released
---

Yesterday PostgreSQL 9.3 was released. It contains many great new features, below is a simple description of those I think are most important. There are many more than the short list, all of them can be find at [PostgreSQL 9.3 Release Notes](http://www.postgresql.org/docs/9.3/static/release-9-3.html) website.

One of the most important features of the new release is the long list of bug fixes and improvements making the 9.3 version faster. I think it is the main reason for upgrading. There are also many new features which your current application will not possibly use, but faster database is always better.

The new mechanism of background workers gives us quite new possibilities to run a custom process in the background. I’ve got a couple of ideas for implementing such background tasks like a custom message queue, or postgres log analyzer, or a tool for accessing PostgreSQL using HTTP (and JSON — just to have API like the NoSQL databases have).

Another nice feature, which I haven’t checked yet, is data checksums. Something really useful for checking data consistency at data files level. It should make all the data updates slower, but I haven’t checked how much slower, there will be another blog post about that.

There is also parallel pg_dump which will lead to faster backups.

The new Postgres version also has switched from SysV to Posix shared memory model. In short: you won’t need setting SHMMAX and SHMALL any more.

There are also many new [JSON functions](http://www.postgresql.org/docs/9.3/static/functions-json.html), I used some of them in one my [previous posts](/blog/2013/06/03/postgresql-as-nosql-with-data-validation).

Another really great feature is the possibility of creating event triggers. So far you could create triggers on data changes. Since PostgreSQL 9.3 you can create a trigger on dropping or creating a table, or even on dropping another trigger.

Views also changed a lot. Simple views are updatable now, and there are materialized views as well.

The Foreign Data Wrapper mechanism has been enhanced. The mechanism allows you to map an external data source to a local view. There is also the great postgres_fdw shipped with Postgres 9.3. This library enables to easily map a table from another PostgreSQL. So you can access many different Postgres databases using one local database. And with materialized views you can even cache it.

Another feature worth mentioning is faster failover of replicated database, so when your master database fail, the failover switch to slave replica is much faster. If you use Postgres for you website, this simply means shorter time your website is offline, when your master database server fails.

More information you can find in the [release announcement](http://www.postgresql.org/about/news/1481/).
