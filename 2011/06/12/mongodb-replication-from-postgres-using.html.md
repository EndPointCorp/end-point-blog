---
author: Greg Sabino Mullane
gh_issue_number: 467
tags: bucardo, database, mongodb, nosql, open-source, perl, postgres
title: MongoDB replication from Postgres using Bucardo
---

<a href="/blog/2011/06/12/mongodb-replication-from-postgres-using/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5616998406288420578" src="/blog/2011/06/12/mongodb-replication-from-postgres-using/image-0.png" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 200px; height: 128px;"/></a>

One of the features of the upcoming version of [Bucardo](https://bucardo.org/Bucardo/) (a replication system for the PostgreSQL RDBMS) is the ability to replicate data to things other than [PostgreSQL](https://www.postgresql.org/) databases. One of those new targets is [MongoDB](https://www.mongodb.com/), a non-relational ‘document-based’ database. (to be clear, we can only use MongoDB as a target, not as a source)

To see this in action, let’s setup a quick example, modified from the [earlier blog post on running Bucardo 5](/blog/2011/06/06/bucardo-multi-master-for-postgresql). We will create a Bucardo instance that replicates from two Postgres master databases to a Postgres database target and a MongoDB instance target. We will start by setting up the prerequisites:

```bash
sudo aptitude install postgresql-server \
perl-DBIx-Safe \
perl-DBD-Pg \
postgresql-contrib
```

Getting Postgres up and running is left as an exercise to the reader. If you have problems, the friendly folks at #postgresql on irc.freenode.net will be able to help you out.

Now for the MongoDB parts. First, we need the server itself. Your distro may have it already available, in which case it’s as simple as:

```bash
aptitude install mongodb
```

For more installation information, follow the links from the [MongoDB Quickstart page](https://docs.mongodb.com/manual/installation/). For my test box, I ended up installing from source by following the directions at the [Building for Linux page](https://web.archive.org/web/20110608014829/http://www.mongodb.org/display/DOCS/Building+for+Linux).

Once MongoDB is installed, we will need to start it up. First, create a place for MongoDB to store its data, and then launch the mongodb process:

```bash
$  mkdir /tmp/mongodata
$  mongod --dbpath=/tmp/mongodata --fork --logpath=/tmp/mongo.log
all output going to: /tmp/mongo.log
forked process: 428
```

You can perform a quick test that it is working by invoking the command-line shell for MongoDB (named “mongo” of course) Use **quit()** to exit:

```bash
$  mongo
MongoDB shell version: 1.8.1
Fri Jun 10 12:45:00
connecting to: test
> quit()
$ 
```

The other piece we need is a Perl driver so that Bucardo (which is written in Perl) can talk to the MongoDB server. Luckily, there is an excellent one available on CPAN named ‘MongoDB’. We started the MongoDB server before doing this step because the driver we will install needs a running MongoDB instance to pass all of its tests. The module has very good documentation available on [its CPAN page](https://metacpan.org/release/MongoDB). Installation may be as easy as:

```bash
$  sudo cpan MongoDB
```

If that did not work for you (case matters!), there are more detailed directions on the [Perl Language Center](http://www.mongodb.org/display/DOCS/Perl+Language+Center) page.

Our next step is to grab the latest Bucardo, install it, and create a new Bucardo instance. See the [previous blog post](/blog/2011/06/06/bucardo-multi-master-for-postgresql) for more details about each step.

```bash
$ git clone git://bucardo.org/bucardo.git
Initialized empty Git repository...

$ cd bucardo
$ perl Makefile.PL
Checking if your kit is complete...
Looks good
Writing Makefile for Bucardo
$ make
cp bucardo.schema blib/share/bucardo.schema
cp Bucardo.pm blib/lib/Bucardo.pm
cp bucardo blib/script/bucardo
/usr/bin/perl -MExtUtils::MY -e 'MY->fixin(shift)' -- blib/script/bucardo
Manifying blib/man1/bucardo.1pm
Manifying blib/man3/Bucardo.3pm
$ sudo make install
Installing /usr/local/lib/perl5/site_perl/5.10.0/Bucardo.pm
Installing /usr/local/share/bucardo/bucardo.schema
Installing /usr/local/bin/bucardo
Installing /usr/local/share/man/man1/bucardo.1pm
Installing /usr/local/share/man/man3/Bucardo.3pm
Appending installation info to /usr/lib/perl5/5.10.0/i386-linux-thread-multi/perllocal.pod
$ sudo mkdir /var/run/bucardo
$ sudo chown $USER /var/run/bucardo
$ bucardo install
This will install the bucardo database into an existing Postgres cluster.
...
Installation is now complete.
```

Now we create some test databases and populate with pgbench:

```bash
$ psql -c 'create database btest1'
CREATE DATABASE
$ pgbench -i btest1
NOTICE:  table "pgbench_branches" does not exist, skipping
...
creating tables...
10000 tuples done.
20000 tuples done.
...
100000 tuples done.
$ psql -c 'create database btest2 template btest1'
CREATE DATABASE
$ psql -c 'create database btest3 template btest1'
CREATE DATABASE
$ psql btest3 -c 'truncate table pgbench_accounts'
TRUNCATE TABLE

$ bucardo add db t1 dbname=btest1
Added database "t1"
$ bucardo add db t2 dbname=btest2
Added database "t2"
$ bucardo add db t3 dbname=btest3
Added database "t3"
$ bucardo list dbs
Database: t1  Status: active  Conn: psql -p 5432 -U bucardo -d btest1
Database: t2  Status: active  Conn: psql -p 5432 -U bucardo -d btest2
Database: t3  Status: active  Conn: psql -p 5432 -U bucardo -d btest3

$ bucardo add tables pgbench_accounts pgbench_branches pgbench_tellers herd=therd
Created herd "therd"
Added table "public.pgbench_accounts"
Added table "public.pgbench_branches"
Added table "public.pgbench_tellers"

$ bucardo list tables
Table: public.pgbench_accounts  DB: t1  PK: aid (int4)
Table: public.pgbench_branches  DB: t1  PK: bid (int4)
Table: public.pgbench_tellers   DB: t1  PK: tid (int4)
```

The next step is to add in our MongoDB instance. The syntax is the same as the “add db” above, but we also tell it the type of database, as it is not the default of “postgres”. We will also assign an arbitrary database name, “btest1”, the same as the others. Everything else (such as the port and host) is default, so all we need to say is:

```bash
$  bucardo add db m1 dbname=btest1 type=mongo
Added database "m1"
$  bucardo list dbs
Database: m1  Type: mongo     Status: active  
Database: t1  Type: postgres  Status: active  Conn: psql -p 5432 -U bucardo -d btest1
Database: t2  Type: postgres  Status: active  Conn: psql -p 5432 -U bucardo -d btest2
Database: t3  Type: postgres  Status: active  Conn: psql -p 5432 -U bucardo -d btest3
```

Next we group our databases together and assign them roles:

```bash
$  bucardo add dbgroup tgroup  t1:source  t2:source  t3:target  m1:target
Created database group "tgroup"
Added database "t1" to group "tgroup" as source
Added database "t2" to group "tgroup" as source
Added database "t3" to group "tgroup" as target
Added database "m1" to group "tgroup" as target
```

Note that “target” is the default action, so we could shorten that to:

```bash
$  bucardo add dbgroup tgroup t1:source  t2  t3  m1
```

However, I think it is best to be explicit, even if it does (incorrectly) hint that m1 could be anything *other* than a target. :)

We are almost ready to go. The final step is to create a sync (a basic replication event in Bucardo), then we can start up Bucardo, put some test data into the master databases, and ‘kick’ the sync:

```bash
$  bucardo add sync mongotest  herd=therd  dbs=tgroup  ping=false
Added sync "mongotest"

$  bucardo start
Checking for existing processes
Starting Bucardo

$  pgbench -t 10000 btest1
starting vacuum...end.
transaction type: TPC-B (sort of)
number of transactions actually processed: 10000/10000
...
tps = 503.300595 (excluding connections establishing)
$  pgbench -t 10000 btest2
number of transactions actually processed: 10000/10000
...
tps = 408.059368 (excluding connections establishing)
$  bucardo kick mongotest
```

We’ll give it a few seconds to replicate those changes (it took 18 seconds on my test box), and then check the output of bucardo status:

```bash
$  bucardo status
PID of Bucardo MCP: 3317
 Name        State    Last good    Time    Last I/D/C    Last bad    Time  
===========+========+============+=======+=============+===========+=======
 mongotest | Good   | 21:57:47   | 11s   | 6/36234/898 | none      |
```

Looks good, but what about the data in MongoDB? Let’s get some counts from the Postgres masters and slave, and then look at the data inside MongoDB with the mongo command-line client:

```bash
$  psql btest1 -c 'SELECT count(*) FROM pgbench_accounts'
100000
$  psql btest2 -c 'SELECT count(*) FROM pgbench_accounts'
100000
$  psql btest3 -c 'SELECT count(*) FROM pgbench_accounts'
18106
$  psql btest1 -qc 'SELECT min(abalance),max(abalance) FROM pgbench_accounts'
-12071 | 13010
$  psql btest2 -qc 'SELECT min(abalance),max(abalance) FROM pgbench_accounts'
-12071 | 13010
$  psql btest3 -qc 'SELECT min(abalance),max(abalance) FROM pgbench_accounts'
-12071 | 13010

$  mongo btest1
MongoDB shell version: 1.8.1
Fri Jun 10 12:46:00
connecting to: btest1
> show collections
bucardo_status
pgbench_accounts
pgbench_branches
pgbench_tellers
system.indexes
>  db.pgbench_accounts.count()
18106
>  db.pgbench_accounts.find().sort({abalance:1}).limit(1).next()
{
  "_id" : ObjectId("4df39bcb8795839660001de5"),
  "abalance" : -12071,
  "aid" : 84733,
  "bid" : 1,
  "filler" : "               "
}
> db.pgbench_accounts.find().sort({abalance:-1}).limit(1).next()
{
  "_id" : ObjectId("4df39bd08795839660002fb0"),
  "abalance" : 13010,
  "aid" : 45500,
  "bid" : 1,
  "filler" : "               "
}
```

Why the difference in counts? We only started replicating after we populated the Postgres tables on the master databases with 100,000 rows, so the eighteen thousand is the number of rows that was changed during the subsequent pgbench run. (Note that pgbench uses randomness, so your numbers will be different than the above). In the future Bucardo will support the [“onetimecopy”](https://bucardo.org/Onetimecopy/) feature for MongoDB, but until then we can fully populate the pgbench_accounts collection simply by ‘touching’ all the records on one of the masters:

```bash
$ psql btest1 -c 'UPDATE pgbench_accounts SET aid=aid'
UPDATE 100000
$ bucardo kick mongotest
Kicked sync mongotest
$ echo 'db.pgbench_accounts.count()' | mongo btest1
MongoDB shell version: 1.8.1
Fri Jun 10 12:47:00
connecting to: btest1
> 100000
> bye

```

A nice feature of MongoDB is its autovivification ability (aka dynamic schemas), which means unlike Postgres you do not have to create your tables first, but can simply ask MongoDB to do an insert, and it will create the table (or, in mongospeak, the collection) automatically for you.

Because MongoDB has no concept of transactions, and because Bucardo does not update, but does deletes plus inserts (for reasons I’ll not get into today), there is one more trick Bucardo does when replicating to a MongoDB instance. A collection named ‘bucardo_status’ is created and updated at the start and the end of a sync (a replication event). Thus, your application can pause if it sees this table has a ‘started’ value, and wait until it sees ‘complete’ or ‘failed’. Not foolproof by any means, but better than nothing :) You should, of course, carefully consider the way your app and Bucardo will coordinate things.

Feedback from Postgres or MongoDB folk is much appreciated: there are probably some rough edges, but as you can see from above, the basics are there are working. Feel free to email the [bucardo-general mailing list](https://mail.endcrypt.com/mailman/listinfo/bucardo-general) or make a feature request / bug report on the [Bucardo GitHub page](https://github.com/bucardo/bucardo/issues).
