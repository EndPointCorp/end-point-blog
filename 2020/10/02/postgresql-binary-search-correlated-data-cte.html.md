---
author: "David Christensen"
title: "Using CTEs to do a binary search of large tables with non-indexed correlated data"
tags: postgresql
---

![Horses racing, accompanied by jockeys](/blog/2020/10/02/postgresql-binary-search-correlated-data-cte/banner.jpg)
[Photo](https://www.flickr.com/photos/colink/8646391995/) by [Colin Knowles](https://www.flickr.com/photos/colink/), used under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/).

Query optimization can take different forms depending on the data represented and the required
needs.  In a recent case, we had a large table that we had to query for some non-indexed criteria.
This table was on an appliance that we were unable to modify and which we had to query based on
some fields which did not have indexes setup for many of the fields we cared about.

The straightforward approach for this query was something along these lines:

```sql
SELECT
    accounts.*
FROM
    accounts
JOIN
    logs
ON accounts.id = logs.account_id
WHERE
    logs.created_at BETWEEN $1 - 'interval 1 minute' AND $1 + 'interval 1 minute' AND
    logs.field1 = $2 AND
    logs.field2 = $3
FETCH FIRST ROW ONLY
```

Unfortunately, none of the fields involved in this query were indexed---nor could they be, due to
our access level on this database system.  This lack of indexes means that our query against those
fields would end up with a `SeqScan` which made things unacceptably slow.  This specific table held
time-series data with ~ 100k records per 1 minute period over a period of several weeks, which
basically meant we were dealing with a lot of data.

While we could not create any additional indexes to help us with this query, we could use some
specific properties to help us:

1) There was a unique primary key field, `id`, which was unique and monotonic (i.e., always
increasing in value).

2) This table was append only; no updates or deletes, so once data existed in the table it was
always the same.

3) The field we actually care about (`created_at`) also ends up being monotonic (in this case,
subsequent records would always have the same or later values).

4) Since records were created sequentially and the `id` field was always increasing, `id` values and
`created_at` fields would be together be generally monotonic; this means there *is* an indexed field
which we can use as a surrogate stand-in for the target field that we want to treat as an index.
While due to the nature of logging ingest it is possible the `created_at` and `id` values are not
strictly monotonic (for instance if there are multiple logging records being created by separate
ingest processes, of which `id`s get assigned in chunks), for our purposes this was close enough,
since we were looking around in a time window which was wider than we were actually expecting the
message to appear.

5) Since we are looking for fields matching a specific window of time, we can substitute the
non-indexed clause `created_at BETWEEN <timestamp_min> and <timestamp_max>` with an expression
matching the indexed statement `id between <id of first id gt timestamp_min> and <id of first id gt
timestamp_max>` to get the same effective approach.

6) In order to find the specific `id` fields which match the `created_at` time ranges we are
interested in, we would need to find the first `id` value which matched the criteria `created_at >
'timestamp'::timestamp`, as all subsequent `id` values would match that condition as well.  This
would effectively require a binary search of the table to check which records match the criteria,
and return the smallest `id` value for which this criteria held.

So now that we have identified how we can use an indexed surrogate key to substitute for the
non-indexed expression, we need to figure out how to calculate the ranges in question.

Based on some recent discoveries about optimizing simple-looking but poorly-performing queries using
more complicated queries[^1], I had instincts that this could be solved with a `WITH RECURSIVE`
Common Table Expression.  After toying around for a while and not coming up with the exact solution,
I ended up visiting the `#postgresql` channel on FreeNode IRC Network.  There, I presented the
problem and got some interested responses, as this is the exact kind of question that database
~~nerds~~ experts love[^2].  The solution that user `xocolatl` (Vik Fearing) came up with for a basic
binary search is the basis for the rest of my solution:

```sql
CREATE TABLE test_table (id integer PRIMARY KEY, ts timestamptz);
​
INSERT INTO test_table SELECT g, date 'today' + interval '1s' * g FROM generate_series(1, 1000000) AS g;
​
WITH RECURSIVE
search (min, max, middle, level) AS (
    SELECT min(id), max(id), (min(id)+max(id))/2, 0 FROM test_table
        UNION ALL
    SELECT v.min, v.max, (v.min + v.max)/2, s.level+1
    FROM search as s
    CROSS JOIN LATERAL (
        SELECT *
        FROM test_table AS e
        WHERE e.id >= s.middle
        ORDER BY e.id
        FETCH FIRST ROW ONLY
    ) AS e
    CROSS JOIN LATERAL (VALUES (
        CASE WHEN e.ts < now() THEN e.id ELSE s.min END,
        CASE WHEN e.ts < now() THEN s.max ELSE e.id END
    )) AS v (min, max)
    WHERE (v.min + v.max)/2 NOT IN (v.min, v.max)
)
SELECT *
FROM search AS s
JOIN test_table AS e ON e.id = s.middle
ORDER BY s.level DESC
FETCH FIRST ROW ONLY
;
```

As expected, the solution involved a `WITH RECURSIVE` CTE.

The basic explanation here is that the `search` expression first starts with the `min`, `max`, and
`middle` (mean) values of `id` for the table (the initialization expression), then iteratively adds
additional rows to the results depending on if the table row with `id >= middle` matches our
specific test criteria, then continues until one of the boundaries of the region is hit.  (Since we
are using integer division in our terminal expression `(v.min + v.max)/2 NOT IN (v.min, v.max)` we
are guaranteed to hit one of the boundary conditions eventually in our search.)

A couple other things worthy of note:

1) This approach uses the check `e.ts < now()` as the condition we are testing, which means in this
specific example, the answer to this "closest id" query would actually change depend on when you run
this query relative to when the initial test data was populated.  However, we can replace that
condition with whatever condition we want to use to test for our surrogate non-indexed data.

2) This approach will work whether or not there are gaps in the sequence.  In order to properly
handle gaps, we are selecting the first row with `id >= middle ... FETCH FIRST ROW ONLY` rather than
just selecting `id = middle`, which you could do in a gapless sequence.

3) In addition to not caring about gaps, we are also not trying to make sure this is using a
balanced binary search; it would be not worth the computing effort to find the middlest existing row
in an index, as we'd need to know the number of rows in the segment we're searching.  Since in
PostgreSQL this would entail a `COUNT(*)` from a subselect, this would be quite slow and not worth
the trouble.

Considering my specific use case was trying to limit the records considered based on two
`created_at` values I needed to calculate a `search_min` and `search_max` to find the start/end
`id`s for each side in the interval.

Given this, I just modified the CTE to calculate those and add the additional conditions we were
wanting to consider.  I also had to turn the result query from a join against the found `id` value
to a range; the final query is as follows:

```sql
WITH RECURSIVE
search_min (min, max, middle, level) AS (
    SELECT min(id), max(id), (min(id)+max(id))/2, 0 FROM logs
        UNION ALL
    SELECT v.min, v.max, (v.min + v.max)/2, s.level+1
    FROM search_min AS s
    CROSS JOIN LATERAL (
        SELECT *
        FROM logs AS e
        WHERE e.id >= s.middle
        ORDER BY e.id
        FETCH FIRST ROW ONLY
    ) AS e
    CROSS JOIN LATERAL (VALUES (
        CASE WHEN extract(epoch FROM e.created_at) :: integer < $1 THEN e.id ELSE s.min END,
        CASE WHEN extract(epoch FROM e.created_at) :: integer < $1 THEN s.max ELSE e.id END
    )) as v (min, max)
    WHERE (v.min + v.max)/2 NOT IN (v.min, v.max)
),
search_max (min, max, middle, level) AS (
    SELECT min(id), max(id), (min(id)+max(id))/2, 0
    FROM logs
        UNION ALL
    SELECT v.min, v.max, (v.min + v.max)/2, s.level+1
    FROM search_max AS s
    CROSS JOIN LATERAL (
        SELECT *
        FROM logs AS e
        WHERE e.id >= s.middle
        ORDER BY e.id
        FETCH FIRST ROW ONLY
    ) AS e
    CROSS JOIN LATERAL (VALUES (
        CASE WHEN extract(epoch FROM e.created_at) :: integer < $2 THEN e.id ELSE s.min END,
        CASE WHEN extract(epoch FROM e.created_at) :: integer < $2 THEN s.max ELSE e.id END
    )) as v (min, max)
    WHERE (v.min + v.max)/2 NOT IN (v.min, v.max)
)
SELECT
    accounts.*
FROM
    accounts
JOIN
    logs
ON
    logs.account_id = accounts.id
WHERE
    logs.field1 = $3 AND
    logs.field2 = $4 AND
    logs.id >= (SELECT middle FROM search_min ORDER BY level DESC FETCH FIRST ROW ONLY)
    logs.id <= (SELECT middle FROM search_max ORDER BY level DESC FETCH FIRST ROW ONLY)
ORDER BY
    logs.id
FETCH FIRST ROW ONLY
```

The final results were drastically improved.  The initial query went from timing out in the
webservice in question to returning results in a fraction of a second.  Clearly this technique --
while not as useful as directly indexing data we care about -- can come in handy in some
circumstances.

Another tool for the toolbag!

[^1]: [https://www.endpoint.com/blog/2020/06/30/postgresql-improve-group-by-max-performance](https://www.endpoint.com/blog/2020/06/30/postgresql-improve-group-by-max-performance)

[^2]: aka [nerdsniping](https://xkcd.com/356/)
