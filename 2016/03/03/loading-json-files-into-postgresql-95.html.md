---
author: Szymon Lipiński
gh_issue_number: 1208
tags: postgres
title: Loading JSON Files Into PostgreSQL 9.5
---

In the [previous](/2016/02/storing-statistics-json-data-in.html) [posts](/2016/02/converting-json-to-postgresql-values.html) I have described a simple database table for storing JSON values, and a way to unpack nested JSON attributes into simple database views. This time I will show how to write a very simple query (thanks to PostgreSQL 9.5) to load the JSON files

Here's a simple Python script to load the database.

This script is made for PostgreSQL 9.4 (in fact it should work for 9.5 too, but is not using a nice new 9.5 feature described below).

```python
#!/usr/bin/env python

import os
import sys
import logging

try:
    import psycopg2 as pg
    import psycopg2.extras
except:
    print "Install psycopg2"
    exit(123)

try:
    import progressbar
except:
    print "Install progressbar2"
    exit(123)

import json

import logging
logger = logging.getLogger()

PG_CONN_STRING = "dbname='blogpost' port='5433'"

data_dir = "data"
dbconn = pg.connect(PG_CONN_STRING)

logger.info("Loading data from '{}'".format(data_dir))

cursor = dbconn.cursor()

counter = 0
empty_files = []

class ProgressInfo:

    def __init__(self, dir):
        files_no = 0
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".json"):
                    files_no += 1
        self.files_no = files_no
        print "Found {} files to process".format(self.files_no)
        self.bar = progressbar.ProgressBar(maxval=self.files_no,
                                           widgets=[' [', progressbar.Timer(), '] [', progressbar.ETA(), '] ', progressbar.Bar(),])

    def update(self, counter):
        self.bar.update(counter)

pi = ProgressInfo(os.path.expanduser(data_dir))

for root, dirs, files in os.walk(os.path.expanduser(data_dir)):
    for f in files:
        fname = os.path.join(root, f)

        if not fname.endswith(".json"):
            continue
        with open(fname) as js:
            data = js.read()
            if not data:
                empty_files.append(fname)
                continue
            import json
            dd = json.loads(data)
            counter += 1
            pi.update(counter)
            cursor.execute("""
                            INSERT INTO stats_data(data)
                            SELECT %s
                            WHERE NOT EXISTS (SELECT 42
                                              FROM stats_data
                                              WHERE
                                                    ((data-&gt;&gt;'metadata')::json-&gt;&gt;'country')  = %s
                                                AND ((data-&gt;&gt;'metadata')::json-&gt;&gt;'installation') = %s
                                                AND tstzrange(
                                                        to_timestamp((data-&gt;&gt;'start_ts')::double precision),
                                                        to_timestamp((data-&gt;&gt;'end_ts'  )::double precision)
                                                    ) &amp;&amp;
                                                    tstzrange(
                                                        to_timestamp(%s::text::double precision),
                                                        to_timestamp(%s::text::double precision)
                                                    )
                                             )
                        """, (data, str(dd['metadata']['country']), str(dd['metadata']['installation']), str(dd['start_ts']), str(dd['end_ts'])))

print ""

logger.debug("Refreshing materialized views")
cursor.execute("""REFRESH MATERIALIZED VIEW sessions""");
cursor.execute("""ANALYZE""");

dbconn.commit()

logger.info("Loaded {} files".format(counter))
logger.info("Found {} empty files".format(len(empty_files)))
if empty_files:
    logger.info("Empty files:")
    for f in empty_files:
        logger.info(" &gt;&gt;&gt; {}".format(f))
```

I have created two example files in the 'data' directory, the output of this script is:

```python
Found 2 files to process
 [Elapsed Time: 0:00:00] [ETA:  0:00:00] |#####################################|
```

Yey, so it works. What's more, I can run the script again on the same files,
and it will try loading the same data without any errors. Do you rememember that
there was an EXCLUDE constraint which doesn't allow us to load any JSON for the same
country, and installation, and overlapping time range? That's why the query is so
long. I also need to check that such a JSON is not in the database, so I can
load it.

This is twice slower than the next solution. The problem is that it needs to
unpack the JSON to run the subquery, then insert the data checking the same
thing (in fact the insert, and the subquery are using the same index made by
the EXCLUDE constraint).

And then PostgreSQL 9.5 was released, with one great feature:
ON CONFLICT DO SOMETHING. The conflict is a UNIQUE index violation.
The EXCLUDE clause in the stats_data table created such a unique index.

There can also be ON CONFLICT DO NOTHING, and that's what I have used.
I changed only one query in the script, and instead of this:

```python

            cursor.execute("""
                            INSERT INTO stats_data(data)
                            SELECT %s
                            WHERE NOT EXISTS (SELECT 42
                                              FROM stats_data
                                              WHERE
                                                    ((data-&gt;&gt;'metadata')::json-&gt;&gt;'country')  = %s
                                                AND ((data-&gt;&gt;'metadata')::json-&gt;&gt;'installation') = %s
                                                AND tstzrange(
                                                        to_timestamp((data-&gt;&gt;'start_ts')::double precision),
                                                        to_timestamp((data-&gt;&gt;'end_ts'  )::double precision)
                                                    ) &amp;&amp;
                                                    tstzrange(
                                                        to_timestamp(%s::text::double precision),
                                                        to_timestamp(%s::text::double precision)
                                                    )
                                             )
                        """, (data, str(dd['metadata']['country']), str(dd['metadata']['installation']), str(dd['start_ts']), str(dd['end_ts'])))

```

It looks like this:

```python

            cursor.execute("""
                            INSERT INTO stats_data(data)
                            VALUES (%s)
                            ON CONFLICT ON CONSTRAINT no_overlapping_jsons DO NOTHING
                        """, (data, ))

```

This version requires PostgreSQL 9.5 and will not work on the previous versions.

It is twice as fast as the original, and works as expected. This means that I can run it on the
already loaded files, and will not load them. This way when I use rsync to download
the new files, I can just run the script, and it will load only the new files into
the database.

Loading 88k of JSON files using the production version of the script with
the first query takes over 1 minute.

Loading the files using the second version takes less than 30 seconds.
