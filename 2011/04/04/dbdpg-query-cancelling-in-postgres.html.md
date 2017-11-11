---
author: Greg Sabino Mullane
gh_issue_number: 438
tags: database, dbdpg, perl, postgres
title: DBD::Pg query cancelling in Postgres
---



A new version of DBD::Pg, the Perl driver for PostgreSQL, has [just been released](http://archives.postgresql.org/pgsql-announce/2011-03/msg00021.php). In addition to fixing some memory leaks and other minor bugs, this release (version 2.18.0) introduces support for the DBI method known as **cancel()**. A giant thanks to Eric Simon, who wrote this new feature. The new method is similar to the existing **pg_cancel()** method, except it works on synchronous rather than asynchronous queries. I'll show an example of both below.

DBD::Pg has been able to handle asynchronous queries for a while now. Basically, that means you don't have to wait around for the database to finish a query. Your application can do other things while the query runs, then check back later to see if it has completed and grab the results. The way to cancel an already kicked-off asynchronous query is with the **pg_cancel()** method (the other asynchronous methods are **pg_ready** and **pg_result**, which have no synchronous equivalents).

The prefix "**pg_**" is used because there is no corresponding built-in DBI method to override, and the convention is to prefix everything custom to a driver with the driver's prefix, in our case 'pg'. Here's an example showing one possible use of asynchronous queries using DBD::Pg in some Perl code:

```perl
  ## We are connecting to two servers and running expensive 
  ## queries on both. We kick both off right away, then wait 
  ## for them both to finish. Our total wait time is thus
  ## max(server1,server2) rather than sum(server1,server2)

  use strict;
  use warnings;
  use DBI;
  use DBD::Pg qw{ :async };

  my $dsn1 = 'dbi:Pg:dbname=sales;host=example1.com';
  my $dsn2 = 'dbi:Pg:dbname=sales;host=example2.com';

  my $dbh1 = DBI->connect($dsn1, '', '', {AutoCommit=>0, RaiseError=>1});
  my $dbh2 = DBI->connect($dsn2, '', '', {AutoCommit=>0, RaiseError=>1});

  my $SQL = 'SELECT gather_yearly_sales_data()';
  print "Kicking off a long, expensive query on database one\n";
  ## Normally, a do() will not return until the query is complete
  ## However, the async flag causes it to return immediately
  $dbh1->do($SQL, {pg_async => PG_ASYNC});

  print "Kicking off a long, expensive query on database two\n";
  $dbh2->do($SQL, {pg_async => PG_ASYNC});

  ## Both queries are running in the 'background'
  ## We have to wait for both, so it doesn't matter which one we wait for here
  ## However, if it's been over 2 minutes, we'll cancel both and quit
  my $time = 0;
  while ( ! $dbh1->pg_ready() ) {
    sleep 1;
    if ($time++ > 120) {
      print "Taking too long, let's cancel the queries\n";
      $dbh1->pg_cancel();
      $dbh2->pg_cancel();
      $dbh1->rollback();
      $dbh2->rollback();
      die "No sales data was retrieved\n";
    }
  }

  ## We know that database 1 has finished, so we read in the results
  my $rows1 = $dbh1->pg_result();
  ## We then grab results from database 2
  ## This will block until done, which is okay
  my $rows2 = $dbh2->pg_result();
```

The new method, simply known as **cancel()**, will kill any synchronously running query. One of the main uses for this is to timeout a query by using the builtin Perl **alarm** function. However, since the builtin alarm function has some quirks, we will instead use the much safer [POSIX::SigAction](http://perldoc.perl.org/POSIX.html) method. Another example:

```perl
  ## We are running a series of queries against a database, but if
  ## the whole thing is taking over 30 seconds, we want to cancel
  ## the currently running query and move on to something else.

  use strict;
  use warnings;
  use DBI;
  use DBD::Pg qw{ :async };

  my $dsn = 'dbi:Pg:dbname=dq';

  my $dbh = DBI->connect($dsn, '', '', {AutoCommit=>0, RaiseError=>1});

  ## Setup all the POSIX alarm plumbing
  my $mask = POSIX::SigSet->new(SIGALRM);
  my $action = POSIX::SigAction->new(
    sub { die "TIMEOUT\n" },
    $mask,
  );
  my $oldaction = POSIX::SigAction->new();
  sigaction( SIGALRM, $action, $oldaction );

  ## Prepare the queries
  my $upd = $dbh->prepare('UPDATE foobar SET x=? WHERE y=?');
  my $inv = $dbh->prepare('SELECT refresh_inventory(?)');

  ## Yes, a double eval. Async is looking better all the time :)
  eval {
    eval {
          alarm 30;
          for my $y (12,24,48) {
              print "Adjusting widget #$y\n";
              $upd->execute(555,$y);
              print "Recalculating inventory\n";
              $inv->execute($y);
          }
        };
        alarm 0; ## Turn off our alarm
        die "$@\n" if $@; ## Bubble the error to the outer eval
    };
    if ($@) { ## Something went wrong
      if ($@ =~ /TIMEOUT/) {
        print "Queries are taking too long! Cancelling\n";
        ## We don't know which one is still running, and don't care
        ## It's safe to cancel a non-active statement handle
        $upd->cancel() or die qq{Failed to cancel the query!\n};
        $inv->cancel() or die qq{Failed to cancel the query!\n};
        $dbh->rollback();
        die "Who has time to wait 30 seconds anymore?";
      }
      ## Some other non-alarm error, so we simply:
      die $@;
    }

    print "Updates are complete\n";
    $dbh->commit();
    exit;
```

Got an interesting use case for asynchronous queries or the new $dbh‑>cancel()? Let me know!


