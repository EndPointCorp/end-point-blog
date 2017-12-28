---
author: Jeff Boes
gh_issue_number: 1095
tags: database, optimization, sql
title: Temporary tables in SQL query optimization
---

SQL queries can get complex in a big hurry. If you are querying multiple tables, and in particular if your query involves operations like UNION and INTERSECT, then you can find yourself in a big, messy pile of SQL. Worse, that big pile will often run slowly, sometimes to the point where a web application times out!

I won’t inflict a real-world example on you; that would be cruel. So let’s look at a “toy” problem, keeping in mind that this won’t illustrate any time-savings, just the technique involved.

Here’s the original SQL:

```sql
SELECT p.* FROM products p
JOIN (SELECT * FROM inventory WHERE /* complex clause here */) i USING (sku)
UNION ALL
SELECT p.* FROM clearance_products p
JOIN (SELECT * FROM inventory WHERE /* complex clause here */) i USING (sku)
```

Bonus hint: using “UNION ALL“ instead of just “UNION” will allow the query processor to skip an unnecessary step here. “UNION ALL” says you know the rows on either side of the clause are unique. “UNION” means the results will be post-processed to remove duplicates. This might save you more than a smidgen of time, depending on how large the two sub-queries get.

Now, many times the query optimizer will just do the right thing here. But sometimes (cough, cough-MySQL), your database isn’t quite up to the task. So you have to shoulder the burden and help out. That’s where we can apply a temporary table.

Temporary tables are created for the length of the database session; that’s different than a transaction. For a web application, that’s usually (not always) the length of the request (i.e., from the time your web application opens a database connection, until it explicitly closes it, or until it returns control to the web server, usually by passing it a completed page). For a script, it’s a similar duration, e.g. until the script exits.

```sql
CREATE TEMPORARY TABLE cross_inventory AS
SELECT * FROM inventory WHERE /* complex clause here */;

CREATE INDEX cross_inv_sku ON cross_inventory(sku);
```

There’s no significant difference for our purposes between a “permanent” and a “temporary” table. However, you do have to keep in mind that these tables are created without indexes, so if your goal is to improve the speed of queries involving the data here, adding an index after creating the table is usually desirable.

With all this in place, now we can:

```sql
SELECT p.* FROM products p
JOIN cross_inventory i USING (sku)
UNION
SELECT p.* FROM clearance_products p
JOIN cross_inventory i USING (sku)
```

Sometimes your temporary table will be built up not by a straightforward “CREATE ... AS SELECT ...”, but by your application:

```sql
CREATE TEMPORARY TABLE tmp_inventory AS SELECT * FROM inventory WHERE false;
CREATE INDEX tmp_inv_sku ON tmp_inventory(sku);
```

And then within the application:

```c
# Pseudocode
while (more_data) {
  row = build_inv_record(more_data);
  sql_do('INSERT INTO tmp_inventory VALUES (?,?,...)', row);
}
```

Here, we are creating an empty “inventory” table template as a temporary table (“SELECT * FROM inventory WHERE false”), then adding rows to it from the application, and finally running our query. Note that in a practical application of this, it’s not likely to be a lot faster, because the individual INSERT statements will take time. But this approach may have some utility where the existing “inventory” table doesn’t have the data we want to JOIN against, or has the data, but not in a way we can easily filter.

I’ve used temporary tables (in a MySQL/Interchange/Perl environment) to speed up a query by a factor of two or more. It’s usually in those cases where you have a complex JOIN that appears in two or more parts of the query (again, usually a UNION). I’ve even had big-win situations where the same temporary table was used in two different queries during the same session.

A similar approach is the [Common Table Expression](https://www.postgresql.org/docs/9.4/static/queries-with.html) (CTE) found in PostgreSQL starting with version 8.4. This allows you to identify the rows you would be pouring into your temporary table as a named result-set, then reference it in your query. Our “toy” example would become:

```sql
WITH cross_inventory AS
(SELECT * FROM inventory WHERE /* complex clause here */)
SELECT p.* FROM products p
JOIN cross_inventory i USING (sku)
UNION
SELECT p.* FROM clearance_products p
JOIN cross_inventory i USING (sku)
```

I’ve not had an opportunity to use CTEs yet, and of course they aren’t available in MySQL, so the temporary-table technique will still have a lot of value for me in the foreseeable future.


