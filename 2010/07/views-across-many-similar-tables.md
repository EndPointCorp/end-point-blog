---
author: Jeff Boes
title: Views across many similar tables
github_issue_number: 325
tags:
- database
- postgres
date: 2010-07-13
---

An application I’m working on has a host of (a dozen or so) status tables, each containing various rows that reflect the state of associated rows in other tables. For instance:

```sql
Table "public.inventory"
...
status_code      | character varying(50)       | not null

Table "public.inventory_statuses"
code          | character varying(50)       | not null
display_label | character varying(70)       | not null

SELECT * FROM inventory_statuses;

  code    | display_label
-----------+---------------
ordered   | Ordered
shipped   | Shipped
returned  | Returned
repaired  | Repaired
```
etc.

Several of the codes are common to several tables. For instance, “void” is a status that occurs in seven tables. The application cares about this; there are code-level triggers that will respond to a change of status to “void” in one table, and pass that information along to another table higher up the chain.

Since I wasn’t present at the birth of the system (nor do I have unlimited memory to keep 180+ codes in my head), I needed a way to answer the question, “In which table(s) does status ‘foo’ occur?” This was made rather easier by attention to detail early on: each of the status tables was named “*_statuses”; each primary key was named “code”; and each human-readable description field was named “display_label”. I wrote a Pl/PgSQL function to create a view spanning all the tables. (I could have just created the SQL by hand, but I wanted a way to reproduce this effort later, if tables are added, dropped, or modified.)

```sql
CREATE FUNCTION create_all_statuses()
RETURNS VOID
LANGUAGE 'plpgsql'
AS $$
DECLARE
   stmt TEXT;
   tbl RECORD;
BEGIN
   stmt := '';
   FOR tbl IN EXECUTE $SQL$
SELECT DISTINCT table_name
FROM information_schema.columns a
JOIN information_schema.columns b
USING (table_name)
JOIN information_schema.tables t
USING (table_name)
WHERE a.column_name = 'code'
AND   b.column_name = 'display_label'
AND   table_name ~ '_statuses$'
AND   t.table_type  = 'BASE TABLE'
$SQL$
   LOOP
       IF (LENGTH(stmt) > 0)
       THEN
           stmt := stmt || ' UNION ';
       END IF;
       stmt := stmt || 'SELECT code, display_label, ' ||
           quote_literal(tbl.table_name) ||
           ' AS table_name FROM ' ||
           quote_ident(tbl.table_name);
   END LOOP;

   EXECUTE 'CREATE VIEW all_statuses AS ' || stmt;
   RETURN;
END;
$$;
```

Now it’s easy to answer the question:

```sql
select * from all_statuses where code = 'void';

code | display_label |              table_name
------+---------------+--------------------------------------
void | Void          | inventory_statuses
void | Void          | parcel_statuses
void | Void          | pick_list_statuses
```
etc.

If your database uses boilerplate columns such as “last_modified” or “date_created” to record timestamps on rows, you could use similar logic to create a view that would tell you which tables were the most recently modified.
