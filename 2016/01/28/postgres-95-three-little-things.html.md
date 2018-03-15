---
author: Greg Sabino Mullane
gh_issue_number: 1199
tags: database, postgres
title: 'Postgres 9.5: three little things'
---

 

<div class="separator" style="clear: both; float:right; padding: .5em .5em 2em 1em; text-align: center;"><a href="/blog/2016/01/28/postgres-95-three-little-things/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/01/28/postgres-95-three-little-things/image-0.jpeg"/></a><br/>
<small><a href="https://flic.kr/p/nobB5c">Photo</a> by <a href="https://www.flickr.com/photos/tambako/">Tambako the Jaguar</a></small></div>

The recent release of Postgres 9.5 has many people excited about the big new features such as [UPSERT](https://web.archive.org/web/20160205092532/http://michael.otacoo.com/postgresql-2/postgres-9-5-feature-highlight-upsert/) ([docs](https://www.postgresql.org/docs/9.5/static/sql-insert.html)) and [row-level security](http://jimkeener.com/posts/postgres-9.5-row-level-security-rls) ([docs](https://www.postgresql.org/docs/9.5/static/ddl-rowsecurity.html)). Today I would like to celebrate three of the smaller features that I love about this release.

Before jumping into my list, I’d like to thank everyone who contributes to Postgres. I did some quick analysis and found that 85 people, from Adrien to Zeus, have helped version 9.5 of Postgres, at least according to the git logs. Of course, that number is actually higher, as it doesn’t take into account people helping out on the #postgresql channel, running buildfarm animals, doing packaging work, keeping the infrastructure running, etc. Thanks to you all!

### Feature: REINDEX VERBOSE

The first feature is one I’ve been wishing for a long time — a verbose form of the REINDEX command. Thanks to Sawada Masahiko for adding this. Similar to VACUUM, REINDEX gets kicked off and then gives no progress or information until it finishes. While VACUUM has long had the VERBOSE option to get around this, REINDEX gives you no clue to which index it was working on, or how much work each index took to rebuild. Here is a normal reindex, along with another 9.5 feature, the ability to reindex an entire schema:

```
greg=# reindex schema public;
## What seems like five long minutes later...
REINDEX
```
  

The new syntax uses parenthesis to support VERBOSE and any other future options. If you are familiar with EXPLAIN’s newer options, you may see a similarity. More on the syntax in a bit. Here is the much improved version in action:

```
greg=# reindex (verbose) schema public;
INFO:  index "foobar_pkey" was reindexed
DETAIL:  CPU 11.00s/0.05u sec elapsed 19.38 sec.
INFO:  index "foobar_location" was reindexed
DETAIL:  CPU 5.21s/0.05u sec elapsed 18.27 sec.
INFO:  index "location_position" was reindexed
DETAIL:  CPU 9.10s/0.05u sec elapsed 19.70 sec.
INFO:  table "public.foobar" was reindexed
INFO:  index "foobaz_pkey" was reindexed
DETAIL:  CPU 7.04s/0.05u sec elapsed 19.61 sec.
INFO:  index "shoe_size" was reindexed
DETAIL:  CPU 12.26s/0.05u sec elapsed 19.33 sec.
INFO:  table "public.foobaz" was reindexed
REINDEX
```
 

Why not **REINDEX VERBOSE TABLE foobar**? Or even **REINDEX TABLE foobar WITH VERBOSE**? There was a good discussion of this on pgsql-hackers when this feature was being developed, but the short answer is that parenthesis are the correct way to do things moving forward. Robert Haas summed it up well:

> *The unparenthesized VACUUM syntax was added back before we realized that that kind of syntax is a terrible idea. It requires every option to be a keyword, and those keywords have to be in a fixed order. I believe the intention is to keep the old VACUUM syntax around for backward-compatibility, but not to extend it. Same for EXPLAIN and COPY.*

The psql help option should show the new syntax:

```
greg=# \h REINDEX
Command:     REINDEX
Description: rebuild indexes
Syntax:
REINDEX [ ( { VERBOSE } [, ...] ) ] { INDEX | TABLE | SCHEMA | DATABASE | SYSTEM } name
```

### Feature: pg_ctl defaults to “fast” mode

<a href="/blog/2016/01/28/postgres-95-three-little-things/image-1.gif" imageanchor="1"><img border="1" src="/blog/2016/01/28/postgres-95-three-little-things/image-1.gif"/></a>

The second feature in Postgres 9.5 I am happy about is the change in niceness of pg_ctl from “smart” mode to “fast” mode. The help of pg_ctl explains the different modes fairly well:

```
pg_ctl is a utility to initialize, start, stop, or control a PostgreSQL server.

Usage:
  pg_ctl stop    [-W] [-t SECS] [-D DATADIR] [-s] [-m SHUTDOWN-MODE]
...
Shutdown modes are:
  smart       quit after all clients have disconnected
  fast        quit directly, with proper shutdown
  immediate   quit without complete shutdown; will lead to recovery on restart
```
 

In the past, the default was “smart”. Which often means your friendly neighborhood DBA would type **“pg_ctl restart -D data”**, then watch the progress dots slowly marching across the screen, until they remembered that the default mode of “smart” is kind of dumb — as long as there is one connected client, the restart will not happen. Thus, the DBA had to cancel the command, and rerun it as **“pg_ctl restart -D data -m fast”**. Then they would vow to remember to add the -m switch in next time. And promptly forget to the next time they did a shutdown or restart. :) Now pg_ctl has a much better default. Thanks, Bruce Momjian! 

### Feature: new “cluster_name” option

When you run a lot of different Postgres clusters on your server, as I tend to do, it can be hard to tell them apart as the version and port are not reported in the ps output. I sometimes have nearly a dozen different clusters running, due to testing different versions and different applications. Similar in spirit to the [application_name]() option, the new cluster_name option solves the problem neatly by allowing a custom string to be put in to the process title. Thanks to Thomas Munro for inventing this. So instead of this:

```
greg      7780     1  0 Mar01 pts/0    00:00:03 /home/greg/pg/9.5/bin/postgres -D data
greg      7787  7780  0 Mar01 ?        00:00:00 postgres: logger process   
greg      7789  7780  0 Mar01 ?        00:00:00 postgres: checkpointer process   
greg      7790  7780  0 Mar01 ?        00:00:09 postgres: writer process   
greg      7791  7780  0 Mar01 ?        00:00:06 postgres: wal writer process   
greg      7792  7780  0 Mar01 ?        00:00:05 postgres: autovacuum launcher process   
greg      7793  7780  0 Mar01 ?        00:00:11 postgres: stats collector process  
greg      6773     1  0 Mar01 pts/0    00:00:02 /home/greg/pg/9.5/bin/postgres -D data2
greg      6780  6773  0 Mar01 ?        00:00:00 postgres: logger process   
greg      6782  6773  0 Mar01 ?        00:00:00 postgres: checkpointer process   
greg      6783  6773  0 Mar01 ?        00:00:04 postgres: writer process   
greg      6784  6773  0 Mar01 ?        00:00:02 postgres: wal writer process   
greg      6785  6773  0 Mar01 ?        00:00:02 postgres: autovacuum launcher process   
greg      6786  6773  0 Mar01 ?        00:00:07 postgres: stats collector process
```
  

One can adjust the cluster_name inside each postgresql.conf (for example, to “alpha” and “bravo”), and get this:

```
greg      8267     1  0 Mar01 pts/0    00:00:03 /home/greg/pg/9.5/bin/postgres -D data
greg      8274  8267  0 Mar01 ?        00:00:00 postgres: alpha: logger process   
greg      8277  8267  0 Mar01 ?        00:00:00 postgres: alpha: checkpointer process   
greg      8278  8267  0 Mar01 ?        00:00:09 postgres: alpha: writer process   
greg      8279  8267  0 Mar01 ?        00:00:06 postgres: alpha: wal writer process   
greg      8280  8267  0 Mar01 ?        00:00:05 postgres: alpha: autovacuum launcher process   
greg      8281  8267  0 Mar01 ?        00:00:11 postgres: alpha: stats collector process  
greg      8583     1  0 Mar01 pts/0    00:00:02 /home/greg/pg/9.5/bin/postgres -D data2
greg      8590  8583  0 Mar01 ?        00:00:00 postgres: bravo: logger process   
greg      8592  8583  0 Mar01 ?        00:00:00 postgres: bravo: checkpointer process   
greg      8591  8583  0 Mar01 ?        00:00:04 postgres: bravo: writer process   
greg      8593  8583  0 Mar01 ?        00:00:02 postgres: bravo: wal writer process   
greg      8594  8583  0 Mar01 ?        00:00:02 postgres: bravo: autovacuum launcher process   
greg      8595  8583  0 Mar01 ?        00:00:07 postgres: bravo: stats collector process
```
  

There are a lot of other things added in Postgres 9.5. I recommend you visit 
[this page](https://bucardo.org/postgres_all_versions.html#version_9.5) for a complete list, and poke around on your own. A final shout out to all the people that are continually improving the tab-completion of psql. You rock.


