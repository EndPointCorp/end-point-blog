---
author: David Christensen
gh_issue_number: 270
tags: postgres, tips
title: 'PostgreSQL tip: dump objects into a new schema'
---



Sometimes the need arises to export a PostgreSQL database and put its contents into its own schema; say you’ve been busy developing things in the public schema. Sometime people suggest manipulating the pg_dump output either manually or using a tool such as sed or perl to explicitly schema-qualify all table objects, etc, but this is error-prone depending on your table names, and can be more trouble than its worth.

One trick that may work for you if your current database is not in use by anyone else is to rename the default public schema to your desired schema name before dumping, and then optionally changing it back to public afterward. This has the benefit that *all* objects will be properly dumped in the new schema (sequences, etc) and not just tables, plus you don’t have to worry about trying to parse SQL with regexes to modify this explicitly.

```bash
$ psql -c "ALTER SCHEMA public RENAME new_name"
$ pg_dump --schema=new_name > new_name_dump.sql
$ psql -c "ALTER SCHEMA new_name RENAME public"
$ # load new_name_dump.sql elsewhere
```

Cheers!


