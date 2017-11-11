---
author: Szymon Lipiński
gh_issue_number: 817
tags: postgres
title: PostgreSQL Functional Indexes
---

PostgreSQL has got the great feature named “functional indexes”. A normal index just stores sorted values of some field. It is great for searching, as the values are already sorted.

You can create an index with a simple query like:

```
CREATE INDEX i_test ON test (i);
```

It will store all values of column i from table test. This index can be used with a query like:

```
SELECT * FROM test WHERE i < 100 ORDER BY i;
```

## Functional Indexes

There is also something I like most. Index can store all values you want, they don’t need to be values from the table. You can use values calculated from the table columns. They will be sorted, so searching with those indexes will be pretty fast.

Creating such index is simple:

```
CREATE INDEX i_test_lower_i ON test (lower(i));
```

The main rule is: this index can be used if you have the same function call in your query, something like:

```
SELECT * FROM test WHERE lower(i) = 'aaa';
```

## Example

Let’s check something more complicated. My test table looks like:

```
CREATE TABLE test(t timestamp);
```

I filled this table with sample data. We need some bigger number of rows:

```
INSERT INTO test(t) SELECT generate_series(now() - '1 year'::interval, now(), '1 minute');
```

This way there are 500k rows.

I need to get two row sets from database. First I will get the rows with dates from the last 10 days. Later I will get all rows with dates from current year.

### The Last 10 Days

I can get the rows with dates from the last 10 days like:

```
postgres=# explain analyze select t from test where t::date > (now() - '10 days'::interval)::date;
                                                  QUERY PLAN
---------------------------------------------------------------------------------------------------------------
 Seq Scan on test  (cost=0.00..14152.02 rows=175200 width=8) (actual time=265.640..272.701 rows=13558 loops=1)
   Filter: ((t)::date > ((now() - '10 days'::interval))::date)
   Rows Removed by Filter: 512043
 Total runtime: 273.152 ms
(4 rows)
```

For speeding this up I will create an index storing sorted dates:

```
CREATE INDEX i_test_t ON test((t::date));
```

With this index the plan is much better and the query is much faster:

```
postgres=# explain analyze select t from test where t::date > (now() - '10 days'::interval)::date;
                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using i_test_t on test  (cost=0.43..459.23 rows=13817 width=8) (actual time=0.083..8.337 rows=13558 loops=1)
   Index Cond: ((t)::date > ((now() - '10 days'::interval))::date)
 Total runtime: 9.990 ms
(3 rows)
```

This index will also be used when you want to sort the results using the same values as stored in index:

```
postgres=# explain analyze select t from test where t::date > (now() - '10 days'::interval)::date order by t::date asc;
                                                        QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------
 Index Scan using i_test_t on test  (cost=0.43..493.78 rows=13817 width=8) (actual time=0.080..13.479 rows=13558 loops=1)
   Index Cond: ((t)::date > ((now() - '10 days'::interval))::date)
 Total runtime: 15.833 ms
(3 rows)
```

And even when you sort backwards:

```
postgres=# explain analyze select t from test where t::date > (now() - '10 days'::interval)::date order by t::date desc;
                                                            QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------
 Index Scan Backward using i_test_t on test  (cost=0.43..493.78 rows=13817 width=8) (actual time=0.053..13.847 rows=13558 loops=1)
   Index Cond: ((t)::date > ((now() - '10 days'::interval))::date)
 Total runtime: 16.230 ms
(3 rows)
```

### All Rows for This Year

You can get current year from a timestamp or date value with the extract function.

```
postgres=# SELECT extract( year from '2013-01-01'::date);
 date_part
-----------
      2013
(1 row)
```

```
postgres=# SELECT extract( year from now());
 date_part
-----------
      2013
(1 row)
```

This can be used for getting all the rows with this year dates:

```
select t from test where extract(year from t) = extract(year from now());
```

Check the plan:

```
postgres=# explain analyze select t from test where extract(year from t) = extract(year from now());
                                                  QUERY PLAN
--------------------------------------------------------------------------------------------------------------
 Seq Scan on test  (cost=0.00..12838.02 rows=2628 width=8) (actual time=136.349..235.307 rows=223670 loops=1)
   Filter: (date_part('year'::text, t) = date_part('year'::text, now()))
   Rows Removed by Filter: 301931
 Total runtime: 242.259 ms
(4 rows)
```

It doesnt look too good. Let’s use the functional index. This time I need to store the year number:

```
CREATE INDEX i_test_t_year ON test (extract(year from t));
```

The plan should improve, so the query should be faster now:

```
postgres=# explain analyze select t from test where extract(year from t) = extract(year from now());
                                                            QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------
 Index Scan using i_test_t_year on test  (cost=0.43..7426.77 rows=225448 width=8) (actual time=0.052..51.715 rows=223670 loops=1)
   Index Cond: (date_part('year'::text, t) = date_part('year'::text, now()))
 Total runtime: 60.969 ms
(3 rows)
```

## Summary

As you can see functional indexes can be used for storing calculated values which you can use for searching. In other database engines this can be achieved with additional columns storing those values (updated with triggers or application) or materialized views.

As usually there are also some cons of this solution. The index needs to be updated each time you change the data, this means that inserts, updates and deletes will be slower. It doesn’t mean that it will be easily noticeable. Another thing worth remembering is that those indexes are stored on disk, so each index means more disk operations. It also means longer time for restoring dumps. The index data is not stored in a database dump – there is stored only index definition, and it needs to be recreated when loading dump into database.

All this means that you should check if the index you want to create is really needed, not used indexes are just a waste of resources which could be used some better way.
