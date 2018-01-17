---
author: Greg Sabino Mullane
gh_issue_number: 1094
tags: database, postgres
title: Postgres ON_ERROR_ROLLBACK explained
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2015/02/24/postgres-onerrorrollback-explained/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/02/24/postgres-onerrorrollback-explained/image-0.jpeg"/></a><br/><small>
(<a href="https://flic.kr/p/jt1ajt">picture</a> by <a href="https://www.flickr.com/photos/pokerbrit/">Steve Wilson</a>)</small></div>

Way back in 2005 I added the **ON_ERROR_ROLLBACK** feature to [psql](https://www.postgresql.org/docs/current/static/app-psql.html), the Postgres command line client. When enabled, any errors cause an immediate rollback to just before the previous command. What this means is that you can stay inside your [transaction](https://www.postgresql.org/docs/current/static/tutorial-transactions.html), even if you make a typo (the main error-causing problem and the reason I wrote it!). Since I sometimes see people wanting to emulate this feature in their application or driver, I thought I would explain exactly how it works in psql.

First, it must be understood that this is not a Postgres feature, and there is no way you can instruct Postgres itself to ignore errors inside of a transaction. The work must be done by a client (such as psql) that can do some voodoo behind the scenes. The ON_ERROR_ROLLBACK feature is available since psql version 8.1.

Normally, any error you make will throw an exception and cause your current transaction to be marked as aborted. This is sane and expected behavior, but it can be very, very annoying if it happens when you are in the middle of a large transaction and mistype something! At that point, the only thing you can do is rollback the transaction and lose all of your work. For example:

```
greg=# CREATE TABLE somi(fav_song TEXT, passphrase TEXT, avatar TEXT);
CREATE TABLE
greg=# begin;
BEGIN
greg=# INSERT INTO somi VALUES ('The Perfect Partner', 'ZrgRQaa9ZsUHa', 'Andrastea');
INSERT 0 1
greg=# INSERT INTO somi VALUES ('Holding Out For a Hero', 'dx8yGUbsfaely', 'Janus');
INSERT 0 1
greg=# INSERT INTO somi BALUES ('Three Little Birds', '2pX9V8AKJRzy', 'Charon');
ERROR:  syntax error at or near "BALUES"
LINE 1: INSERT INTO somi BALUES ('Three Little Birds', '2pX9V8AKJRzy'...
greg=# INSERT INTO somi VALUES ('Three Little Birds', '2pX9V8AKJRzy', 'Charon');
ERROR:  current transaction is aborted, commands ignored until end of transaction block
greg=# rollback;
ROLLBACK
greg=# select count(*) from somi;
 count
-------
     0
```

When ON_ERROR_ROLLBACK is enabled, psql will issue a [SAVEPOINT](https://www.postgresql.org/docs/current/static/sql-savepoint.html) before every command you send to Postgres. If an error is detected, it will then issue a [ROLLBACK TO](https://www.postgresql.org/docs/current/static/sql-rollback-to.html) the previous savepoint, which basically rewinds history to the point in time just before you issued the command. Which then gives you a chance to re-enter the command without the mistake. If an error was not detected, psql does a [RELEASE savepoint](https://www.postgresql.org/docs/current/static/sql-release-savepoint.html) behind the scenes, as there is no longer any reason to keep the savepoint around. So our example above becomes:

```
greg=# \set ON_ERROR_ROLLBACK interactive
greg=# begin;
BEGIN
greg=# INSERT INTO somi VALUES ('Volcano', 'jA0EBAMCV4e+-^', 'Phobos');
INSERT 0 1
greg=# INSERT INTO somi VALUES ('Son of a Son of a Sailor', 'H0qHJ3kMoVR7e', 'Proteus');
INSERT 0 1
greg=# INSERT INTO somi BALUES ('Xanadu', 'KaK/uxtgyT1ni', 'Metis');
ERROR:  syntax error at or near "BALUES"
LINE 1: INSERT INTO somi BALUES ('Xanadu', 'KaK/uxtgyT1ni'...
greg=# INSERT INTO somi VALUES ('Xanadu', 'KaK/uxtgyT1ni', 'Metis');
INSERT 0 1
greg=# commit;
COMMIT
greg=# select count(*) from somi;
 count
-------
     3
```

What about if you create a savepoint yourself? Or even a savepoint with the same name as the one that psql uses internally? Not a problem—Postgres allows multiple savepoints with the same name, and will rollback or release the latest one created, which allows ON_ERROR_ROLLBACK to work seamlessly with user-provided savepoints.

Note that the example above sets ON_ERROR_ROLLBACK (yes it is case sensitive!) to ‘interactive’, not just ‘on’. This is a good idea, as you generally want it to catch human errors, and not just plow through a SQL script.

So, if you want to add this to your own application, you will need to wrap each command in a hidden savepoint, and then rollback or release it. The end-user should not see the SAVEPOINT, ROLLBACK TO, or RELEASE commands. Thus, the SQL sent to the backend will change from this:

```
BEGIN; ## entered by the user
INSERT INTO somi VALUES ('Mr. Roboto', '3gNc841Rmy+a', 'Triton');
INSERT INTO somi VALUES ('A Mountain We Will Climb', 'O2DMZfqnfj8Tle', 'Tethys');
INSERT INTO somi BALUES ('Samba de Janeiro', 'W2rQpGU0MfIrm', 'Dione');
```

to this:

```
BEGIN; ## entered by the user
SAVEPOINT myapp_temporary_savepoint ## entered by the application
INSERT INTO somi VALUES ('Mr. Roboto', '3gNc841Rmy+a', 'Triton');
RELEASE myapp_temporary_savepoint

SAVEPOINT myapp_temporary_savepoint
INSERT INTO somi VALUES ('A Mountain We Will Climb', 'O2DMZfqnfj8Tle', 'Tethys');
RELEASE myapp_temporary_savepoint

SAVEPOINT myapp_temporary_savepoint
INSERT INTO somi BALUES ('Samba de Janeiro', 'W2rQpGU0MfIrm', 'Dione');
ROLLBACK TO myapp_temporary_savepoint
```

Here is some pseudo-code illustrating the sequence of events. To see the actual implementation in psql, take a look at bin/psql/common.c

```

run("SAVEPOINT myapp_temporary_savepoint");
run($usercommand);
if (txn_status == ERROR) {
  run("ROLLBACK TO myapp_temporary_savepoint");
}
if (command was "savepoint" or "release" or "rollback") {
  ## do nothing
}
elsif (txn_status == IN_TRANSACTION) {
  run("RELEASE myapp_temporary_savepoint");
}
```

While there is there some overhead in constantly creating and tearing down so many savepoints, it is quite small, especially if you are using it in an interactive session. This ability to automatically roll things back is especially powerful when you remember that Postgres can roll everything back, including DDL (e.g. CREATE TABLE). Certain other expensive database systems [do not play well when mixing DDL and transactions](https://wiki.postgresql.org/wiki/Transactional_DDL_in_PostgreSQL:_A_Competitive_Analysis).

 

