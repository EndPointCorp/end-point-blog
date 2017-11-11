---
author: Joshua Tolley
gh_issue_number: 814
tags: database, postgres, sql
title: Window functions in action
---



<a href="https://commons.wikimedia.org/wiki/File:Window_boxes,_Derry,_August_2009.JPG" imageanchor="1"><img border="0" src="/blog/2013/06/05/window-functions-in-action/image-0.jpeg" width="300"/></a>

*Image by Wikimedia user [Ardfern](https://commons.wikimedia.org/wiki/User:Ardfern)*

Yesterday I ran on to a nice practical application of a number of slightly unusual SQL features, in particular, window functions. PostgreSQL has had window functions for quite a while now (since version 8.4, in fact, the oldest version still officially supported), but even though they're part of the SQL standard, window functions aren't necessarily a feature people use every day. As a bonus, I also threw in some common table expressions (also known as CTEs, also a SQL standard feature), to help break up what could have been a more confusing, complex query.

A client of ours noticed a problem in some new code they were working on. It was possible for users to submit duplicate orders to the system in quick succession, by double-clicking or something similar. This was fixed in the code easily enough, but we needed to clean up the duplicate orders in the database. Which meant we had to find them. We defined a group of duplicates as all orders involving the same line items, with one of a set of possible status codes, created in an interval of less than five minutes by the same user.

This discussion of the time interval between two different records should immediately signal "window functions" (or possibly a self-join, but window functions are much easier in this case). A window function takes a set of rows and lets you chop them up into subsets, processing the subsets in various ways. In this case, we want to take all the rows in the orders table with a particular status value, group them by the customer who placed the order as well as by the items in the order, and then evaluate each of those groups.

As might be expected, the items associated with an order are in a different table from the orders themselves. There are probably several different ways I could have compared the items; I chose to accumulate all the items in an order into an array, and compare the resulting arrays (I imagine this would be awfully slow if orders had many different items attached to them, but it wasn't a problem in this instance). An item consists of its ID value, and an integer quantity; I created a composite type, so I could compare these values as an array.

```sql
CREATE TYPE order_item AS (
   item_id integer,
   quantity integer
);
```

Now I need a query that will gather all the items on an order into an array. I'll use the [array_agg()](http://www.postgresql.org/docs/9.1/static/functions-aggregate.html) aggregate to do that. While I'm at it, I'll also filter out order status codes I don't want. One important note here is that later, I'll be comparing the results of array_agg() with each other, and array element ordering will matter. So I need to sort the rows as they're being aggregated. Fortunately we've been able to do that easily since version 9.0, with ordered aggregates (NB! many of the features in use in this post are part of the SQL standard; ordered aggregates are a PostgreSQL-specific extension).

```sql
SELECT
    o.id, o.created_at, o.user_id,
    array_agg((item_id, quantity)::order_item ORDER BY item_id, quantity) AS order_items
FROM
    orders o
    JOIN order_items oi
        ON (o.id = oi.order_id)
WHERE o.status >= 200 AND o.status <= 400
GROUP BY o.id
```

The result, taken from a sample data set I created for demonstration purposes, is this:

```nohighlight
 id |         created_at         | user_id |        order_items         
----+----------------------------+---------+----------------------------
  4 | 2013-06-04 17:56:22.857817 |       3 | {"(2,3)"}
  5 | 2013-06-04 17:57:11.099472 |       1 | {"(1,11)","(2,1)","(3,2)"}
  1 | 2013-06-04 17:56:16.017938 |       1 | {"(1,10)","(2,1)","(3,2)"}
  2 | 2013-06-04 17:56:19.27393  |       1 | {"(1,10)","(2,1)","(3,2)"}
  3 | 2013-06-04 17:56:21.137858 |       2 | {"(1,1)"}
(5 rows)
```

Now I need to compare various rows in this list, and that's where window functions come in. A call to a window function looks like any other function call, except that it is followed by a "window definition", which describes the window of rows the function will operate on: how rows are grouped into windows, and optionally, how rows within a window are sorted. Here a query I used to get started.

```sql
SELECT
    id, created_at,
    first_value(created_at) OVER (PARTITION BY user_id ORDER BY created_at)
FROM orders
```

The *OVER* and subsequent parenthetical expression is the window clause. This one tells PostgreSQL to group all the orders by the user ID that created them, and sort them in ascending order of their creation time. In future iterations I'll need to partition by the items in the order as well, but we're keeping it simple for this query. The first_value() function is the actual window function, and returns the expression it is passed, evaluated in terms of the first row in the window. In this case the sort order is important; without it, there is no guarantee which of the window's rows is considered "first". There are lots of other window functions available, documented [here](http://www.postgresql.org/docs/9.2/static/functions-window.html).

It's time to start combining these queries together. For this, I like to use common table expressions, which essentially let me define a named view for purposes of just this query. My first such expression will gather the items associated with an order into an array. The second part of the query will use window functions to compare the results of the first part with each other.

```sql
WITH order_items_array AS (
    SELECT
        o.id, o.created_at, o.user_id,
        array_agg((item_id, quantity)::order_item ORDER BY item_id, quantity) AS order_items
    FROM
        orders o
        JOIN order_items oi
            ON (o.id = oi.order_id)
    WHERE o.status >= 200 AND o.status <= 400
    GROUP BY o.id
)
SELECT
    id, user_id, created_at,
    first_value(id) OVER user_order_partition AS first_id,
    first_value(created_at) OVER user_order_partition AS first_created
FROM order_items_array
WINDOW user_order_partition AS (PARTITION BY user_id, order_items ORDER BY created_at);
```

This gives these results:

```nohighlight
 id | user_id |         created_at         | first_id |       first_created        
----+---------+----------------------------+----------+----------------------------
  1 |       1 | 2013-06-04 17:56:16.017938 |        1 | 2013-06-04 17:56:16.017938
  2 |       1 | 2013-06-04 17:56:19.27393  |        1 | 2013-06-04 17:56:16.017938
  5 |       1 | 2013-06-04 17:57:11.099472 |        5 | 2013-06-04 17:57:11.099472
  3 |       2 | 2013-06-04 17:56:21.137858 |        3 | 2013-06-04 17:56:21.137858
  4 |       3 | 2013-06-04 17:56:22.857817 |        4 | 2013-06-04 17:56:22.857817
(5 rows)
```

This shows the order ID, user ID, and creation timestamp, as well as the ID and creation timestamp of the first order in the window each row belongs to. Note that in order to avoid having to retype the same long window definition twice, I used an alternate syntax whereby I created a named window definition, and referred to that name. Anyway, you can see that the first two rows have the same first_id value; this means they're duplicates, and we want to get rid of one of them. You'll have to trust me that that's the only duplicated order in my sample database; suffice it to say that these results are, in fact, correct. I'll decide (because it turns out to be easier this way) to keep the earliest of the duplicate orders, so from the results above, I can see that I want to remove order ID 2. It would be nice, though, to have a list of just the order IDs I need to remove without any other information. Even better, a list of SQL commands to run to remove them. Like this:

```sql
WITH order_items_array AS (
    SELECT
        o.id, o.created_at, o.user_id,
        array_agg((item_id, quantity)::order_item ORDER BY item_id, quantity) AS order_items
    FROM
        orders o
        JOIN order_items oi
            ON (o.id = oi.order_id)
    WHERE o.status >= 200 AND o.status <= 400
    GROUP BY o.id
), order_duplicates AS (
    SELECT
        id, user_id, created_at,
        first_value(id) OVER user_order_partition AS first_id,
        first_value(created_at) OVER user_order_partition AS first_created
    FROM order_items_array
    WINDOW user_order_partition AS (PARTITION BY user_id, order_items ORDER BY created_at)
)
    SELECT 'DELETE FROM orders WHERE id = ' || id || ';' FROM order_duplicates
    WHERE first_id != id;
```

...which returns this one result:

```nohighlight
 ?column?
----------------------------------
 DELETE FROM orders WHERE id = 2;
(1 row)
```

So by combining common table expressions, ordered aggregates, composite types, arrays, and window functions, we've successfully cleaned up this database. Until we find another application bug...


