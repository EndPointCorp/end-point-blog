---
author: Greg Sabino Mullane
gh_issue_number: 200
tags: open-source, perl, postgres
title: Migrating Postgres with Bucardo 4
---



Bucardo just released a major version (4). The latest version, 4.0.3, can be found at [the Bucardo website](http://bucardo.org/wiki/Bucardo). The [complete list of changes](http://bucardo.org/wiki/Bucardo/Changes) is available on the new Bucardo wiki.

One of the neat tricks you can do with Bucardo is an in-place upgrade of Postgres. While it still requires application downtime, you can minimize your downtime to a very, very small window by using Bucardo. We'll work through an example below, but for the impatient, the basic process is this:

1. Install Bucardo and add large tables to a pushdelta sync
1. Copy the tables to the new server (e.g. with pg_dump)
1. Start up Bucardo and catch things up (e.g. copy all rows changes since step 2)
1. Stop your application from writing to the original database
1. Do a final Bucardo sync, and copy over non-replicated tables
1. Point the application to the new server

With this, you can migrate very large databases from one server to another (or from Postgres 8.2 to 8.4, for example) with a downtime measured in minutes, not hours or days. This is possible because Bucardo supports replicating a "pre-warmed" database - one in which most of the data is already there.

Let's test out this process, using the handy pgbench utility to create a database. We'll go from PostgreSQL 8.2 (the original database, called "A") to PostgreSQL 8.4 (the new database, called "B"). The first step is to create and populate database A:

```bash
  initdb -D testA
  echo port=5555 &gt;&gt; testA/postgresql.conf
  pg_ctl -D testA -l a.log start
  createdb -p 5555 alpha
  pgbench -p 5555 -i alpha
  psql -p 5555 -c 'create user bucardo superuser'
```

At this point, we have four tables:

```bash
  $ psql -p 5555 -d alpha -c '\d+'
                          List of relations
   Schema |   Name   | Type  |  Owner   |    Size    | Description
  --------+----------+-------+----------+------------+-------------
   public | accounts | table | postgres | 13 MB      |
   public | branches | table | postgres | 8192 bytes |
   public | history  | table | postgres | 0 bytes    |
   public | tellers  | table | postgres | 8192 bytes |
```

For the purposes of this example, let's make believe that accounts table is actually 13 **TB**. :) The next step is to prepare the 8.4 database:

```bash
  initdb -D testB
  echo port=5566 &gt;&gt; testB/postgresql.conf
  pg_ctl -D testB -l b.log start
```

We'll copy everything except the data itself to the new server:

```bash
  pg_dumpall --schema-only -p 5555 | psql -p 5566 -f -
```

Because the other tables are very small, we're only going to use Bucardo to copy over the large "accounts" table. So let's install Bucardo and add a sync to do just that:

```bash
  sudo yum install perl-DBIx-Safe
  tar xvf Bucardo-4.0.3.tar.gz
  cd Bucardo-4.0.3
  perl Makefile.PL
  sudo make install
```

(That's a very quick overview - see the  [Installation page](http://bucardo.org/wiki/Bucardo/Installation) for more information.)

Let's install bucardo on the new database:

```bash
  mkdir /tmp/bctest
  bucardo_ctl install --dbport=5566 --piddir=/tmp/bctest
```

Set the port so we don't have to keep typing it in:

```bash
  echo dbport=5566 &gt; .bucardorc
```

Now teach Bucardo about both databases:

```bash
  bucardo_ctl add db alpha name=oldalpha port=5555
  bucardo_ctl add db alpha name=newalpha port=5566
```

Finally, create a sync to copy from old to new:

```bash
  bucardo_ctl add sync pepper type=pushdelta source=oldalpha targetdb=newalpha tables=accounts ping=false
```

This adds a new sync named "pepper" which is of type pushdelta (master-slave: copy changes from the source  table to the target(s).). The source is our old server, named "oldalpha" by Bucardo. The target database is our new server, named "newalpha". The only table in this sync is "accounts", and we set ping as false, which means that we do NOT create a trigger on this table to signal Bucardo that a change has been made, as we will be kicking the sync manually.

At this point, the accounts table has a trigger on it that is capturing which rows have been changed. The next step is to copy the existing table from the old database to the new database. There are many ways to do this, such as a NetApp snapshot, using ZFS, etc., but we'll use the traditional way of a slow but effective pg_dump:

```bash
  pg_dump alpha -p 5555 --data-only -t accounts | psql -p 5566 -d alpha -f -
```

This can take as long as it needs to. Reads and writes can still happen against the old server, and changes can be made to the accounts tables. Once that is done, here's the situation:

- The old server is still in production
- The new server has a full but outdated copy of 'accounts'
- The new server has empty tables for everything but 'accounts'
- All changes to the accounts table on the old server are being logged.

Our next step is to start up Bucardo, and let it "catch up" the new server with all changes that have occurred since we created the sync:

```bash
  bucardo_ctl start
```

You can keep track of how far along the sync is by tailing the log file (syslog and ./log.bucardo by default) or by checking on the sync itself:

```bash
  bucardo_ctl status pepper
```

Once it has caught up (how long depends on how busy the accounts table is, of course), the only disparity should be any rows that have changed since the sync last ran. You can kick off the sync again if you want:

```bash
  bucardo_ctl kick pepper 0
```

The final 0 there will allow you to see when the sync has finished.

For the final step, we'll need to move the remainder of the data over. This begins our production downtime window. First, stop the app from writing to the database (reading is okay). Next, once you've confirmed nothing is making changes to the database, make a final kick:

```bash
  bucardo_ctl kick pepper 0
```

Next, copy over the other data that was not replicated by Bucardo. This should be small tables that will copy quickly. In our case, we can do it like this:

```bash
  pg_dump alpha -p 5555 --data-only -T accounts -N bucardo | psql -p 5566 -d alpha -f -
```

Note that we excluded the schema bucardo, and copied all tables *except* the 'accounts' one.

That's it! You can now point your application to the new server. There are no Bucardo triggers or other artifacts on the new server to clean up. At this point, you can shutdown Bucardo itself:

```bash
  bucardo_ctl stop
```

Then shutdown your old Postgres and start enjoying your new 8.4 server!


