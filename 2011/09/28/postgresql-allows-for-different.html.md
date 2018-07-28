---
author: Greg Sabino Mullane
gh_issue_number: 501
tags: bucardo, database, postgres
title: PostgreSQL Serializable and Repeatable Read Switcheroo
---



<a href="/blog/2011/09/28/postgresql-allows-for-different/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5657240288526769410" src="/blog/2011/09/28/postgresql-allows-for-different/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 240px; height: 160px;"/></a>

PostgreSQL allows for different transaction isolation levels to be specified. Because [Bucardo](https://bucardo.org/Bucardo/) needs a consistent snapshot of each database involved in replication to perform its work, the first thing that the Bucardo daemon does when connecting to a remote [PostgreSQL](https://www.postgresql.org/) database is:

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE;
```

The ‘READ WRITE’ bit sets us in read/write mode, just in case the entire database has been set to read only (a quick and easy way to make your slave databases non-writeable!). It also sets the transaction isolation level to ‘SERIALIZABLE’. At least, it used to. Now Bucardo uses ‘REPEATABLE READ’ like this:

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ WRITE;
```

Why the change? In version 9.1 of PostgreSQL the concept of [SSI (Serializable Snapshot Isolation)](https://wiki.postgresql.org/wiki/SSI) was introduced. How it actually works is a little complicated (follow the link for more detail), but before 9.1 PostgreSQL was only *sort of* doing serialized transactions when you asked for serializable mode. What it was really doing was repeatable read and not trying to really serialize the transactions. In 9.1, PostgreSQL is doing *true* [serializable transactions](https://www.postgresql.org/docs/9.1/static/transaction-iso.html#XACT-SERIALIZABLE). It also adds a new distinct ‘internal’ transaction mode, [‘repeatable read’](https://www.postgresql.org/docs/9.1/static/transaction-iso.html#XACT-REPEATABLE-READ), which does exactly what the old ‘serializable’ used to do. Finally, if you issue a ‘repeatable read’ on a pre-9.1 database, it silently upgrades it to the old ‘serializable’ mode.

So in summary, if your application was using ‘SERIALIZABLE’ before, you can now replace that with ‘REPEATABLE READ’ and get the exact same behavior as before, regardless of the version. Of course, if you want *true* serializable transactions, use SERIALIZABLE. It will continue to mean the same as ‘REPEATABLE READ’ in pre-9.1 databases, and provide true serializability in 9.1 and beyond. (I haven’t determined yet if Bucardo is going to use this new level, as it comes with a little bit of overhead)

Since this can be a little confusing, here’s a handy chart showing how version 9.1 changed the meaning of SERIALIZABLE, and added a new ‘internal’ isolation level:

<table border="2" cellpadding="7"><tbody><tr style="background-color: #00aaee"><th colspan="4">Postgres version 9.0 and earlier</th><th colspan="4">Postgres version 9.1 and later</th></tr><tr style="background-color: #00bbbb"><th>Requested isolation level</th><th>→</th><th>Actual internal isolation level</th><th colspan="2">Version comparison</th><th>Actual internal isolation level</th><th>←</th><th>Requested isolation level</th></tr><tr style="background-color: #ffcccc"><th>READ UNCOMMITTED</th><td>↘</td><th rowspan="2">Read committed</th><th colspan="2" rowspan="2">Exact same</th><th rowspan="2">Read committed</th><td>↙</td><th>READ UNCOMMITTED</th></tr><tr style="background-color: #ffcccc"><th>READ COMMITTED</th><td>↗</td><td>↖</td><th>READ COMMITTED</th></tr><tr style="background-color: #ffee99"><th>REPEATABLE READ</th><td>↘</td><th rowspan="2">Serializable</th><th colspan="2" rowspan="2">Functionally identical</th><th rowspan="2">Repeatable read</th><td rowspan="2">←</td><th rowspan="2">REPEATABLE READ</th></tr><tr style="background-color: #ffee99"><th>SERIALIZABLE</th><td>↗</td></tr><tr style="background-color: #aaffaa"><th colspan="3"> </th><th colspan="2">9.1 only!</th><th>Serializable (true)</th><td>←</td><th>SERIALIZABLE</th></tr></tbody></table>

Congratulations and thanks to Kevin Grittner and Dan Ports for making true serializability a reality!


