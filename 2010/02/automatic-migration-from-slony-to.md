---
author: Josh Tolley
title: Automatic migration from Slony to Bucardo
github_issue_number: 261
tags:
- postgres
date: 2010-02-01
---



About [a month ago](https://mail.endcrypt.com/pipermail/bucardo-general/2009-December/000489.html), Bucardo added an interesting set of features in the form of a [new script called slony_migrator.pl](https://github.com/bucardo/bucardo/blob/master/scripts/slony_migrator.pl). In this post I’ll describe slony_migrator.pl and its three major functions.

### The Setup

For these examples, I’m using the [pagila sample database](http://pgfoundry.org/projects/dbsamples/) along with a set of scripts I wrote and made available [here](http://josh.endpoint.com/slony-pagila.tgz). These scripts build two different Slony clusters. The first is a simple one, which replicates this database from a database called "pagila1" on one host to a database "pagila2" on another host. The second is more complex. Its one master node replicates the pagila database to two slave nodes, one of which replicates it again to a fourth slave using Slony’s FORWARD function as described [here](/blog/2010/01/postgres-slony-cascading-subscription). I implemented this setup on two FreeBSD virtual machines, known as myfreebsd and myfreebsd2. The reset-simple.sh and reset-complex.sh scripts in the script package I’ve linked to will build all the necessary databases from one pagila database and do all the Slony configuration.

### Slony Synopsis

The slony_migrator.pl script has three possible actions, the first of which is to connect to a running Slony cluster and print a synopsis of the Slony setup it discovers. You can do this safely against a running, production Slony cluster; it gathers all its necessary information from a few simple Slony queries. Here’s the synopsis the script writes for the simple configuration I described above:

```plain
josh@eddie:~/devel/bucardo/scripts$ ./slony_migrator.pl -db pagila1 -H myfreebsd
Slony version: 1.2.16
psql version: 8.3
Postgres version: 8.3.7
Slony schema: _pagila
Local node: 1
SET 1: All pagila tables
* Master node: 1  Active: Yes  PID: 3309  Comment: "Cluster node 1"
  (dbname=pagila1 host=myfreebsd user=postgres)
  ** Slave node:  2  Active: Yes  Forward: Yes  Provider:  1  Comment: "Node 2"
     (dbname=pagila2 host=myfreebsd2 user=postgres)
```

The script has reported the Slony, PostgreSQL, and psql versions, the Slony schema name, and shows that there’s only one set, replicated from the master node to one slave node, including connection information for each node. Here is the output of the same action, run against the complex slony setup. Notice that node 3 has node 2 as its provider, not node 1:

```plain
josh@eddie:~/devel/bucardo/scripts$ ./slony_migrator.pl -db pagila1 -H myfreebsd
Slony version: 1.2.16
psql version: 8.3
Postgres version: 8.3.7
Slony schema: _pagila
Local node: 1
SET 1: All pagila tables
* Master node: 1  Active: Yes  PID: 3764  Comment: "Cluster node 1"
  (dbname=pagila1 host=myfreebsd  user=postgres)
  ** Slave node:  2  Active: Yes  Forward: Yes  Provider:  1  Comment: "Cluster node 2"
     (dbname=pagila2 host=myfreebsd2 user=postgres)
  ** Slave node:  3  Active:  No  Forward: Yes  Provider:  2  Comment: "Cluster node 3"
     (dbname=pagila3 host=myfreebsd2 user=postgres)
  ** Slave node:  4  Active: Yes  Forward: Yes  Provider:  1  Comment: "Cluster node 4"
     (dbname=pagila4 host=myfreebsd  user=postgres)
```

This is a simple way to get an idea of how a Slony cluster is organized. Again, we can get all this without downtime or any impact on the Slony cluster.

### Creating Slonik Scripts Automatically

Slony gets its configuration entirely through scripts passed to an application called Slonik, which writes configuration entries into a Slony schema within a replicated database. At least as far as I know, however, Slony doesn’t provide a way to regenerate those scripts based on the contents of that schema. The slony_migrator.pl script will do that for you with the --slonik option. For example, here is the Slonik script it generates for the simple configuration:

```plain
josh@eddie:~/devel/bucardo/scripts$ ./slony_migrator.pl -db pagila1 -H myfreebsd --slonik
CLUSTER NAME = pagila;
NODE 1 ADMIN CONNINFO = 'dbname=pagila1 host=myfreebsd user=postgres';
NODE 2 ADMIN CONNINFO = 'dbname=pagila2 host=myfreebsd2 user=postgres';
INIT CLUSTER (ID = 1, COMMENT = 'Cluster node 1');
STORE NODE (ID = 2, EVENT NODE = 1, COMMENT = 'Node 2');
STORE PATH (SERVER = 1, CLIENT = 2, CONNINFO = 'dbname=pagila1 host=myfreebsd user=postgres', CONNRETRY = 10);
STORE PATH (SERVER = 2, CLIENT = 1, CONNINFO = 'dbname=pagila2 host=myfreebsd2 user=postgres', CONNRETRY = 10);
ECHO 'Please start up replication nodes here';
TRY {
    CREATE SET (ID = 1, ORIGIN = 1, COMMENT = 'All pagila tables');
} ON ERROR {
    EXIT -1;
}
SET ADD TABLE (ID = 6, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.customer', KEY = 'customer_pkey', COMMENT = 'public.customer');
SET ADD TABLE (ID = 11, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.language', KEY = 'language_pkey', COMMENT = 'public.language');
--- snip ---
SET ADD SEQUENCE (ID = 13, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.store_store_id_seq', COMMENT = 'public.store_store_id_seq');
SET ADD SEQUENCE (ID = 10, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.payment_payment_id_seq', COMMENT = 'public.payment_payment_id_seq');
SET ADD SEQUENCE (ID = 5, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.country_country_id_seq', COMMENT = 'public.country_country_id_seq');
SUBSCRIBE SET (ID = 1, PROVIDER = 1, RECEIVER = 2, FORWARD = YES);
```

The pagila database contains many tables and sequences, and I’ve removed the repetitive commands to tell Slony about all of them, for the sake of brevity, but in its original form, the code above would rebuild the simple Slony cluster exactly, and can be very useful for getting an idea of how an otherwise unknown cluster is configured. I won’t promise the Slonik code is ideal, but it does recreate a working cluster. The more complex Slonik output is very similar, differing only in how the sets are subscribed. Here I’ll show only the major differences, which are the commands required to create the more complex Slony subscription scheme. In the downloadable script package I mentioned above, this subscription code is somewhat more complex, specifically because Slony won’t let you subscribe node 3 to updates from node 2 until node 2 is fully subscribed itself. The slony_migrator.pl script isn’t smart enough on its own to add necessary WAIT FOR EVENT Slonik commands, but it does get most of the code right, and, importantly, creates the subscriptions in the proper order.

```plain
SET ADD SEQUENCE (ID = 10, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.payment_payment_id_seq', COMMENT = 'public.payment_payment_id_seq');
SET ADD SEQUENCE (ID = 5, ORIGIN = 1, SET ID = 1, FULLY QUALIFIED NAME = 'public.country_country_id_seq', COMMENT = 'public.country_country_id_seq');
SUBSCRIBE SET (ID = 1, PROVIDER = 1, RECEIVER = 4, FORWARD = YES);
SUBSCRIBE SET (ID = 1, PROVIDER = 1, RECEIVER = 2, FORWARD = YES);
SUBSCRIBE SET (ID = 1, PROVIDER = 2, RECEIVER = 3, FORWARD = YES);
```

### Migrating Slony Clusters to Bucardo

The final slony_migrator.pl option will create a set of bucardo_ctl commands to create a Bucardo cluster to match an existing Slony setup. Although Bucardo can be configured by directly modifying its configuration database, a great deal of work of late has gone into making configuration easier through the bucardo_ctl program. Here’s the output from slony_migrator.pl on the simple Slony cluster. Note the --bucardo command-line option, which invokes this function:

```plain
josh@eddie:~/devel/bucardo/scripts$ ./slony_migrator.pl -db pagila1 -H myfreebsd --bucardo
./bucardo_ctl add db pagila_1 dbname=pagila1  host=myfreebsd user=postgres
./bucardo_ctl add db pagila_2 dbname=pagila2  host=myfreebsd2 user=postgres
./bucardo_ctl add table public.customer db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.language db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.store db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.category db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.film db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
--- snip ---
./bucardo_ctl add sequence public.city_city_id_seq db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add sequence public.store_store_id_seq db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add sequence public.payment_payment_id_seq db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add sequence public.country_country_id_seq db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add sync pagila_set1_node1_to_node2 source=pagila_node1_set1 targetdb=pagila_2 type=pushdelta
```

The Bucardo model of a replication system differs from Slony, but the two match fairly closely, especially for a simple scenario like this one. But slony_migrator.pl will work for the more complex Slony example I’ve been using, shown here:

```plain
josh@eddie:~/devel/bucardo/scripts$ ./slony_migrator.pl -db pagila1 -H myfreebsd --bucardo
./bucardo_ctl add db pagila_1 dbname=pagila1  host=myfreebsd user=postgres
./bucardo_ctl add db pagila_4 dbname=pagila4  host=myfreebsd user=postgres
./bucardo_ctl add db pagila_3 dbname=pagila3  host=myfreebsd2 user=postgres
./bucardo_ctl add db pagila_2 dbname=pagila2  host=myfreebsd2 user=postgres
./bucardo_ctl add table public.customer db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.language db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.store db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
--- snip ---
./bucardo_ctl add sequence public.payment_payment_id_seq db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add sequence public.country_country_id_seq db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add sync pagila_set1_node1_to_node4 source=pagila_node1_set1 targetdb=pagila_4 type=pushdelta
./bucardo_ctl add sync pagila_set1_node1_to_node2 source=pagila_node1_set1 targetdb=pagila_2 type=pushdelta target_makedelta=on
./bucardo_ctl add table public.customer db=pagila_2 ping=true standard_conflict=source herd=pagila_node2_set1
./bucardo_ctl add table public.language db=pagila_2 ping=true standard_conflict=source herd=pagila_node2_set1
./bucardo_ctl add table public.store db=pagila_2 ping=true standard_conflict=source herd=pagila_node2_set1
--- snip ---
./bucardo_ctl add sequence public.store_store_id_seq db=pagila_2 ping=true standard_conflict=source herd=pagila_node2_set1
./bucardo_ctl add sequence public.payment_payment_id_seq db=pagila_2 ping=true standard_conflict=source herd=pagila_node2_set1
./bucardo_ctl add sequence public.country_country_id_seq db=pagila_2 ping=true standard_conflict=source herd=pagila_node2_set1
./bucardo_ctl add sync pagila_set1_node2_to_node3 source=pagila_node2_set1 targetdb=pagila_3 type=pushdelta
```

I mentioned the Bucardo data model differs from that of Slony. Slony contains a set of tables and sequences in a “set”, and that Slony set remains a distinct object on all databases where those objects are found. Bucardo, on the other hand, has a concept of a “sync”, which is a replication job from one database to one or more slaves (here I’m talking only about master->slave syncs, and ignoring for purposes of this post Bucardo’s ability to do multi-master replication). This makes the setup slightly different for the more complex Slony scenario, in that whereas Slony has one set and different subscriptions, in Bucardo I need to define the tables and sequences involved in each of three syncs: one from node 1 to node 2, one from node 1 to node 4, and one from node 2 to node 3. I also need to turn on Bucardo’s “makedelta” option for the node 1 -> node 2 sync, which is the Bucardo equivalent of the Slony FORWARD subscription option.

### Migrating from Slony to Bucardo

This post is getting long, but for the sake of demonstration let’s show a migration from Slony to Bucardo, using the more complex Slony example. First, I’ll create a blank database, and install Bucardo in it:

```plain
josh@eddie:~/devel/bucardo$ createdb bucardo
josh@eddie:~/devel/bucardo$ ./bucardo_ctl install
This will install the bucardo database into an existing Postgres cluster.
Postgres must have been compiled with Perl support,
and you must connect as a superuser

We will create a new superuser named 'bucardo',
and make it the owner of a new database named 'bucardo'

Current connection settings:
1. Host:          /tmp
2. Port:          5432
3. User:          postgres
4. Database:      postgres
5. PID directory: /var/run/bucardo
Enter a number to change it, P to proceed, or Q to quit: 
```

I’ll make the necessary configuration changes, and run the installation by following the simple menu.

```plain
Current connection settings:
1. Host:          /tmp
2. Port:          5432
3. User:          postgres
4. Database:      bucardo
5. PID directory: /home/josh/devel/bucardo/pid
Enter a number to change it, P to proceed, or Q to quit: p

Postgres version is: 8.3
Attempting to create and populate the bucardo database and schema
Database creation is complete

Connecting to database 'bucardo' as user 'bucardo'
Updated configuration setting "piddir"
Installation is now complete.

If you see any unexpected errors above, please report them to bucardo-general@bucardo.org

You should probably check over the configuration variables next, by running:
./bucardo_ctl show all
Change any setting by using: ./bucardo_ctl set foo=bar
```

Now I’ll use slony_migrator.pl to get a set of bucardo_ctl scripts to build my Bucardo cluster:

```plain
josh@eddie:~/devel/bucardo/scripts$ ./slony_migrator.pl -db pagila1 -H myfreebsd --bucardo > pagila-slony2bucardo.sh
josh@eddie:~/devel/bucardo/scripts$ head pagila-slony2bucardo.sh 
./bucardo_ctl add db pagila_1 dbname=pagila1  host=myfreebsd user=postgres
./bucardo_ctl add db pagila_4 dbname=pagila4  host=myfreebsd user=postgres
./bucardo_ctl add db pagila_3 dbname=pagila3  host=myfreebsd2 user=postgres
./bucardo_ctl add db pagila_2 dbname=pagila2  host=myfreebsd2 user=postgres
./bucardo_ctl add table public.customer db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.language db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.store db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.category db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.film db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
./bucardo_ctl add table public.film_category db=pagila_1 ping=true standard_conflict=source herd=pagila_node1_set1
```

I’ll run the script...

```plain
josh@eddie:~/devel/bucardo$ sh scripts/pagila-slony2bucardo.sh
Added database "pagila_1"   
Added database "pagila_4"   
Added database "pagila_3"   
Added database "pagila_2"   
Created herd "pagila_node1_set1"
Added table "public.customer"
Added table "public.language"
Added table "public.store"
--- snip ---
Added sequence "public.store_store_id_seq"
Added sequence "public.payment_payment_id_seq"
Added sequence "public.country_country_id_seq"
Added sync "pagila_set1_node1_to_node4"
Added sync "pagila_set1_node1_to_node2"
Created herd "pagila_node2_set1"
Added table "public.customer"
Added table "public.language"
Added table "public.store"
--- snip ---
Added sequence "public.store_store_id_seq"
Added sequence "public.payment_payment_id_seq"
Added sequence "public.country_country_id_seq"
Added sync "pagila_set1_node2_to_node3"
```

Now all that’s left is to shut down Slony (I just use the "pkill slon" command on each database server), start Bucardo, and, eventually, remove the Slony schemas. Note that Bucardo runs only on one machine (which in this case isn’t either of the database servers I’m using for this demonstration—​Bucardo can run effectively anywhere you want).

```plain
josh@eddie:~/devel/bucardo$ ./bucardo_ctl start
Checking for existing processes
Removing /home/josh/devel/bucardo/pid/fullstopbucardo
Starting Bucardo
josh@eddie:~/devel/bucardo$ tail -f log.bucardo 
[Mon Feb  1 21:45:27 2010]  KID Setting sequence public.actor_actor_id_seq to value of 202, is_called is 1
[Mon Feb  1 21:45:27 2010]  KID Setting sequence public.city_city_id_seq to value of 600, is_called is 1
[Mon Feb  1 21:45:27 2010]  KID Setting sequence public.store_store_id_seq to value of 2, is_called is 1
[Mon Feb  1 21:45:27 2010]  KID Setting sequence public.payment_payment_id_seq to value of 32098, is_called is 1
[Mon Feb  1 21:45:27 2010]  KID Setting sequence public.country_country_id_seq to value of 109, is_called is 1
[Mon Feb  1 21:45:27 2010]  KID Total delta count: 0
[Mon Feb  1 21:45:27 2010]  CTL Got notice "bucardo_syncdone_pagila_set1_node1_to_node2_pagila_2" from 22961
[Mon Feb  1 21:45:27 2010]  CTL Sent notice "bucardo_syncdone_pagila_set1_node1_to_node2"
[Mon Feb  1 21:45:27 2010]  CTL Got notice "bucardo_syncdone_pagila_set1_node1_to_node4_pagila_4" from 22962
[Mon Feb  1 21:45:27 2010]  CTL Sent notice "bucardo_syncdone_pagila_set1_node1_to_node4"
```

Based on those logs, it looks like everything’s running fine, but just to make sure, I’ll use bucardo_ctl’s "list syncs" and "status" commands:

```plain
josh@eddie:~/devel/bucardo$ ./bucardo_ctl list syncs
Sync: pagila_set1_node1_to_node2  (pushdelta)  pagila_node1_set1 =>  pagila_2  (Active)
Sync: pagila_set1_node1_to_node4  (pushdelta)  pagila_node1_set1 =>  pagila_4  (Active)
Sync: pagila_set1_node2_to_node3  (pushdelta)  pagila_node2_set1 =>  pagila_3  (Active)

josh@eddie:~/devel/bucardo$ ./bucardo_ctl status
Days back: 3  User: bucardo  Database: bucardo  Host: /tmp  PID of Bucardo MCP: 22936
Name                       Type  State PID   Last_good Time  I/U/D Last_bad Time
==========================+=====+=====+=====+=========+=====+=====+========+====
pagila_set1_node1_to_node2| P   |idle |22952|52s      |0s   |0/0/0|unknown |    
pagila_set1_node1_to_node4| P   |idle |22953|52s      |0s   |0/0/0|unknown |    
pagila_set1_node2_to_node3| P   |idle |22954|52s      |0s   |0/0/0|unknown |    
```

Everything looks good. Before I test that data are really replicated correctly, I’ll issue the a "DROP SCHEMA _pagila CASCADE" command in each database, which I can do while Bucardo’s running. If this were a production system, the best strategy, to avoid things getting replicated twice) would be to stop all applications, stop Slony, start Bucardo, and start the applications, though because Slony and Bucardo both replicate rows using primary keys, doing otherwise wouldn’t cause duplicated data.

Finally, I’ll tail the Bucardo logs while inserting rows in the pagila1 database, to see what happens. These rows tell me it’s working:

```plain
[Mon Feb  1 21:55:42 2010]  KID Setting sequence public.payment_payment_id_seq to value of 32098, is_called is 1
[Mon Feb  1 21:55:42 2010]  KID Setting sequence public.inventory_inventory_id_seq to value of 4581, is_called is 1
[Mon Feb  1 21:55:42 2010]  KID Setting sequence public.country_country_id_seq to value of 109, is_called is 1
[Mon Feb  1 21:55:42 2010]  KID Total delta count: 1
[Mon Feb  1 21:55:42 2010]  KID Deleting rows from public.actor
[Mon Feb  1 21:55:42 2010]  KID Begin COPY to public.actor
[Mon Feb  1 21:55:42 2010]  KID End COPY to public.actor
[Mon Feb  1 21:55:42 2010]  KID Pushdelta counts: deletes=0 inserts=1
[Mon Feb  1 21:55:42 2010]  KID Updating bucardo_track for public.actor on pagila_1
...
[Mon Feb  1 21:55:43 2010]  CTL Got notice "bucardo_syncdone_pagila_set1_node1_to_node4_pagila_4" from 22962
[Mon Feb  1 21:55:43 2010]  CTL Sent notice "bucardo_syncdone_pagila_set1_node1_to_node4"
[Mon Feb  1 21:55:43 2010]  CTL Got notice "bucardo_syncdone_pagila_set1_node1_to_node2_pagila_2" from 22961
[Mon Feb  1 21:55:43 2010]  CTL Sent notice "bucardo_syncdone_pagila_set1_node1_to_node2"
```

In this case I need to "kick" the node 2 -> node 3 sync to get it to replicate, but I could configure the sync with a timeout so that happened automatically. Once I do that, I get log messages for it as well.

```plain
[Mon Feb  1 22:00:34 2010]  CTL Got notice "bucardo_syncdone_pagila_set1_node2_to_node3_pagila_3" from 22963
[Mon Feb  1 22:00:34 2010]  CTL Sent notice "bucardo_syncdone_pagila_set1_node2_to_node3"
```

Please consider giving slony_migrator.pl a try. I’d be glad to hear how it works out.


