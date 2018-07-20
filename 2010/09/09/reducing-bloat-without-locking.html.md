---
author: Josh Tolley
gh_issue_number: 347
tags: postgres
title: Reducing bloat without locking
---



It’s not altogether uncommon to find a database where someone has turned off vacuuming, for a table or for the entire database. I assume people do this thinking that vacuuming is taking too much processor time or disk IO or something, and needs to be turned off. While this fixes the problem very temporarily, in the long run it causes tables to grow enormous and performance to take a dive. There are two ways to fix the problem: moving rows around to consolidate them, or rewriting the table completely. Prior to PostgreSQL 9.0, VACUUM FULL did the former; in 9.0 and above, it does the latter. CLUSTER is another suitable alternative, which also does the latter. Unfortunately all these methods require heavy table locking.

Recently I’ve been experimenting with an alternative method—​sort of a VACUUM FULL Lite. Vanilla VACUUM **can** reduce table size when the pages at the end of a table are completely empty. The trick is to empty those pages of live data. You do that by paying close attention to the table’s *ctid* column:

```nohighlight
5432 josh@josh# \d foo
      Table "public.foo"
 Column |  Type   | Modifiers 
--------+---------+-----------
 a      | integer | not null
 b      | integer | 
Indexes:
    "foo_pkey" PRIMARY KEY, btree (a)

5432 josh@josh# select ctid, * from foo;
 ctid  | a | b 
-------+---+---
 (0,1) | 1 | 1
 (0,2) | 2 | 2
(2 rows)
```

The *ctid* is one of several hidden columns found in each PostgreSQL table. It shows up in query results only if you explicitly ask for it, and tells you two values: a page number, and a tuple number. Pages are numbered sequentially from zero, starting with the first page in the relation’s first file, and ending with the last page in its last file. Tuple numbers refer to entries within each page, and are numbered sequentially starting from one. When I update a row, the row’s ctid changes, because the update creates a new version of the row and leaves the old version behind (see [this page](http://www.postgresql.org/docs/current/static/mvcc.html) for explanation of that behavior).

```nohighlight
5432 josh@josh# update foo set a = 3 where a = 2;
UPDATE 1
5432 josh@josh*# select ctid, * from foo;
 ctid  | a | b 
-------+---+---
 (0,1) | 1 | 1
 (0,3) | 3 | 2
(2 rows)
```

Note the changed ctid for the second row. If I vacuum this table now, I’ll see it remove one dead row version, from both the table and its associated index:

```nohighlight
5432 josh@josh# VACUUM verbose foo;
INFO:  vacuuming "public.foo"
INFO:  scanned index "foo_pkey" to remove 1 row versions
DETAIL:  CPU 0.00s/0.00u sec elapsed 0.00 sec.
INFO:  "foo": removed 1 row versions in 1 pages
DETAIL:  CPU 0.00s/0.00u sec elapsed 0.00 sec.
INFO:  index "foo_pkey" now contains 2 row versions in 2 pages
DETAIL:  1 index row versions were removed.
0 index pages have been deleted, 0 are currently reusable.
CPU 0.00s/0.00u sec elapsed 0.00 sec.
INFO:  "foo": found 1 removable, 2 nonremovable row versions in 1 pages
DETAIL:  0 dead row versions cannot be removed yet.
There were 0 unused item pointers.
1 pages contain useful free space.
0 pages are entirely empty.
CPU 0.00s/0.00u sec elapsed 0.00 sec.
VACUUM
```

So given these basics, how can I make tables smaller? Let’s build a bloated table:

```nohighlight
5432 josh@josh# truncate foo;
TRUNCATE TABLE
5432 josh@josh*# insert into foo select generate_series(1, 1000);
INSERT 0 1000
5432 josh@josh*# delete from foo where a % 2 = 0;
DELETE 500
5432 josh@josh*# select max(ctid) from foo;
   max   
---------
 (3,234)
(1 row)
5432 josh@josh# vacuum verbose foo;
INFO:  vacuuming "public.foo"
INFO:  scanned index "foo_pkey" to remove 500 row versions
DETAIL:  CPU 0.00s/0.00u sec elapsed 0.00 sec.
INFO:  "foo": removed 500 row versions in 4 pages
...
```

I’ve filled the table with 1000 rows, and then deleted every other row. The last tuple is on the fourth page (remember they’re numbered starting with zero), but since half the table is empty space, I can probably squish it into three or maybe just two pages. I’ll start by moving the tuples on the last page off to another page, by updating them:

```sql
5432 josh@josh# begin;
BEGIN
5432 josh@josh*# update foo set a = a where ctid >= '(3,0)';
UPDATE 117
5432 josh@josh*# update foo set a = a where ctid >= '(3,0)';
UPDATE 117
5432 josh@josh*# update foo set a = a where ctid >= '(3,0)';
UPDATE 21
5432 josh@josh*# update foo set a = a where ctid >= '(3,0)';
UPDATE 0
5432 josh@josh*# commit;
COMMIT
```

Here I’m not changing the row at all, but the tuples are moving around into dead space earlier in the table; this is apparent because the number of rows affected decreases. For the first update or two, there’s room enough on the page to store all the new rows, but after a few updates they have to start moving to new pages. Eventually the row count goes to zero, meaning there are no rows on or after page #3, so vacuum can truncate that page:

```nohighlight
5432 josh@josh# vacuum verbose foo;
INFO:  vacuuming "public.foo"
...

INFO:  "foo": truncated 4 to 3 pages
```

It’s important to note that I did this all within a transaction. If I hadn’t, there’s a possibility that vacuum would have reclaimed some of the dead space made by the updates, so instead of moving to different pages, the tuples would have moved back and forth within the same page.

There remains one problem: I can’t remove index bloat, and in fact, all this tuple-moving causes more index bloat. I can’t fix that completely, but in PostgreSQL 8.3 and later I can avoid creating too much new bloat by updating an unindexed column instead of an indexed one. In PostgreSQL 8.3 and later, the heap-only tuples (HOT) feature avoids modifying indexes if:

1. the update touches only unindexed columns, and
1. there’s sufficient free space available for the tuple to stay on the same page.

Despite the index bloat caveat, this can be a useful technique to slim down particularly bloated tables without VACUUM FULL and its associated locking.


