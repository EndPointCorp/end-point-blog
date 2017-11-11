---
author: David Christensen
gh_issue_number: 330
tags: postgres
title: 'PostgreSQL: Dynamic SQL Function'
---



Sometimes when you're doing something in SQL, you find yourself doing something repetitive, which naturally lends itself to the desire to abstract out the boring parts.  This pattern is often prevalent when doing maintenance-related tasks such as creating or otherwise modifying DDL in a systematic kind of way.  If you've ever thought, "Hey, I could write a query to handle this," then you're probably looking for dynamic SQL.

The standard approach to using dynamic SQL in PostgreSQL is plpgsql's EXECUTE function, which takes a text argument as the SQL statement to execute.  One technique fairly well-known on the #postgresql IRC channel is to create a function which essentially wraps the EXECUTE statement, commonly known as exec().  Here is the definition of exec():

```sql
CREATE FUNCTION exec(text) RETURNS text AS $$ BEGIN EXECUTE $1; RETURN $1; END $$ LANGUAGE plpgsql;
```

Using exec() then takes the form of a SELECT query with the appropriately generated query to be executed passed as the sole argument.  We return the generated query text as an ease in auditing the actually executed results.  Some examples:

```sql
SELECT exec('CREATE TABLE partition_' || generate_series(1,100) || ' (LIKE original_table)');
SELECT exec('ALTER TABLE ' || quote_identifier(attrelid::regclass) || ' DROP COLUMN foo') FROM pg_attribute WHERE attname = 'foo';
```

Some notes about the exec() function: since the generated SQL statement is being run inside a function, it is not run in a top-level transaction, so some commands will not work, including CREATE/DROP DATABASE, ALTER TABLESPACE, VACUUM, etc.

Starting in PostgreSQL 9.0, the plpgsql language will be pre-installed in all new databases, which will make this recipe even easier to use.


