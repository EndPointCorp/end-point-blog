---
author: Josh Tolley
gh_issue_number: 903
tags: database, java, performance, postgres
title: Database federation performance showdown
---



<div class="separator" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><a href="http://www.flickr.com/photos/garryknight/" imageanchor="1"><img border="0" src="/blog/2013/12/19/database-federation-performance-showdown/image-0.jpeg"/></a><p align="center"><small>Flickr user <a href="http://www.flickr.com/photos/garryknight/">garryknight</a></small></p></div>

The [PostgreSQL Foreign Data Wrapper](http://www.postgresql.org/docs/9.3/static/postgres-fdw.html) has gotten a fair bit of attention since its release in PostgreSQL version 9.3. Although it does much the same thing the [dblink](http://www.postgresql.org/docs/9.3/static/dblink.html) contrib module has long done, it is simpler to implement for most tasks and reuses the same foreign data wrapper infrastructure employed by several other contrib modules. It allows users to "federate" distinct PostgreSQL databases; that is, it allows them to work in combination as though they were one database. This topic of database federation has interested me for some time -- I [wrote about it](/blog/2010/07/29/distributed-transactions-and-two-phase) a couple years ago -- and when postgres_fdw came out I wanted to see how it compared to the solution I used back then.

First, some background. The key sticking point of database federation that I'm focused on is transaction management. Transactions group a series of steps, so either they all complete in proper sequence, or none of them does. While lots of databases, and other technologies like messaging servers, can handle transactions that involve only one service (one database or one messaging server instance, for example), federation aims to allow transactions to span multiple services. If, for instance, given a transaction involving multiple databases, one database fails to commit, all the other databases in the transaction roll back automatically. See my post linked above for a more detailed example and implementation details. In that post I talked about the Bitronix transaction manager, whose job is to coordinate the different databases and other services in a transaction, and make sure they all commit or roll back correctly, even in the face of system failures and other misbehavior. There are [other](http://www.atomikos.com/Main/TransactionsEssentials) [standalone](http://jotm.objectweb.org/) [transaction](http://simplejta.sourceforge.net/) [managers](http://www.jboss.org/narayana) available. I used Bitronix simply because a knowledgeable friend recommended it, and it proved sufficient for the testing I had in mind.

So much for introduction. I wanted to see how Bitronix compared to postgres_fdw, and to get started I took the simple sequence of queries used by default by pgbench, and created a test database with pgbench, and then made three identical copies of it (named, of course, athos, porthos, aramis, and dartagnan -- I wasn't energetic enough to include the apostrophe in the name of the fourth database). The plan was to federate athos and porthos with Bitronix, and aramis and dartagnan with postgres_fdw. More precisely, the pgbench test schema consists of a small set of tables representing a simple banking scenario. In its default benchmark, pgbench selects from, inserts into, and updates these tables with a few simple queries, shown below. Like pgbench, my test script replaces identifiers starting with a ":" character with values selected randomly for each iteration.

```sql
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
```

I decided to configure my test as though pgbench's "accounts" table was in one database, and the "tellers", "branches", and "history" tables were in another. For the Bitronix test I can simply connect to both databases and ignore the tables that aren't applicable, but for testing postgres_fdw I need to set up dartagnan's pgbench_accounts table as a foreign table in the aramis database, like this:

```sql
aramis=# drop table pgbench_accounts;
DROP TABLE
aramis=# create server dartagnan foreign data wrapper postgres_fdw options (dbname 'dartagnan');
CREATE SERVER
aramis=# create user mapping for josh server dartagnan options (user 'josh');
CREATE USER MAPPING
aramis=# create foreign table pgbench_accounts (aid integer not null, bid integer, abalance integer, filler character(84)) server dartagnan;
CREATE FOREIGN TABLE
```

The [test script](http://josh.endpoint.com/bitronix2.rb) I wrote has two modes: Bitronix mode, and postgres_fdw mode. For each, it repeats the pgbench test queries a fixed number of times, grouping a certain number of these iterations into a single transaction. It then changes the number of iterations per transaction, and repeats the test. In the end, it gave me the following results, which I found very interesting:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/12/19/database-federation-performance-showdown/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/12/19/database-federation-performance-showdown/image-0.png"/></a></div>

The results show that for small transactions, postgres_fdw performs much better. But when the transactions get large, Bitronix catches up and takes the lead. The graph shows a curve that may be part of an interesting trend, but it didn't seem worthwhile to test larger numbers of iterations per single transaction, because the larger transactions in the test are already very large compared to typical real-life workloads. It's difficult to see exactly what's going on in the center of the graph; here's a log rescaling of the data to make it clear   what the numbers are up to.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/12/19/database-federation-performance-showdown/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/12/19/database-federation-performance-showdown/image-1.png"/></a></div>

All in all, it doesn't surprise me that postgres_fdw would be faster than Bitronix for small and medium-sized transactions. Being more tightly coupled to PostgreSQL, it has a faster path to get done what it wants to do, and in particular, isn't restricted to using two-phase commit, which is generally considered slow. I was surprised, however, to see that Bitronix managed to catch up for very large transactions.


