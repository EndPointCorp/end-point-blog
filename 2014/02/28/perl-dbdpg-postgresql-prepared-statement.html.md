---
author: Greg Sabino Mullane
gh_issue_number: 935
tags: dbdpg, perl, postgres
title: DBD::Pg prepared statement change
---



One of the changes in the recently released [DBD::Pg version 3](http://blog.endpoint.com/2014/02/perl-postgresql-driver-dbdpg-300.html) (in addition to the [big utf8 change](http://blog.endpoint.com/2014/02/dbdpg-utf-8-perl-postgresql.html)), is the addition of a new attribute, **pg_switch_prepared**. This accompanies a behavior change in the use of prepare/execute. DBD::Pg will now postpone creating a server-side PREPARE statement until the second time a query is run via the execute() method.

Technically, DBD::Pg will use **PQexecParams** (part of the underlying libpq system that DBD::Pg uses) the first time a statement is executed, and switch to using **PQexecPrepared** the second time the statement is executed (by calling **PQprepare** first). When it actually switches is controlled by the pg_switch_prepared attribute, which defaults to 2 (the behavior above). You can set it to 0 or 1 to always use PQexecPrepared (as the older versions did), or you can set it to -1 to always use PQexecParams and avoid creating prepared statements entirely.

The typical flow of events in a DBI script is to create a statement handle via the prepare() method, then call the execute() time with varying arguments as many times as needed.

```
#!perl

use strict;
use warnings;
use DBI;

my $DSN = 'DBI:Pg:dbname=postgres';
my $dbh = DBI->connect($DSN, '', '', {AutoCommit=>0,RaiseError=>1,PrintError=>0})
  or die "Connection failed!\n";
print "DBI is version $DBI::VERSION, DBD::Pg is version $DBD::Pg::VERSION\n";

## We do this so we can see the version number in the logs
my $SQL = 'SELECT ?::text';
$dbh->do($SQL, undef, "DBD::Pg version $DBD::Pg::VERSION");

my $sth = $dbh->prepare('SELECT count(*) FROM pg_class WHERE relname = ?');
$sth->execute('foobar1');
$sth->execute('foobar2');
$sth->execute('foobar3');

```

When the script above is run on DBD::Pg versions 2.19.1 and 3.0.0, you can see the difference:

```

LOG:  execute <unnamed>: SELECT $1::text
DETAIL:  parameters: $1 = 'DBD::Pg version 2.19.1'
LOG:  execute dbdpg_p30462_1: SELECT count(*) FROM pg_class WHERE relname = $1
DETAIL:  parameters: $1 = 'foobar1'
LOG:  execute dbdpg_p30462_1: SELECT count(*) FROM pg_class WHERE relname = $1
DETAIL:  parameters: $1 = 'foobar2'
LOG:  execute dbdpg_p30462_1: SELECT count(*) FROM pg_class WHERE relname = $1
DETAIL:  parameters: $1 = 'foobar3'

LOG:  execute <unnamed>: SELECT $1::text
DETAIL:  parameters: $1 = 'DBD::Pg version 3.0.0'
LOG:  execute <unnamed>: SELECT count(*) FROM pg_class WHERE relname = $1
DETAIL:  parameters: $1 = 'foobar1'
LOG:  execute dbdpg_p30618_1: SELECT count(*) FROM pg_class WHERE relname = $1
DETAIL:  parameters: $1 = 'foobar2'
LOG:  execute dbdpg_p30618_1: SELECT count(*) FROM pg_class WHERE relname = $1
DETAIL:  parameters: $1 = 'foobar3'

```

As you can see, the do() method always uses PQexecParams (this is what creates the "<unnamed>" statement seen in the logs). For the prepare/execute section, the older versions issued an implicit prepare right away, while 3.0.0 uses an unnamed statement for the first iteration, and only when called more than once switches to a named prepared statement. The use of PQexecParams is faster than doing a PQprepare plus a PQexecParams, but if you are going to execute the same query a number of times, it is more efficient to simply send the arguments via PQexecPrepared and absorb the one-time cost of creating the statement via PQprepare.

What does this mean for users of DBD::Pg? Probably nothing, as the new default is already a decent compromise, but it's good to know about the pg_switch_prepared knob, that is there if you need it.


