---
author: Greg Sabino Mullane
gh_issue_number: 302
tags: database, postgres, testing
title: PostgreSQL template databases to restore to a known state
---

<a href="/blog/2010/05/12/postgresql-template-databases-to/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5470469048527692914" src="/blog/2010/05/12/postgresql-template-databases-to/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 320px; height: 200px;"/></a>

Someone asked on the mailing lists recently about restoring a PostgreSQL database to a known state for testing purposes. How to do this depends a little bit on what one means by "known state", so let’s explore a few scenarios and their solutions.

First, let’s assume you have a Postgres [cluster](https://www.postgresql.org/docs/current/static/creating-cluster.html) with one or more databases that you create for developers or QA people to mess around with. At some point, you want to “reset” the database to the pristine state it was in before people starting making changes to it.

The first situation is that people have made both DDL changes (such as ALTER TABLE ... ADD COLUMN) and DML changes (such as INSERT/UPDATE/DELETE). In this case, what you want is a complete snapshot of the database at a point in time, which you can then restore from. The easiest way to do this is to use the TEMPLATE feature of the CREATE DATABASE command.

Every time you run CREATE DATABASE, it uses an already existing database as the [“template”](https://www.postgresql.org/docs/current/static/manage-ag-templatedbs.html). Basically, it creates a copy of the template database you specify. If no template is specified, it uses “template1” by default, so that these two commands are equivalent:

```sql
CREATE DATABASE foobar;
CREATE DATABASE foobar TEMPLATE template1;
```

Thus, if we want to create a complete copy of an existing database, we simply use it as a template for our copy:

```sql
CREATE DATABASE mydb_template TEMPLATE mydb;
```

Thus, when we want to restore the **mydb** database to the exact same state as it was when we ran the above command, we simply do:

```sql
DROP DATABASE mydb;
CREATE DATABASE mydb TEMPLATE mydb_template;
```

You may want to make sure that nobody changes your new template database. One way to do this is to not allow any non-superusers to connect to the database by setting the user limit to zero. This can be done either at creation time, or afterwards, like so:

```sql
CREATE DATABASE mydb_template TEMPLATE mydb CONNECTION LIMIT 0;

ALTER DATABASE mydb_template CONNECTION LIMIT 0;
```

You may want to go further by granting the database official “template” status by adjusting the **datistemplate** column in the pg_database table:

```sql
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'mydb_template';
```

This will allow anyone to use the database as a template, as long as they have the CREATEDB privilege. You can also restrict ***all*** connections to the database, even superusers, by adjusting the **datallowconn** column:

```sql
UPDATE pg_database SET datallowconn = FALSE WHERE datname = 'mydb_template';
```

-----------

Another way to restore the database to a known state is to use the [pg_dump utility](https://www.postgresql.org/docs/current/static/app-pgdump.html) to create a file, then use [psql](https://www.postgresql.org/docs/current/static/app-psql.html) to restore that database. In this case, the command to save a copy would be:

```sql
pg_dump mydb --create > mydb.template.pg
```

The **--create** option tells pg_dump to create the database itself as the first command in the file. If you look at the generated file, you’ll see that it is using **template0** as the template database in this case. Why does Postgres have template0 *and* template1? The template1 database is meant as a user configurable template that you can make changes to that will be picked up by all future CREATE DATABASE commands (a common example is a [CREATE LANGUAGE](https://www.postgresql.org/docs/current/static/sql-createlanguage.html) command). The template0 database on the other hand is meant as a “hands off, don’t ever change it” stable database that can always safely be used as a template, with no changes from when the cluster was first created. To that end, you are not even allowed to connect to the template0 database (thanks to the datallowconn column metioned earlier).

Now that we have a file (mydb.template.pg), the procedure to recreate the database becomes:

```bash
psql -X -c 'DROP DATABASE mydb'

psql -X --set ON_ERROR_STOP=on --quiet --file mydb.template.pg
```

We use the **-X** argument to ensure we don’t have any surprises lurking inside of psqlrc files. The **--set ON_ERROR_STOP=on** option tells psql to stop processing the moment it encounters an error, and the **--quiet** tells psql to not be verbose and only let us know about very important things. (While I normally advocate using the **--single-transaction** option as well, we cannot in this case as our file contains a CREATE DATABASE line).

-----------

What if (as someone posited in the thread) the original poster really wanted only the *data* to be cleaned out, and not the schema (e.g. DDL)?. In this case, what we want to do is remove all rows from all tables. The easiest way to do this is with the TRUNCATE command of course. Because we don’t want to worry about which tables need to be deleted before other ones because of foreign key constraints, we’ll also use the CASCADE option to TRUNCATE. We’ll query the system catalogs for a list of all user tables, generate truncate commands for them, and then play back the commands we just created. First, we create a simple text file containing commands to truncate all the tables:

```sql
SELECT 'TRUNCATE TABLE '
 || quote_ident(nspname)
 || '.'
 || quote_ident(relname)
 || ' CASCADE;'
FROM pg_class
JOIN pg_namespace n ON (n.oid = relnamespace)
WHERE nspname !~ '^pg'
AND nspname <> 'information_schema'
AND relkind = 'r';
```

Once that’s saved as **truncate_all_tables.pg**, resetting the database by removing all rows from all tables becomes as simple as:

```sql
psql mydb -X -t -f truncate_all_tables.pg | psql mydb --quiet
```

We again use the **--quiet** option to limit the output, as we don’t need to see a string of “TRUNCATE TABLE” strings scroll by. The **-t** option (also written as **--tuples-only**) prevents the headers and footers from being output, as we don’t want to pipe those back in.

It’s most likely you’d also want the sequences to be reset to their starting point as well. While sequences generally start at “1”, we’ll take out the guesswork by using the “ALTER SEQUENCE seqname RESTART” syntax. We’ll append the following SQL to the text file we created earlier:

```sql
SELECT 'ALTER SEQUENCE '
 || quote_ident(nspname)
 || '.'
 || quote_ident(relname)
 || ' RESTART;'
FROM pg_class
JOIN pg_namespace n ON (n.oid = relnamespace)
WHERE nspname !~ '^pg'
AND nspname <> 'information_schema'
AND relkind = 'S';
```

The command is run the same as before, but now in addition to table truncation, the sequences are all reset to their starting values.

-----------

A final way to restore the database to a known state is a variation on the previous pg_dump command. Rather than save the schema **and** data, we simply want to restore the database without any data:

```bash
## Create the template file:
pg_dump mydb --schema-only --create > mydb.template.schemaonly.pg

## Restore it:
psql -X -c 'DROP DATABASE mydb'
psql -X --set ON_ERROR_STOP=on --file mydb.template.schemaonly.pg
```

Those are a few basic ideas on how to reset your database. There are a few limitations that got glossed over, such as that nobody can be connected to the database that is being used as a template for another one when the CREATE DATABASE command is being run, but this should be enough to get you started.
