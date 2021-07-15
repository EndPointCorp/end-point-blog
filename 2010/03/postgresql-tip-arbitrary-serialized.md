---
author: David Christensen
title: 'PostgreSQL tip: arbitrary serialized rows'
github_issue_number: 274
tags:
- postgres
- tips
date: 2010-03-08
---



Sometimes when using PostgreSQL, you want to deal with a record in its serialized form. If you’re dealing with a specific table, you can accomplish this using the table name itself:

```sql
psql # CREATE TABLE foo (bar text, baz int);
CREATE TABLE

psql # INSERT INTO foo VALUES ('test 1', 1), ('test 2', 2);
INSERT 0 2

psql # SELECT foo FROM foo;
     foo      
--------------
 ("test 1",1)
 ("test 2",2)
(2 rows)
```

This works fine for defined tables, but how to go about this for arbitrary SELECTs? The answer is simple: wrap in a subselect and alias as so:

```sql
psql # SELECT q FROM (SELECT 1, 2) q;
   q   
-------
 (1,2)
(1 row)
```

