---
author: Szymon Lipiński
title: PostgreSQL search_path Behaviour
github_issue_number: 724
tags:
- postgres
date: 2012-11-15
---

PostgreSQL has a great feature: schemas. So you have one database with multiple schemas. This is a really great solution for the data separation between different applications. Each of them can use different schema, and they also can share some schemas between them.

I have noticed that some programmers tend to name the working schema as their user name. This is not a bad idea, however once I had a strange behaviour with such a solution.

I'm using user name szymon in the database szymon.

First let's create a simple table and add some values. I will add one row with information about the table name.

```sql
# CREATE TABLE a ( t TEXT );
# INSERT INTO a(t) VALUES ('This is table a');
```

Let's check if the row is where it should be:

```sql
# SELECT t FROM a;

        t
-----------------
 This is table a
(1 row)
```

Now let's create another schema, name it like my user's name.

```sql
# CREATE SCHEMA szymon;
```

Let's now create table a in the new schema.

```sql
# CREATE TABLE szymon.a ( t TEXT );
```

So there are two tables a in different schemas.

```sql
# SELECT t FROM pg_tables WHERE tablename = 'a';

 schemaname | tablename | tableowner | tablespace | hasindexes | hasrules | hastriggers
------------+-----------+------------+------------+------------+----------+-------------
 public     | a         | szymon     | \N         | f          | f        | f
 szymon     | a         | szymon     | \N         | f          | f        | f
(2 rows)
```

I will just add a row similar to the previous one.

```sql
# INSERT INTO szymon.a(t) VALUES ('This is table szymon.a');
```

Let's check the data in the table "szymon.a".

```sql
# SELECT t FROM szymon.a;

           t
------------------------
 This is table szymon.a
(1 row)
```

OK, now I have all the data prepared for showing the quite interesting behaviour. As you might see in the above queries, selecting table "a" when there is only one schema works. What's more, selecting "szymon.a" works as well.

What will hapeen when I get data from the table "a"?

```sql
# SELECT t FROM a;

           t
------------------------
 This is table szymon.a
(1 row)
```

Suddenly PostgreSQL selects data from other table than at the beginning. The reason of this is the schema search mechanism. There is a PostgreSQL environment variable "search_path". If you set the value of this variable to "x,a,public" then PostgreSQL will look for all the tables, types and function names in the schema "x". If there is no such table in this schema, then it will look for this table in the next schema, which is "a" in this example.

What's the default value of the search_path variable? You can check the current value of this variable with the following query:

```sql
# show search_path;

  search_path
----------------
 "$user",public
(1 row)
```

The default search path makes PostgreSQL search first in the schema named exactly as the user name you used for logging into database. If the user name is different from the schema names, or there is no table "szymon.a" then there would be used the "public.a" table.

The problem is even more tricky, even using simple EXPLAIN doesn't help, as it shows only table name omitting the schema name. So the plan for this query looks exactly the same, regardless of the schema used:

```sql
# EXPLAIN SELECT * FROM a;
                      QUERY PLAN
------------------------------------------------------
 Seq Scan on a  (cost=0.00..1.01 rows=1 width=32)
(1 row)
```

For plan with more information you should use EXPLAIN VERBOSE, then you will have the plan with schema name, so it will be easier to spot the usage of different schema:

```sql
# EXPLAIN VERBOSE SELECT * FROM a;
                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on szymon.a  (cost=0.00..1.01 rows=1 width=32)
   Output: t
(2 rows)
```
