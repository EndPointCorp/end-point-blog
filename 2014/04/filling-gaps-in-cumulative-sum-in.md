---
author: Szymon Lipiński
title: Filling Gaps in Cumulative Sum in Postgres
github_issue_number: 959
tags:
- postgres
date: 2014-04-08
---

I found an interesting problem. There was a table with some data, among which there was a date and an integer value. The problem was to get cumulative sum for all the dates, however including dates for which we don’t have entries. In case of such dates we should use the last calculated sum.

### Example Data

I will use an example table:

```sql
# CREATE TABLE test (d DATE, v INTEGER);
```

with sample data:

```sql
# INSERT INTO test(d,v)
  VALUES('2014-02-01', 10),
        ('2014-02-02', 30),
        ('2014-02-05', 10),
        ('2014-02-10', 3);
```

Then the data in the table looks like:

```sql
# SELECT * FROM test;
     d      |  v
------------+----
 2014-02-01 | 10
 2014-02-02 | 30
 2014-02-05 | 10
 2014-02-10 |  3
(4 rows)
```

What I want is to have a cumulative sum for each day. Cumulative sum is a sum for all the earlier numbers, so for the above data I want to get:

```sql
     d      |  v
------------+----
 2014-02-01 | 10
 2014-02-02 | 40
 2014-02-05 | 50
 2014-02-10 | 53
(4 rows)
```

The simple query for getting the data set like shown above is:

```sql
SELECT DISTINCT d, SUM(v) OVER (ORDER BY d) v
FROM test
ORDER BY d ASC;
```

### Filling The Gaps

The query calculates the cumulative sum for each row. Unfortunately this way there are gaps between dates, and the request was to fill those in using the values from previous days.

What I want to get is:

```sql
     d      |  v
------------+----
 2014-02-01 | 10
 2014-02-02 | 40
 2014-02-03 | 40
 2014-02-04 | 40
 2014-02-05 | 50
 2014-02-06 | 50
 2014-02-07 | 50
 2014-02-08 | 50
 2014-02-09 | 50
 2014-02-10 | 53
```

My first idea was to use the generate_series() function, which can generate a series of data. What I need is a series of all dates between min and max dates. This can be done using:

```sql
# SELECT generate_series(
    '2014-02-01'::timestamp,
    '2014-02-05'::timestamp,
    '1 day')::date;
 generate_series
-----------------
 2014-02-01
 2014-02-02
 2014-02-03
 2014-02-04
 2014-02-05
```

The generate_series() function arguments are (begin, end, interval). The function returns all timestamps from beginning to end with given interval. The return value is timestamp, so I had to cast it to date with ‘::date’, which is a nice PostgreSQL shortcut for the standard syntax, CAST(generate_series(...) AS DATE).

I also want to use the first query to use the cumulative sum I calculated before. It can be simply achieved using the great WITH command which creates something like a temporary table, which can be queried:

```sql
# WITH temp AS
(
  SELECT generate_series(1, 1000) d
)
SELECT d
FROM temp
WHERE d < 4
ORDER BY d DESC;

 d
---
 3
 2
 1
```

Combining all the above queries resulted in the below one:

```sql
WITH y AS
(
  SELECT DISTINCT d, SUM(v) OVER (ORDER BY d) v
  FROM test
)
SELECT g.d,
  (SELECT v
   FROM y
   WHERE y.d <= g.d
   ORDER BY d DESC
   LIMIT 1)
FROM
  (SELECT generate_series(min(d), max(d), '1 day')::date d
   FROM y) g
ORDER BY d ASC
```

After the earlier explanations understanding this one should be easy.

- I placed the original query calculating the cumulative sum in the WITH block.
- SELECT creates a row set with two columns

        - The first column is date returns from subselect, just before ORDER BY. There are returned all dates between min and max date from the original data.
        - The second column is a subquery getting calculated cumulative sum. It gets the sum for current date (from the first column), or the previous calculated.

- And of course we need ordering at the end. The database can reorder the data as it wants during executing the query, so we always need to declare the ordering at the end. Otherwise strange things can happen (like having the same ordering of rows for years, and suddenly a totally different one, just because someone added new row, deleted some other, or just restarted application).
