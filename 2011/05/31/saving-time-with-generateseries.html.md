---
author: Josh Tolley
gh_issue_number: 461
tags: postgres, sql
title: Saving time with generate_series()
---



I was giving a presentation once on various SQL constructs, and, borrowing an analogy I'd seen elsewhere, described PostgreSQL's generate_series() function as something you might use in places where, in some other language, you'd use a FOR loop. One attendee asked, "So, why would you ever want a FOR loop in a SQL query?" A fair question, and one that I answered using examples later in the presentation. Another such example showed up recently on a client's system where the [ORM](http://en.wikipedia.org/wiki/Object-Relational_Mapping) was trying to be helpful, and chose a really bad query to do it.

The application in question was trying to display a list of records, and allow the user to search through them, modify them, filter them, etc. Since the ORM knew users might filter on a date-based field, it wanted to present a list of years containing valid records. So it did this:  

```sql
SELECT DISTINCT DATE_TRUNC('year', some_date_field) FROM some_table;
```

In fairness to the ORM, this query wouldn't be so bad if *some_table* only had a few hundred or thousand rows. But in our case it has several tens of millions. This query results in a sequential scan of each of those records, in order to build a list of, as it turns out, about fifty total years. There must be a better way...

The better way we chose turns out to be, in essence, this: find the years of the maximum and minimum date values in the date field, construct a list of all years between the minimum and maximum, inclusive, and see which ones exist in the table. This date field is indexed, so finding its maximum and minimum is very fast:

```sql
SELECT
    DATE_TRUNC('year', MIN(some_date_field)) AS mymin,
    DATE_TRUNC('year', MAX(some_date_field)) AS mymax
FROM some_table
```

Here's where the FOR loop idea comes in, though it's probably better described as an "iterator" rather than a FOR loop specifically: for each year between *mymin* and *mymax* inclusive, I want a database row. The analogy may not hold terribly well, but the technique is very useful, because it will create a list of all the possible years I might be interested in, and it will do it with just two scans of the *some_date_field* index, rather than a sequential scan of millions of rows.

```sql
SELECT
    generate_series(mymin::INTEGER, mymax::INTEGER) AS yearnum
FROM (
    SELECT
        DATE_TRUNC('year', MIN(some_date_field)) AS mymin,
        DATE_TRUNC('year', MAX(some_date_field)) AS mymax
    FROM some_table
) minmax_tbl
```

Now I simply have to convert these values to years, and see which ones exist in the underlying table:

```sql
SELECT
    yearbegin::timestamptz
FROM
    (
        SELECT
            yearnum * INTERVAL '1 year' + '0000-01-01'::date AS yearbegin
        FROM (
            SELECT
                generate_series(mymin::INTEGER, mymax::INTEGER) AS yearnum
            FROM (
                SELECT
                    DATE_TRUNC('year', MIN(some_date_field)) AS mymin,
                    DATE_TRUNC('year', MAX(some_date_field)) AS mymax
                FROM some_table
        ) yearnum_tbl
    ) beginend_tbl
WHERE
    EXISTS (
        SELECT 1 FROM some_table
        WHERE
            some_date_field BETWEEN yearbegin AND yearbegin + INTERVAL '1 year'
    )
ORDER BY yearbegin ASC
;
```

As expected, this probes the *some_date_field* index twice, to get the maximum and minimum date values, and then once for each year between those values. Because of some strangely-dated data in there, that means nearly 10,000 index probes, but that's still much faster than scanning the entire table.


