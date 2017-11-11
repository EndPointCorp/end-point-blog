---
author: Szymon Lipiński
gh_issue_number: 717
tags: postgres
title: How to make a PostgreSQL query slow
---

Some applications can be very vulnerable to long running queries. When you test an application, sometimes it is good to have a query running for, let's say, 10 minutes. What's more it should be a normal query, so the application can get the normal results, however this query should run for some longer time than usual.

PostgreSQL has quite a nice function pg_sleep which takes exactly one parameter, it is the number of seconds this function will wait before returning. You can use it as a normal PostgreSQL function, however it's not very sensible:

```sql
# SELECT pg_sleep(10);

 pg_sleep
----------

(1 row)

Time: 10072.794 ms
```

The most interesting usage is adding this function into a query. Let's take this query:

```sql
# SELECT schemaname, tablename
  FROM pg_tables
  WHERE schemaname &lt;&gt; 'pg_catalog';

Time: 0.985 ms
```

As you can see, this query is quite fast and returns data in less than 1 ms. Let's now make this query much slower, however returning exactly the same data, but after 15 seconds:

```sql
# SELECT schemaname, tablename
  FROM pg_tables, pg_sleep(15)
  WHERE schemaname &lt;&gt; 'pg_catalog';

Time: 15002.084 ms
```

In fact the query execution time is a little bit longer, the pg_sleep function was waiting 15 seconds, but PostgreSQL had to spend some time on query parsing, execution and returning proper data.

I was using this solution many times to simulate a long running query, without changing the application logic, to check how the application behaves during some load peaks.
