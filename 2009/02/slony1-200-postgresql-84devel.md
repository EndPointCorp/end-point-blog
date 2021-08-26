---
author: Josh Tolley
title: Slony1-2.0.0 + PostgreSQL 8.4devel
github_issue_number: 96
tags:
- postgres
date: 2009-02-02
---

Many people use [Slony](http://www.slony.info) to replicate PostgreSQL databases in various interesting ways. Slony is a bit tough to get used to, but works very well, and can be found in important places at a number of high-load, high-profile sites. A few weeks back I set up Slony1-2.0.0 (the latest release) with a development version of PostgreSQL 8.4, and kept track of the play-by-play, as follows:

### Starting Environment

On this machine, PostgreSQL is installed from the CVS tree. I updated the tree and reinstalled just to have a well-known starting platform (output of each command has been removed for brevity).

```
jtolley@uber:~/devel/pgsql$ make distclean
jtolley@uber:~/devel/pgsql$ cvs update -Ad
jtolley@uber:~/devel/pgsql$ ./configure --prefix=/home/jtolley/devel/pgdb
jtolley@uber:~/devel/pgsql$ make
jtolley@uber:~/devel/pgsql$ make install
jtolley@uber:~/devel/pgsql$ cd ../pgdb
jtolley@uber:~/devel/pgdb$ initdb data
jtolley@uber:~/devel/pgdb$ pg_ctl -l ~/logfile -D data start
```

The --prefix option in ./configure tells PostgreSQL where to install itself.

Slony uses a daemon called slon to do its work, and slon connects to a database over TCP, so I needed to configure PostgreSQL to allow TCP connections by editing postgresql.conf appropriately and restarting PostgreSQL.
[edit] Installing Slony

Next, I downloaded slony1-2.0.0.tar.bz2 and checked its MD5 checksum

```
jtolley@uber:~/downloads$ wget http://www.slony.info/downloads/2.0/source/slony1-2.0.0.tar.bz2
--2008-12-17 11:29:54--  http://www.slony.info/downloads/2.0/source/slony1-2.0.0.tar.bz2
Resolving www.slony.info... 207.173.203.170
Connecting to www.slony.info|207.173.203.170|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 909567 (888K) [application/x-tar]
Saving to: `slony1-2.0.0.tar.bz2'
...
jtolley@uber:~/downloads$ md5sum slony1-2.0.0.tar.bz2 
d0c4955f10fe8efb7f4bbacbe5ee732b  slony1-2.0.0.tar.bz2
```

The MD5 checksum matches the one given on the slony website, so we can continue. First, I unzipped the download into /home/jtolley/devel/slony1-2.0.0. Now we need to configure and build the source. Again, the output of each command has been removed for brevity.

```
jtolley@uber:~/devel/slony1-2.0.0$ ./configure --with-pgconfigdir=/home/jtolley/devel/pgdb/bin/ \
> --prefix=/home/jtolley/devel/slony --with-perltools=/home/jtolley/devel/pgdb/bin
jtolley@uber:~/devel/slony1-2.0.0$ make
jtolley@uber:~/devel/slony1-2.0.0$ make install
```

The configure options tell slony where to find pg_config, a program that reports the locations of various important PostgreSQL libraries and other components, where to install slony, and where to put slony’s perl-based toolset, which we’ll use later.

I also added /home/jtolley/devel/slony/bin to my PATH.

### Setting Up Replication

#### Configuring PostgreSQL

The Slony documentation demonstrates setting up a database with pgbench and replicating it to another database. This document demonstrates the same thing. We’ll create a slony user, databases pgbench and pgbenchslave, use the pgbench utility to create a schema, and then copy that schema to pgbenchslave. We’ll then set up slony to replicate changes in pgbench to pgbenchslave.

Each slony database needs a slon process connected to it using a superuser account. First, we’ll create the superuser account, called slony, and a pair of databases called pgbench and pgbenchslave:

```
jtolley@uber:~/devel/pgdb$ createuser -sP slony
Enter password for new role: 
Enter it again: 
jtolley@uber:~/devel/pgdb$ createdb pgbench
jtolley@uber:~/devel/pgdb$ createdb pgbenchslave
```

Now we’ll create some schema objects in the pgbench database using the pgbench utility (the output from pgbench isn’t shown here):

```
jtolley@uber:~/devel/pgdb$ pgbench -i -s 1 pgbench
```

Slony requires PL/pgSQL, so we’ll install it now, in both databases:

```
jtolley@uber:~/devel/pgdb$ for i in pgbench pgbenchslave ; do createlang plpgsql $i ; done
```

Note: Here we have to make changes from what older versions of slony expect. Slony requires every replicated table to have a primary key, and used to be able to create keys for tables that didn’t otherwise have them, if instructed to do so. As of version 2.0.0 that’s no longer possible, perhaps because it was a bad idea anyway, in most cases, for users to do it. So we have to make sure each table has a primary key. The pgbench schema consists of four tables, called accounts, branches, tellers, and history. Of these four, history doesn’t have a primary key, so we need to create one. Here’s how I did it:

```
jtolley@uber:~/devel/pgdb$ psql -Xc "alter table history add id serial primary key;" pgbench
NOTICE:  ALTER TABLE will create implicit sequence "history_id_seq" for serial column "history.id"
NOTICE:  ALTER TABLE / ADD PRIMARY KEY will create implicit index "history_pkey" for table "history"
ALTER TABLE
```

Note the -X in the call to psql; this prevents the “\set AUTOCOMMIT off” setting in my psqlrc file from taking effect, so I didn’t have to add a “commit” command to the stuff I send psql.

Now that our schema is set up properly, let’s copy it from pgbench to pgbenchslave. In this case we want to replicate all tables, so we’ll copy everything.

```
jtolley@uber:~/devel/pgdb$ pg_dump -s pgbench | psql -X pgbenchslave
```

#### Configuring Slony’s altperl Scripts

Now we’re ready to set up slony, and we’ll make use of slony’s altperl scripts to do most of the configuration grunt work for us. To make altperl work, we need to set up slon_tools.conf. A sample already lives in slony/etc/slon_tools.conf-sample.

```
jtolley@uber:~/devel/pgdb$ cd ../slony/etc/
jtolley@uber:~/devel/slony/etc$ cp slon_tools.conf-sample slon_tools.conf
jtolley@uber:~/devel/slony/etc$ vim slon_tools.conf
```

This file defines nodes and sets, and is written in Perl. First, a group of nodes makes a slony cluster, which is a named object. You can set that name with the $CLUSTER_NAME parameter. We also need a directory where log information will be written, which goes in the $LOGDIR parameter. In this case, I’ve set it to “/home/jtolley/devel/slony/log”, which I’ve manually created. The slon daemons need write access to this directory; since they’ll be running as me on this machine, that’s fine.

Next we add all the nodes. In this case, there are only two nodes, defined as follows:

```
    add_node(node     => 1,
             host     => 'localhost',
             dbname   => 'pgbench',
             port     => 5432,
             user     => 'slony',
             password => 'slony');
    add_node(node     => 2,
             host     => 'localhost',
             dbname   => 'pgbenchslave',
             port     => 5432,
             user     => 'slony',
             password => 'slony');
```

I had to remove definitions of nodes 3 and 4 from the sample configuration.

Now we define replication sets. This involves defining tables and the unique, not null indexes slony can use as a primary key. If the table has an explicitly defined primary key, slony will use it automatically. Because of our modifications to the history table above, all four of our tables have primary keys, so this part is simple. All our table names go in the pkeyedtables element of the $SLONY_SETS hash, as follows:

```
        "pkeyedtables" => [     
                                'public.accounts',
                                'public.tellers',
                                'public.history',
                                'public.branches'
                           ],
```

We don’t have any tables without primary keys, so we don’t need the keyedtables element, and Slony no longer creates serial indexes for you as of v2.0.0, so we can delete the serialtables element. We do need to replicate the history_id_seq we created as part of the history table’s primary key, so add that to the sequences element, as follows:

```
        "sequences" => ['history_id_seq' ],
```

Finally, remove the sample configuration for set 2, and save the file.

#### Generating Slonik Configuration

Now that we’ve configured the altperl stuff, we can use it to generate scripts that will be passed to slonik, that will actually set things up.

```
jtolley@uber:~/devel/pgdb$ slonik_init_cluster > initcluster
jtolley@uber:~/devel/pgdb$ slonik_create_set 1 > createset
jtolley@uber:~/devel/pgdb$ slonik_subscribe_set 1 2 > subscribeset
```

This creates three files each containing slonik code to set up a cluster and get it running. If you tried to use the serialtables stuff, you’ll run into problems here with new versions of slony (not that I had that problem or anything...). Note that the arguments to slonik_subscribeset differ from those given in the documentation. This script requires two arguments: the set you’re interested in, and the node that’s subscribing to it.

### Starting Everything Up

We’re ready to do real work. Tell slonik to initialize the cluster:

```
jtolley@uber:~/devel/pgdb$ slonik < initcluster 
<stdin>:6: Possible unsupported PostgreSQL version (80400) 8.4, defaulting to 8.3 support
<stdin>:6: could not open file /home/jtolley/devel/slony/share/postgresql/slony1_base.sql
</stdin></stdin>
```

The complaints about version 8.4 aren’t surprising, as I’m using bleeding-edge PostgreSQL. But I think I had something wrong with my directories when I built slony. The files in question ended up in /home/jtolley/devel/pgdb/share/postgresql, so I did this:

```
jtolley@uber:~/devel/pgdb$ mkdir ../slony/share
jtolley@uber:~/devel/pgdb$ cp -r share/postgresql/ ../slony/share/
jtolley@uber:~/devel/pgdb$ slonik < initcluster 
<stdin>:6: Possible unsupported PostgreSQL version (80400) 8.4, defaulting to 8.3 support
<stdin>:9: Possible unsupported PostgreSQL version (80400) 8.4, defaulting to 8.3 support
<stdin>:10: Set up replication nodes
<stdin>:13: Next: configure paths for each node/origin
<stdin>:16: Replication nodes prepared
<stdin>:17: Please start a slon replication daemon for each node
</stdin></stdin></stdin></stdin></stdin></stdin>
```

This looks right, so the next step is to start the slon daemon for each node:

```
jtolley@uber:~/devel/pgdb$ slon_start 1
Invoke slon for node 1 - /home/jtolley/devel/slony/bin/slon -s 1000 -d2 replication 'host=localhost dbname=pgbench user=slony port=5432 passwor
d=slony' > /home/jtolley/devel/slony/log/slony1/node1/pgbench-2008-12-17_12:33:18.log 2>&1 &                                                   Slon successfully started for cluster replication, node node1
PID [24745]
Start the watchdog process as well...
jtolley@uber:~/devel/pgdb$ syntax error at /home/jtolley/devel/pgdb/bin/slon_watchdog line 47, near "open "
Execution of /home/jtolley/devel/pgdb/bin/slon_watchdog aborted due to compilation errors.
```

Slony shipped a bug in slon_watchdog—​line 46 needs to have a semicolon at the end.

```
jtolley@uber:~/devel/pgdb$ pkill slon
jtolley@uber:~/devel/pgdb$ vim ../pgdb/bin/slon_watchdog
```

Change line 46 to read:

```
    my ($logfile) = "$LOGDIR/slon-$dbname-$node.err";
```

... and try again:

```
jtolley@uber:~/devel/pgdb$ slon_start 1
Invoke slon for node 1 - /home/jtolley/devel/slony/bin/slon -s 1000 -d2 replication 'host=localhost dbname=pgbench user=slony port=5432 passwor
d=slony' > /home/jtolley/devel/slony/log/slony1/node1/pgbench-2008-12-17_12:35:29.log 2>&1 &                                                   Slon successfully started for cluster replication, node node1
PID [24918]
Start the watchdog process as well...
jtolley@uber:~/devel/pgdb$ slon_start 2
Invoke slon for node 2 - /home/jtolley/devel/slony/bin/slon -s 1000 -d2 replication 'host=localhost dbname=pgbenchslave user=slony port=5432 pa
ssword=slony' > /home/jtolley/devel/slony/log/slony1/node2/pgbenchslave-2008-12-17_12:35:31.log 2>&1 &                                         Slon successfully started for cluster replication, node node2
PID [24962]
Start the watchdog process as well...
```

Now we need to create the cluster and subscribe:

```
jtolley@uber:~/devel/pgdb$ slonik < createset 
<stdin>:16: Subscription set 1 created
<stdin>:17: Adding tables to the subscription set
<stdin>:21: Add primary keyed table public.accounts
<stdin>:25: Add primary keyed table public.tellers
<stdin>:29: Add primary keyed table public.history
<stdin>:33: Add primary keyed table public.branches
<stdin>:36: Adding sequences to the subscription set
<stdin>:40: Add sequence public.history_id_seq
<stdin>:41: All tables added
jtolley@uber:~/devel/pgdb$ slonik < subscribeset 
<stdin>:10: Subscribed nodes to set 1
</stdin></stdin></stdin></stdin></stdin></stdin></stdin></stdin></stdin></stdin>
```

### Watching It Work

Now we can make it do something interesting. First, start watching the logs. They live in /home/jtolley/devel/slony/log/slony1, and we can watch them like this, since there aren’t too many log files involved:

```
jtolley@uber:~/devel/slony/log/slony1$ find . -type f | xargs tail -f
```

This shows lots of log info. If you want to see more, run another pgbench instance:

```
jtolley@uber:~/devel/pgdb$ pgbench -s 1 -c 5 -t 1000 pgbench
```

For extra credit, add another table to the replication set, get it replicated, and manually insert data. See if the new data come across.
