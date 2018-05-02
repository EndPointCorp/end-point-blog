---
author: Greg Sabino Mullane
gh_issue_number: 986
tags: database, dbdpg, postgres
title: DBD::Pg, array slices, and pg_placeholder_nocolons
---



<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/05/25/dbdpg-array-slices-and/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/25/dbdpg-array-slices-and/image-0.jpeg"/></a>
<br/><small><a href="https://flic.kr/p/eszxcS">Howler monkey</a> by <a href="https://www.flickr.com/photos/83713276@N03/">Miguel Rangel Jr</a></small></div>

New versions of [DBD::Pg](http://search.cpan.org/dist/DBD-Pg), the Perl driver for PostgreSQL, have been recently released. In addition to some bug fixes, the handling of colons inside SQL statements has been improved in version 3.2.1, and a new attribute named **pg_placeholder_nocolons** was added by Graham Ollis in version 3.2.0. Before seeing it in action, let’s review the concept of [placeholders](http://search.cpan.org/dist/DBD-Pg/Pg.pm#Placeholders) in DBI and DBD::Pg.

Placeholders allow you store a dummy representation of a value inside your SQL statement. This means you can prepare a SQL statement in advance without specific values, and fill in the values later when it is executed. The two main advantages to doing it this way are to avoid worrying about quoting, and to re-use the same statement with different values. DBD::Pg allows for three styles of placeholders: question mark, dollar sign, and named parameters (aka colons). Here’s an example of each:

```sql
$SQL = 'SELECT tbalance FROM pgbench_tellers WHERE tid = ? AND bid = ?';
$sth = $dbh->prepare($SQL);
$sth->execute(12,33);

$SQL = 'SELECT tbalance FROM pgbench_tellers WHERE tid = $1 AND bid = $2';
$sth = $dbh->prepare($SQL);
$sth->execute(12,33);

$SQL = 'SELECT tbalance FROM pgbench_tellers WHERE tid = :teller AND bid = :bank';
$sth = $dbh->prepare($SQL);
$sth->bind_param(':teller', 10);
$sth->bind_param(':bank', 33);
$sth->execute()
```

One of the problems with placeholders is that the symbols used are not exclusive for DBI only, but can be valid SQL characters as well, with their own special meaning. For example, question marks are used by [geometric operators](http://www.postgresql.org/docs/current/interactive/functions-geometry.html), dollar signs are used in Postgres for 
[dollar quoting](http://www.postgresql.org/docs/current/interactive/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING), and colons are used for both [type casts](https://www.postgresql.org/docs/current/interactive/sql-expressions.html#SQL-SYNTAX-TYPE-CASTS) and [array slices](https://www.postgresql.org/docs/current/interactive/arrays.html). DBD::Pg has a few ways to solve these problems.

Question marks are the preferred style of placeholders for many users of DBI (as well as some other systems). They are easy to visualize and great for simple queries. However, question marks can be used as operators inside of Postgres. To get around this, you can use the handle attribute 
[pg_placeholder_dollaronly](http://search.cpan.org/dist/DBD-Pg/Pg.pm#pg_placeholder_dollaronly_%28boolean%29), which will ignore any placeholders other than dollar signs:

 

```perl
## Fails:
$SQL="SELECT ?- lseg'((-1,0),(1,0))' FROM pg_class WHERE relname = \$1";
$sth = $dbh->prepare($SQL);
## Error is: Cannot mix placeholder styles "?" and "$1"

## Works:
$dbh->{pg_placeholder_dollaronly} = 1;
$sth = $dbh->prepare($SQL);
$sth->execute('foobar');
## For safety:
$dbh->{pg_placeholder_dollaronly} = 0;
```

Another good form of placeholder is the dollar sign. Postgres itself uses dollar signs for 
[its prepared queries](https://www.postgresql.org/docs/current/static/sql-prepare.html). DBD::Pg will actually transform the question mark and colon versions to dollar signs internally before sending the query off to Postgres to be prepared. A big advantage of using dollar sign placeholders is the re-use of parameters. Dollar signs have two problems: first, Perl uses them as a [sigil](https://en.wikipedia.org/wiki/Sigil_%28computer_programming%29), Postgres uses them for dollar quoting. However, DBD::Pg is smart enough to tell the difference between dollar quoting and dollar-sign placeholders, so dollar signs as placeholders should always simply work.

The final form of placeholder is ‘named parameters’ or simply ‘colons’. In this format, an alphanumeric string comes right after a colon to “name” the parameter. The main advantage to this form of placeholder is the ability to bind variables by name in your code. The downside is that colons are used by Postgres for both type casting and array slices. The type casting (e.g. 123::int) is detected by DBD::Pg and is not a problem. The detection of array slices was improved in 3.2.1, such that a number-colon-number sequence is never interpreted as a placeholder. However, there are many other ways to write array slices. Therefore, the **pg_placeholder_nocolons** attribute was invented. When activated, it effectively turns off the use of named parameters:

```perl
## Works:
$SQL = q{SELECT relacl[1:2] FROM pg_class WHERE relname = ?};
$sth = $dbh->prepare($SQL);
$sth->execute('foobar');

## Fails:
$SQL = q{SELECT relacl[1 :2] FROM pg_class WHERE relname = ?};
$sth = $dbh->prepare($SQL);
## Error is: Cannot mix placeholder styles ":foo" and "?"

## Works:
$dbh->{pg_placeholder_nocolons} = 1;
$SQL = q{SELECT relacl[1 :2] FROM pg_class WHERE relname = ?};
$sth = $dbh->prepare($SQL);
$sth->execute('foobar');
```

Which placeholder style you use is up to you (or your framework / supporting module!), but there should be enough options now between **pg_placeholder_dollaronly** and **pg_placeholder_nocolons** to support your style peacefully.


