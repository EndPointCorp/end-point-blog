---
author: "David Christensen"
title: "Large Data in PostgreSQL: Improving max() performance: GROUP BY vs CTE"
tags: postgresql
gh_issue_number: 
---

![Spice Baazar](/blog/2020/06/29/postgresql-improve-group-by-max-performance/banner.jpg)
[Photo](https://www.flickr.com/photos/maxpax/3638954095/) by [Chris Young](https://www.flickr.com/photos/maxpax/), used under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/), cropped from original.

This blog article is one of a number of posts that I will write based on working with large tables in PostgreSQL.  When working with large datasets, it is important to understand your tools and use more efficient queries in order to accomplish more naive approaches with smaller datasets.  This article covers the case where you want to get the maximum value of some number of groupings in a single table.

(**Note:** We are using PostgreSQL 12, which supports some nice features like parallel btree index building, which can speed up parts of this process compared to earlier versions.  We are using the default settings for this, which lets PostgreSQL use up to 2 parallel backend workers to speed up some operations.)

Say you have a table `table_a` with multiple grouping fields `field_a` and `field_b` and you want to find the maximum value of another table `field_c` for each group.

The direct approach is to do something like the following:

```sql
SELECT field_a, field_b, max(field_c) from table_a GROUP BY 1,2;
```

This is functional and very straightforward, however even if you have an index on `(field_a, field_b, field_c)` this can end up taking quite a bit more time if the tables are large.  Let’s look at an actual example and the numbers we use.

So first, let’s create our table:

```sql
CREATE TABLE table_a (field_a varchar, field_b integer, field_c date);
```

Populate with some data:

```sql
INSERT INTO table_a SELECT field_a,field_b,now ()::date + (random()*100)::int as field_c from unnest(array['AAA','BBB','CCC','DDD','EEE','FFF']) field_a,generate_series(1,10000) field_b,generate_series(1,1000);
```

This statement will populate this table with 60 million rows, consisting of 1000 random dates per each `field_a,field_b` pair; our task will now be to see how to efficiently find the max value for field_c for each grouping.

Let’s now create an index on all 3 fields:

```sql
CREATE INDEX ON table_a (field_a, field_b, field_c);
```

For the purposes of sanity/clarify when testing approaches, let’s VACUUM and ANALYZE that table:

```sql
VACUUM ANALYZE table_a;
```

And let’s check out the plan:

```
postgres=# EXPLAIN SELECT field_a, field_b, max(field_c) FROM table_a GROUP BY 1,2;
                                             QUERY PLAN
-----------------------------------------------------------------------------------------------------
 Finalize GroupAggregate  (cost=767659.40..781742.03 rows=54510 width=12)
   Group Key: field_a, field_b
   ->  Gather Merge  (cost=767659.40..780379.28 rows=109020 width=12)
         Workers Planned: 2
         ->  Sort  (cost=766659.37..766795.65 rows=54510 width=12)
               Sort Key: field_a, field_b
               ->  Partial HashAggregate  (cost=761825.91..762371.01 rows=54510 width=12)
                     Group Key: field_a, field_b
                     ->  Parallel Seq Scan on table_a  (cost=0.00..574325.52 rows=25000052 width=12)
(9 rows)
```

We can see that the plan is using an index-only scan for our table, which is good, but it also is using a separate GroupAggregate group/gather in order to get the grouping done, which still has to iterate through all the rows in the ip

Best of 3 timings: 5.60s

Hypothetically, PostgreSQL *could* detect that we’re asking for a `max()` value from an index with the individual keys as group values and just derive the `max()` value directly from the index, but it does not currently have this sort of capability, so instead we will rewrite our query to include more of the smarts.

Since we have a btree index on all of the fields, we know that the max value is easy to find, so let’s consider the conditions in which we can find this:

For one of the grouping `(field_a,field_b)`, we can find the maximum value for that group by using an `ORDER BY` clause and `LIMIT 1`, so if we knew the `(field_a,field_b)` pair the max could be found easily in the index by:

```sql
postgres=# SELECT field_c FROM table_a WHERE field_a = 'AAA' and field_b = 1 ORDER BY field_c DESC LIMIT 1;
  field_c
------------
 2020-10-01
(1 row)
```

Plan:

```sql
postgres=# explain SELECT field_c FROM table_a WHERE field_a = 'AAA' and field_b = 1 ORDER BY field_c DESC LIMIT 1;
                                                        QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.43..4.43 rows=1 width=4)
   ->  Index Only Scan Backward using table_a_field_a_field_b_field_c_idx on table_a  (cost=0.43..404.15 rows=101 width=4)
         Index Cond: ((field_a = 'AAA'::text) AND (field_b = 1))
(3 rows)
```

Since we want to find *all* the values in this table, we effectively want to do this query for each `(field_a, field_b)` pairing; but how can we iterate over this in an efficient way?

The keyword “iterate” should bring to mind a `WITH RECURSIVE` CTE, and here is where the trick comes in.  Since we want *all* the values, we can use *any* of them to start with and end up checking against the last known value to find the next.

An important thing to know is that for a btree index over `(a,b,c)`, there is a well-defined index ordering of all leading subsets of columns, so we can compare `(a,b)` against `(a0,b0)` in an indexed way and use this to our advantage.  This means that `('AAA',1) < ('AAA',2) < ('BBB',1)` just by virtue of how the row indexing works.

Using this property, we can then construct the following query:

```sql
WITH RECURSIVE t AS
(
    (SELECT field_a,field_b,field_c from table_a ORDER BY field_a DESC, field_b DESC, field_c DESC LIMIT 1)
    UNION ALL
    SELECT s.field_a, s.field_b, s.field_c FROM t,
    LATERAL (
        SELECT field_a, field_b, field_c FROM table_a
        WHERE (table_a.field_a, table_a.field_b) < (t.field_a,t.field_b)
        ORDER BY field_a DESC, field_b DESC, field_c DESC LIMIT 1
    ) s
) SELECT * FROM t;
```

Wow, pretty different, eh?  Breaking it down into what it does, we basically start with the most extreme value in the index, then recursively add the next row for fields `(field_a,field_b)` which is the next lowest value in the index.

 Let’s see the plan:

```sql
                                                                            QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------------------------
 CTE Scan on t  (cost=66.41..68.43 rows=101 width=40)
   CTE t
     ->  Recursive Union  (cost=0.56..66.41 rows=101 width=12)
           ->  Limit  (cost=0.56..0.60 rows=1 width=12)
                 ->  Index Only Scan Backward using table_a_field_a_field_b_field_c_idx on table_a  (cost=0.56..1825278.43 rows=60000124 width=12)
           ->  Nested Loop  (cost=0.56..6.38 rows=10 width=12)
                 ->  WorkTable Scan on t t_1  (cost=0.00..0.20 rows=10 width=36)
                 ->  Limit  (cost=0.56..0.60 rows=1 width=12)
                       ->  Index Only Scan Backward using table_a_field_a_field_b_field_c_idx on table_a table_a_1  (cost=0.56..658429.28 rows=20000041 width=12)
                             Index Cond: (ROW(field_a, field_b) < ROW((t_1.field_a)::text, t_1.field_b))
(10 rows)
```

Again, taking the best of 3 timings, we get 0.86s.

As you can see, the CTE approach is 6 - 7 times faster over the same data for the same results.

This same approach can work for finding the `min()` value, by just changing the `ORDER` clauses and comparison operator:

Compare:

```sql
WITH RECURSIVE t AS
(
    (SELECT field_a,field_b,field_c from table_a ORDER BY field_a, field_b, field_c LIMIT 1)
    UNION ALL
    SELECT s.field_a, s.field_b, s.field_c FROM t,
    LATERAL (
        SELECT field_a, field_b, field_c FROM table_a
        WHERE (table_a.field_a, table_a.field_b) > (t.field_a,t.field_b)
        ORDER BY field_a, field_b, field_c LIMIT 1
    ) s
) SELECT * FROM t;
```

Timing: 0.81s

vs `GROUP BY`:

```sql
SELECT field_a, field_b, min(field_c) FROM table_a GROUP BY 1,2;
```

Timing: 5.45s

This technique is generalizable to any number of fields in the table, it just relies on using the same index as you would want for `GROUP BY`.  This is another nice tool to have in the DBA toolbox.

