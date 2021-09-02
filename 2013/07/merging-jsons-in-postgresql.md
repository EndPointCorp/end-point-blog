---
author: Szymon Lipiński
title: Merging JSONs in PostgreSQL
github_issue_number: 840
tags:
- postgres
- python
date: 2013-07-29
---

PostgreSQL’s JSON support is great, however there is one thing missing, and it will be missing in the next PostgreSQL release. It is not too easy to manipulate the values stored in such a JSON field. Fortunately there is an easy way to do anything you want, you can use some external programming language.

### Merging JSONs

Sometimes you need to update one JSON with values from another. Or you just need to change one field in a JSON value. There is no easy way to do it in PostgreSQL, but with the help of external language, it seems trivial.

Let’s use simple JSONs:

```sql
WITH j AS (
  SELECT
    '{"a":42, "b":"test"}'::JSON a,
    '{"a":1764, "x":"test x"}'::JSON b
)
SELECT a, b
FROM j;
```
```sql
a           |            b
-------------------------------------------------------
 {"a":42, “b”:"test"} | {"a":1764, “x”:“test x”}<p></p>
```

Let’s assume I have value a stored in a table, and I want to update it with values from b. So I want to do something like:

```sql
UPDATE data SET j = something(j, b) WHERE id = 10;
```

The question is: how to merge those JSONs.

### Merging

For merging I’ve written a simple plpython function:

```sql
CREATE FUNCTION merge_json(left JSON, right JSON)
RETURNS JSON AS $$
  import simplejson as json
  l, r = json.loads(left), json.loads(right)
  l.update(r)
  j = json.dumps(l)
  return j
$$ LANGUAGE PLPYTHONU;
```

This function merges the “left” argument with the “right” overwriting values if they exist.

This way if we use this function for the above JSONs, then (using the pretty print json function from previous post):

```sql
WITH j AS (
  SELECT
    '{"a":42, "b":"test"}'::JSON a,
    '{"a":1764, "x":"test x"}'::JSON b
)
SELECT
  pp_json(a) as "a",
  pp_json(b) as "b",
  pp_json(merge_json(a, b)) as "a+b"
FROM j;

        a        |         b         |        a + b
-----------------+-------------------+-------------------
 {              +| {                +| {                +
     "a": 42,   +|     "a": 1764,   +|     "a": 1764,   +
     "b": "test"+|     "x": "test x"+|     "b": "test", +
 }               | }                 |     "x": "test x"+
                 |                   | }
```

So it is pretty easy to manipulate JSON using plpython, if standard PostgreSQL’s operators and functions are not sufficient, however I’m sure that in the release after 9.3 there will be much wider JSON support, so hopefuly the functions like the above won’t be needed.
