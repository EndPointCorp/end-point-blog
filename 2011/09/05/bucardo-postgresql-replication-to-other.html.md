---
author: Greg Sabino Mullane
gh_issue_number: 491
tags: bucardo, cloud, database, postgres
title: Bucardo PostgreSQL replication to other tables with customname
---



<a href="/blog/2011/09/05/bucardo-postgresql-replication-to-other/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5648699560032368754" src="/blog/2011/09/05/bucardo-postgresql-replication-to-other/image-0.jpeg" style="cursor:pointer; cursor:hand;width: 320px; height: 214px;"/></a>

Image by Flickr user [Soggydan](https://www.flickr.com/photos/soggydan/)

(Don’t miss the Bucardo5 talk at [Postgres Open](https://web.archive.org/web/20110927094014/http://postgresopen.org/2011/home/) in Chicago)

Work on the next major version of Bucardo is wrapping up (version 5 is now in beta), and two new features have been added to this major version. The first, called **customname**, allows you to replicate to a table with a different name. This has been a feature people have been asking for a long time, and even allows you to replicate between differently named Postgres schemas. The second option, called **customcols**, allows you replicate to different columns on the target: not only a subset, but different column names (and types), as well as other neat tricks.

The "customname" options allows changing of the table name for one or more targets. Bucardo replicates tables from the source databases to the target databases, and all tables must have the same name and schema everywhere. With the customname feature, you can change the target table names, either globally, per database, or per sync.

We’ll go through a full example here, using a stock 64-bit RedHat 6.1 EC2 box (ami-5e837b37). I find EC2 a great testing platform—​not only can you try different operating systems and architectures, but (as my own personal box is very customized) it is great to start afresh from a stock configuration.

First, let’s turn off SELinux, install the [EPEL rpm](https://fedoraproject.org/wiki/EPEL), update the box, and install a few needed packages.

```bash
echo 0 > /selinux/enforce
wget http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm        
rpm -ivh epel-release-6-5.noarch.rpm
yum update
yum install emacs-nox perl-DBIx-Safe perl-DBD-Pg git postgresql-plperl
cpan boolean
```

The yum update takes a while to run, but I always feel better when things are up to date. Next, we will create a new database cluster, create the /var/run/bucardo directory that Bucardo uses to store its PIDs, adjust the ultraconservative stock pg_hba.conf file, and start Postgres up:

```bash
service postgresql initdb
mkdir /var/run/bucardo
chown postgres.postgres /var/run/bucardo
emacs /var/lib/pgsql/data/pg_hba.conf                                        
service postgresql start
```

For the pg_hba.conf configuration file, because we want to be able to connect to the database as the bucardo user without actually logging into that account, we will allow access using the ‘md5’ (password) method instead of ‘ident’. But we don’t want to bother creating a password for the postgres user, we will still allow those connections via ident. The relevant lines in the pg_hba.conf will end up like this:

```bash
# TYPE   DATABASE   USER       METHOD
local    all        postgres   ident                          
local    all        all        md5                          
```

At this point, we (as the postgres user) download and install Bucardo itself:

```bash
su - postgres
git clone git://bucardo.org/bucardo.git
cd bucardo
perl Makefile.PL
make
sudo make install                                      
bucardo install# (enter 'p' and keep the default values)
```

We are now ready to start testing out the new customname feature. First we will need some data to replicate! For this demo we are going to use one of the handy sample datasets from [the dbsamples project](http://pgfoundry.org/projects/dbsamples/). The one we will use has a few small tables with information about towns in France. Note that the tarball does not (sadly) contain a top-level directory, so we have to create one ourselves. We will then create three identical databases holding the data from that file.

```bash
wget http://pgfoundry.org/frs/download.php/935/french-towns-communes-francaises-1.0.tar.gz                
mkdir frenchtowns
cd frenchtowns
tar xvfz ../french-towns-communes-francaises-1.0.tar.gz
psql -c 'create database french1'
psql french1 -q -f french-towns-communes-francaises.sql
psql -c 'create database french2 template french1'
psql -c 'create database french3 template french1'
psql -c 'create database french4 template french1'
```

Bucardo is installed but does not know what to do yet, so we will teach Bucardo about each of the databases, and add in all the tables, grouping then into a herd in the process. Finally, we create a sync in which french1 and french2 are both source (master) databases, and french3 and french4 will be target (slave) databases.

```bash
bucardo add db f1 db=french1
bucardo add db f2 db=french2
bucardo add db f3 db=french3
bucardo add db f4 db=french4
bucardo add all tables herd=fherd
bucardo add sync wildstar herd=fherd dbs=f1=source,f2=source,f3=target,f4=target
```

Before starting it up, I usually raise the debug level, as it gives a much clearer picture of what is going on in the logs. It does make the logs a lot more crowded, so it is not recommended for production use:

```bash
echo log_level=DEBUG >> ~/.bucardorc
```

Next, we start Bucardo up and make sure everything is working as it should. Scanning the log.bucardo file that is generated is a great way to do this:

```bash
bucardo start
sleep 3
tail log.bucardo
```

If all goes well, you should see something very similar to this in the last lines of your log.bucardo file:

```bash
(972) [Sat Sep  3 16:18:54 2011] KID Total time for sync "wildstar" (0 rows): 0.05 seconds
(966) [Sat Sep  3 16:18:55 2011] CTL Got NOTICE ctl_syncdone_wildstar from 973 (line 1624)
(966) [Sat Sep  3 16:18:55 2011] CTL Kid 973 has reported that sync wildstar is done
(966) [Sat Sep  3 16:18:55 2011] CTL Sending NOTIFY "syncdone_wildstar" (line 1709)
(954) [Sat Sep  3 16:18:55 2011] MCP Got NOTICE syncdone_wildstar from 967 (line 749)
(954) [Sat Sep  3 16:18:55 2011] MCP Sync wildstar has finished
(954) [Sat Sep  3 16:18:55 2011] MCP Sending NOTIFY "syncdone_wildstar" (line 812)
(954) [Sat Sep  3 16:18:56 2011] MCP Got NOTICE syncdone_wildstar from 957 (Bucardo DB) (line 749)
```

From the above, we see that a KID finished running the sync we created, without finding any changed rows to replicate. Then there is some chatter between the different Bucardo processes. Now to test out the customname feature. We’ll rename one of the tables, tell Bucardo about the change, reload the sync, and verify that all is still being replicated.

```bash
psql french3 -c 'ALTER TABLE regions RENAME TO tesla'
bucardo add customname regions tesla db=f3
bucardo reload wildstar
```

```bash
psql french3 -c 'truncate table tesla cascade'
TRUNCATE
psql french3 -t -c 'select count(*) from tesla'
0
psql french1 -c 'update regions set name=name'
UPDATE 26
psql french3 -t -c 'select count(*) from tesla'
26
```

In the above, the update on the regions table inthe french1 database calls a trigger that notifies Bucardo that some rows have changed; Bucardo then has a KID copy the rows from the source databases french1 to the other source database french2, as well as the targets french3 and french4. The final internal DELETE and COPY that it performs is done on database french3 to the tesla table rather than the regions table.

The customname feature cannot be used to change the tables in a source database, as they must all be the same (for obvious reasons). We can, however, specify that a different *schema* be used for a target, as well as a different table. This only applies to Postgres targets, as other database types (e.g. MySQL) do not use schemas. Let’s see that in action:

```bash
psql french4 -c 'create schema banana'
psql french4 -c 'alter table regions set schema banana'
psql french4 -c 'truncate table banana.regions cascade'
bucardo add customname regions banana.regions db=f4
bucardo reload wildstar
```

```bash
psql french4 -t -c 'select count(*) from banana.regions'
0
psql french2 -c 'update regions set name=name'
UPDATE 26
psql french4 -t -c 'select count(*) from banana.regions'
26
```

As before, the update on a source causes the changes to propagate to the other source database, as well as both targets. Note that the ALTER TABLE also mutated the associated sequence for the table, so there will be warnings in Bucardo’s logs about the DEFAULT values for the primary keys in the regions’ tables being different. Since this post is getting long, I will save the discussion of customcols for another day.


