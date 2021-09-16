---
author: Greg Sabino Mullane
title: Text sequences
github_issue_number: 187
tags:
- database
- perl
- postgres
date: 2009-08-20
---

Somebody recently asked on the [Postgres mailing list](https://www.postgresql.org/list/pgsql-general/) about "Generating random unique alphanumeric IDs". While there were some interesting solutions given, from a simple [Pl/pgsql function](https://www.postgresql.org/docs/current/static/plpgsql.html) to using mathematical transformations, I’d like to lay out a simple and powerful solution using [Pl/PerlU](https://www.postgresql.org/docs/current/static/plperl.html)

First, to paraphrase the original request, the poster needed a table to have a text column be its primary key, and to have a five-character alphanumeric string used as that key. Let’s knock out a quick function using Pl/PerlU that solves the generation part of the question:

```sql
DROP FUNCTION IF EXISTS nextvalalpha(TEXT);
CREATE FUNCTION nextvalalpha(TEXT)
RETURNS TEXT
LANGUAGE plperlu
AS $_$
  use strict;
  my $numchars = 5;
  my @chars = split // => qw/abcdefghijkmnpqrstwxyzABCDEFGHJKLMNPQRSTWXYZ23456789/;
  my $value = join '' => @chars[map{rand @chars}(1..$numchars)];
  return $value;
$_$;
```

Pretty simple: it simply pulls a number of random characters from a string 
(with some commonly confused letters and number removed) and returns a string:

```sql
greg=# SELECT nextvalalpha('foo');
 nextvalalpha
--------------
 MChNf
(1 row)

greg=# SELECT nextvalalpha('foo');
 nextvalalpha
--------------
 q4jHm
(1 row)
```

So let’s set up our test table. Since Postgres can use many things column DEFAULTS, including user-defined functions, this is pretty straightforward:

```sql
DROP TABLE IF EXISTS seq_test;
CREATE TABLE seq_test (
  id    VARCHAR(5) NOT NULL DEFAULT nextvalalpha('foo'),
  city  TEXT,
  state TEXT
);
```

A quick test shows that the id column is auto-propagated with some random values:

```sql
greg=#< PREPARE abc(TEXT,TEXT) AS INSERT INTO seq_test(city,state) 
greg=# VALUES($1,$2) RETURNING id;

greg=# EXECUTE abc('King of Prussia', 'Pennsylvania');
  id
-------
 9zbsd
(1 row)

INSERT 0 1

greg=# EXECUTE abc('Buzzards Bay', 'Massachusetts');
  id
-------
 4jJ5D
(1 row)

INSERT 0 1
```

So far so good. But while those returned values are random, they are not in any way unique, which a primary key needs to be. First, let’s create a helper table to keep track of which values we’ve already seen. We’ll also track the ‘name’ of the sequence as well, to allow for more than one unique set of sequences at a time:

```sql
DROP TABLE IF EXISTS alpha_sequence;
CREATE TABLE alpha_sequence (
  sname TEXT,
  value TEXT
);
CREATE UNIQUE INDEX alpha_sequence_unique_value ON alpha_sequence(sname,value);
```

Now we tweak the original function to use this new table.

```sql
CREATE OR REPLACE FUNCTION nextvalalpha(TEXT)
RETURNS TEXT
SECURITY DEFINER
LANGUAGE plperlu
AS $_$
  use strict;
  my $sname = shift;
  my @chars = split // => qw/abcdefghijkmnpqrstwxyzABCDEFGHJKLMNPQRSTWXYZ23456789/;
  my $numchars = 5;
  my $toomanyloops = 10000; ## Completely arbitrary pick
  my $loops = 0;

  my $SQL = 'SELECT 1 FROM alpha_sequence WHERE sname = $1 AND value = $2';
  my $sth = spi_prepare($SQL, 'text', 'text');

  my $value = '';
  SEARCHING:
  {
    ## Safety valve
    if ($loops++ >= $toomanyloops) {
      die "Could not find a unique value, even after $toomanyloops tries!\n";
    }
    ## Build a new value, then test it out
    $value = join '' => @chars[map{rand @chars}(1..$numchars)];
    my $count = spi_exec_prepared($sth,$sname,$value)->{processed};
    redo if $count >= 1;
  } 

  ## Store it and commit the change
  $SQL = 'INSERT INTO alpha_sequence VALUES ($1,$2)';
  $sth = spi_prepare($SQL, 'text', 'text');
  spi_exec_prepared($sth,$sname,$value);
  return $value;
$_$;
```

Alright, that seems to work well, and prevents duplicate values. Or does it? Recall that one of the properties of [sequences in Postgres](https://www.postgresql.org/docs/current/static/functions-sequence.html) is that they live outside of the normal MVCC rules. In other words, once you get a number via a call to nextval(), nobody else can get that number again (even you!)—​regardless of whether you commit or rollback. Thus, sequences are guaranteed unique across all transactions and sessions, even if used for more than one table, called manually, etc. Can we do the same with our text sequence? Yes!

For this trick, we’ll need to ensure that we only return a new value if we are 100% sure it is unique. We also need to record the value returned, even if the transaction that calls it rolls back. In other words, we need to make a small ‘subtransaction’ that commits, regardless of the rest of the transaction. Here’s the solution:

```sql
CREATE OR REPLACE FUNCTION nextvalalpha(TEXT)
RETURNS TEXT
SECURITY DEFINER
LANGUAGE plperlu
AS $_$
  use strict;
  use DBI;
  my $sname = shift;
  my @chars = split // => qw/abcdefghijkmnpqrstwxyzABCDEFGHJKLMNPQRSTWXYZ23456789/;
  my $numchars = 5;
  my $toomanyloops = 10000;
  my $loops = 0;

  ## Connect to this very database, but with a new session
  my $port = spi_exec_query('SHOW port')->{rows}[0]{port};
  my $dbname = spi_exec_query('SELECT current_database()')->{rows}[0]{current_database};
  my $dbuser = spi_exec_query('SELECT current_user')->{rows}[0]{current_user};
  my $dsn = "dbi:Pg:dbname=$dbname;port=$port";
  my $dbh = DBI->connect($dsn, $dbuser, '', {AutoCommit=>1,RaiseError=>1,PrintError=>0});

  my $SQL = 'SELECT 1 FROM alpha_sequence WHERE sname = ? AND value = ?';
  my $sth = $dbh->prepare($SQL);

  my $value = '';
  SEARCHING:
  {
    ## Safety valve
    if ($loops++ >= $toomanyloops) {
      die "Could not find a unique value, even after $toomanyloops tries!\n";
    }
    ## Build a new value, then test it out
    $value = join '' => @chars[map{rand @chars}(1..$numchars)];
    my $count = $sth->execute($sname,$value);
    $sth->finish();
    redo if $count >= 1;
  } 

  ## Store it and commit the change
  $SQL = 'INSERT INTO alpha_sequence VALUES (?,?)';
  $sth = $dbh->prepare($SQL);
  $sth->execute($sname,$value); ## Does a commit

  ## Only now do we return the value to the caller
  return $value;
$_$;
```

What’s the big difference between this one and the previous version? Rather than examine the alpha_sequence table in our /current/ session, we figure out who and where we are, and make a completely separate connection to the same database using DBI. Then we find an unused value, INSERT that value into the alpha_sequence table, and commit that outside of our current transaction.Only then can we return the value to the caller.

Postgres sequences also have a currval() function, which returns the last value returned via a nextval() in the current session. The lastval() function is similar, but it returns the last call to nextval(), regardless of the name used. We can make a version of these easy enough, because Pl/Perl functions have a built-in shared hash named ‘%_SHARED’. Thus, we’ll add two new lines to the end of the function above:

```perl
...
  $sth->execute($sname,$value); ## Does a commit
  $_SHARED{nva_currval}{$sname} = $value;
  $_SHARED{nva_lastval} = $value;
...
```

Then we create a simple function to display that value, as well as throw an error if called too early—​just like nextval() does:

```sql
DROP FUNCTION IF EXISTS currvalalpha(TEXT)
CREATE FUNCTION currvalalpha(TEXT)
RETURNS TEXT
SECURITY DEFINER
LANGUAGE plperlu
AS $_$
  my $sname = shift;
  if (exists $_SHARED{nva_currval}{$sname}) {
    return $_SHARED{nva_currval}{$sname};
  }
  else {
    die qq{currval of text sequence "$sname" is not yet defined in this session\n};
  }
$_$;
```

Now the lastval() version:

```sql
DROP FUNCTION IF EXISTS lastvalalpha();
CREATE FUNCTION lastvalalpha()
RETURNS TEXT
SECURITY DEFINER
LANGUAGE plperlu
AS $_$
  if (exists $_SHARED{nva_lastval}) {
    return $_SHARED{nva_lastval};
  }
  else {
    die qq{lastval (text) is not yet defined in this session\n};
  }
$_$;
```

For the next tests, we’ll create a normal (integer) sequence, and see how it acts compared to our newly created text sequence:

```sql
DROP SEQUENCE IF EXISTS newint;
CREATE SEQUENCE newint STARTS WITH 42;

greg=# SELECT lastval();
ERROR: lastval is not yet defined in this session

greg=# SELECT currval('newint');
ERROR:  currval of sequence "newint" is not yet defined in this session

greg=# SELECT nextval('newint');
 nextval
---------
      42
(1 row)

greg=# SELECT currval('newint');
 currval
---------
      42

greg=# SELECT lastval();
 lastval
---------
      42
```

```sql
greg=# SELECT lastvalalpha();
ERROR: error from Perl function "lastvalalpha": lastval (text) is not yet defined in this session

greg=# SELECT currvalalpha('newtext');
ERROR:  error from Perl function "currvalalpha": currval of text sequence "newtext" is not yet defined in this session

greg=# SELECT nextvalalpha('newtext');
 nextvalalpha
--------------
 rRwJ6

greg=# SELECT currvalalpha('newtext');
 currvalalpha
--------------
 rRwJ6

greg=# SELECT lastvalalpha();
 lastvalalpha
--------------
 rRwJ6
```

There is one more quick optimization we could make. Since the %_SHARED hash is available across our session, there is no need to do anything in the function more than once if we can cache it away. In this case, we’ll cache away the server information we look up, the database handle, and the prepares. Our final function looks like this:

```sql
CREATE OR REPLACE FUNCTION nextvalalpha(TEXT)
RETURNS TEXT
SECURITY DEFINER
LANGUAGE plperlu
AS $_$
  use strict;
  use DBI;
  my $sname = shift;
  my @chars = split // => qw/abcdefghijkmnpqrstwxyzABCDEFGHJKLMNPQRSTWXYZ23456789/;
  my $numchars = 5;
  my $toomanyloops = 10000;
  my $loops = 0;

  ## Connect to this very database, but with a new session
  if (! exists $_SHARED{nva_dbi}) {
    my $port = spi_exec_query('SHOW port')->{rows}[0]{port};
      my $dbname = spi_exec_query('SELECT current_database()')->{rows}[0]{current_database};
    my $dbuser = spi_exec_query('SELECT current_user')->{rows}[0]{current_user};
    my $dsn = "dbi:Pg:dbname=$dbname;port=$port";
    $_SHARED{nva_dbi} = DBI->connect($dsn, $dbuser, '', {AutoCommit=>1,RaiseError=>1,PrintError=>0});
    my $dbh = $_SHARED{nva_dbi};
    my $SQL = 'SELECT 1 FROM alpha_sequence WHERE sname = ? AND value = ?';
    $_SHARED{nva_sth_check} = $dbh->prepare($SQL);
    $SQL = 'INSERT INTO alpha_sequence VALUES (?,?)';
    $_SHARED{nva_sth_add} = $dbh->prepare($SQL);
  }

  my $value = '';
  SEARCHING:
  {
    ## Safety valve
    if ($loops++ >= $toomanyloops) {
      die "Could not find a unique value, even after $toomanyloops tries!\n";
    }
    ## Build a new value, then test it out
    $value = join '' => @chars[map{rand @chars}(1..$numchars)];
    my $count = $_SHARED{nva_sth_check}->execute($sname,$value);
    $_SHARED{nva_sth_check}->finish();
    redo if $count >= 1;
  } 

  ## Store it and commit the change
  $_SHARED{nva_sth_add}->execute($sname,$value); ## Does a commit
  $_SHARED{nva_currval}{$sname} = $value;
  $_SHARED{nva_lastval} = $value;
  return $value;
$_$;
```

Having the ability to reach outside the database in Pl/PerlU—​even if simply to go back in again!—​can be a powerful tool, and allows us to do things that might otherwise seem impossible.
