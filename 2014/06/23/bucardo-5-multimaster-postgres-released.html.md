---
author: Greg Sabino Mullane
gh_issue_number: 1001
tags: bucardo, database, postgres, replication, mongodb, mysql
title: Version 5 of Bucardo database replication system
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/06/23/bucardo-5-multimaster-postgres-released/image-0.jpeg" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/06/23/bucardo-5-multimaster-postgres-released/image-0.jpeg" width="350"/></a>
<br/><small><a href="https://flic.kr/p/6GYFk5">Goat & Kid</a> by Flickr user <a href="https://www.flickr.com/photos/bala_/">Bala Sivakumar</a></small></div>

Bucardo 5, the next generation of the async multimaster replication system, has been released. This major release removes the previous two source database limitation, allowing you to have as many sources (aka masters) and as many targets (aka slaves) as you wish. Bucardo can also replicate to other targets, including MySQL, MariaDB, Oracle, SQLite, MongoDB, and Redis. Bucardo has been completely rewritten and is more powerful and efficient 
than the previous version, known as Bucardo 4. You can always find the latest version [here](https://bucardo.org/).

This article will show a quick demonstration of Bucardo. Future posts will explore its capabilities further: 
for now, we will show how easy it is to get basic multimaster replication up and running.

For this demo, I used a quick and disposable server from [Amazon Web Services](https://aws.amazon.com/) (AWS, specifically a basic t1.micro server running Amazon Linux). If you want to follow along, it’s free and simple to create your own instance. Once it is created and you have SSH’ed in as the ec2-user account, we can start to install PostgreSQL and Bucardo.

```
# Always a good idea:
$ sudo yum update
# This also installs other postgresql packages:
$ sudo yum install postgresql-plperl
# Create a new Postgres cluster:
$ initdb btest
```

We cannot start Postgres up yet, as this distro uses both /var/run/postgresql and 
/tmp for its socket directory. Once we adjust the permissions of the first directory, 
we can start Postgres, and then create our first test database:

```
$ sudo chmod 777 /var/run/postgresql
$ pg_ctl -D btest -l logfile start
$ createdb shake1
```

Next, we need something to replicate! For a sample dataset, I like to use the open source Shakespeare project. It’s a small, free, simple schema that is easy to load. There’s a nice little [project on github](https://github.com/catherinedevlin/opensourceshakespeare) the contains a ready-made Postgres schema, so we will load that in to our new database:

```
$ sudo yum install git
$ git clone -q https://github.com/catherinedevlin/opensourceshakespeare.git
$ psql shake1 -q -f opensourceshakespeare/shakespeare.sql
# You can safely ignore the 'role does not exist' errors
```

We want to create duplicates of this database, to act as the other sources. In other words, other servers that have the identical data and can be written to. Simple enough:

```
$ createdb shake2 -T shake1
$ createdb shake3 -T shake1
```

Bucardo has some dependencies that need installing. You may have a different 
list depending on your distro: this is what Amazon Linux needed when I wrote this.
(If you are lucky, your distro may have Bucardo already available, in which case many of the steps below can be 
replaced e.g. with “yum install bucardo”—​just make sure it is using version 5 or better! (e.g. with yum info bucardo))

```
$ sudo yum install  perl-ExtUtils-MakeMaker  perl-DBD-Pg \
> perl-Encode-Locale  perl-Sys-Syslog perl-boolean \
> perl-Time-HiRes  perl-Test-Simple  perl-Pod-Parser
$ sudo yum install cpan
$ echo y | cpan DBIx::Safe
```

The Perl module DBIx::Safe was not available on this system’s yum, hence we 
needed to install it via [CPAN](https://www.cpan.org/). Once all of that is 
done, we are ready to install Bucardo. We’ll grab the official tarball, verify it, 
untar it, and run make install:

```
$ wget -nv http://bucardo.org/Bucardo.tar.gz
$ wget -nv http://bucardo.org/Bucardo.tar.gz.asc
$ gpg -q --keyserver pgp.mit.edu --recv-key 14964AC8
$ gpg --verify Bucardo.tar.gz.asc
$ tar xfz Bucardo.tar.gz
$ ln -s Bucardo-5.0.0 bucardo
$ cd bucardo
$ perl Makefile.PL
$ make
$ sudo make install
```

Let’s make some small adjustments via the bucardorc file (which sets some global information). Then we can run the 
“bucardo install”, which creates the main bucardo database, containing the information the Bucardo daemon will need:

```
$ mkdir pid
$ echo -e "piddir=pid\nlogdest=." > .bucardorc
$ bucardo install --batch --quiet
Creating superuser 'bucardo'
```

Now that Bucardo is installed and ready to go, let’s setup the replication. In this case, we 
are going to have three of our databases replicate to each other. We can do all this in 
only two commands:

```
$ bucardo add dbs s1,s2,s3 dbname=shake1,shake2,shake3
Added databases "s1","s2","s3"
$ bucardo add sync bard dbs=s1:source,s2:source,s3:source tables=all
Added sync "bard"
Created a new relgroup named "bard"
Created a new dbgroup named "bard"
  Added table "public.chapter"
  Added table "public.character"
  Added table "public.character_work"
  Added table "public.paragraph"
  Added table "public.wordform"
  Added table "public.work"
```

With the first command, we told Bucardo how to connect to three databases, and gave 
them names for Bucardo to refer to as (s1,s2,s3). You can also specify the 
port and host, but in this case the default values of 5432 and no host (Unix sockets) were sufficient.

The second command creates a named replication system, called a **sync**, and assigns 
it the name “bard”. It needs to know where and how to replicate, so we tell it to 
use the three databases s1,s2, and s3. Each of these is to act as a source, so we 
append that information as well. Finally, we need to know what to replicate. In this 
case, we simply want all tables (or to be more precise, all tables with a primary 
key or a unique index). Notice that Bucardo always puts databases and tables into 
named groups—​in this case, it was done automatically, and the dbgroup and relgroup 
are simply named after the sync.

Let’s verify that replication is working, by checking that a changed row replicates 
to all systems involved in the sync:

```
$ bucardo start
$ psql shake1 -c \
> "update character set speechcount=123 where charname='Hamlet'"
UPDATE 1
$ for i in {1,2,3}; do psql shake$i -tc "select \
> current_database(), speechcount from character \
> where charname='Hamlet'"; done | grep s
 shake1       |     123
 shake2       |     123
 shake3       |     123
```

We can also take a peek in the Bucardo log file, "log.bucardo" to see the replication happening:

```
$ tail -2 log.bucardo
(25181) KID (bard) Delta count for s1.public."character": 1
(25181) KID (bard) Totals: deletes=2 inserts=2 conflicts=0
```

There are two deletes and inserts because the changed row was first deleted, and then inserted 
(via COPY, technically) to the other two databases. Next, let’s see how Bucardo handles a conflict. 
We will have the same row get changed on all the servers, which should lead to a conflict:

```
$ for i in {1,2,3}; do psql shake$i -tc \
> "update character set speechcount=$i$i$i \
> where charname='Hamlet'"; done
UPDATE 1
UPDATE 1
UPDATE 1
```

Looking in the logs shows that we did indeed have a conflict, and that it was resolved. The default conflict resolution declares the last database to be updated the winner. All three databases now have the same winning row:

```
$ tail log.bucardo
(25181) KID (bard) Delta count for s1.public."character": 1
(25181) KID (bard) Delta count for s2.public."character": 1
(25181) KID (bard) Delta count for s3.public."character": 1
(25181) KID (bard) Conflicts for public."character": 1
(25181) KID (bard) Conflicts have been resolved
(25181) KID (bard) Totals: deletes=2 inserts=2 conflicts=1

$ for i in {1,2,3}; do psql shake$i -tc \
> "select current_database(), speechcount \
> from character where charname='Hamlet'"; done | grep s
 shake1       |     333
 shake2       |     333
 shake3       |     333
```

Sometimes when I was developing this demo, Bucardo was so fast that conflicts did not happen. In 
other words, because the updates were sequential, there is a window in which Bucardo can replicate 
a change before the next update occurs. The “pause a sync” feature can be very handy for this, 
as well as other times in which you need a sync to temporarily stop running:

```
$ bucardo pause bard
Syncs paused: bard
$ psql shake1 -c "update character set speechcount=1234 where charname='Hamlet'"
UPDATE 1
$ psql shake2 -c "update character set speechcount=4321 where charname='Hamlet'"
UPDATE 1
$ bucardo resume bard
Syncs resumed: bard

$ tail log.bucardo
(27344) KID (bard) Delta count for s1.public."character": 1
(27344) KID (bard) Delta count for s2.public."character": 1
(27344) KID (bard) Conflicts for public."character": 1
(27344) KID (bard) Conflicts have been resolved
(27344) KID (bard) Totals: deletes=2 inserts=2 conflicts=1
```

There is a lot more to Bucardo 5 than what is shown here. Future posts will cover 
other things it can do, from replicating to non-Postgres systems such as Oracle, 
MySQL, or MongoDB, to using custom conflict resolution mechanisms, to transforming 
data on the fly while replicating. If you have any questions, use the comments below, 
or drop a line to the Bucardo mailing list at bucardo-general@bucardo.org.

This major release would not have been possible without the help of many people 
over the years who have contributed code, raised bugs, tested Bucardo out, 
and asked (and/or answered!) important questions. Please see the [Changes](https://github.com/bucardo/bucardo/blob/master/Changes) file 
for a partial list. Thanks to all of you, and special thanks to Jon Jensen, who started 
this whole project, many moons ago.
