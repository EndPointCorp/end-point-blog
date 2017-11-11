---
author: Greg Sabino Mullane
gh_issue_number: 1065
tags: bucardo, postgres, replication
title: Bucardo replication trigger enabling
---

<div class="separator" style="clear: both; margin-bottom: 1em; float: right; text-align: center;"><a href="/blog/2014/12/22/bucardo-replication-trigger-enabling/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/12/22/bucardo-replication-trigger-enabling/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/7MuYEP">Armadillo</a> by <a href="https://www.flickr.com/photos/chrisvandyck/">Chris van Dyck</a></small></div>

[Bucardo](http://bucardo.org/) is one of the trigger-based replication systems for Postgres (others include Slony and Londiste). All of these not only use triggers to gather information on what has changed, but they also disable triggers when copying things to remote databases. They do this to ensure that only the data itself gets copied, in as fast as manner as possible. This also has the effect of disabling foreign keys, which Postgres implements by use of triggers on the underlying tables. There are times, however, when you need a trigger on a target to fire (such as data masking). Here are four approaches to working around the disabling of triggers. The first two solutions will work with any replication system, but the third and fourth are specific to Bucardo.

First, let's understand how the triggers get disabled. A long time ago (Postgres 8.2 and older), triggers had to be disabled by direct changes to the system catalogs. Luckily, those days are over, and now this is done by issuing this command before copying any data:

```
SET session_replication_role = 'replica';
```

This prevents all normal triggers and rules from being activated. There are times, however, when you want certain triggers (or their effects) to execute during replication.

Let's use a simple hypothetical to illustrate all of these solutions. We will start with the Postgres built-in [pgbench utility](https://wiki.postgresql.org/wiki/Pgbench), The initialize option (**-i**) can be used to create and populate some tables:

```
$ createdb btest1
$ pgbench -i btest1
NOTICE:  table "pgbench_history" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_branches" does not exist, skipping
creating tables...
100000 of 100000 tuples (100%) done (elapsed 0.16 s, remaining 0.00 s).
vacuum...
set primary keys...
done.
```

We want to replicate all four of the tables pgbench just created. Bucardo requires that a table have a primary key or a unique index to be replicated, so we will need to make an immediate adjustment to the **pgbench_history** table:

```
$ psql btest1 -c 'ALTER TABLE pgbench_history ADD hid SERIAL PRIMARY KEY'
ALTER TABLE
```

Now to make things a little more interesting. Let's add a new column to the **pgbench_accounts** table named "phone", which will hold the account owner's phone number. As this is confidential information, we do not want it to be available - except on the source database! For this example, database btest1 will be the source, and database btest2 will be the target.

```
$ psql btest1 -c 'ALTER TABLE pgbench_accounts ADD phone TEXT'
ALTER TABLE
$ createdb btest2 --template=btest1
```

To prevent the phone number from being revealed to anyone querying btest2, a trigger and supporting function is used to change the phone number to always display the word 'private'. Here is what they look like.

```
btest2=# CREATE OR REPLACE FUNCTION elide_phone()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $bc$
BEGIN
  NEW.phone = 'private';
  RETURN NEW;
END;
$bc$;
CREATE FUNCTION

btest2=# CREATE TRIGGER elide_phone
  BEFORE INSERT OR UPDATE
  ON pgbench_accounts
  FOR EACH ROW
  EXECUTE PROCEDURE elide_phone();
CREATE TRIGGER
```

Now that everything is setup, we can install Bucardo and teach it how to replicate those tables:

```
$ bucardo install
This will install the bucardo database into ...
...
Installation is now complete.

$ bucardo add db A,B dbname=btest1,btest2
Added databases "A","B"

$ bucardo add sync pgb dbs=A,B tables=all
Added sync "pgb"
Created a new relgroup named "pgb"
Created a new dbgroup named "pgb"
  Added table "public.pgbench_accounts"
  Added table "public.pgbench_branches"
  Added table "public.pgbench_history"
  Added table "public.pgbench_tellers"

$ bucardo start
```

A demonstration of the new trigger is now in order. On the database btest2, we will update a few rows and attempt to set the phone number. However, our new trigger will overwrite our changes:

 Jenny
```
$ psql btest2 -c "update pgbench_accounts set abalance=123, phone='867-5309' where aid <= 3"
UPDATE 3

$ psql btest2 -c 'select aid,abalance,phone from pgbench_accounts order by aid limit 3'
 aid | abalance |  phone
-----+----------+---------
   1 |      123 | private
   2 |      123 | private
   3 |      123 | private
```

So, all is as we expected: any changes made to this table have the phone number changed. Let's see what happens when the changes are done via Bucardo replication. Note that we are updating btest1 but querying btest2:

```
$ psql btest1 -c "update pgbench_accounts set abalance=99, phone='867-5309' WHERE aid <= 3"
UPDATE 3

$ psql btest2 -c 'select aid,abalance,phone from pgbench_accounts order by aid limit 3'
 aid | abalance |  phone
-----+----------+----------
   1 |       99 | 867-5309
   2 |       99 | 867-5309
   3 |       99 | 867-5309
```

As you can see, our privacy safeguard is gone, as Bucardo disables the trigger on btest2 before making the changes. So what can we do? There are four solutions: set the trigger as ALWAYS, set the trigger as REPLICA, use Bucardo's customcode feature, or use Bucardo's customcols feature.

## Solution one: ALWAYS trigger

The easiest way is to simply mark the trigger as ALWAYS, which means that it will always fire, regardless of what session_replication_role is set to. This is the best solution for most problems of this sort. Changing the trigger requires an ALTER TABLE command. Once done, psql will show you the new state of the trigger as well:

```
btest2=# \d pgbench_accounts
   Table "public.pgbench_accounts"
  Column  |     Type      | Modifiers
----------+---------------+-----------
 aid      | integer       | not null
 bid      | integer       |
 abalance | integer       |
 filler   | character(84) |
 phone    | text          |
Indexes:
    "pgbench_accounts_pkey" PRIMARY KEY, btree (aid)
Triggers:
    elide_phone BEFORE INSERT OR UPDATE ON pgbench_accounts FOR EACH ROW EXECUTE PROCEDURE elide_phone()

btest2=# ALTER TABLE pgbench_accounts ENABLE ALWAYS TRIGGER elide_phone;
ALTER TABLE

btest2=# \d pgbench_accounts
   Table "public.pgbench_accounts"
  Column  |     Type      | Modifiers
----------+---------------+-----------
 aid      | integer       | not null
 bid      | integer       |
 abalance | integer       |
 filler   | character(84) |
 phone    | text          |
Indexes:
    "pgbench_accounts_pkey" PRIMARY KEY, btree (aid)
Triggers firing always:
    elide_phone BEFORE INSERT OR UPDATE ON pgbench_accounts FOR EACH ROW EXECUTE PROCEDURE elide_phone()
```

That is some ugly syntax for changing the triggers, eh? (To restore a trigger to its default state, you would simply leave out the ALWAYS clause, so it becomes ***ALTER TABLE pgbench_accounts ENABLE TRIGGER elide_phone***). Time to verify that the ALWAYS trigger fires even when Bucardo is updating the table:

 Who ya gonna call?
```
$ psql btest1 -c "update pgbench_accounts set abalance=11, phone='555-2368' WHERE aid <= 3"
UPDATE 3

$ psql btest2 -c 'select aid,abalance,phone from pgbench_accounts order by aid limit 3'
 aid | abalance |  phone
-----+----------+----------
   1 |       11 | private
   2 |       11 | private
   3 |       11 | private
```

## Solution two: REPLICA trigger

Trigger-based replication solutions, you may recall from above, issue this command: ***SET session_replication_role = 'replica'***. What this means is that all rules and triggers that are *not* of type replica are skipped (with the exception of always triggers of course). Thus, another solution is to set the triggers you want to fire to be of type "replica". Once you do this, however, the triggers will NOT fire in ordinary use - so be careful. Let's see it in action:

```
btest2=# ALTER TABLE pgbench_accounts ENABLE REPLICA TRIGGER elide_phone;
ALTER TABLE

btest2=# \d pgbench_accounts
   Table "public.pgbench_accounts"
  Column  |     Type      | Modifiers
----------+---------------+-----------
 aid      | integer       | not null
 bid      | integer       |
 abalance | integer       |
 filler   | character(84) |
 phone    | text          |
Indexes:
    "pgbench_accounts_pkey" PRIMARY KEY, btree (aid)
Triggers firing on replica only:
    elide_phone BEFORE INSERT OR UPDATE ON pgbench_accounts FOR EACH ROW EXECUTE PROCEDURE elide_phone()
```

As before, we can test it out and verify the trigger is firing:

 Freeze, Vegan Police!
```
$ psql btest1 -c "update pgbench_accounts set abalance=22, phone='664-7665' WHERE aid <= 3"
UPDATE 3

$ psql btest2 -c 'select aid,abalance,phone from pgbench_accounts order by aid limit 3'
 aid | abalance |  phone
-----+----------+----------
   1 |       22 | private
   2 |       22 | private
   3 |       22 | private
```

## Solution three: Bucardo customcode

Bucardo supports a number of hooks into the replication process. These are called "customcodes" and consist of Perl code that is invoked by Bucardo. To solve the problem at hand, we will create some code for the "code_before_trigger_enable" hook - in other words, right after the actual data copying is performed. To create the customcode, we write the actual code to a text file, then do this:

```
$ bucardo add code nophone whenrun=before_trigger_enable sync=pgb src_code=./nophone.pl
```

This creates a new customcode named "nophone" that contains the code inside the local file "nophone.pl". It runs after the replication, but before the triggers are re-enabled. It is associated with the sync named "pgb". The content of the file looks like this:

```
my $info = shift;

return if ! exists $info->{rows};

my $schema = 'public';
my $table = 'pgbench_accounts';
my $rows = $info->{rows};
if (exists $rows->{$schema} and exists $rows->{$schema}{$table}) {
  my $dbh = $info->{dbh}{B};
  my $SQL = "UPDATE $schema.$table SET phone=? "
    . "WHERE aid = ? AND phone <> ?";
  my $sth = $dbh->prepare($SQL);
  my $string = 'private';
  for my $pk (keys %{ $rows->{$schema}{$table} }) {
    $sth->execute($string, $pk, $string);
  }
}
return;
```

Every customcode is passed a hashref of information from Bucardo. One of the things passed in a list of changed rows. At the top, we see that we exit right away (via return, as the customcodes become Perl subroutines) if there are no rows this round. Then we check that something has changed for the pgbench_accounts tables. We grab the database handle, also passed to the subroutine. Note that this is actually a [DBIx::Safe handle](http://search.cpan.org/dist/DBIx-Safe/Safe.pm), not a direct DBI handle. The difference is that certain operations, such as commit, are not allowed.

Once we have the handle, we walk through all the rows that have changed, and set the phone to something safe. The above code is a good approach, but we can make the UPDATE much smarter because we are using a modern Postgres which supports ANY, and a modern [DBD::Pg](https://metacpan.org/pod/DBD::Pg) that supports passing Perl arrays in and out. Once we combine those two, we can move the execute() out of the loop into a single call like so:

```
...
if (exists $rows->{$schema} and exists $rows->{$schema}{$table}) {
  my $dbh = $info->{dbh}{B};
  my $SQL = "UPDATE $schema.$table SET phone=?"
    . "WHERE aid = ANY(?) AND phone <> ?";
  my $sth = $dbh->prepare($SQL);
  my $string = 'private';
  $sth->execute($string, [ keys %{ $rows->{$schema}{$table} } ], $string);
}
```

Note that this solution requires Bucardo version 5.3.0 or better. Let's verify it:

 800-588-2300, Em-pire!
```
$ psql btest1 -c "update pgbench_accounts set abalance=33, phone='588-2300' WHERE aid <= 3"
UPDATE 3

$ psql btest2 -c 'select aid,abalance,phone from pgbench_accounts order by aid limit 3'
 aid | abalance |  phone
-----+----------+----------
   1 |       33 | private
   2 |       33 | private
   3 |       33 | private
```

## Solution four: Bucardo customcols

The final way to keep the information in that column masked is to use Bucardo's 'customcols' feature. This allows rewriting of the command that grabs rows from the source databases.  Bucardo uses COPY to grab rows from a source, DELETE to remove the rows if they exist on the target, and another COPY to add the rows to the target tables. Postgres supports adding a SELECT clause to a COPY command, as we will see below. To hide the values of the phone column using the customcols feature, we simply do:

```
$ bucardo add customcols public.pgbench_accounts "select aid,bid,abalance,filler,'private' as phone" db=B sync=pgb
New columns for public.pgbench_accounts: "select aid,bid,abalance,filler,'private' as phone" (for database B) (for sync pgb)
```

The list of columns must be the same as in the original table, but we can modify things! So rather than Bucardo doing this:

```
COPY (SELECT * FROM public.pgbench_accounts WHERE aid IN (1,2,3)) TO STDOUT
```

Bucardo will instead do this thanks to our customcols:

```
COPY (SELECT aid,bid,abalance,filler,'private' as phone FROM public.pgbench_accounts WHERE aid IN (1,2,3)) TO STDOUT
```

Let's verify it:

 Glenn Miller hit
```
$ psql btest1 -c "update pgbench_accounts set abalance=44, phone='736-5000' WHERE aid <= 3"
UPDATE 3

$ psql btest2 -c 'select aid,abalance,phone from pgbench_accounts order by aid limit 3'
 aid | abalance |  phone
-----+----------+----------
   1 |       44 | private
   2 |       44 | private
   3 |       44 | private
```

Those are the four approaches to firing (or emulating) triggers when using replication. Which one you choose depends on what exactly your trigger does, but overall, the best solution is probably the 'trigger ALWAYS', followed by 'Bucardo customcols'. If you have another solution, or some problem that is not covered by the above, please let me know in the comments.
