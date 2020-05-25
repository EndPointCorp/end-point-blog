---
author: Szymon Lipiński
gh_issue_number: 1207
tags: postgres
title: Converting JSON to PostgreSQL values, simply
---

In the [previous post](/blog/2016/02/24/storing-statistics-json-data-in) I showed a simple PostgreSQL table for storing JSON data. Let’s talk about making the JSON data easier to use.

One of the requirements was to store the JSON from the files unchanged.
However using the JSON operators for deep attributes is a little bit unpleasant.
In the example JSON there is attribute country inside metadata.
To access this field, we need to write:

```sql
SELECT data->'metadata'->>'country' FROM stats_data;
```

The native SQL version would rather look like:

```sql
SELECT country FROM stats;
```

So let’s do something to be able to write the queries like this.
We need to repack the data to have the nice SQL types, and hide all the nested
JSON operators.

I’ve made a simple view for this:

```sql
CREATE VIEW stats AS
SELECT
  id                                                    AS id,
  created_at                                            AS created_at,
  to_timestamp((data->>'start_ts')::double precision)   AS start_ts,
  to_timestamp((data->>'end_ts')::double precision)     AS end_ts,
  tstzrange(
    to_timestamp((data->>'start_ts')::double precision),
    to_timestamp((data->>'end_ts')::double precision)
  )                                                     AS ts_range,
  ( SELECT array_agg(x)::INTEGER[]
    FROM jsonb_array_elements_text(data->'resets') x)   AS resets,
  (data->'sessions')                                    AS sessions,
  (data->'metadata'->>'country')                        AS country,
  (data->'metadata'->>'installation')                   AS installation,
  (data->>'status')                                     AS status
FROM stats_data;
```

This is a normal view, which means that it is only a query stored in the database.
Each time the view is queried, the data must be taken from the stats_data table.

There is some code I could extract to separate functions.
This will be useful in the future, and the view sql should be cleaner.

Here are my new functions:

```sql
CREATE OR REPLACE FUNCTION to_array(j jsonb) RETURNS integer[] AS $$
  SELECT array_agg(x)::INTEGER[] FROM jsonb_array_elements_text(j) x;
$$
LANGUAGE sql
IMMUTABLE;

CREATE OR REPLACE FUNCTION to_timestamp(j jsonb) RETURNS timestamptz AS $$
  SELECT to_timestamp(j::text::double precision);
$$
LANGUAGE sql
IMMUTABLE;

CREATE OR REPLACE FUNCTION to_timestamp_range(start_ts jsonb, end_ts jsonb) RETURNS tstzrange AS $$
  SELECT tstzrange(
    to_timestamp(start_ts::text::double precision),
    to_timestamp(end_ts::text::double precision)
  );
$$
LANGUAGE sql
IMMUTABLE;
```

And now the view can be changed to this:

```sql
CREATE VIEW stats AS
SELECT
  id                                                   AS id,
  created_at                                           AS created_at,
  to_timestamp(data->'start_ts')                       AS start_ts,
  to_timestamp(data->'end_ts'  )                       AS end_ts,
  to_timestamp_range(data->'start_ts', data->'end_ts') AS ts_range,
  to_array(data->'resets')                             AS resets,
  (data->'sessions')                                   AS sessions,
  (data->'metadata'->>'country')                       AS country,
  (data->'metadata'->>'installation')                  AS installation,
  (data->>'status')                                    AS status
FROM stats_data;
```

So currently we have normal SQL fields, except for the sessions part,
which is there as JSON for a purpose.

The types made by PostgreSQL are:

```sql
                 View "public.stats"
    Column    │           Type           │ Modifiers
──────────────┼──────────────────────────┼───────────
 id           │ integer                  │
 created_at   │ timestamp with time zone │
 start_ts     │ timestamp with time zone │
 end_ts       │ timestamp with time zone │
 ts_range     │ tstzrange                │
 resets       │ integer[]                │
 sessions     │ jsonb                    │
 country      │ text                     │
 installation │ text                     │
 status       │ text                     │
```

The data from this view looks like this:

```sql
SELECT * FROM stats WHERE id = 1;

-[ RECORD 1 ]+----------------------------------------------------------------
id           | 1
created_at   | 2016-02-09 16:46:15.369802+01
start_ts     | 2015-08-03 21:10:33+02
end_ts       | 2015-08-03 21:40:33+02
ts_range     | ["2015-08-03 21:10:33+02","2015-08-03 21:40:33+02")
resets       | \N
sessions     | [{"end_ts": 1438629089, "start_ts": 1438629058, "application": "first"},
                {"end_ts": 1438629143, "start_ts": 1438629123, "application": "second"},
                {"end_ts": 1438629476, "start_ts": 1438629236, "application": "third"}]
country      | USA
installation | FIRST
status       | on
```

The last part left is to extract information about the sessions.
To make the reports simpler, I’ve extracted the sessions list into another view.
However, because the operation of extracting the data is more expensive,
I made it as a MATERIALIZED VIEW. This means that this view not only stores
the query, but also keeps all the view data. This also means that this view
is not updated automatically when the stats_data changes.
I refresh the view data automatically in a script which loads the JSON files.

The sessions view looks like this:

```sql
CREATE MATERIALIZED VIEW sessions AS
SELECT
  id                                                      AS id,
  country                                                 AS country,
  installation                                            AS installation,
  s->>'application'                                       AS appname,
  to_timestamp_range(s->'start_ts', s->'end_ts')          AS ts_range,
  COALESCE(bool(s->>'occupancy_triggered'), false)        AS occupancy_triggered,
  to_timestamp(s->'end_ts') - to_timestamp(s->'start_ts') AS session_length
FROM stats, jsonb_array_elements(sessions) s;

CREATE INDEX i_sessions_country  ON sessions (country);
CREATE INDEX i_sessions_retailer ON sessions (installation);
CREATE INDEX i_sessions_ts_range ON sessions USING GIST (ts_range);
```

I’ve also created indexes on the materialized view, as my report queries will
contain the where clause like:

```sql
WHERE country='' and installation='' and ts_range && tstzrange(fromdate, todate)
```

An example data extracted from the JSON looks like this:

```sql
select * from sessions;

id | country | installation | appname |                      ts_range                       | occupancy_triggered | session_length
----+---------+--------------+---------+-----------------------------------------------------+---------------------+----------------
 1 | USA     | FIRST        | first   | ["2015-08-03 21:10:58+02","2015-08-03 21:11:29+02") | f                   | 00:00:31
 1 | USA     | FIRST        | second  | ["2015-08-03 21:12:03+02","2015-08-03 21:12:23+02") | f                   | 00:00:20
 1 | USA     | FIRST        | third   | ["2015-08-03 21:13:56+02","2015-08-03 21:17:56+02") | f                   | 00:04:00
(3 rows)
```

In the next part I will show how to load the same JSON files multiple times,
without any errors in a very simple Python script.
