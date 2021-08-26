---
author: Szymon Lipiński
title: PostgreSQL auto_explain Module
github_issue_number: 714
tags:
- postgres
date: 2012-10-30
---

PostgreSQL has many nice additional modules, usually hidden and not enabled by default. One of them is auto_explain, which can be very helpful for bad query plan reviews. Autoexplain allows for automatic logging of query plans, according to the module's configuration.

This module is very useful for testing. Due to some ORM features, it is hard to repeat exactly the same queries with exactly the same parameters as ORMs do. Even without ORM, many applications make a lot of different queries depending on input data and it can be painful the repeat all the queries from logs. It's much easier to run the app and let it perform all the queries normally. The only change would be adding a couple of queries right after the application connects to the database.

At the beginning let's see how my logs look when I run "SELECT 1" query:

```sql
2012-10-24 14:55:09.937 CEST 5087e52d.22da 1 [unknown]@[unknown] LOG:  connection received: host=127.0.0.1 port=33004
2012-10-24 14:55:09.947 CEST 5087e52d.22da 2 szymon@szymon LOG:  connection authorized: user=szymon database=szymon
2012-10-24 14:55:10.860 CEST 5087e52d.22da 3 szymon@szymon LOG:  statement: SELECT 1;
2012-10-24 14:55:10.860 CEST 5087e52d.22da 4 szymon@szymon LOG:  duration: 0.314 ms
```

Your logs can look a little bit different depending on your settings. The settings I use for logging on my development machine are:

```nohighlight
log_destination = 'stderr'
logging_collector = on
log_directory = '/var/log/postgresql/'
log_filename = 'postgresql-9.1-%Y-%m-%d_%H%M%S.log'
log_file_mode = 0666
log_rotation_age = 1d
log_rotation_size = 512MB
client_min_messages = notice
log_min_messages = notice
log_min_duration_statement = -1
log_connections = on
log_disconnections = on
log_duration = on
log_line_prefix = '%m %c %l %u@%d '
log_statement = 'all'
```

The main idea for the above logging configuration is to log all queries before execution, so when a query fails (e.g. because of Out Of Memory Error), it will be logged as well. The execution time won't be logged, but the query will.

Let's run the simple query SELECT 1/0; which should fail. Then the log entries look like:

```sql
2012-10-24 15:00:24.767 CEST 5087e52d.22da 5 szymon@szymon LOG:  statement: SELECT 1/0;
2012-10-24 15:00:24.823 CEST 5087e52d.22da 6 szymon@szymon ERROR:  division by zero
2012-10-24 15:00:24.823 CEST 5087e52d.22da 7 szymon@szymon STATEMENT:  SELECT 1/0;
```

Enabling it for whole PostgreSQL installation is not the best idea, I always enable it only for my session using the following query:

```sql
LOAD 'auto_explain';
```

Now we have to configure this plugin a little bit. The main thing is to set the minimum statement execution time to log, let's set this to 0, just to explain all queries:

```sql
SET auto_explain.log_min_duration = 0;
```

Now let's create a table for tests:

```sql
CREATE TABLE x(t text);
INSERT INTO x(t) SELECT generate_series(1,10000);
```

The first query will be quite simple, let's just take the first ten rows.

```sql
SELECT t FROM x ORDER BY t LIMIT 10;
```

```sql
2012-10-24 16:21:34.102 CEST 5087f8f8.3fe6 16 szymon@szymon LOG:  statement: SELECT * FROM x ORDER BY t LIMIT 10;
2012-10-24 16:21:34.109 CEST 5087f8f8.3fe6 17 szymon@szymon LOG:  duration: 6.586 ms  plan:
 Query Text: SELECT * FROM x ORDER BY t LIMIT 10;
 Limit  (cost=361.10..361.12 rows=10 width=4)
   ->  Sort  (cost=361.10..386.10 rows=10000 width=4)
         Sort Key: t
         ->  Seq Scan on x  (cost=0.00..145.00 rows=10000 width=4)
2012-10-24 16:21:34.109 CEST 5087f8f8.3fe6 18 szymon@szymon LOG:  duration: 7.285 ms
```

Other things we can do with auto_explain module is to use EXPLAIN ANALYZE. First set the setting:

```sql
SET auto_explain.log_analyze = true;
```

Now PostgreSQL adds into logs the following lines:

```sql
2012-10-24 16:23:22.514 CEST 5087f8f8.3fe6 21 szymon@szymon LOG:  statement: SELECT * FROM x ORDER BY t LIMIT 10;
2012-10-24 16:23:22.522 CEST 5087f8f8.3fe6 22 szymon@szymon LOG:  duration: 8.248 ms  plan:
 Query Text: SELECT * FROM x ORDER BY t LIMIT 10;
 Limit  (cost=361.10..361.12 rows=10 width=4) (actual time=8.214..8.218 rows=10 loops=1)
   ->  Sort  (cost=361.10..386.10 rows=10000 width=4) (actual time=8.211..8.213 rows=10 loops=1)
         Sort Key: t
         Sort Method: top-N heapsort  Memory: 25kB
         ->  Seq Scan on x  (cost=0.00..145.00 rows=10000 width=4) (actual time=0.032..2.663 rows=10000 loops=1)
2012-10-24 16:23:22.522 CEST 5087f8f8.3fe6 23 szymon@szymon LOG:  duration: 8.722 ms
```

There are other settings, but I didn't find them as useful as the above.

Auto_explain is a great module for testing, however it can be a little painful on production databases when you enable EXPLAIN ANALYZE, as all the queries will always be run with calculating the node plan times, regardless of the log_min_duration setting. So the query can be much slower than usually, even if its plan is not logged.
