---
author: Joshua Tolley
gh_issue_number: 128
tags: postgres
title: OFFSET 0, FTW
---

A query I worked with the other day gave me a nice example of a useful PostgreSQL query planner trick. This query originally selected a few fields from a set of inner-joined tables, sorting by one particular field in descending order and limiting the results, like this:

```sql
SELECT <some stuff> FROM table_a INNER JOIN table_b ON (...)
INNER JOIN table_c ON (...) WHERE table_a.field1 = 'value'
ORDER BY table_a.field2 DESC LIMIT 20
```

The resulting query plan involved a bunch of index scans on the various tables, joined with nested loops, all based on a backward index scan of an index on the table_a.field2 column, looking for rows that matched the condition in the WHERE clause. PostgreSQL likes to choose backward index scans when there's a LIMIT clause and it needs result sorted in reverse order, because although backward index scans can be fairly slow, they're easy to interrupt when it finds enough rows to satisfy the LIMIT. In this case, it figured it could search backward through the index on table_a.field2 and quickly find 20 rows where table_a.field1 = 'value' is true. The problem was that it didn't find enough rows as quickly as it thought it would.

One way of dealing with this is to improve your statistics, which is what PostgreSQL uses to estimate how long the backward index scan will take in the first place. But sometimes that method still doesn't pan out, and it takes a lot of experimentation to be sure it works. That level of experimenting didn't seem appropriate in this case, so I used another trick. I guessed that maybe if I could get PostgreSQL to first pull out all the rows matching the WHERE clause, it could join them to the other tables involved and then do a separate sorting step, and come out faster than the plan that it was using currently. Step one is to separate out the part that filters table_a:

```sql
SELECT <some stuff> FROM
(SELECT * FROM table_a WHERE field1 = 'value') a
INNER JOIN table_b ON (...) INNER JOIN table_c ON (...)
ORDER BY a.field2 DESC LIMIT 20
```

The problem is that this doesn't change the query plan at all. PostgreSQL tries to "flatten" nested subqueries -- that is, it fiddles with join orders and query ordering to avoid subquery operations. In order to convince it not to flatten the new subquery, I added "OFFSET 0" to the subquery. This new query gives me the plan I want:

```sql
SELECT <some stuff> FROM
(SELECT * FROM table_a WHERE field1 = 'value' OFFSET 0) a
INNER JOIN table_b ON (...) INNER JOIN table_c ON (...)
ORDER BY a.field2 DESC LIMIT 20
```

This selects all rows from table_a where field1 = 'value', and uses them as a distinct relation for the rest of the query. This led to a distinct sorting step, and made the resulting query much faster than it had been previously.

**CAVEAT:** The query planner is pretty much always smarter than whoever is sending it queries. This trick just happened to work, but can be a really bad idea in some cases. It tells PostgreSQL to pull all matching rows out of the table and keep them all in memory (or worse, temporary disk files), and renders useless any indexes on the original table. If there were lots of rows matching the condition, this would be Very Bad. If one day my table changes and suddenly has lots of rows matching that condition, it will be Very Bad. It's because of potential problems like this that PostgreSQL doesn't support planner hints -- such things are a potent foot gun. Use with great care.
