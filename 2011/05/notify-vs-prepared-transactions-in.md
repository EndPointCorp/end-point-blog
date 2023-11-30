---
author: Greg Sabino Mullane
title: NOTIFY vs Prepared Transactions in Postgres (the Bucardo solution)
github_issue_number: 447
tags:
- bucardo
- database
- postgres
date: 2011-05-03
---



<a href="/blog/2011/05/notify-vs-prepared-transactions-in/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5602612861890245794" src="/blog/2011/05/notify-vs-prepared-transactions-in/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 240px; height: 160px;"/></a>

We recently had a client use Bucardo to migrate their app from Postgres 8.2 to Postgres 9.0 with no downtime (which went great). They also were using Bucardo to replicate from the new 9.0 mater to a bunch of 9.0 slaves. This ran into problems the moment the application started, as we started seeing these messages in the logs:

```
ERROR:  cannot PREPARE a transaction that has 
executed LISTEN, UNLISTEN or NOTIFY
```

The problem is that the Postgres LISTEN/NOTIFY system cannot be used with prepared transactions. Bucardo uses a trigger on the source tables that issues a NOTIFY to let the main Bucardo daemon know that something has changed and needs to be replicated. However, their application was issuing a PREPARE TRANSACTION as an occasional part of its work. Thus, they would update the table, which would fire the trigger, which would send the NOTIFY. Then the application would issue the PREPARE TRANSACTION which produced the error given above. Bucardo is setup to deal with this situation; rather than using notify triggers, the Bucardo daemon can be set to look for any changes at a set interval. The steps to change Bucardo’s behavior for a given sync is simply:

```bash
$ bucardo_ctl update sync foobar ping=false checktime=15
$ bucardo_ctl validate foobar
$ bucardo_ctl reload foobar
```

The first command tells the sync not to use notify triggers (these are actually statement-level triggers that simply issue a **NOTIFY bucardo_kick_sync_foobar**. It also sets a checktime of 15 seconds, which means that the Bucardo daemon will check for changes every 15 seconds—​or as if the original notify trigger is firing every 15 seconds. The second command validates the sync but checking that all supporting tables, functions, triggers, etc. are installed and up to date. It also removes triggers that are no longer needed: in this case, the statement-level notify triggers for all tables in this sync. Finally, the third command simply tells the Bucardo daemon to stop the sync, load in the new changes, and restart it.

Another solution to the problem is to simply not use prepared transactions: very few applications actually need it, but I’ve noticed a few that use it anyway when they should not be. What exactly is a prepared transaction? It’s the Postgres way of implementing two-part commit. Basically, this means that a transaction’s state is stored away on disk, and can be committed or rolled back at a later time—​even by a different session. This is handy if you need to ensure that, for example, you can atomically commit multiple database connections. By atomically, I mean that either they all commit or none of them do. This is done by doing work on each database, issuing a PREPARE TRANSACTION, and then, once all have been prepared, issuing the COMMIT TRANSACTION against each one.

As an aside, prepared **transactions** are often confused with prepared **statements**. While the use of prepared statements is very common, use of prepared transactions is very rare. Prepared statements are simply a way of planning a query one time, then re-running it multiple times without having to run the query through the planner each time. Many interfaces, such as DBD::Pg, will do this for you automatically behind the scenes. Sometimes using prepared statements can [cause issues](/blog/2009/08/debugging-prepared-statements/), but it is usually a win.

As mentioned above, the use of 2PC (two-phase commit) is very rare, which is why the default for the **max_prepared_transactions** variable [was recently changed](https://www.postgresql.org/message-id/7105.1240422511@sss.pgh.pa.us) to **0**, which effectively disallows the use of prepared transactions until you explicitly turning them on in your postgresql.conf file. This helps prevent people from accidentally issuing a PREPARE TRANSACTION and then leaving them around. This mistake is easy to do, for once you issue the command, everything goes back to normal and it’s easy to forget about them. However, having them around is a bad thing, as they continue to hold locks, and can prevent vacuum from running.The check_postgres program even has a specific check for this situation:[check_prepared_txns](https://bucardo.org/check_postgres/check_postgres.pl.html#prepared_txns).

What does two-part commit look like? There are only three basic commands: PREPARE TRANSACTION, COMMIT PREPARED, and ROLLBACK PREPARED. Each takes a name, which is an arbitrary string 200 characters or less. Usage is to start a transaction, do some work, and then issue a PREPARE TRANSACTION instead of a COMMIT. At this point, all the work you have done is gone from your session and stored on disk. You cannot get back into this transaction: you can only commit it or roll it back. See the [docs on PREPARE TRANSACTION](https://www.postgresql.org/docs/current/static/sql-prepare-transaction.html) for the full details.

Here’s an example of two-part commit in action:

```sql
testdb=# BEGIN;
BEGIN
testdb=#* CREATE TABLE preptest(a int);
CREATE TABLE
testdb=#* INSERT INTO preptest VALUES (1),(2),(3);
INSERT 0 3
testdb=#* SELECT * FROM preptest;
 a 
---
 1
 2
 3
(3 rows)

testdb=#* PREPARE TRANSACTION 'foobar';
PREPARE TRANSACTION
testdb=# SELECT * FROM preptest;
ERROR:  relation "preptest" does not exist
LINE 1: SELECT * FROM preptest;
                      ^
testdb=# COMMIT PREPARED 'foobar';
COMMIT PREPARED
testdb=# SELECT * FROM preptest;
 a 
---
 1
 2
 3
(3 rows)
```

A contrived example, but you can see how easy it could be to issue 
a PREPARE TRANSACTION and not even realize that it actually sticks 
around forever!


