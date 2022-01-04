---
author: Jeff Boes
title: Hidden inefficiencies in Interchange searching
github_issue_number: 679
tags:
- interchange
date: 2012-08-13
---



A very common, somewhat primitive approach to Interchange searching uses an approach like this:

The search profile contains something along the lines of

```plain
  mv_search_type=db
  mv_search_file=products
  mv_column_op=rm
  mv_numeric=0
  mv_search_field=category

[search-region]
  [item-list]
    [item-field description]
  [/item-list]
[/search-region]
```

In other words, we search the products table for rows whose column “category” matches an expression (with a single query), and we list all the matches (description only). However, this can be inefficient depending on your database implementation: the item-field tag *issues a query* every time it’s encountered, which you can see if you “tail” your database log. If your item-list contains many different columns from the search result, you’ll end up issuing *many* such queries:

```plain
[item-list]
    [item-field description], [item-field weight], [item-field color],
    [item-field size], [item field ...]
  ...
```

resulting in:

```sql
SELECT description FROM products WHERE sku='ABC123'
SELECT weight FROM products WHERE sku='ABC123'
SELECT color FROM products WHERE sku='ABC123'
SELECT size FROM products WHERE sku='ABC123'
...
```

(Now, some databases are smart enough to cache query results, but some aren’t, so avoiding this extra work is probably worth your trouble even on a “smart” database, in case your Interchange application gets moved to a “dumb” database sometime in the future.)

Fortunately, it’s easy to correct:

```plain
mv_return_fields=*
```

and then

```plain
...
    [item-param description]
...
```

in place of “item-field”.


