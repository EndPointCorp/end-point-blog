---
author: Greg Sabino Mullane
gh_issue_number: 1128
tags: database, postgres, scalability
title: Connected to PgBouncer or Postgres?
---

<div class="separator" style="clear: both; text-align: center; float: right"><a href="/blog/2015/05/18/connected-to-pgbouncer-or-postgres/image-0-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" data-original-height="280" data-original-width="320" src="/blog/2015/05/18/connected-to-pgbouncer-or-postgres/image-0.png"/></a><br/><small><a href="https://flic.kr/p/9X5Z89">Image</a> by <a href="https://www.flickr.com/people/dhwright/">David Wright</a></small></div>

Determining if your current database connection is using
[PgBouncer](https://wiki.postgresql.org/wiki/PgBouncer),
or going directly to Postgres itself, can be challenging, as PgBouncer
is a very low-level, transparent interface. It is possible, and
here are some detection methods you can use.

This was inspired by someone asking on the Perl DBD IRC
channel if it was possible to easily tell if your current
database handle (usually “$dbh”) is connected to PgBouncer or not.
Since I’ve seen this question asked in other venues, I decided to
take a crack at it.

There are actually two questions to be answered: (1) are we connected
to PgBouncer, and if so, (2) what pool_mode is being run? The quickest
and easiest way I found to answer the first question is to try and
connect to a non-existent database. Normally, this is a FATAL message,
as seen here:

```
$ psql testdb -p 5432
testdb=# \c ghostdb
FATAL:  database "ghostdb" does not exist
Previous connection kept
testdb=#
```

However, a slightly different ERROR message is returned if the same
thing is attempted while connected to PgBouncer:

```
$ psql testdb -p 6432
testdb=# \c ghostdb
ERROR:  No such database: ghostdb
Previous connection kept
testdb=#
```

Thus, an ERROR will always indicate that you are connected to
PgBouncer and not directly to Postgres, which will always issue
a FATAL.

In the future, there will be an even simpler method. As of this writing,
pgBouncer 1.6 has not been released, but it will have the ability to customize
the [application_name](https://www.postgresql.org/docs/current/static/runtime-config-logging.html#GUC-APPLICATION-NAME). This is a configurable session-level variable that is fairly new in Postgres.
Andrew Dunstan [wrote a patch](http://adpgtech.blogspot.com/2014/05/pgbouncer-enhancements.html) which enables adding this to your **pgbouncer.ini** file:

```
application_name_add_host = 1
```

This will make PgBouncer modify the application_name to append some
information to it such as the remote host, the remote port, and the local port.
This is a feature many PgBouncer users will appreciate,
as it offers an escape from the black hole of connection information
that PgBouncer suffers from. Here is what it looks like on both a normal
Postgres connection, and a PgBouncer connection. As you can see, this is an
easier check than the “invalid database connection” check above:

```
## Postgres:
$ psql testdb -p 5432 -c 'show application_name'
 application_name
------------------
 psql

## PgBouncer:
$ psql testdb -p 6432 -c 'show application_name'
        application_name
--------------------------------
 psql - unix(7882@gtsm.com):6432

## DBD::Pg connections to PgBouncer get a very similar change:
$ perl testme.tmp.pl --port 6432
app - unix(6772@gtsm.com):6432
```


Now we have answered question of “are we connected to PgBouncer
or not?”. The next question is which pool mode we are in.
There are three pool modes you can set for PgBouncer, which
controls when your particular connection is returned to “the pool”.
For “session” mode, you keep the same Postgres backend the entire time you are
connected. For “transaction”, you keep the same Postgres backend until the end of a
transaction. For “statement”, you may get a new Postgres backend after each statement.

First, we can check if we are connected to PgBouncer in a statement level
pool mode by taking advantage of the fact that multi-statement transactions
are prohibited. PgBouncer enforces this by intercepting any attempts to
enter a transaction (e.g. by issuing a BEGIN command). A very PgBouncer specific
error about “Long transactions not allowed” is issued back to the client
like so:

```
$ psql testdb -p 6432
testdb=# begin;
ERROR:  Long transactions not allowed
```

So, that takes care of detecting a pool_mode set to “statement”. The other two modes,
transaction and session, will *not* give the same error. Thus, seeing that
error indicates you are using a statement-level PgBouncer connection.

The next pool mode is “transaction”, which means that the server connection
if released back to the pool at the end of a transaction. To figure out
if we are in this mode, we take advantage of the fact that PgBouncer can
be set to clean up the connection at the end of each transaction by issuing a specific
command. By default, the command set by server_reset_query is
[DISCARD ALL](https://www.postgresql.org/docs/current/static/sql-discard.html), which invalidates
any prepared statements, temporary tables, and other transaction-spanning,
session-level items. Thus, our test will see if these session-level
artifacts get discarded or not:

```
## Direct Postgres:
$ psql testdb -p 5432
testdb=# prepare abc(int) as select $1::text;
PREPARE
testdb=# execute abc(1);
 text
------
 1

## PgBouncer:
$ psql testdb -p 6432
testdb=# prepare abc(int) as select $1::text;
PREPARE
testdb=# execute abc(1);
ERROR:  prepared statement "abc" does not exist
```

Keep in mind that there are no true “transactionless” commands in Postgres.
Even though we did not use a BEGIN in the psql prompt above, each command
is treated as its own mini-transaction. In the case of the PgBouncer
connection, the prepare is immediately followed with a DISCARD ALL,
which means that our prepared statement no longer exists. Hence, we
have determined that we  are using a transaction-level
PgBouncer connection.

Unfortunately, not getting an error does not necessarily mean your
PgBouncer is NOT in transaction mode!  A very negative sentence!
It could be that server_reset_query is empty, meaning that temporary artifacts
are not discarded at the end of the transaction. In such a case, we can
take advantage of the fact that PgBouncer will allow other clients to share
in our current connection, and thus be able to see the temporary items.
If we create a temporary table in one pgbouncer connection, then connect
again as a new client, the temporary table will only show up if we are
sharing sessions but not transactions. Easier shown than explained, I suspect:

```
## Regular Postgres gets a fresh session:
$ psql test1 -p 5432
test1=# create temp table abc(a int);
CREATE TABLE
test1=# select * from abc;
(No rows)
test1=# ^Z ## (we suspend with CTRL-Z)
[2]+  Stopped                 psql test1 -p 5432

$ psql test1 -p 5432
test1=# select * from abc;
ERROR:  relation "abc" does not exist

## PgBouncer will re-use the same session:
$ psql test1 -p 6432
test1=# create temp table abc(a int);
CREATE TABLE
test1=# select * from abc;
(No rows)
test1=# ^Z
[2]+  Stopped                 psql test1 -p 6432

$ psql test1 -p 6432
test1=# select * from abc;
(No rows)
```

The final PgBouncer pool mode is “session”, and basically means
the only advantage over a normal Postgres connection is the overhead
to start up and connect to a new Postgres backend. Thus, the
PgBouncer connections are only returned to the pool upon disconnection.
The only way to tell if you are in this mode is by determining that you
are *not* in the other two modes. :)

So, although PgBouncer is extremely transparent, there are some tricks to
determine if you are connected to it, and at what pool_mode. If you
can think of other (SQL-level!) ways to check, please let me know
in the comments section.
