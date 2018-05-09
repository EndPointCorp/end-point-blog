---
author: Greg Sabino Mullane
gh_issue_number: 1225
tags: postgres
title: Postgres concurrent indexes and the curse of IIT
---
[Postgres](http://postgres.org) has a wonderful feature called [concurrent indexes](http://www.postgresql.org/docs/current/static/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY). It allows you to create indexes on a table without blocking reads ***OR*** writes, which is quite a handy trick. There are a number of circumstances in which one might want to use concurrent indexes, the most common one being not blocking writes to production tables. There are a few other use cases as well, including:

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2016/04/28/postgres-concurrent-indexes-and-curse/image-0.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img src="/blog/2016/04/28/postgres-concurrent-indexes-and-curse/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/m8ckHX">Photograph</a> by <a href="https://www.flickr.com/photos/nicholas_t/">Nicholas A. Tonelli</a></small></div>

- Replacing a corrupted index
- Replacing a bloated index
- Replacing an existing index (e.g. better column list)
- Changing index parameters
- Restoring a production dump as quickly as possible

In this article, I will focus on that last use case, restoring a database as quickly as possible. We recently upgraded a client from a very old version of Postgres to the current version (9.5 as of this writing). The fact that use of [pg_upgrade](http://www.postgresql.org/docs/current/static/pgupgrade.html) was not available should give you a clue as to just how old the “very old” version was!

Our strategy was to create a new 9.5 cluster, get it [optimized for bulk loading](http://www.postgresql.org/docs/current/static/populate.html), import the globals and schema, stop write connections to the old database, transfer the data from old to new, and bring the new one up for reading and writing.

The goal was to reduce the application downtime as much as reasonably possible. To that end, we did not want to wait until all the indexes were created before letting people back in, as testing showed that the index creations were the longest part of the process. We used the “--section” flags of [pg_dump](http://www.postgresql.org/docs/current/static/app-pgdump.html) to create pre-data, data, and post-data sections. All of the index creation statements appeared in the post-data file.

Because the client determined that it was more important for the data to be available, and the tables writable, than it was for them to be fully indexed, we decided to try using CONCURRENT indexes. In this way, writes to the tables could happen at the same time that they were being indexed—​and those writes could occur as soon as the table was populated. That was the theory anyway.

The migration went smooth—​the data was transferred over quickly, the database was restarted with a new postgresql.conf (e.g. turn fsync back on), and clients were able to connect, albeit with some queries running slower than normal. We parsed the post-data file and created a new file in which all the CREATE INDEX commands were changed to CREATE INDEX CONCURRENTLY. We kicked that off, but after a certain amount of time, it seemed to freeze up.

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2016/04/28/postgres-concurrent-indexes-and-curse/image-1.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img id="gtsm.com/cursed_frogurt.png" src="/blog/2016/04/28/postgres-concurrent-indexes-and-curse/image-1.png"/></a><br/><small><em>The frogurt is also cursed.</em></small></div>

Looking closer showed that the CREATE INDEX CONCURRENTLY statement was waiting, and waiting, and never able to complete—​because other transactions were not finishing. This is why concurrent indexing is both a blessing and a curse. The concurrent index creation is so polite that it never blocks writers, but this means processes can charge ahead and be none the wiser that the create index statement is waiting on them to finish their transaction. When you also have a misbehaving application that stays “idle in transaction”, it’s a recipe for confusion. (Idle in transaction is what happens when your application keeps a database connection open without doing a COMMIT or ROLLBACK). A concurrent index can only completely finish being created once any transaction that has referenced the table has completed. The problem was that because the create index did not block, the app kept chugging along, spawning new processes that all ended up in idle in transaction.

At that point, the only way to get the concurrent index creation to complete was to forcibly kill all the other idle in transaction processes, forcing them to rollback and causing a lot of distress for the application. In contrast, a regular index creation would have caused other processes to block on their first attempt to access the table, and then carried on once the creation was complete, and nothing would have to rollback.

Another business decision was made—​the concurrent indexes were nice, but we needed the indexes, even if some had to be created as regular indexes. Many of the indexes were able to be completed (concurrently) very quickly—​and they were on not-very-busy tables—​so we plowed through the index creation script, and simply canceled any concurrent index creations that were being blocked for too long. This only left a handful of uncreated indexes, so we simply dropped the “invalid” indexes (these appear when a concurrent index creation is interrupted), and reran with regular CREATE INDEX statements.

The lesson here is that nothing comes without a cost. The overly polite concurrent index creation is great at letting everyone else access the table, but it also means that large complex transactions can chug along without being blocked, and have to have all of their work rolled back. In this case, things worked out as we did 99% of the indexes as CONCURRENT, and the remaining ones as regular. All in all, the use of concurrent indexes was a big win, and they are still an amazing feature of Postgres.
