---
author: Greg Sabino Mullane
gh_issue_number: 80
tags: postgres
title: Why is my function slow?
---

I often hear people ask “Why is my function so slow? The query runs fast when I do it from the command line!” The answer lies in the fact that a function’s query plans are cached by Postgres, and the plan derived by the function is not always the same as shown by an EXPLAIN from the command line. To illustrate the difference, I downloaded the [pagila](http://pgfoundry.org/frs/?group_id=1000150&release_id=998) test database. To show the problem, we’ll need a table with a lot of rows, so I used the largest table, rental, which has the following structure:

```
pagila# \d rental
                       Table "public.rental"
    Column    |   Type     |             Modifiers
--------------+-----------------------------+--------------------------------
 rental_id    | integer    | not null default nextval('rental_rental_id_seq')
 rental_date  | timestamp  | not null
 inventory_id | integer    | not null
 customer_id  | smallint   | not null
 return_date  | timestamp  |
 staff_id     | smallint   | not null
 last_update  | timestamp  | not null default now()
Indexes:
    "rental_pkey" PRIMARY KEY (rental_id)
    "idx_unq_rental" UNIQUE (rental_date, inventory_id, customer_id)
    "idx_fk_inventory_id" (inventory_id)
```

It only had 16044 rows, however, not quite enough to demonstrate the difference we need. So let’s add a few more rows. The unique index means any new rows will have to vary in one of the three columns: rental_date, inventory_id, or customer_id. The easiest to change is the rental date. By changing just that one item and adding the table back into itself, we can quickly and exponentially increase the size of the table like so:

```
INSERT INTO rental(rental_date, inventory_id, customer_id, staff_id)
  SELECT rental_date + '1 minute'::interval, inventory_id, customer_id, staff_id
  FROM rental;
```

I then ran the same query again, but with ‘2 minutes’, ‘4 minutes’, ‘8 minutes’, and finally ‘16 minutes’. At this point, the table had 513,408 rows, which is enough for this example. I also ran an ANALYZE on the table in question (this should always be the first step when trying to figure out why things are going slower than expected). The next step is to write a simple function that accesses the table by counting how many rentals have occurred since a certain date:

```
DROP FUNCTION IF EXISTS count_rentals_since_date(date);

CREATE FUNCTION count_rentals_since_date(date)
RETURNS BIGINT
LANGUAGE plpgsql
AS $body$
  DECLARE
    tcount INTEGER;
  BEGIN
    SELECT INTO tcount
      COUNT(*) FROM rental WHERE rental_date > $1;
  RETURN tcount;
  END;
$body$;
```

Simple enough, right? Let’s test out a few dates and see how long each one takes:

```
pagila# \timing

pagila# select count_rentals_since_date('2005-08-01');
 count_rentals_since_date
--------------------------
                   187901
Time: 242.923 ms

pagila# select count_rentals_since_date('2005-09-01');
 count_rentals_since_date
--------------------------
                     5824
Time: 224.718 ms
```

*Note: all of the queries in this article were run multiple times first to reduce any caching effects.* Those times appear to be about the same, but I know from the distribution of the data that the first query will not hit the index, but the second one should. Thus, when we try and emulate what the function is doing on the command line, the first effort often looks like this:

```
pagila# explain analyze select count(*) from rental where rental_date > '2005-08-01';
                     QUERY PLAN
--------------------------------------------------------------------------------
 Aggregate (actual time=579.543..579.544)
   Seq Scan on rental (actual time=4.462..403.122 rows=187901)
     Filter: (rental_date > '2005-08-01 00:00:00')
 Total runtime: 579.603 ms

pagila# explain analyze select count(*) from rental where rental_date > '2005-09-01';

                     QUERY PLAN
--------------------------------------------------------------------------------
 Aggregate  (actual time=35.133..35.133)
   Bitmap Heap Scan on rental (actual time=1.852..30.451)
     Recheck Cond: (rental_date > '2005-09-01 00:00:00')
     -> Bitmap Index Scan on idx_unq_rental (actual time=1.582..1.582 rows=5824)
         Index Cond: (rental_date > '2005-09-01 00:00:00')
 Total runtime: 35.204 ms

```

Wow, that’s a huge difference! The second query is hitting the index and using some bitmap magic to pull back the rows in a blistering time of 35 milliseconds. However, the same date, using the function, takes 224 ms—​over six times as slow! What’s going on? Obviously, the function is *not* using the index, regardless of which date is passed in. This is because the function cannot know ahead of time what the dates are going to be, but caches a single query plan. In this case, it is caching the ‘wrong’ plan.

The correct way to see queries as a function sees them is to use prepared statements. This caches the query plan into memory and simply passes a value to the already prepared plan, just like a function does. The process looks like this:

```
pagila# PREPARE foobar(DATE) AS SELECT count(*) FROM rental WHERE rental_date > $1;
PREPARE

pagila# EXPLAIN ANALYZE EXECUTE foobar('2005-08-01');
                QUERY PLAN
--------------------------------------------------------------
 Aggregate  (actual time=535.708..535.709 rows=1)
   ->  Seq Scan on rental (actual time=4.638..364.351 rows=187901)
         Filter: (rental_date > $1)
 Total runtime: 535.781 ms

pagila# EXPLAIN ANALYZE EXECUTE foobar('2005-09-01');
                QUERY PLAN
--------------------------------------------------------------
 Aggregate  (actual time=280.374..280.375 rows=1)
   ->  Seq Scan on rental  (actual time=5.936..274.911 rows=5824)
         Filter: (rental_date > $1)
 Total runtime: 280.448 ms
```

These numbers match the function, so we can now see the reason the function is running as slow as it does: it is sticking to the “Seq Scan” plan. What we want to do is to have it use the index when the given date argument is such that the index would be faster. Functions cannot have more than one cached plan, so what we need to do is dynamically construct the SQL statement every time the function is called. This costs us a small bit of overhead versus having a cached query plan, but in this particular case (and you’ll find in nearly all cases), the overhead lost is more than compensated for by the faster final plan. Making a dynamic query in plpgsql is a little more involved than the previous function, but it becomes old hat after you’ve written a few. Here’s the same function, but with a dynamically generated SQL statement inside of it:

```
DROP FUNCTION IF EXISTS count_rentals_since_date_dynamic(date);

CREATE FUNCTION count_rentals_since_date_dynamic(date)
RETURNS BIGINT
LANGUAGE plpgsql
AS $body$
  DECLARE
    myst TEXT;
    myrec RECORD;
  BEGIN
    myst = 'SELECT count(*) FROM rental WHERE rental_date > ' || quote_literal($1);
    FOR myrec IN EXECUTE myst LOOP
      RETURN myrec.count;
    END LOOP;
  END;
$body$;
```

Note that we use the quote_literal function to take care of any quoting we may need. Also notice that we need to enter into a loop to run the query and then parse the output, but we can simply return right away, as we only care about the output from the first (and only) returned row. Let’s see how this new function performs compared to the old one:

```
pagila# \timing

pagila# select count_rentals_since_date_dynamic('2005-08-01');
 count_rentals_since_date_dynamic
----------------------------------
                           187901
Time: 255.022 ms

pagila# select count_rentals_since_date('2005-08-01');
 count_rentals_since_date
--------------------------
                   187901
Time: 249.724 ms

pagila# select count_rentals_since_date('2005-09-01');
 count_rentals_since_date
--------------------------
                     5824
Time: 228.224 ms

pagila# select count_rentals_since_date_dynamic('2005-09-01');
 count_rentals_since_date_dynamic
----------------------------------
                             5824
Time: 6.618 ms
```

That’s more like it! Problem solved. The function is running much faster now, as it can hit the index. The take-home lessons here are:

1. Always make sure the tables you are using have been analyzed.
1. Emulate the queries inside a function by using PREPARE + EXPLAIN EXECUTE, not EXPLAIN.
1. Use dynamic SQL inside a function to prevent unwanted query plan caching.
