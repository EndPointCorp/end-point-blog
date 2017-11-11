---
author: Szymon Lipiński
gh_issue_number: 1206
tags: postgres
title: Storing Statistics JSON Data in PostgreSQL
---

We have plenty of Liquid Galaxy systems, where we write statistical information in json files. This is quite a nice solution. However we end with a bunch of files on a bunch of machines.

Inside we have a structure like:

```javascript
{
    "end_ts": 1438630833,
    "resets": [],
    "metadata": {
        "country": "USA",
        "installation": "FIRST"
    },
    "sessions": [
        {
            "application": "first",
            "end_ts": 1438629089,
            "start_ts": 1438629058
        },
        {
            "application": "second",
            "end_ts": 1438629143,
            "start_ts": 1438629123
        },
        {
            "application": "third",
            "end_ts": 1438629476,
            "start_ts": 1438629236
        }
    ],
    "start_ts": 1438629033,
    "status": "on"
}
```

And the files are named like "{start_ts}.json".
The number of files is different on each system.
For January we had from 11k to 17k files.

The fields in the json mean:

- start_ts/end_ts - timestamps for start/end for the file
- resets - is an array of timestamps when system was resetted
- sessions - a list of sessions, each contains application name and start/end timestamps

We keep these files in order to get statistics from them.
So we can do one of two things: keep the files on disk, and write a script
for making reports. Or load the files into a database, and make the reports
from the database.

The first solution looks quite simple.
However for a year of files, and a hundred of systems,
there will be about 18M files.

The second solution has one huge advantage: it should be faster.
A database should be able to have some indexes,
where the precomputed data should be stored for faster querying.

For a database we chose PostgreSQL.
The 9.5 version released in January has plenty of great features for managing JSON data.

The basic idea behind the database schema is:

- the original jsons should be stored without any conversion
- the report queries must be fast
- there should be only one json entry for a site for given time
- the script loading the data should load the same file many times without any error

I've started with the main table for storing jsons:

```sql
CREATE TABLE stats_data (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  data JSONB NOT NULL
);
```

This is not enough. We also want to avoid storing the same json multiple times.
This can easily be done with an EXCLUDE clause.

```sql
CREATE TABLE stats_data (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  data JSONB NOT NULL,

  CONSTRAINT no_overlapping_jsons
  EXCLUDE USING gist (
    tstzrange(
      to_timestamp((data->>'start_ts')::double precision),
      to_timestamp((data->>'end_ts'  )::double precision)
    ) WITH &&,
    ((data->>'metadata')::json->>'country')      WITH =,
    ((data->>'metadata')::json->>'installation') WITH =
  )
);
```

The above SQL requires a small extention to be installed

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;
```

And now inserting the same json results in error:

```sql
$ insert into stats_data(data) select data from stats_data;
ERROR:  conflicting key value violates exclusion constraint "no_overlapping_jsons"
```

So for now we have a simple table with original json,
and with a constraint disallowing to insert overlapping jsons.

In the next part I will show how to make simple reports and load the json files.
