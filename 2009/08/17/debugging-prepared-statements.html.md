---
author: Greg Sabino Mullane
gh_issue_number: 185
tags: perl, postgres, tips
title: Debugging prepared statements
---



I was recently tasked with the all-too-familiar task for DBAs of “why is this script running so slow?”. After figuring out exactly which script and where it was running from, I narrowed down the large number of SQL commands it was issuing to one particularly slow one, that looked something like this in the [pg_stat_activity view](https://www.postgresql.org/docs/current/static/monitoring-stats.html#MONITORING-STATS-VIEWS):

```sql
current_query 
-------------
SELECT DISTINCT id
FROM containers
WHERE code LIKE $1
```

Although the query ran too quick to really measure a finite time just by watching pg_stat_activity, it did show up quite often. So it was likely slow *and* being called many times in a loop somewhere. The use of ‘LIKE’ always throws a yellow flag, so those factors encouraged me look closer into the query.

While the table in question did have an index on the ‘code’ column, it was not being used. This is because LIKE (on non-C locale databases) cannot work against normal indexes—​it needs a simpler character by character index. In Postgres, you can achieve this by using some of the built in operator classes when creating an index. More details can be found at [the documentation on operator classes](https://www.postgresql.org/docs/current/static/indexes-opclass.html). What I ended up doing was using text_pattern_ops:

```
SET maintenance_work_mem = '2GB';

CREATE INDEX CONCURRENTLY containers_code_textops
  ON containers (code text_pattern_ops);
```

Since this was on a production system (yes, I tested on a QA box first!), the CONCURRENTLY phrase ensured that the index did not block any reads or writes on the table while the index was being built. Details on this awesome option can be found in [the docs on CREATE INDEX](https://www.postgresql.org/docs/8.4/static/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY).

After the index was created, the following test query went from 800ms to 0.134ms!:

```sql
EXPLAIN ANALYZE SELECT * FROM containers WHERE code LIKE 'foobar%';
```

I then created a copy of the original script, stripped out any parts that made changes to the database, added a rollback to the end of it, and tested the speed. Still slow! Recall that the original query looked like this:

```sql
SELECT DISTINCT id
FROM containers
WHERE code LIKE $1
```

The **$1** indicates that this is a prepared query. This leads us to the most important lesson of this post: whenever you see that a prepared statement is being used, it’s not enough to test with a normal EXPLAIN or EXPLAIN ANALYZE. You must emulate what the script (e.g. the database driver) is really doing. So from psql, I did the following:

```sql
PREPARE foobar(text) AS SELECT DISTINCT id FROM containers WHERE code LIKE $1;
EXPLAIN ANALYZE EXECUTE('foobar%');
```

Bingo! This time, the new index was *not* being used. This is the great trade-off of prepared statements—​while it allows you to prepare and rewrite the query only once, the planner cannot anticipate what you might pass in as a possible argument, so it makes the best generic plan possible. Thus, your EXPLAIN of the same query using literals or placeholders via PREPARE may look very different.

While it’s possible to make workarounds at the database level for the problem of prepared statements using the “wrong” plan, in this case it was simply easier to tell the existing script not to use prepared statements at all for this one query. As the script was using [DBD::Pg](https://metacpan.org/release/DBD-Pg), the solution was to simply use the pg_server_prepare attribute like so:

```perl
$dbh->{pg_server_prepare} = 0;
my $sth = $dbh->prepare('SELECT DISTINCT id FROM containers WHERE code LIKE ?');
$dbh->{pg_server_prepare} = 1;
```

The effect of this inside of DBD::Pg is that instead of using PQprepare and then PQexecPrepared for each call to $sth->execute(), DBD::Pg will, for every call to $sth->execute(), quote the parameter itself, build a string containing the original SQL statement and the quoted literal, and send it to the backend via PQexec. Normally not something you want to do, but the slight overhead of doing it that way was completely overshadowed by the speedup of using the new index.

The final result: the script that used to take over 6 hours to run now only takes about 9 minutes to complete. Not only are the people using the script much happier, but it means less load on the database.


