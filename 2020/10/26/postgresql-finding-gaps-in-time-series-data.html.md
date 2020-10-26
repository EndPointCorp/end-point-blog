---
author: "David Christensen"
title: "Detecting gaps in time-series data in PostgreSQL"
tags: postgres, database
---

![Mosaic 18](/blog/2020/10/26/postgresql-finding-gaps-in-time-series-data/banner.jpg)
[Photo](https://www.flickr.com/photos/phoebe_photo/33735147071/) by [Phoebe Baker](https://www.flickr.com/photos/phoebe_photo/), under Public Domain.


A client has a number of data feeds that are supposed to update at regular intervals.  Like most
things in the universe (thanks, entropy!) this does not always end up working out the way we want.
We recently discovered that some of the data had not loaded as expected, and were brought in to
assess the extent of the issue.

There were 2 main feeds that had issues, with different types of time data.  The first had
date-based data with batches and the second had full-range timestamps.  We will examine each type
individually, since they have similar---but not the same---characteristics.

Date-based, with batches
========================

In the first data feed there was a table which tracked which files had been loaded by file date and
batch number (there was a morning/evening batch designated by a `batch` field with either `A` or
`B`).  Since the files that had not loaded successfully did not have entries in this table we could
find that one or both of the day's batch files would be missing, but since the table tracked those
which *did* get loaded, we needed to turn this list into something useful.

Any time I find myself considering sequences of data, I remember my friend `generate_series()`.
While `generate_series()` is often called with numeric data, it can also generate date ranges, which
can come in very handy:

```
postgres=# SELECT * FROM generate_series('2020-01-01'::date, '2020-10-01'::date, interval '1 day') limit 10;
    generate_series     
------------------------
 2020-01-01 00:00:00-06
 2020-01-02 00:00:00-06
 2020-01-03 00:00:00-06
 2020-01-04 00:00:00-06
 2020-01-05 00:00:00-06
 2020-01-06 00:00:00-06
 2020-01-07 00:00:00-06
 2020-01-08 00:00:00-06
 2020-01-09 00:00:00-06
 2020-01-10 00:00:00-06
(10 rows)
```

Let's create our sample table and populate with data to simulate the situation we ran into:

```
CREATE TABLE loader_manifest (filename text, batch char, status char, processed_at timestamptz);

INSERT INTO loader_manifest (filename, batch, status, processed_at)
SELECT
    to_char(generate_series('2020-01-01'::date, '2020-10-22'::date, '1 day'), 'YYYYMMDD'),
    batch,
    'L',
    now()
FROM (VALUES ('A'::char) ,('B')) batches(batch)
ORDER BY 1,2
;

-- create some gaps to later detect

DELETE FROM loader_manifest WHERE filename = '20200218' AND batch = 'B';
DELETE FROM loader_manifest WHERE filename = '20200426' AND batch = 'A';
DELETE FROM loader_manifest WHERE filename = '20201019';

```

The data that we were trying to match against looked similar to the following:

```
postgres=# select * from loader_manifest limit 5;
 filename | batch | status |         processed_at          
----------+-------+--------+-------------------------------
 20200101 | A     | L      | 2020-10-18 11:25:05.878229-05
 20200101 | B     | L      | 2020-10-18 11:25:05.878229-05
 20200102 | A     | L      | 2020-10-18 11:25:05.878229-05
 20200102 | B     | L      | 2020-10-18 11:25:05.878229-05
 20200103 | A     | L      | 2020-10-18 11:25:05.878229-05
(5 rows)
```

Since either the batch or entire days could have been missing we basically needed to generate the
list of expected combinations and use a `LEFT JOIN` to find which values in this table were missing.
While this example has only 2 batch options, this solution would work for additional numbers of
expected batches.

Because `generate_series()` is a set-returning function we can use it as a source in our `FROM`
clause, in combination with the explicit values we want for our `batch` field.  We also will need to
extract the date pieces out in a way that we can match the expected `filename` format.  We use
something similar to the following:

```
postgres=# SELECT to_char(filename,'YYYYMMDD') as filename, batch FROM generate_series('2020-01-01'::date, '2020-10-01'::date, interval '1 day') as filename, (values ('A'),('B')) as batches(batch) limit 10;
 filename  | batch 
----------+-------
 20200101  | A
 20200101  | B
 20200102  | A
 20200102  | B
 20200103  | A
 20200103  | B
 20200104  | A
 20200104  | B
 20200105  | A
 20200105  | B
(10 rows)
```

So as we can see, this will generate the list of all expected filename/batch combinations that we
can then check the original table against for missing values:

```sql
SELECT
    candidates.*
FROM (
    SELECT
        to_char(filename,'YYYYMMDD') as filename,
        batch
    FROM
        generate_series('2020-01-01'::date, '2020-10-01'::date, interval '1 day') AS filename,
        (values ('A'),('B')) AS batches(batch)
    ) candidates
NATURAL LEFT JOIN
    loader_manifest
WHERE loader_manifest.filename IS NULL
```

Here `candidates` is the generated list of all expected file/batch combinations.

And the results from our sample dataset:

```
 filename | batch
----------+-------
 20200218 | B
 20200426 | A
 20201019 | A
 20201019 | B
(4 rows)
```

As expected, this has identified the rows that we know are missing from the table.  Success!

Non-date-based
==============

The second type of query had to identify similar gaps in loaded data, but used a different approach.
This data feed had a `processing_time_utc` field which would vary, but we expected this to have
fairly regular updates.  This data feed could be processed somewhat erratically, but if the data was
complete we would expect to see records with `processing_time_utc` approximately every 10 minutes.
If we found that there were gaps much larger than every 10 minutes we could suspect missing data and
would need to locate/reprocess the underlying data files.

This approach also uses `generate_series()`, but since we do not have a single date that we can
check existence of, the `JOIN` approach does not work directly.  This means that in order to find
the gaps we care about, the need to check that at least *some* data exists within each timeperiod in
question.

Here's the query:

```sql
SELECT
    day
FROM generate_series('2020-07-01'::date, '2020-08-01'::date, INTERVAL '10 minutes') AS day
LEFT JOIN LATERAL
    (SELECT day FROM the_table WHERE processing_time_utc >= day AND processing_time_utc < day + INTERVAL '10 minutes' LIMIT 1) gap ON day = gap.day
WHERE gap.day IS NULL;
```

The key here is that we use `generate_series()` with an `INTERVAL` of the window size we care about,
and then use that same `INTERVAL` when checking for any row's existence that fits that criteria.
With the `LIMIT 1` on the `gap` subquery, we stop at the first record we find in that range, and
thus we can exclude in the antijoin to find our results.

I should note that this approach works regardless of the size of the logical date partitions, and
can be used to identify all gaps of at least the interval size we are looking at; the same query can
check for gaps every 10 minutes as for hourly, daily, weekly, etc; it is purely a matter of
selecting the proper interval size in the query in question.

Also note that the `processing_time_utc` field is indexed, or this would be painfully slow; we use a
`LATERAL` query to pull in one specific row that matches the time interval we care about and ignore
any others.  (Note that this technique finds only the cases where *no* data is present for the time
interval, not less than expected.  You could certainly adapt this approach to that situation by
using an appropriate query.)

Summary
=======

These approaches definitely come in handy when trying to isolate missing data based on time; which
tack you take will depend on the expected data present, as well as the granularity in which you
identify your gaps.
