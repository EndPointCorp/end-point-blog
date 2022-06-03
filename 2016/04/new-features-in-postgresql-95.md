---
author: Szymon Lipiński
title: New Features in PostgreSQL 9.5
github_issue_number: 1217
tags:
- postgres
date: 2016-04-07
---

The new PostgreSQL 9.5 release has a bunch of great features. I describe below the ones I find most interesting.

### Upsert

UPSERT is simply a combination of INSERT and UPDATE. This works like this: if a row exists, then update it, if it doesn’t exist, create it.

Before Postgres 9.5 when I wanted to insert or update a row, I had to write this:

```sql
INSERT INTO test(username, login)
SELECT 'hey', 'ho ho ho'
WHERE NOT EXISTS (SELECT 42 FROM test WHERE username='hey');

UPDATE test SET login='ho ho ho' WHERE username='hey' AND login <> 'ho ho ho';
```

Which was a little bit problematic. You need to make two queries, and both can have quite complicated WHERE clauses.

In PostgreSQL 9.5 there is much simpler version:

```sql
INSERT INTO test(username, login) VALUES ('hey', 'ho ho ho')
ON CONFLICT (username)
DO UPDATE SET login='ho ho ho';
```

The only requirement is that there should be a UNIQUE constraint on a column which should fail while inserting a row.

The version above makes the UPDATE when the INSERT fails. There is also another form of the UPSERT query, which I used in [this blog post](/blog/2016/03/loading-json-files-into-postgresql-95/).
You can just ignore the INSERT failure:

```sql
INSERT INTO test(username, login) VALUES ('hey', 'ho ho ho')
ON CONFLICT (username)
DO NOTHING;
```

### Switching Tables to Logged and Unlogged

PostgreSQL keeps a transaction write ahead log, which helps restore the
  database after a crash, and is used in replication, but it comes with some
  overhead, as additional information must be stored on disk.

In PostgreSQL 9.5 you can simply switch a table from logged to unlogged. The unlogged version can be much faster when filling it with data, processing it etc. However at the end of such operations it might be good to make it a normal logged table. Now it is simple:

```sql
ALTER TABLE barfoo SET LOGGED;
```

### JSONB Operators and Functions

This is the binary JSON type, and these new functions allow us to perform
  more operations without having to convert our data first to the slower,
  non-binary JSON alternative.

Now you can remove a key from a JSONB value:

```sql
SELECT '{"a": 1, "b": 2, "c": 3}'::jsonb || '{"x": 1, "y": 2, "c": 42}'::jsonb;

     ?column?
──────────────────
 {"b": 2, "c": 3}
```

And merge JSONB values (the last value’s keys overwrite the first’s one):

```sql
SELECT '{"a": 1, "b": 2, "c": 3}'::jsonb || '{"x": 1, "y": 2, "c": 42}'::jsonb;

                 ?column?
───────────────────────────────────────────
 {"a": 1, "b": 2, "c": 42, "x": 1, "y": 2}
```

And we have the nice jsonb_pretty() function which instead of this:

```sql
SELECT jsonb_set('{"name": "James", "contact": {"phone": "01234 567890",
                   "fax": "01987 543210"}}'::jsonb,
                   '{contact,phone}', '"07900 112233"'::jsonb);

                                   jsonb_set
────────────────────────────────────────────────────────────────────────────────
 {"name": "James", "contact": {"fax": "01987 543210", "phone": "07900 112233"}}
```

prints this:

```sql
SELECT jsonb_pretty(jsonb_set('{"name": "James", "contact": {"phone": "01234 567890",
                   "fax": "01987 543210"}}'::jsonb,
                   '{contact,phone}', '"07900 112233"'::jsonb));

         jsonb_pretty
─────────────────────────────────
  {                              ↵
      "name": "James",           ↵
      "contact": {               ↵
          "fax": "01987 543210", ↵
          "phone": "07900 112233"↵
      }                          ↵
  }
```

### More Information

There are more nice features in the new PostgreSQL 9.5. You can read the full list at https://wiki.postgresql.org/wiki/What's*new*in*PostgreSQL*9.5
