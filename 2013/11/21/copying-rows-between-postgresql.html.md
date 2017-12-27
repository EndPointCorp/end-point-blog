---
author: Szymon Lipiński
gh_issue_number: 887
tags: postgres
title: Copying Rows Between PostgreSQL Databases
---

A recurring question is: “how can I copy a couple of rows from one database to another”? People try to set up some replication, or dump entire database, however the solution is pretty simple.

## Example

For this blog post I will create two similar tables, I will be copying data from one to another. They are in the same database, but in fact that doesn’t matter, you can use this example to copy to another database as well. Even on another server, that’s enough to change arguments for the psql commands.

The tables are:

```sql
test=# CREATE TABLE original_table (i INTEGER, t TEXT);
CREATE TABLE
test=# CREATE TABLE copy_table (i INTEGER, t TEXT);
CREATE TABLE
```

Now I will insert two rows, which I will copy later to the “copy_table”.

```sql
test=# INSERT INTO original_table(i, t) VALUES
  (1, 'Lorem ipsum dolor sit amet'),
  (2, 'consectetur adipiscing elit');
INSERT 0 2

test=# SELECT * FROM original_table ;
 i |              t
---+-----------------------------
 1 | Lorem ipsum dolor sit amet
 2 | consectetur adipiscing elit
(2 rows)

test=# SELECT * FROM copy_table;
 i | t
---+---
(0 rows)
```

## The Solution

Of course I can set up replication, which is too much effort for ad hoc copying two rows. Of course I could dump entire database, but imagine a database with millions of rows, and you just want to copy those two rows.

Fortunately there is “copy” command. However simple copy saves file on the same server as PostgreSQL is running, and usually you don’t have access to the file system there. There is another command, that’s internal command for psql, it is named “\copy”. It behaves exactly like copy, but it writes files on the machine you run psql at.

### Save To File

The first and simplest solution we could save those two rows into a file, and load it later on another database.

First, let’s find out how “\copy” works:

```sql
$ psql test -c \
"\copy (SELECT i, t FROM original_table ORDER BY i) TO STDOUT"

1 Lorem ipsum dolor sit amet
2 consectetur adipiscing elit
```

As you can see, the main part of this command is the select query which allows to choose rows we want to export. You can provide there any “where” clause you want.

So now we can save it to a file:

```sql
$ psql test -c \
"\copy (SELECT i, t FROM original_table ORDER BY i) TO STDOUT" > /tmp/f.tsv
```

Loading now is also pretty easy with the same “\copy” command.

```sql
psql test -c "\copy copy_table (i, t) FROM STDIN"
```

### Don’t Save to File

Saving to a file has one drawback: if the data amount is huge, then the file will be huge as well, it will waste disk space, and can be slower than using a pipe to load data. You can use a pipe to join the output of one psql command with input of another one. This is as simple as:

```sql
psql test -c \
"\copy (SELECT i, t FROM original_table ORDER BY i) TO STDOUT" | \
psql test -c "\copy copy_table (i, t) FROM STDIN"

test=# SELECT * FROM copy_table ;
 i |              t
---+-----------------------------
 1 | Lorem ipsum dolor sit amet
 2 | consectetur adipiscing elit
(2 rows)
```

As you can see, that’s much simpler than setting up replication or dumping whole database.
