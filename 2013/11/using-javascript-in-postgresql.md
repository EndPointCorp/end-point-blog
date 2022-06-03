---
author: Szymon Lipiński
title: Using JavaScript in PostgreSQL
github_issue_number: 891
tags:
- javascript
- postgres
date: 2013-11-22
---

This time I will describe two things: installing a new extension using pgxn and using JavaScript for writing a PostgreSQL stored procedure.

The last time I was describing a couple of nice features of the incoming PostgreSQL 9.3, I wrote about [merging JSONs in Postgres](/blog/2013/07/merging-jsons-in-postgresql/) using a stored procedure written in Python. In one of the comments there was a suggestion that I should try using JavaScript for that, as JSON is much more native there.

So let’s try JavaScript with PostgreSQL.

### Installing PL/V8

PL/V8 is a PostgreSQL procedural language powered by V8 JavaScript Engine. This way we can have JavaScript backed, something funny which could be used to create something like NoSQL database, with JavaScript procedures and storing JSON.

To have this procedural language, you need to install it as a separate extension. This can be done with system packages, if your system provides them. For Ubuntu, which I use, there are packages ready, however I use PostgreSQL compiled from source, and I keep it in my local directory, so I had to install it in a little bit different way.

I keep my PostgreSQL in ~/postgres directory. The ~/postgres/bin directory is added to environmnent $PATH variable. It is important, as the further steps will use pg_config program, which prints lots of information about the PostgreSQL installation.

The code for PL/V8 can be found in [the project’s PGXN page](https://pgxn.org/dist/plv8/). You can of course download source, and install it. However there is much simpler way to do it. PGXN provides a tool for managing extensions stored there.

To get the client for pgxn, it’s enough to write:

```bash
$ pip install pgxnclient
```

To install PL/V8 you also need to have the developer library for the V8 engine:

```bash
$ sudo apt-get install libv8-dev
$ pgxn install plv8
```

Now you can install the extension with a simple command:

```bash
$ pgxn install plv8
```

This should download, compile and copy all the files into a proper directory described by the pg_config program.

### Use PL/V8

For each database where you want to use this extension, you need to create it:

```sql
plv8=# CREATE EXTENSION plv8;
CREATE EXTENSION
```

### Write Procedure in JavaScript

This is an example I used in the previous post:

```sql
WITH j AS (
  SELECT
    '{"a":42, "b":"test"}'::JSON a,
    '{"a":1764, "x":"test x"}'::JSON b
)
SELECT a, b
FROM j;
          a           |            b
----------------------+--------------------------
 {"a":42, "b":"test"} | {"a":1764, "x":"test x"}
```

The implementation of the merging function in JavaScript can look like this one:

```sql
CREATE OR REPLACE FUNCTION merge_json_v8(left JSON, right JSON)
RETURNS JSON AS $$
  for (var key in right) { left[key] = right[key]; }
  return left;
$$ LANGUAGE plv8;
```

You can use it exactly like the previous Python version:

```sql
WITH j AS (
  SELECT
    '{"a":42, "b":"test"}'::JSON a,
    '{"a":1764, "x":"test x"}'::JSON b
)
SELECT
  a,
  b,
  merge_json_v8(a, b)
FROM j;
```
