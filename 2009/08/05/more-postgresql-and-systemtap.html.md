---
author: Josh Tolley
gh_issue_number: 181
tags: postgres
title: More PostgreSQL and SystemTap
---

Recently I've been working on a database with many multi-column indexes, and I've wondered how often all the columns of the index were used. Many of the indexes in question are primary key indexes, and I need all the columns to guarantee uniqueness, but for non-unique indexes, it would make sense to remove as many indexes from the column as possible. Especially with PostgreSQL 8.3 or greater, where I can take advantage of heap-only tuples[1], leaving columns out of the index would be a big win. PostgreSQL's statistics collector will already tell me how often an index is scanned. That shows up in pg_stat_all_indexes. But for a hypothetical index scanned 100 times, there's no way to know how many of those 100 scans used all the columns of the index, or, for instance, just the first column.

First, an example. I'll create a table with three integer columns, and fill it with random data:

```sql
5432 josh@josh# CREATE TABLE a (i INTEGER, j INTEGER, k INTEGER);
CREATE TABLE
5432 josh@josh*# INSERT INTO a SELECT i, j, k FROM (SELECT FLOOR(RANDOM() * 10) AS i, FLOOR(RANDOM() * 100) AS j, FLOOR(RANDOM() * 1000) AS k, GENERATE_SERIES(1, 1000)) f;
INSERT 0 1000
5432 josh@josh*# CREATE INDEX a_ix ON a (i, j, k);
CREATE INDEX
5432 josh@josh*# ANALYZE a;
ANALYZE
5432 josh@josh*# COMMIT;
COMMIT
```

This leaves me with a three-column index on 1000 rows of the following:

```nohighlight
5432 josh@josh*# SELECT * FROM a LIMIT 10;
 i | j  |  k  
---+----+-----
 3 |  6 | 380
 7 | 94 | 933
 1 | 73 | 326
 2 | 86 | 224
 2 | 59 | 336
 9 | 44 | 220
 9 | 48 | 694
 3 | 27 | 268
 3 |  0 | 410
 8 | 25 | 337
(10 rows)
```

Now I need to make a query that will use the index. That's easy enough, with these two queries. As shown by the index condition, the first query uses all three columns of the index, and the second, only two.

```nohighlight
5432 josh@josh# EXPLAIN SELECT * FROM a WHERE i > 8 AND j > 80 AND k > 800;
                            QUERY PLAN                             
-------------------------------------------------------------------
 Bitmap Heap Scan on a  (cost=5.64..10.74 rows=4 width=12)
   Recheck Cond: ((i > 8) AND (j > 80) AND (k > 800))
   ->  Bitmap Index Scan on a_ix  (cost=0.00..5.64 rows=4 width=0)
         Index Cond: ((i > 8) AND (j > 80) AND (k > 800))
(4 rows)

5432 josh@josh*# EXPLAIN SELECT * FROM a WHERE i > 8 AND j > 80;
                             QUERY PLAN                             
--------------------------------------------------------------------
 Bitmap Heap Scan on a  (cost=5.37..10.67 rows=20 width=12)
   Recheck Cond: ((i > 8) AND (j > 80))
   ->  Bitmap Index Scan on a_ix  (cost=0.00..5.36 rows=20 width=0)
         Index Cond: ((i > 8) AND (j > 80))
(4 rows)
```

Inside PostgreSQL, these queries result in a call to _bt_first() inside src/backend/access/nbtree/nbtsearch.c. This function two parameters: an IndexScanDesc object called *scan*, which describes the index to scan, the key to look for, and some other stuff, and a ScanDirection parameter to tell _bt_first() which direction to scan the index. It's this call that tells the statistics collector about each index scan, and it's this call that we'll instrument with SystemTap. I'm interested in the value in scan->numberOfKeys, which tells me how many of the index's keys will be considered in each scan. SystemTap makes getting this information really easy. I gave an introduction to SystemTap and using it with PostgreSQL in [an earlier post](http://blog.endpoint.com/2009/05/postgresql-with-systemtap.html); the following assumes familiarity with that material.

Since PostgreSQL doesn't come with a DTrace probe built into the _bt_first() function, I'll use SystemTap's ability to probe directly into a function. Conveniently, SystemTap also allows access to the values of variables in the function's memory space at runtime. Note that the technique shown below requires a PostgreSQL binary built with --enable-debug. Without debug information in the binary, different techniques are used, and the information is harder to get.

The test script I used is as follows:

```nohighlight
probe process("/usr/local/pgsql/bin/postgres").function("_bt_first")
{
          /* Time of call */
        printf ("_bt_first at time %d\n", get_cycles())
          /* Number of scan keys */
        printf("%d scan keys\n", $scan->numberOfKeys)
          /* OID of index being scanned */
        printf("%u index oid\n\n", $scan->indexRelation->rd_id)
}
```

Note that the script above accesses variables in the _bt_first() function just as standard C functions would. The script has the following output:

```nohighlight
[josh@localhost ~]$ sudo /usr/local/bin/stap -v test.d
Pass 1: parsed user script and 59 library script(s) in 130usr/70sys/196real ms.
Pass 2: analyzed script: 2 probe(s), 3 function(s), 0 embed(s), 0 global(s) in 50usr/50sys/103real ms.
Pass 3: translated to C into "/tmp/stapzCCwZE/stap_1854c2da59908c3e3633d6385ca6ce52_2782.c" in 120usr/80sys/209real ms.
Pass 4, preamble: (re)building SystemTap's version of uprobes.
Pass 4: compiled C into "stap_1854c2da59908c3e3633d6385ca6ce52_2782.ko" in 2240usr/3270sys/8102real ms.
Pass 5: starting run.
_bt_first at time 49379911010213
1 scan keys
2703 index oid

_bt_first at time 49379982691988
1 scan keys
2684 index oid

_bt_first at time 49379987397126
1 scan keys
2684 index oid
```

You'll note several indexes get scanned immediately. These are indexes from the PostgreSQL catalog. The index we created above has OID 16388. First, I'll run the query with three scan keys, followed by the query with two keys:

```nohighlight
_bt_first at time 50357469430819
3 scan keys
16388 index oid

_bt_first at time 50363763650571
2 scan keys
16388 index oid
```

As expected, SystemTap reported first three and then two scan keys used, along with the OID of the a_ix index I created. With a technique like this I could, at least theoretically, get an exact usage profile for each index, and determine whether they need all the columns they have.

[1] See, for example, [this page](http://pgsql.tapoueh.org/site/html/misc/hot.html).
