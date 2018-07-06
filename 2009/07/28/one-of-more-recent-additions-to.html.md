---
author: Greg Sabino Mullane
gh_issue_number: 178
tags: database, open-source, perl, postgres
title: Comparing databases with check_postgres
---

One of the more recent additions to [check_postgres](https://bucardo.org/check_postgres/), the all-singing, all-dancing [Postgres](https://www.postgresql.org/) monitoring tool, is the "same_schema" action. This was necessitated by clients who wanted to make sure that their schemas were identical across different servers. The two use cases I’ve seen are servers that are being replicated by [Bucardo](https://bucardo.org/) or [Slony](http://slony.info/), and servers that are doing horizontal sharding (e.g. same schema and database on different servers: which server you go to depends on (for example) your customer id). Oft times a new index fails to make it to one of the slaves, or some function is tweaked on one server by a developer, who then forgets to change it back or propagate it. This program allows a quick and automatable check for such problems.

The idea behind the same_schema check is simple: we walk the schema and check for any differences, then throw a warning if any are found. In this case, we’re using the term "schema" in the classic sense of a description of your database objects. Thus, one of the things we check is that all the schemas (in the classic RDBMS sense of a container of other database objects) are the same, when running the "same_schema" check. Only slightly confusing. :)

Not only is this program nice for monitoring (e.g. as a [Nagios](https://www.nagios.org/) check), but if you pass in a --verbose argument, you get a simple not-all-on-one-line breakdown of all the differences between the two databases. Let’s do a quick example.

First, we download and install check_postgres. We’ll pull straight from a [git](https://git-scm.org/) repository for check_postgres. While we have our own repo at bucardo.org, we also are keeping it in sync with a [tree at github.org](https://github.com/bucardo/check_postgres/tree/master), so we’ll use that one:

```bash
git clone git://github.com/bucardo/check_postgres.git
cd check_postgres
perl Makefile.PL
make
make test
sudo make install
```
Let’s create a Postgres cluster with the initdb command, start it up, then create two new databases to compare to each other.

```bash
initdb -D cptest
echo port=5555 >> cptest/postgresql.conf
pg_ctl -D cptest -l cp.log start
psql -p 5555 -c 'CREATE DATABASE yin'
psql -p 5555 -c 'CREATE DATABASE yang'
```

We’re ready to run the script. By default, it outputs things in a Nagios-friendly manner. We should see an ‘OK’ because the two databases are identical:

```bash
./check_postgres.pl --action=same_schema --dbport=5555 --dbname=yin --dbport2=5555 --dbname2=yang

POSTGRES_SAME_SCHEMA OK: DB "yin" (port=5555 => 5555) Both databases have identical items | time=0.01
```

The message could be clearer and show both database names, but the check worked and showed that things are exactly the same. Let’s throw some differences in and run it again:

```bash
psql -p 5555 -d yin -c 'create table foobar(a int primary key, b text, c text)'
psql -p 5555 -d yang -c 'create table foobar(a int, b text, c varchar(99))'
psql -p 5555 -d yin -c 'create schema yinonly'
psql -p 5555 -d yang -c 'create table pineapple(id int)'

./check_postgres.pl --action=same_schema --dbport=5555 --dbname=yin --dbport2=5555 --dbname2=yang

POSTGRES_SAME_SCHEMA CRITICAL: DB "yin" (port=5555 => 5555) Databases were different. Items not matched: 5 | time=0.01
Schema in 1 but not 2: yinonly  Table in 2 but not 1: public.pineapple  Column "a" of "public.foobar": nullable is NO on 1, but YES on 2.  Column "c" of "public.foobar": type is text on 1, but character varying on 2.  Table "public.foobar" on 1 has constraint "public.foobar_pkey", but 2 does not. 
```

It works, but a little messy for human consumption. Nagios requires everything to be in a single line, but we’ll add a --verbose argument to ask the script for prettier formatting:

```bash
./check_postgres.pl --action=same_schema --dbport=5555 --dbname=yin --dbport2=5555 --dbname2=yang

POSTGRES_SAME_SCHEMA CRITICAL: DB "yin" (port=5555 => 5555) Databases were different. Items not matched: 5 | time=0.01
Schema in 1 but not 2: yinonly
Table in 2 but not 1: public.pineapple
Column "a" of "public.foobar": nullable is NO on 1, but YES on 2.
Column "c" of "public.foobar": type is text on 1, but character varying on 2.
Table "public.foobar" on 1 has constraint "public.foobar_pkey", but 2 does not.
```

There are also ways to filter the output, for times when you have known differences. For example, to exclude any tables with the word ‘bucardo’ in them, you could add this argument:

```bash
--warning="notable=bucardo"
```

The [online documentation](https://bucardo.org/check_postgres/check_postgres.pl.html#same_schema) has more details about all the filtering options.

So what kind of things do we check for? Right now, we are checking:

- users (existence and powers, i.e. createdb, superuser)
- schemas
- tables
- sequences
- views
- triggers
- constraints
- columns
- functions (including volatility, strictness, etc.)

Got something else we aren’t covering? Send in a patch, or a quick request, to [the mailing list](https://mail.endcrypt.com/mailman/listinfo/check_postgres).
