---
author: Josh Tolley
title: PL/LOLCODE and INLINE functions
github_issue_number: 215
tags:
- postgres
date: 2009-11-03
---



PostgreSQL 8.5 [recently learned](https://www.postgresql.org/message-id/20090922234343.B4246753FB7@cvs.postgresql.org) how to handle “inline functions” through the [DO statement](https://www.postgresql.org/docs/devel/static/sql-do.html). Further discussion is [here](https://www.depesz.com/2009/11/01/waiting-for-8-5-do/), but the basic idea is that within certain limitations, you can write ad hoc code in any language that supports it, without having to create a full-fledged function. One of those limitations is that you can’t actually return anything from your function. Another is that the language has to support an “inline handler”.

PostgreSQL procedural languages all have a language handler function, which gets called whenever you execute a stored procedure in that language. An inline handler is a separate function, somewhat slimmed down from the standard language handler. PostgreSQL gives the inline handler an argument containing, among other things, the source text passed in the DO block, which the inline handler simply has to parse and execute.

As of when the change was committed in PostgreSQL, only PL/pgSQL supported inline functions. Other languages may now support them; today I spent the surprisingly short time needed to add the capability to PL/LOLCODE. Here’s a particularly useless example:

```nohighlight
DO $$
HAI
 VISIBLE "This is a test of INLINE stuff"
KTHXBYE
$$ language pllolcode;
```

