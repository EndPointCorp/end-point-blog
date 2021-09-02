---
author: Greg Sabino Mullane
title: 'Tickle me Postgres: Tcl inside PostgreSQL with pl/tcl and pl/tclu'
github_issue_number: 298
tags:
- database
- postgres
date: 2010-05-04
---



Although I really love Pl/Perl and find it the most useful language to write PostgreSQL functions in, Postgres has had (for a long time) another set of procedural languages: **Pl/Tcl** and **Pl/TclU**. The Tcl language is pronounced “tickle”, so those two languages are pronounced as “pee-el-tickle” and “pee-el-tickle-you”. The pl/tcl languages have been around since before any others, even pl/perl; for a long time in the early days of Postgres using pl/tclu was the only way to do things “outside of the database”, such as making system calls, writing files, sending email, etc.

Sometimes people are surprised when they hear I still use Tcl. Although it’s not as widely mentioned as other procedural languages, it’s a very clean, easy to read, powerful language that shouldn’t be overlooked. Of course, with Postgres, you have a wide variety of languages to write your functions in, including:

- [Perl](https://www.postgresql.org/docs/current/static/plperl.html) (my favorite)

- [Tcl](https://www.postgresql.org/docs/current/interactive/pltcl-overview.html) (second favorite)

- [Python](https://www.postgresql.org/docs/current/interactive/plpython.html) (distant third)

- [Ruby](https://github.com/knu/postgresql-plruby)

- [Scheme](https://github.com/vy/plscheme)

- [LOLCODE](http://pgfoundry.org/projects/pllolcode)

- [PHP](http://plphp.sourceforge.net/)

- [sh](https://github.com/petere/plsh)

- [Java](http://pgfoundry.org/projects/pljava/)

The nice thing about [Tcl](https://wiki.tcl.tk/299) is that not only is it an easy language to write in, it’s fully supported by Postgres. Only three languages are maintained inside the Postgres tree itself: Perl, Tcl, and Python. Only two of those have a trusted and untrusted version: Perl and Tcl. All procedural languages in Postgres are untrusted by default, which means they can do things like make system calls. To be a trusted language, there must be some capacity to limit what can be done by the language. With Perl, this is accomplished through the “Safe” Perl module. For Tcl, this is accomplished by having two versions of the Tcl interpreter: a normal one for pltclu and a separate one that uses the [“Safe-Tcl mechanism”](https://www.tcl.tk/software/plugin/safetcl.html) for pltcl.

Let’s take a quick look at what a pltcl function looks like. We’ll use pl/tcl to implement the common problem of “SELECT COUNT(*) is very slow” by tracking the row count using [triggers](https://www.postgresql.org/docs/current/interactive/trigger-definition.html) as we go along. For this, we’ll start with a sample table that we want to be able to find out exactly how many rows are inside of any time, without suffering the delay of COUNT(*). Here’s the table definition, and a quick command to populate it with some dummy data:

```sql
CREATE SEQUENCE customer_id_seq;

CREATE TABLE customer (
  id      INTEGER     NOT NULL DEFAULT nextval('customer_id_seq') PRIMARY KEY,
  email   TEXT            NULL,
  address TEXT            NULL,
  cdate   TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO customer (email, address)
  SELECT 'jsixpack@example.com', '123 Main Street'
  FROM generate_series(1,10000);
```

A quick review: we create a [sequence](https://www.postgresql.org/docs/current/interactive/functions-sequence.html) for use by the table to populate its primary key, the ‘id’ column. Each customer also has an optional email and address, plus we automatically track when we create the row by using the “DEFAULT now()” trick on the ‘cdate’ column. Finally, we use the super handy [generate_series](https://www.postgresql.org/docs/current/static/functions-srf.html) function to populate the new table with ten thousand rows of data.

Next, we’ll create a helper table that will keep track of the rows for us. We’ll make it generic so that it can track any number of tables:

```sql
CREATE TABLE table_count (
  schemaname TEXT   NOT NULL,
  tablename  TEXT   NOT NULL,
  rows       BIGINT NOT NULL DEFAULT 0
);

INSERT INTO table_count(schemaname,tablename,rows)
  SELECT 'public', 'customer', count(*) FROM customer;
```

We also populated it with the current number of rows in customer. Of course, this will be out of date as soon as someone updates the table, so let’s add our triggers. We don’t want to update the table_count table on every single row change, but only at the end of each statement. To do that, we’ll make a row-level trigger that stores up the changes inside a global variable, and then a statement-level trigger that uses the global variable to update the table_count table.

```sql
CREATE FUNCTION update_table_count_row()
  RETURNS TRIGGER
  SECURITY DEFINER
  VOLATILE
  LANGUAGE pltcl
AS $BC$

  ## Declare tablecount as a global variable so other functions
  ## can access our changes
  variable tablecount

  ## Set the local count of rows changed to 0
  set rows 0

  ## $TG_op indicates what type of command was just run
  ## Modify the local variable rows depending on what we just did
  switch $TG_op {
    INSERT {
      incr rows 1
    }
    UPDATE {
      ## No change in number of rows
      ## We could also leave out the ON UPDATE from the trigger below
    }
    DELETE {
      incr rows -1
    }
  }

  ## The tablecount variable will be an associative array
  ## The index will be this table's name, the value is the rows changed
  ## We should probably be using $TG_schema_name as well, but we'll ignore that

  ## If there is no variable for this table yet, create it, otherwise just change it
  if {![ info exists tablecount($TG_table_name) ] } {
    set tablecount($TG_table_name) $rows
  } else {
    incr tablecount($TG_table_name) $rows
  }

  return OK
$BC$;

CREATE FUNCTION update_table_count_statement()
  RETURNS TRIGGER
  SECURITY DEFINER
  LANGUAGE pltcl
AS $BC$

  ## Make sure we access the global version of the tablecount variable
  variable tablecount

  ## If it doesn't exist yet (for example, when an update changes no 
  ## rows), we simply exit early without making changes
  if { ! [ info exists tablecount ] } {
    return OK
  }
  ## Same logic if our specific entry in the array does not exist
  if { ! [ info exists tablecount($TG_table_name) ] } {
    return OK
  }
  ## If no rows were changed, we simply exit
  if { $tablecount($TG_table_name) == 0 } {
    return OK
  }

  ## Update the table_count table: may be a positive ior negative shift
  spi_exec "
    UPDATE table_count
    SET rows=rows+$tablecount($TG_table_name)
    WHERE tablename = '$TG_table_name'
  "

  ## Reset the global variable for the next round
  set tablecount($TG_table_name) 0

  return OK
$BC$;

CREATE TRIGGER update_table_count_row
  AFTER INSERT OR UPDATE OR DELETE
  ON public.customer
  FOR EACH ROW
  EXECUTE PROCEDURE update_table_count_row();

CREATE TRIGGER update_table_count_statement
  AFTER INSERT OR UPDATE OR DELETE
  ON public.customer
  FOR EACH STATEMENT
  EXECUTE PROCEDURE update_table_count_statement();

```

(Caveat: because there is a single Tcl interpreter for all pl/tcl functions, these functions are not 100% safe, as there is a theoretical chance that changes made by processes running at the exact same time may step on each other’s global variables. In practice, this is unlikely.)

If everything is working correctly, we should see the entries in the table_count table match up with the output of SELECT COUNT(*). Let’s take a look via a psql session:

```sql
psql=# \t
Showing only tuples.
psql=# \a
Output format is unaligned.

psql=# SELECT * FROM table_count; SELECT COUNT(*) FROM customer;
public|customer|10000
10000

psql=# UPDATE customer SET email=email WHERE id <= 10;
UPDATE 10

psql=# SELECT * FROM table_count; SELECT COUNT(*) FROM customer;
public|customer|10000
10000

psql=# INSERT INTO customer (email, address)
psql-# SELECT email, address FROM customer LIMIT 4;
INSERT 0 4

psql=# SELECT * FROM table_count; SELECT COUNT(*) FROM customer;
public|customer|10004
10004

psql=# DELETE FROM customer WHERE id <= 10;
DELETE 10

psql=# SELECT * FROM table_count; SELECT COUNT(*) FROM customer;
public|customer|9994
9994

psql=# TRUNCATE TABLE customer;
TRUNCATE TABLE

psql=# SELECT * FROM table_count; SELECT COUNT(*) FROM customer;
public|customer|9994
0
```

Whoops! Everything matched up until that TRUNCATE. On earlier versions of Postgres, there was no way around that problem, but if we have Postgres version 8.4 or better, we can use truncate triggers!

```sql
CREATE FUNCTION update_table_count_truncate()
  RETURNS TRIGGER
  SECURITY DEFINER
  LANGUAGE pltcl
AS $BC$

  spi_exec "
    UPDATE table_count
    SET rows=0
    WHERE tablename = '$TG_table_name'
  "

  set tablecount($TG_table_name) 0

 return OK
$BC$;

CREATE TRIGGER update_table_count_truncate
  AFTER TRUNCATE
  ON public.customer
  FOR EACH STATEMENT
  EXECUTE PROCEDURE update_table_count_truncate();

```

Pretty straightforward, let’s make sure it works:

```sql
psql=# TRUNCATE TABLE customer;
TRUNCATE TABLE

psql=# SELECT * FROM table_count; SELECT COUNT(*) FROM customer;
public|customer|0
0
```

Success! This was a fairly contrived example, but Tcl (and especially pl/tclU) offers a lot more functionality. If you want to examine pl/tcl and pl/tclu for yourself, you’ll need to make sure it’s compiled into the Postgres you are using. If using a packaging system, it’s as simple as doing this (or something like it, depending on what packaging system you use):

```bash
yum install postgresql-pltcl
```

If compiling from source, just pass the *--with-tcl* option to **configure**. You’ll probably also need to install the Tcl development package, e.g. with yum install tcl-devel

Once installed, installing it into a specific database is as simple as:

```sql
$ CREATE LANGUAGE pltcl;
CREATE LANGUAGE
$ CREATE LANGUAGE pltclu;
CREATE LANGUAGE
```

For more about Tcl, check out the [The Tcl Wiki](https://wiki.tcl.tk/), the [Tcl tutorial](https://www.tcl.tk/man/tcl8.5/tutorial/tcltutorial.html), or this [Tcl reference](https://www.tcl.tk/man/tcl8.5/). For more about pl/tcl and pl/tclu. visit the [Postgres pltcl documentation](https://www.postgresql.org/docs/current/static/pltcl-overview.html)


