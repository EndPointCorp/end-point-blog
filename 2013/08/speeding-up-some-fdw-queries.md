---
author: Szymon Lipiński
title: Speeding Up Some FDW Queries
github_issue_number: 844
tags:
- postgres
date: 2013-08-08
---

There was a very interesting question about PostgreSQL optimization. It was about speeding up a query on foreign tables.

### Foreign Data Wrappers

FDW is quite a nice idea, it allows to use different sources of data and access them like a normal database table.

You can find some more [information about writing custom FDW handlers](https://www.postgresql.org/docs/9.2/static/fdwhandler.html) or [use some already created](https://wiki.postgresql.org/wiki/Foreign_data_wrappers). This way you can connect to another database, or even use CSV files as Postgres tables without loading them into database.

### Introduction

Let’s take a couple of tables and a view created on the top of them:

```
CREATE TABLE t_10_20(i INTEGER);
CREATE TABLE t_15_20(i INTEGER);
CREATE TABLE t_10_16(i INTEGER);

CREATE VIEW all_tables AS
  SELECT i FROM t_10_20
  UNION ALL
  SELECT i FROM t_15_20
  UNION ALL
  SELECT i FROM t_10_16;
```

I assume, as it was in the original question, that there are some strict ranges of data in the tables. For the example I encoded the ranges in table names, so table t_10_20 contains values from the range [10,20] and table t_10_16 has values from [10,16];

The above view will be used for getting all data.

For filling them up, I used a function which I wrote long time ago, it returns a random number with uniform distribution from the given range:

```
CREATE FUNCTION
random_range(INTEGER, INTEGER) RETURNS INTEGER
AS $$
    SELECT floor(($1 + ($2 - $1 + 1) * random()))::INTEGER;
$$ LANGUAGE SQL;

INSERT INTO t_10_20(i) SELECT random_range(10, 20) FROM generate_series(1,1000*1000);
INSERT INTO t_15_20(i) SELECT random_range(15, 20) FROM generate_series(1,1000*1000);
INSERT INTO t_10_16(i) SELECT random_range(10, 16) FROM generate_series(1,1000*1000);
```

I also need to update the stats:

```
ANALYZE t_10_20;
ANALYZE t_15_20;
ANALYZE t_10_16;
```

### Getting Data

The query for getting all data is simple, and the plan is terrible of course, but it is a normal plan for a query like SELECT * FROM x.

```
# EXPLAIN SELECT * FROM all_tables;
                              QUERY PLAN
-----------------------------------------------------------------------
 Append  (cost=0.00..43275.00 rows=3000000 width=4)
   ->  Seq Scan on t_10_20  (cost=0.00..14425.00 rows=1000000 width=4)
   ->  Seq Scan on t_15_20  (cost=0.00..14425.00 rows=1000000 width=4)
   ->  Seq Scan on t_10_16  (cost=0.00..14425.00 rows=1000000 width=4)
(4 rows)
```

And what about querying only numbers between 10 and 14? This could be optimized to use only the tables t_10_20 and t_10_16. The table t_15_20 could be omitted, as it doesn’t contain data we need.

```
# EXPLAIN SELECT * FROM all_tables WHERE i BETWEEN 10 AND 14;
                              QUERY PLAN
----------------------------------------------------------------------
 Append  (cost=0.00..58275.00 rows=1165534 width=4)
   ->  Seq Scan on t_10_20  (cost=0.00..19425.00 rows=453133 width=4)
         Filter: ((i >= 10) AND (i <= 14))
   ->  Seq Scan on t_15_20  (cost=0.00..19425.00 rows=1 width=4)
         Filter: ((i >= 10) AND (i <= 14))
   ->  Seq Scan on t_10_16  (cost=0.00..19425.00 rows=712400 width=4)
         Filter: ((i >= 10) AND (i <= 14))
(7 rows)
```

As you can see, there is no change. The query planner needs some help.

This can be fixed with a very simple solution. We can add constraints, so the planner can use them for better planning:

```
ALTER TABLE t_10_20 ADD CHECK(i BETWEEN 10 AND 20);
ALTER TABLE t_15_20 ADD CHECK(i BETWEEN 15 AND 20);
ALTER TABLE t_10_16 ADD CHECK(i BETWEEN 10 AND 16);
```

And the plan for the previous query is:

```
# EXPLAIN SELECT * FROM all_tables WHERE i BETWEEN 10 AND 14;
                              QUERY PLAN
----------------------------------------------------------------------
 Append  (cost=0.00..38850.00 rows=1165533 width=4)
   ->  Seq Scan on t_10_20  (cost=0.00..19425.00 rows=453133 width=4)
         Filter: ((i >= 10) AND (i <= 14))
   ->  Seq Scan on t_10_16  (cost=0.00..19425.00 rows=712400 width=4)
         Filter: ((i >= 10) AND (i <= 14))
(5 rows)
```

Great, so we have one less sequential scan.

The original question was about foreign tables. The foreign tables created using foreign data wrapper (fdw) cannot have check constraints.

I removed the previously added checks, so I can use them to simulate the foreign tables:

```
ALTER TABLE t_10_20 DROP CONSTRAINT t_10_20_i_check;
ALTER TABLE t_15_20 DROP CONSTRAINT t_15_20_i_check;
ALTER TABLE t_10_16 DROP CONSTRAINT t_10_16_i_check;
```

Another idea was to change the view definition to:

```
CREATE VIEW all_tables_2 AS
  SELECT i FROM t_10_20 WHERE i BETWEEN 10 AND 20
  UNION ALL
  SELECT i FROM t_15_20 WHERE i BETWEEN 15 AND 20
  UNION ALL
  SELECT i FROM t_10_16 WHERE i BETWEEN 10 AND 16;
```

Unfortunately that didn’t help, and the plan is as ugly as it was in the beginning.

```
# EXPLAIN SELECT * FROM all_tables_2 WHERE i BETWEEN 10 AND 14;
                              QUERY PLAN
-----------------------------------------------------------------------
 Append  (cost=0.00..84930.34 rows=1165534 width=4)
   ->  Seq Scan on t_10_20  (cost=0.00..24425.00 rows=453133 width=4)
         Filter: ((i >= 10) AND (i <= 20) AND (i >= 10) AND (i <= 14))
   ->  Seq Scan on t_15_20  (cost=0.00..24425.00 rows=1 width=4)
         Filter: ((i >= 15) AND (i <= 20) AND (i >= 10) AND (i <= 14))
   ->  Seq Scan on t_10_16  (cost=0.00..24425.00 rows=712400 width=4)
         Filter: ((i >= 10) AND (i <= 16) AND (i >= 10) AND (i <= 14))
(7 rows)
```

As you can see, there is the worse plan used. Planner doesn’t want to use the view definition to optimize the query plan.

### Changing Postgres Settings

There is a setting named constraint_exclusion in postgresql.conf. Changing that from “partition” to “on” helps a lot:

```
# EXPLAIN SELECT * FROM all_tables_2 WHERE i BETWEEN 10 AND 14;
                              QUERY PLAN
-----------------------------------------------------------------------
 Append  (cost=0.00..60505.33 rows=1165533 width=4)
   ->  Seq Scan on t_10_20  (cost=0.00..24425.00 rows=453133 width=4)
         Filter: ((i >= 10) AND (i <= 20) AND (i >= 10) AND (i <= 14))
   ->  Seq Scan on t_10_16  (cost=0.00..24425.00 rows=712400 width=4)
         Filter: ((i >= 10) AND (i <= 16) AND (i >= 10) AND (i <= 14))
(5 rows)
```

### Fixing the Ugly Part

This works great, however nothing is for free. The description of the different values for this setting says:

>
>
>
> Currently, constraint exclusion is enabled by default only for cases that are often used to implement table partitioning. Turning it on for all tables imposes extra planning overhead that is quite noticeable on simple queries, and most often will yield no benefit for simple queries. If you have no partitioned tables you might prefer to turn it off entirely.
>
>
>
>
> [PostgreSQL doc](https://www.postgresql.org/docs/9.1/static/runtime-config-query.html#GUC-CONSTRAINT-EXCLUSION)
>
>
>

So generally setting that for the whole database is not too wise, you can always set it for your specific query only, so it will help with this one query and won’t cause any problems with others. This can be done like this:

```
BEGIN;
SET LOCAL constraint_exclusion TO 'on';
SELECT * FROM all_tables_2 WHERE i BETWEEN 10 AND 14;
END;
```

This should work.
