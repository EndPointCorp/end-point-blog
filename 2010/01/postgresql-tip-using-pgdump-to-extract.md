---
author: David Christensen
title: 'PostgreSQL tip: using pg_dump to extract a single function'
github_issue_number: 260
tags:
- postgres
date: 2010-01-31
---



A common task that comes up in PostgreSQL is the need to dump/edit a specific function. While ideally, you’re using DDL files and version control (hello, git!) to manage your schema, you don’t always have the luxury of working in such a controlled environment. Recent versions of psql have the \ef command to edit a function from within your favorite editor, but this is available from version 8.4 onward only.

An alternate approach is to use the following invocation:

```bash
  pg_dump -Fc -s | pg_restore -P 'funcname(args)'
```

The -s flag is the short form of --schema-only; i.e., we don’t care about wasting time/space with the data. -P tells pg_restore to extract the function with the following signature.

As always, there are some caveats: the function name must be spelled out explicitly using the full types as they occur in the dump’s custom format (i.e., you must use ‘foo_func(integer)’ instead of ‘foo_func(int)’). You can always see a list of all of the available functions by using the command:

```bash
  pg_dump -Fc -s | pg_restore -l | grep FUNCTION
```

