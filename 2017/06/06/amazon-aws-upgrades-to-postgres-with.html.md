---
author: Greg Sabino Mullane
gh_issue_number: 1312
tags: aws, database, postgres
title: Amazon AWS upgrades to Postgres with Bucardo
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2017/06/06/amazon-aws-upgrades-to-postgres-with/image-0.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" data-original-height="236" data-original-width="320" src="/blog/2017/06/06/amazon-aws-upgrades-to-postgres-with/image-0.jpeg"/></a><br/><small>(<a href="https://flic.kr/p/6uzTXi">Bird-chasing photo</a> by <a href="https://www.flickr.com/photos/dougww/">Doug Waldron</a>)</small></div>

Many of our clients at End Point are using the incredible [Amazon Relational Database Service](https://aws.amazon.com/rds/) (RDS),
which allows for quick setup and use of a database system. Despite minimizing
many database administration tasks, some issues still exist, one of which is
upgrading. Getting to a new version of Postgres is simple enough with
RDS, but we've had clients use [Bucardo](https://github.com/bucardo/bucardo) to do the upgrade, rather than Amazon's built-in upgrade process.
Some of you may be exclaiming  *"A trigger-based replication system just to upgrade?!"*;
while using it may seem unintuitive, there are some very good reasons to use Bucardo
for your RDS upgrade:

#### Minimize application downtime

Many businesses are very sensitive to any database downtime, and upgrading your database
to a new version always incurs that cost. Although RDS uses the ultra-fast [pg_upgrade --links](https://www.postgresql.org/docs/current/static/pgupgrade.html) method, the whole upgrade process can take quite
a while - or at least too long for the business to accept. Bucardo can reduce the application
downtime from around seven minutes to ten seconds or less.

#### Upgrade more than one version at once

As of this writing (June 2017), RDS only allows upgrading of one major Postgres version at a time. Since
pg_upgrade can easily handle upgrading older versions, this limitation will probably be fixed
someday. Still, it means even more application downtime - to the tune of seven minutes for
each major version. If you are going from 9.3 to 9.6 (via 9.4 and 9.5), that's at least 21 minutes
of application downtime, with many unnecessary steps along the way. The total time
for Bucardo to jump from 9.3 to 9.6 (or any major version to another one) is still under ten seconds.

#### Application testing with live data

The Bucardo upgrade process involves setting up a second RDS instance running the newer version,
copying the data from the current RDS server, and then letting Bucardo replicate the changes
as they come in. With this system, you can have two "live" databases you can point your applications
to. With RDS, you must create a snapshot of your current RDS, upgrade *that*, and then point
your application to the new (and frozen-in-time) database. Although this is still useful for testing your application
against the newer version of the database, it is not as useful as having an automatically-updated version of
the database.

#### Control and easy rollback

With Bucardo, the initial setup costs, and the overhead of using triggers on your production
database, is balanced a bit by ensuring you have complete control over the upgrade process.
The migration can happen when you want, at a pace you want, and can even happen in stages as you point
some of the applications in your stack to the new version, while keeping some pointed at
the old. And rolling back is as simple as pointing apps back at the older version. You could
even set up Bucardo as "master-master", such that both new and old versions can write data
at the same time (although this step is rarely necessary).

#### Database bloat removal

Although the pg_upgrade program that Amazon RDS uses for upgrading is extraordinarily
fast and efficient, the data files are seldom, if ever, changed at all, and [table and index bloat](https://www.compose.com/articles/postgresql-bloat-origins-monitoring-and-managing/) is never removed. On the other hand,
an upgrade system using Bucardo creates the tables from scratch on the new database, and
thus completely removes all historical bloat. (Indeed, one time a client thought
something had gone wrong, as the new version's total database size had shrunk radically -
but it was simply removal of all table bloat!).

#### Statistics remain in place

The pg_upgrade program currently has a glaring flaw - no copying of the information in
the pg_statistic table. Which means that although an Amazon RDS upgrade completes in about
seven minutes, the performance will range somewhere from slightly slow to completely unusable,
until all those statistics are regenerated on the new version via
the [ANALYZE command](https://www.postgresql.org/docs/current/static/sql-analyze.html). How long this can take depends on a number of factors,
but in general, the larger your database, the longer it will take - a database-wide
analyze can take hours on very large databases. As mentioned above, upgrading via
Bucardo relies on COPYing the data to a fresh copy of the table. Although the statistics
also need to be created when using Bucardo, the time cost for this does NOT apply to
the upgrade time, as it can be done any time earlier, making the effective cost of
generating statistics zero.

## Upgrading RDS the Amazon way

Having said all that, the native upgrade system for RDS is very simple and fast. If the
drawbacks above do not apply to you - or can be suffered with minimal business pain -
then this way should always be the upgrade approach to use. Here is a quick walk through
of how an Amazon RDS upgrade is done.

For this example, we will create a new Amazon RDS instance. The creation is
amazingly simple: just log into aws.amazon.com, choose RDS, choose PostgreSQL
(always the best choice!), and then fill in a few details, such as preferred version,
server size, etc. The "DB Engine Version" was set as
PostgreSQL 9.3.16-R1", the "DB Instance Class" as
db.t2.small -- 1 vCPU, 2 GiB RAM, and "Multi-AZ Deployment" as
no. All other choices are the default. To finish up this section
of the setup, "DB Instance Identifier" was set to gregtest, the
"Master Username" to greg, and the "Master Password" to b5fc93f818a3a8065c3b25b5e45fec19

Clicking on "Next Step" brings up more options, but the only one that needs to change is to
specify the "Database Name" as gtest. Finally, the "Launch DB Instance" button.
The new database is on the way! Select "View your DB Instance" and then keep reloading
until the "Status" changes to Active.

Once the instance is running, you will be shown a connection string that looks like this:
gregtest.zqsvirfhzvg.us-east-1.rds.amazonaws.com:5432. That standard
port is not a problem, but who wants to ever type that hostname out, or
even have to look at it? The [pg_service.conf file](/blog/2016/10/26/postgres-connection-service-file) comes to the rescue with
this new entry inside the ~/.pg_service.conf file:

```
[gtest]
host=gregtest.zqsvirfhzvg.us-east-1.rds.amazonaws.com
port=5432
dbname=gtest
user=greg
password=b5fc93f818a3a8065c3b25b5e45fec19
connect_timeout=10
```

Now we run a quick test to make sure psql is able to connect, and that the database is an Amazon RDS database:

```
$ psql service=gtest -Atc "show rds.superuser_variables"
session_replication_role
```

We want to use the pgbench program to add a little content to the database, just
to give the upgrade process something to do. Unfortunately, we cannot simply
feed the "service=gtest" line to the pgbench program, but a little
environment variable craftiness gets the job done:

```
$ unset PGSERVICEFILE PGSERVICE PGHOST PGPORT PGUSER PGDATABASE
$ export PGSERVICEFILE=/home/greg/.pg_service.conf PGSERVICE=gtest
$ pgbench -i -s 4
NOTICE:  table "pgbench_history" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_branches" does not exist, skipping
creating tables...
100000 of 400000 tuples (25%) done (elapsed 0.66 s, remaining 0.72 s)
200000 of 400000 tuples (50%) done (elapsed 1.69 s, remaining 0.78 s)
300000 of 400000 tuples (75%) done (elapsed 4.83 s, remaining 0.68 s)
400000 of 400000 tuples (100%) done (elapsed 7.84 s, remaining 0.00 s)
vacuum...
set primary keys...
done.
```

At 68MB in size, this is still not a big database - so let's create a large table, then
create a bunch of databases, to make pg_upgrade work a little harder:

```
## Make the whole database 1707 MB:
$ psql service=gtest -c "CREATE TABLE extra AS SELECT * FROM pgbench_accounts"
SELECT 400000
$ for i in {1..5}; do psql service=gtest -qc "INSERT INTO extra SELECT * FROM extra"; done

## Make the whole cluster about 17 GB:
$ for i in {1..9}; do psql service=gtest -qc "CREATE DATABASE gtest$i TEMPLATE gtest" ; done
$ psql service=gtest -c "SELECT pg_size_pretty(sum(pg_database_size(oid))) FROM pg_database WHERE datname ~ 'gtest'"
17 GB
```

To start the upgrade, we log into the AWS console, and choose "Instance Actions", then "Modify". Our only choices for
instances are
"9.4.9" and "9.4.11", plus some older revisions in the 9.3 branch. Why anything other than the latest revision in
the next major branch (i.e. 9.4.11) is shown, I have no idea! Choose 9.4.11, scroll down to the
bottom, choose "Apply Immediately", then "Continue", then "Modify DB Instance". The upgrade has begun!

How long will it take? All one can do is keep refreshing to see when your new database is ready. As mentioned above,
7 minutes and 30 seconds is the total time. The logs show how things break down:

```
11:52:43 DB instance shutdown
11:55:06 Backing up DB instance
11:56:12 DB instance shutdown
11:58:42 The parameter max_wal_senders was set to a value incompatible with replication. It has been adjusted from 5 to 10.
11:59:56 DB instance restarted
12:00:18 Updated to use DBParameterGroup default.postgres9.4
```

How much of that time is spent on upgrading though? Surprisingly little. We can do a quick local test to see how
long the same database takes to upgrade from 9.3 to 9.4 using pg_upgrade --links: 20 seconds! Ideally Amazon
will improve upon the total downtime at some point.

## Upgrading RDS with Bucardo

As an asynchronous, trigger-based replication system, Bucardo is perfect for situations like this where you need to
temporarily sync up two concurrent versions of Postgres. The basic process is to create a new Amazon RDS instance
of your new Postgres version (e.g. 9.6), install the Bucardo program on a cheap EC2 box, and then have Bucardo replicate
from the old Postgres version (e.g. 9.3) to the new one. Once both instances are in sync, just point your application
to the new version and shut the old one down. One way to perform the upgrade is detailed below.

Some of the steps are simplified, but the overall process is
intact. First, find a temporary box for Bucardo to run on. It doesn't have to
be powerful, or have much disk space, but as network connectivity is important, using an EC2 box
is recommended. Install Postgres (9.6 or better, because of pg_dump) and Bucardo (latest or HEAD recommended), then put your
old and new RDS databases into your pg_service.conf file as "rds93" and "rds96" to keep things
simple.

The next step is to make a copy of the database on the new Postgres 9.6 RDS database. We want the bare
minimum schema here: no data, no triggers, no indexes, etc. Luckily, this is simple using pg_dump:

```
$ pg_dump service=rds93 --section=pre-data | psql -q service=rds96
```

From this point forward, no [DDL](https://en.wikipedia.org/wiki/Data_definition_language) should be run on the old server. We take a snapshot of the
post-data items right away and save it to a file for later:

```
$ pg_dump service=rds93 --section=post-data -f rds.postdata.pg
```

Time to get Bucardo ready. Recall that Bucardo can only replicate tables that have a
primary key or unique index. But if those tables are small enough, you can simply
copy them over at the final point of migration later.

```
$ bucardo install
$ bucardo add db A dbservice=rds93
$ bucardo add db B dbservice=rds96
## Create a sync and name it 'migrate_rds':
$ bucardo add sync migrate_rds tables=all dbs=A,B
```

That's it! The current database will now have triggers that are recording
any changes made, so we may safely do a bulk copy to the new database. This
step might take a very long time, but that's not a problem.

```
$ pg_dump service=rds93 --section=data | psql -q service=rds96
```

Before we create the indexes on the new server, we start the Bucardo sync to copy
over any rows that were changed while the pg_dump was going on. After that, the
indexes, primary keys, and other items can be created:

```
$ bucardo start
$ tail -f log.bucardo ## Wait until the sync finishes once
$ bucardo stop
$ psql service=rds96 -q -f rds.postdata.pg
```

For the final migration, we simply stop anything from writing to the 9.3 database,
have Bucardo perform a final sync of any changed rows, and then point your
application to the 9.6 database. The whole process can happen very quickly:
well under a minute for most cases.

Upgrading major Postgres versions is never a trivial task, but both Bucardo and pg_upgrade
allow it to be orders of magnitude faster and easier than the old method of using the
pg_dump utility. Upgrading your Amazon AWS Postgres instance is fast and easy
using the AWS pg_upgrade method, but it has limitations, so having Bucardo
help out can be a very useful option.
