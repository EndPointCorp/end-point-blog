---
author: Greg Sabino Mullane
gh_issue_number: 170
tags: database, open-source, perl, postgres
title: Bucardo and truncate triggers
---

Version 8.4 of Postgres was recently released. One of the [features](https://www.postgresql.org/docs/8.4/static/release-8-4.html) that hasn’t gotten a lot of press, but which I’m excited about, is truncate triggers. This fixes a critical hole in trigger-based PostgreSQL replication systems, and support for these new triggers is now working in the [Bucardo replication program.](https://bucardo.org)

Truncate triggers were added to Postgres by [Simon Riggs](https://wiki.postgresql.org/wiki/Simon_Riggs%27_Development_Projects) (thanks Simon!), and unlike other types of triggers (UPDATE, DELETE, and INSERT), they are statement-level only, as truncate is not a row-level action.

Here’s a quick demo showing off the new triggers. This is using the development version of Bucardo—​a major new version is expected to be released in the next week or two that will include truncate trigger support and many other things. If you want to try this out for yourself, just run:

```bash
$ git clone git-clone http://bucardo.org/bucardo.git/
```

Bucardo does three types of replication; for this example, we’ll be using the ‘pushdelta’ method, which is your basic “master to slaves” relationship. In addition to the master database (which we’ll name A) and the slave database (which we’ll name B), we’ll create a third database for Bucardo itself.

```bash
$ initdb -D bcdata
$ initdb -D testA 
$ initdb -D testB 
```

(Technically, we are creating three new database clusters, and since we are doing this as the postgres user, the default database for all three will be ‘postgres’)

Let’s give them all unique port numbers:

```bash
$ echo port=5400 >> bcdata/postgresql.conf
$ echo port=5401 >> testA/postgresql.conf 
$ echo port=5402 >> testB/postgresql.conf 
```

Now start them all up:

```bash
$ pg_ctl start -D bcdata -l bc.log
$ pg_ctl start -D testA -l A.log
$ pg_ctl start -D testB -l B.log
```

We’ll create a simple test table on both sides:

```bash
$ psql -d postgres -p 5401 -c 'CREATE TABLE trtest(id int primary key)'
$ psql -d postgres -p 5402 -c 'CREATE TABLE trtest(id int primary key)'
```

Before we go any further, let’s install Bucardo itself. Bucardo is a Perl daemon that uses a central database to store its configuration information. The first step is to create the Bucardo schema. This, like almost everything else with Bucardo, is done with the ‘bucardo_ctl’ script. The install process is interactive:

```bash
$ bucardo_ctl install --dbport=5400

This will install the bucardo database into an existing Postgres cluster.
Postgres must have been compiled with Perl support,
and you must connect as a superuser

We will create a new superuser named 'bucardo',
and make it the owner of a new database named 'bucardo'

Current connection settings:
1. Host:          <none>
2. Port:          5400
3. User:          postgres
4. PID directory: /var/run/bucardo
Enter a number to change it, P to proceed, or Q to quit: <b>P</b>

Version is: 8.4
Attempting to create and populate the bucardo database and schema
Database creation is complete

Connecting to database 'bucardo' as user 'bucardo'
Updated configuration setting "piddir"
Installation is now complete.

If you see any unexpected errors above, please report them to bucardo-general@bucardo.org

You should probably check over the configuration variables next, by running:
bucardo_ctl show all
Change any setting by using: bucardo_ctl set foo=bar
</none>
```

Because we don’t want to tell the bucardo_ctl program our custom port each time we call it, we’ll store that info into the ~/.bucardorc file:

```bash
$ echo dbport=5400 > ~/.bucardorc
```

Let’s double check that everything went okay by checking the list of databases that Bucardo knows about:

```bash
$ bucardo_ctl list db
There are no entries in the 'db' table.
```

Time to teach Bucardo about our two new databases. The format for the add commands is: bucardo_ctl add [type of thing] [name of thing within the database] [arguments of foo=bar format]

```bash
$ bucardo_ctl add database postgres name=master port=5401
Database added: master

$ bucardo_ctl add database postgres name=slave1 port=5402
Database added: slave1
```

Before we go any further, let’s look at our databases:

```bash
$ bucardo_ctl list dbs
Database: master   Status: active
Conn: psql -h  -p 5401 -U bucardo -d postgres

Database: slave1   Status: active
Conn: psql -h  -p 5402 -U bucardo -d postgres
```

Note that by default we connect as the ‘bucardo’ user. This is a highly recommended practice, for safety and auditing. Since that user obviously does not exist on the newly created databases, we need to add them in:

```bash
$ psql -p 5401 -c 'create user bucardo superuser'
$ psql -p 5402 -c 'create user bucardo superuser'
```

Now we need to teach Bucardo about the tables we want to replicate:

```bash
$ bucardo_ctl add table trtest db=master herd=herd1
Created herd "herd1"
Table added: public.trtest
```

A herd is simply a named connection of tables. Typically, you put tables that are linked together by foreign keys or other logic into a herd so that they all get replicated at the same time.

The final setup step is to create a replication event, which in Bucardo is known as a ‘sync’:

```bash
$ bucardo_ctl add sync willow source=herd1 targetdb=slave1 type=pushdelta
NOTICE:  Starting validate_sync for willow
CONTEXT:  SQL statement "SELECT validate_sync('willow')"
Sync added: willow
```

This command actually did quite a bit of work behind the scenes, including creating all the supporting schemas, tables, functions, triggers, and indexes that Bucardo will need.

We are now ready to start Bucardo up. Simple enough:

```bash
$ bucardo_ctl start
Checking for existing processes
Starting Bucardo
```

Let’s add a row to the master table and make sure it goes to the slave:

```sql
$ psql -p 5401 -c 'insert into trtest(id) VALUES (1)'
INSERT 0 1
$ psql -p 5402 -c 'select * from trtest'
 id
----
  1
(1 row)
```

Looks fine, so let’s try out the truncate. On versions of Postgres less than 8.4, there was no way for Bucardo (or Slony) to know that a truncate had been run, so the rows were removed from the master but not from the slave. We’ll do a truncate and add a new row in a single operation:

```sql
$ psql -p 5401 -c 'begin; truncate table trtest; insert into trtest values (2); commit'
COMMIT
$ psql -p 5402 -c 'select * from trtest'
 id
----
  2
(1 row)
```

It works! Let’s clean up our test environment for good measure:

```bash
$ bucardo_ctl stop
$ pg_ctl stop -D bcdata
$ pg_ctl stop -D testA
$ pg_ctl stop -D testB
```

As mentioned, there are three types of syncs in Bucardo. The other type that can make use of truncate triggers is the ‘swap’ sync, aka “master to master”. I’ve not yet decided on the behavior for such syncs, but one possibility is simply:

- Database A gets truncated at time X
- Bucardo truncates database B, then discards all delta rows older than X for both A and B, and all delta rows for B
- Everything after X gets processed as normal (conflict resolution, etc.)
- The same thing for a truncate on database B (truncate A, discard all older rows).

Second proposal:

- Database A gets truncated at time X
- We populate the delta table with every primary key in the table before truncation (assuming we can get at it)
- That’s it! Bucardo does its normal thing as if we just deleted a whole bunch of rows on A, and in theory deletes them from B as well.

Comments on this strategy welcome!

**Update:** Clarified initdb cluster vs. database per comment #1 below, and added new truncation handling scheme for multi-master replication per comment #2.
