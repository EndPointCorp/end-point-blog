---
author: Greg Sabino Mullane
title: 'Perl+Postgres: changes in DBD::Pg 2.15.1'
github_issue_number: 182
tags:
- database
- open-source
- perl
- postgres
date: 2009-08-12
---

[DBD::Pg](https://metacpan.org/release/DBD-Pg), the Perl interface to [Postgres](https://www.postgresql.org/), recently released version 2.15.1. The last two weeks has seen a quick flurry of releases: 2.14.0, 2.14.1, 2.15.0, and 2.15.1. Per the usual versioning convention, the numbers on the far right (in this case the “dot one” releases) were simply bug fixes, while 2.14.0 and 2.15.0 introduced API and/or major internal changes. Some of these changes are explained below.

From the [Changes](https://fastapi.metacpan.org/source/TURNSTEP/DBD-Pg-2.15.1/Changes) file for 2.15.0:

```nohighlight
CHANGE:
 - Allow execute_array and bind_param_array to take oddly numbered items, 
   such that DBI will make missing entries undef/null (CPAN bug #39829) [GSM]
```

The Perl Database Interface (DBI) has a neat feature to allow you to execute many sets of items at one time, known as execute_array. The basic format is to pass in an list of arrays, in which each array contains the placeholders needed to execute the query. For example:

```perl
## Create a simple test table with two columns
$dbh->do('DROP TABLE IF EXISTS people');
$dbh->do('CREATE TABLE people (id int, fname text)');

## Pass in all ids as a single array
my @numbers = (1,2,3);

## Pass in all names as a single array
my @names = ("Garrett", "Viktoria", "Basso");

## Prepare the statement
my $sth = $dbh->prepare('INSERT INTO people VALUES (?, ?)');

## Execute the statement multiple times (three times in this case)
$sth->execute_array(undef, \@numbers, \@names);
## (the first argument is an optional argument hash which we don't use here)

## Pull back and display the rows from our new table
$SQL = 'SELECT id, fname FROM people ORDER BY fname';
for my $row (@{$dbh->selectall_arrayref($SQL)}) {
    print "Found: $row->[0] : $row->[1]\n";
}

$ perl testscript.pl
Found: 3 : Basso
Found: 1 : Garrett
Found: 2 : Viktoria
```

In 2.15.0, we loosened the requirement that the number of placeholders in each array match up with the expected number. Per the DBI spec, any “missing” items are considered undef, which maps to a SQL NULL. Thus:

```perl
$dbh->do('DROP TABLE IF EXISTS people');
$dbh->do('CREATE TABLE people (id int, fname text)');

## Note that this time there are only two ids given, not three:
my @numbers = (1,2);
my @names = ("Garrett", "Viktoria", "Basso");
my $sth = $dbh->prepare("INSERT INTO people VALUES (?, ?)");

$sth->execute_array(undef, \@numbers, \@names);

## Show a question mark for any null ids
$SQL = q{
SELECT CASE WHEN id IS NULL THEN '?' ELSE id::text END, fname 
FROM people ORDER BY fname
};
for my $row (@{$dbh->selectall_arrayref($SQL)}) {
    print "Found: $row->[0] : $row->[1]\n";
}

$ perl testscript2.pl
Found: ? : Basso
Found: 1 : Garrett
Found: 2 : Viktoria
```

Also note that bind_param_array is an alternate way to add the list of arrays before the execute is called. This is similar in concept to a regular execute: if you bind the values first, you can call execute without any arguments:

```perl
...
$sth->bind_param_array(1, \@numbers);
$sth->bind_param_array(2, \@names);
$sth->execute_array(undef);
...
```

-----------

```nohighlight
CHANGE:
 - Use PQexecPrepared even when no placeholders (CPAN bug #48155) [GSM]
```

Sending queries to Postgres via DBD::Pg usually involves two steps: prepare and execute. The prepare is done one time, while the execute can be called many times, often times with different arguments. Previously, DBD::Pg would call PQexec for queries that had no placeholders. However, the ability to handle placeholders smoothly is only one advantage of using server-side prepares in Postgres. The other advantage is that Postgres only has to parse the query a single time, in the initial prepare. In 2.15.0, we use PQexecPrepared for all queries, whether they have placeholders or not. The upshot of this is that multiple calls to the execute() function will be a little bit faster, and that we only use PQexec when we really have to.

-----------

```nohighlight
CHANGE:
 - Fix quoting of booleans to respect more Perlish variants (CPAN bug #41565) [GSM]
```

In previous versions, the mapping of Perl vars to booleans was very simple, and did only simple 0/1 mapping. However, Perl’s values of “truth” is richer than that. We can now do things like this:

```perl
for my $name ('0', '1', '0E0', '0 but true', 'F', 'T', 'TRUE', 'false') {
  printf qq{Value '%s' is %s\n}, $name, $dbh->quote($name, {pg_type => PG_BOOL});
}

$ perl testscript3.pl
Value '0' is FALSE
Value '1' is TRUE
Value '0E0' is TRUE
Value '0 but true' is TRUE
Value 'F' is FALSE
Value 'T' is TRUE
Value 'TRUE' is TRUE
Value 'false' is FALSE
```

-----------

```nohighlight
CHANGE:
  - Return ints and bools-cast-to-number from the db as true Perlish numbers.
    (CPAN bug #47619) [GSM]
```

This one is a little more subtle. When a value is returned from the database, it gets mapped back to a string. So even if the value in the database came from an INTEGER column, by the time it made it’s way back to your Perl script it was a string that happened to hold an integer value. DBD::Pg now attempts to cast some types to their Perl equivalent. This is normally hard to see without peering inside Perl internals, but using Data::Dumper can show you the difference:

```perl
## Ask Postgres to return a string and an integer
$SQL = 'SELECT 123::text, 123::integer';
$info = $dbh->selectall_arrayref($SQL)->[0];
print Dumper $info;

## Older versions of DBD::Pg give:
$VAR1 = [
          '123',
          '123'
        ];

## The new and improved version gives:
$VAR1 = [
          '123',
          123
        ];
```

A small difference, but not unimportant—​this change came about through a [bug request](https://rt.cpan.org/Public/Dist/Display.html?Name=DBD-Pg), as it was causing problems when DBD::Pg was interacting with [JSON::XS](https://stackoverflow.com/questions/1087308/why-cant-i-properly-encode-a-boolean-from-postgresql-via-jsonxs-via-perl). Special thanks to [Tim Bunce](https://blog.timbunce.org/), (author of DBI, maintainer of the amazing [NYTProf](https://metacpan.org/release/Devel-NYTProf), and all around Perl guru) who found an important bug regarding this solution in 2.14.0, which led to the quick release of 2.14.1. Lesson learned: don’t try converting ints to floats via sv_setnv.

-----------

Most of the other changes to 2.14 and 2.15 are bug fixes of one sort or another. To keep up on the changes or to talk about the project more, please join the [mailing list](https://www.nntp.perl.org/group/perl.dbd.pg/).
