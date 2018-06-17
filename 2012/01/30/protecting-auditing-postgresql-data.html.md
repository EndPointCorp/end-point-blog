---
author: Greg Sabino Mullane
gh_issue_number: 548
tags: audit, database, perl, postgres, security
title: Protecting and auditing your secure PostgreSQL data
---



<a href="/blog/2012/01/30/protecting-auditing-postgresql-data/image-0-big.png"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5703579175260784338" src="/blog/2012/01/30/protecting-auditing-postgresql-data/image-0.png" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 310px; height: 320px;"/></a>

PostgreSQL functions can be written in [many languages](http://www.postgresql.org/docs/current/static/xplang.html). These languages fall into two categories, 'trusted' and 'untrusted'. Trusted languages cannot do things "outside of the database", such as writing to local files, opening sockets, sending email, connecting to other systems, etc. Two such languages are [PL/pgSQL](http://www.postgresql.org/docs/current/static/plpgsql-overview.html) and and [PL/Perl](http://www.postgresql.org/docs/current/static/plperl.html). For "untrusted" languages, such as PL/PerlU, all bets are off, and they have no limitations placed on what they can do. Untrusted languages can be very powerful, and sometimes dangerous.

One of the reasons untrusted languages can be considered dangerous is that they can cause side effects outside of the normal transactional flow that cannot be rolled back. If your function writes to local disk, and the transaction then rolls back, the changes on disk are still there. Working around this is extremely difficult, as there is no way to detect when a transaction has rolled back at the level where you could, for example, undo your local disk changes.

However, there are times when this effect can be very useful. For example, in an [email thread](https://www.postgresql.org/message-id/flat/CAH3i69mC1prNKr8y5D2bBosngCLM0eCtiQmGBePd%2BpLFZcOT-Q%40mail.gmail.com#CAH3i69mC1prNKr8y5D2bBosngCLM0eCtiQmGBePd+pLFZcOT-Q@mail.gmail.com) on the PostgreSQL "general" mailing list (aka pgsql-general), somebody asked for a way to audit SELECT queries into a logging table that would survive someone doing a ROLLBACK. In other words, if you had a function named weapon_details() and wanted to have that function log all requests to it by inserting to a table, a user could simply run the query, read the data, and then rollback to thwart the auditing:

```sql
BEGIN;

SELECT weapon_details('BFG 9000'); -- also inserts to an audit table

ROLLBACK;                          -- inserts to the audit table are now gone!
```

Certainly there are other ways to track who is using this query, the most obvious being by enabling full Postgres logging (by setting log_statement = 'all' in your postgresql.conf file.) However, extracting that information from logs is no fun, so let's find a way to make that INSERT stick, even if the surrounding function was rolled back.

Stepping back for one second, we can see there are actually two problems here: restricting access to the data, and logging that access somewhere. The ultimate access restriction is to simply force everyone to go through your custom interface. However, in this example, we will assume that someone has [psql](http://www.postgresql.org/docs/current/static/app-psql.html) access and needs to be able to run ad hoc SQL queries, as well as be able to BEGIN, ROLLBACK, COMMIT, etc.

Let's assume we have a table with some Very Important Data inside of it. Further, let's establish that regular users can only see some of that data, and that we need to know who asked for what data, and when. For this example, we will create a normal user named Alice:

```sql
postgres=> CREATE USER alice;
CREATE ROLE
```

We need a way to tell which rows are suitable for people like Alice to view. We will set up a quick classification scheme using the nifty [ENUM feature](http://www.postgresql.org/docs/current/static/datatype-enum.html) of PostgreSQL:

```sql
postgres=> CREATE TYPE classification AS ENUM (
 'unclassified',
 'restricted',
 'confidential',
 'secret',
 'top secret'
);
CREATE TYPE
```

Next, as a superuser, we create the table containing sensitive information, and populate it:

```text
postgres=> CREATE TABLE weapon (
  id              SERIAL          PRIMARY KEY,
  name            TEXT            NOT NULL,
  cost            TEXT            NOT NULL,
  security_level  CLASSIFICATION  NOT NULL,
  description     TEXT            NOT NULL DEFAULT 'a fine weapon'
);
NOTICE:  CREATE TABLE will create implicit sequence "weapon_id_seq" for serial column "weapon.id"
NOTICE:  CREATE TABLE / PRIMARY KEY will create implicit index "weapon_pkey" for table "weapon"
CREATE TABLE

postgres=> INSERT INTO weapon (name,cost,security_level) VALUES
 ('Crowbar',  10,  'unclassified'),
 ('M9',  200,  'restricted'),
 ('M16A2',  300,  'restricted'),
 ('M4A1',  400,  'restricted'),
 ('FGM-148 Javelin',  700,  'confidential'),
 ('Pulse Rifle',  50000,  'secret'),
 ('Zero Point Energy Field Manipulator',  'unknown',  'top secret');
INSERT 0 7
```

We don't want anyone but ourselves to be able to access this table, so for safety, we make some explicit revocations. We'll examine the permissions before and after we do this:

```text
postgres=> \dp weapon
                          Access privileges
 Schema |  Name  | Type  | Access privileges | Column access privileges 
--------+--------+-------+-------------------+--------------------------
 public | weapon | table |                   | 

postgres=> REVOKE ALL ON TABLE weapon FROM public;
REVOKE

postgres=> \dp weapon
                               Access privileges
 Schema |  Name  | Type  |     Access privileges     | Column access privileges 
--------+--------+-------+---------------------------+--------------------------
 public | weapon | table | postgres=arwdDxt/postgres | 
```

As you can see, what the REVOKE really does is remove the implicit "no permission" and grant explicit permissions to only the postgres user to view or modify the table. Let's confirm that Alice cannot do anything with that table:

```text
postgres=> \c postgres alice
You are now connected to database "postgres" as user "alice".

postgres=> SELECT * FROM weapon;
ERROR:  permission denied for relation weapon

postgres=> UPDATE weapon SET id = id;
ERROR:  permission denied for relation weapon
```

Alice does need to have access to parts of this table, so we will create a "wrapper function" that will query the table for us and return some results. By declaring this function as SECURITY DEFINER, it will run as if the person who created the function invoked it  - in this case, the postgres user. For this example, we'll be letting Alice see the "cost and description" of exactly one item at a time. Further, we are not going to let her (or anyone else using this function) view certain items. Only those items classified as "confidential" or lower can be viewed (i.e. "confidential", "restricted", or "unclassified"). Here's the first version of our function:

```text
postgres=> CREATE LANGUAGE plperlu;
CREATE LANGUAGE

postgres=> CREATE OR REPLACE FUNCTION weapon_details(TEXT)
RETURNS TABLE (name TEXT, cost TEXT, description TEXT)
LANGUAGE plperlu
SECURITY DEFINER
AS $bc$

use strict;
use warnings;

## The item they are looking for
my $name = shift;
## We will be nice and ignore the case and any whitespace
$name =~ s{^\s*(\S+)\s*$}{lc $1}e;

## What is the maximum security_level that people who are 
## calling this function can view?
my $seclevel = 'confidential';

## Query the table and pull back the matching row
## We need to differentiate between "not found" and "not allowed",
## by comparing a passed-in level to the security_level for that row.
my $SQL = q{
SELECT name,cost,description,
  CASE WHEN security_level <= $1 THEN 1 ELSE 0 END AS allowed
FROM weapon
WHERE LOWER(name) = $2};

## Run the query, pull back the first row, as well as the allowed column value
my $sth = spi_prepare($SQL, 'CLASSIFICATION', 'TEXT');
my $rv = spi_exec_prepared($sth, $seclevel, $name);
my $row = $rv->{rows}[0];
my $allowed = delete $row->{allowed};

## Did we find anything? If not, simply return undef
if (! $rv->{processed}) {
   return undef;
}

## Throw an exception if we are not allowed to view this row
if (! $allowed) {
   die qq{Sorry, you are not allowed to view information on that weapon!\n};
}

## Return the requested data
return_next($row);

$bc$;
CREATE FUNCTION
```

The above should be fairly self-explanatory. We are using PL/Perl's [built-in database access functions](http://www.postgresql.org/docs/current/static/plperl-builtins.html), such as spi_prepare, to do the actual querying. Let's confirm that this works as it should for Alice:

```sql
postgres=> \c postgres alice
You are now connected to database "postgres" as user "alice".

postgres=> SELECT * FROM weapon_details('crowbar');
  name   | cost |  description  
---------+------+---------------
 Crowbar | 10   | a fine weapon
(1 row)

postgres=> SELECT * FROM weapon_details('anvil');
 name | cost | description 
------+------+-------------
(0 rows)

postgres=> SELECT * FROM weapon_details('pulse rifle');
ERROR:  Sorry, you are not allowed to view information on that weapon!
CONTEXT:  PL/Perl function "weapon_details"
```

Now that we have solved the restricted access problem, let's move on the auditing. We will create a simple table to hold information about who accessed what and when:

```text
postgres=> CREATE TABLE data_audit (
  tablename TEXT         NOT NULL,
  arguments TEXT             NULL,
  results   INTEGER          NULL,
  status    TEXT         NOT NULL  DEFAULT 'normal',
  username  TEXT         NOT NULL  DEFAULT session_user,
  txntime   TIMESTAMPTZ  NOT NULL  DEFAULT now(),
  realtime  TIMESTAMPTZ  NOT NULL  DEFAULT clock_timestamp()
);
CREATE TABLE
```

The 'tablename' column simply records which table they are getting data from. The 'arguments' is a free-form field describing what they were looking for. The 'results' column shows how many matching rows were found. The 'status' column will be used primarily to log unusual requests, such as the case where Alice looks for a forbidden item. The 'username' column records the name of the user doing the searching. Because we are using functions with SECURITY DEFINER set, this needs to be session_user, not current_user, as the latter will switch to 'postgres' within the function, and we want to log the real caller (e.g. 'alice'). The final two columns tell us then the current transaction started, and the exact time when an entry was made inside of this table. As a first attempt, we'll have our function do some simple inserts to this new data_audit table:

```text
postgres=> CREATE OR REPLACE FUNCTION weapon_details(TEXT)
RETURNS TABLE (name TEXT, cost TEXT, description TEXT)
LANGUAGE plperlu
SECURITY DEFINER
AS $bc$

use strict;
use warnings;

## The item they are looking for
my $name = shift;
## We will be nice and ignore the case and any whitespace
$name =~ s{^\s*(\S+)\s*$}{lc $1}e;

## What is the maximum security_level that people who are 
## calling this function can view?
my $seclevel = 'confidential';

## Query the table and pull back the matching row
## We need to differentiate between "not found" and "not allowed",
## by comparing a passed-in level to the security_level for that row.
my $SQL = q{
SELECT name,cost,description,
  CASE WHEN security_level <= $1 THEN 1 ELSE 0 END AS allowed
FROM weapon
WHERE LOWER(name) = $2};

## Run the query, pull back the first row, as well as the allowed column value
my $sth = spi_prepare($SQL, 'CLASSIFICATION', 'TEXT');
my $rv = spi_exec_prepared($sth, $seclevel, $name);
my $row = $rv->{rows}[0];
my $allowed = delete $row->{allowed};

## Log this request
$SQL = 'INSERT INTO data_audit(tablename,arguments,results,status)
  VALUES ($1,$2,$3,$4)';
my $status = $rv->{rows}[0] ? $allowed ? 'normal' : 'forbidden' : 'na';
$sth = spi_prepare($SQL, 'TEXT', 'TEXT', 'INTEGER', 'TEXT');
spi_exec_prepared($sth, 'weapon', $name, $rv->{processed}, $status);

## Did we find anything? If not, simply return undef
if (! $rv->{processed}) {
   return undef;
}

## Throw an exception if we are not allowed to view this row
if (! $allowed) {
   die qq{Sorry, you are not allowed to view information on that weapon!\n};
}

## Return the requested data
return_next($row);

$bc$;
```

However, this fails the case pointed out in the original poster's email about viewing the data within a transaction that is then rolled back. It also fails to work at all when a forbidden item is requested, as that insert is rolled back by the die() call:

```sql
postgres=> \c postgres alice
You are now connected to database "postgres" as user "alice".

postgres=> SELECT * FROM weapon_details('crowbar');
  name   | cost |  description  
---------+------+---------------
 Crowbar | 10   | a fine weapon
(1 row)

postgres=> SELECT * FROM weapon_details('pulse rifle');
ERROR:  Sorry, you are not allowed to view information on that weapon!
CONTEXT:  PL/Perl function "weapon_details"

postgres=> BEGIN;
BEGIN
postgres=> SELECT * FROM weapon_details('m9');
 name | cost |  description  
------+------+---------------
 M9   | 200  | a fine weapon
(1 row)
postgres=> ROLLBACK;
ROLLBACK

postgres=> \c postgres postgres
You are now connected to database "postgres" as user "postgres".
postgres=> SELECT * FROM data_audit \x \g
Expanded display is on.
-[ RECORD 1 ]----------------------------
tablename | weapon
arguments | crowbar
results   | 1
status    | normal
username  | alice
txntime   | 2012-01-30 17:37:39.497491-05
realtime  | 2012-01-30 17:37:39.545891-05
```

How do we get around this? We need a way to commit something that will survive the surrounding transaction's rollback. The closest thing Postgres has to such a thing at the moment is to connect back to the database with a new and entirely separate connection. Two such popular ways to do so are with [the dblink program](http://www.postgresql.org/docs/current/static/dblink.html) and [the PL/PerlU language](http://www.postgresql.org/docs/current/static/plperl.html). Obviously, we are going to focus on the latter, but all of this could be done with dblink as well. Here are the additional steps to connect back to the database, do the insert, and then leave again:

```sql
postgres=> CREATE OR REPLACE FUNCTION weapon_details(TEXT)
RETURNS TABLE (name TEXT, cost TEXT, description TEXT)
LANGUAGE plperlu
SECURITY DEFINER
VOLATILE
AS $bc$
```

```perl
use strict;
use warnings;
use DBI;

## The item they are looking for
my $name = shift;
## We will be nice and ignore the case and any whitespace
$name =~ s{^\s*(\S+)\s*$}{lc $1}e;

## What is the maximum security_level that people who are 
## calling this function can view?
my $seclevel = 'confidential';

## Query the table and pull back the matching row
## We need to differentiate between "not found" and "not allowed",
## by comparing a passed-in level to the security_level for that row.
my $SQL = q{
SELECT name,cost,description,
  CASE WHEN security_level <= $1 THEN 1 ELSE 0 END AS allowed
FROM weapon
WHERE LOWER(name) = $2};

## Run the query, pull back the first row, as well as the allowed column value
my $sth = spi_prepare($SQL, 'CLASSIFICATION', 'TEXT');
my $rv = spi_exec_prepared($sth, $seclevel, $name);
my $row = $rv->{rows}[0];
my $allowed = defined $row ? delete $row->{allowed} : 1;

## Log this request
$SQL = 'INSERT INTO data_audit(username,tablename,arguments,results,status)
  VALUES (?,?,?,?,?)';
my $status = $rv->{rows}[0] ? $allowed ? 'normal' : 'forbidden' : 'na';
my $dbh = DBI->connect('dbi:Pg:service=auditor', '', '',
  {AutoCommit=>0, RaiseError=>1, PrintError=>0});
$sth = $dbh->prepare($SQL);
my $user = spi_exec_query('SELECT session_user')->{rows}[0]{session_user};
$sth->execute($user, 'weapon', $name, $rv->{processed}, $status);
$dbh->commit();

## Did we find anything? If not, simply return undef
if (! $rv->{processed}) {
   return undef;
}

## Throw an exception if we are not allowed to view this row
if (! $allowed) {
   die qq{Sorry, you are not allowed to view information on that weapon!\n};
}

## Return the requested data
return_next($row);

$bc$;
CREATE FUNCTION
```

Note that because we are making external changes, we marked the function as VOLATILE, which ensures that it will always be run every time it is called, and not cached in any form. We are also using [a Postgres service file](https://www.endpoint.com/blog/2016/10/26/postgres-connection-service-file) with the 'db:Pg:service=auditor'. This means that the connection information (username, password, database) is contained in an external file. This is not only tidier than hard-coding those values into this function, but safer as well, as the function itself can be viewed by Alice. Finally, note that we are passing the 'username' directly into the function this time, as we have a brand new connection which is no longer linked to the 'alice' user, so we have to derive it ourselves from "SELECT session_user" and then pass it along.

Once this new function is in place, and we re-run the same queries as we did before, we see three entries in our audit table:

```sql
postgres=> \c postgres postgres
You are now connected to database "postgres" as user "postgres".
Expanded display is on.
-[ RECORD 1 ]----------------------------
tablename | weapon
arguments | crowbar
results   | 1
status    | normal
username  | alice
txntime   | 2012-01-30 17:56:01.544557-05
realtime  | 2012-01-30 17:56:01.54569-05
-[ RECORD 2 ]----------------------------
tablename | weapon
arguments | pulse rifle
results   | 1
status    | forbidden
username  | alice
txntime   | 2012-01-30 17:56:01.559532-05
realtime  | 2012-01-30 17:56:01.561225-05
-[ RECORD 3 ]----------------------------
tablename | weapon
arguments | m9
results   | 1
status    | normal
username  | alice
txntime   | 2012-01-30 17:56:01.573335-05
realtime  | 2012-01-30 17:56:01.574989-05
```

So that's the basic premise of how to solve the auditing problem. For an actual production script, you would probably want to cache the database connection by sticking things inside of the special [%_SHARED hash available to PL/Perl and Pl/PerlU](http://www.postgresql.org/docs/current/static/plperl-global.html). Note that each user gets their own version of that hash, so Alice will not be able to create a function and have access to the same %_SHARED hash that the postgres user has access to. It's probably a good idea to simply not let users like Alice use the language at all. Indeed, that's the default when we do the CREATE LANGUAGE call as above:

```sql
postgres=>  \c postgres alice
You are now connected to database "postgres" as user "alice".

postgres=> CREATE FUNCTION showplatform()
RETURNS TEXT
LANGUAGE plperlu
AS $bc$
  return $^O;
$bc$;
ERROR:  permission denied for language plperlu
```

Further refinements to the actual script might include refactoring the logging bits to a separate function, writing some of the auditing data to a file on the local disk, recording the actual results returned to the user, and sending the data to another Postgres server entirely. For that matter, as we are using DBI, you could send it to other place entirely - such as a MySQL, Oracle, or DB2 database!

Another place for improvement would be associating each user with a security_level classification, such that any user could run the function and only see things at or below their level, rather than hard-coding the level as "confidential" as we have done here. Another nice refinement might be to always return undef (no matches) for items marked "top secret", to prevent the very existence of a top secret weapon from being deduced. :)


