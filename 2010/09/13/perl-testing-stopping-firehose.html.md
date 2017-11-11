---
author: Greg Sabino Mullane
gh_issue_number: 349
tags: perl, postgres, testing
title: Perl Testing - stopping the firehose
---



<a href="/blog/2010/09/13/perl-testing-stopping-firehose/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5516463759234506722" src="/blog/2010/09/13/perl-testing-stopping-firehose/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 266px; height: 400px;"/></a>

I maintain a large number of Perl modules and scripts, and one thing they all have in common is a test suite, which is basically a collection of scripts inside a "t" subdirectory used to thoroughly test the behavior of the program. When using Perl, this means you are using the awesome [Test::More module](http://search.cpan.org/~mschwern/Test-Simple-0.96/lib/Test/More.pm), which uses the Test Anything Protocol (TAP). While I love Test::More, I often find myself needing to stop the testing entirely after a certain number of failures (usually one). This is the solution I came up with.

Normally tests are run as a group, by invoking all files named t/*.t; each file has numerous tests inside of it, and these individual tests issue a pass or a fail. At the end of each file, a summary is output stating how many tests passed and how many failed. So why is stopping after a failed test even needed? The reasons below mostly relate to the tests I write for the [Bucardo program](http://bucardo.org/wiki/Bucardo), which has a fairly large and complex test suite. Some of the reasons I like having fine-grained control of when to stop are:

- Scrolling back through screens and screens of failing tests to find the point where the test began to fail is not just annoying, but a very unproductive use of my time.- Tests are very often dependent. If test #23 fails, it means there is a very good chance that most if not all of the subsequent tests are going to fail as well, and it makes no sense for me to look at fixing anything but test #23 first.- Tests can take a very long time to run, and I can't wait around for the errors to start appearing and hit ctrl-c. I need to kick them off, go do something else, and then come back and have the tests stop running immediately after the first failed test. Bucardo tests, for example, create and startup four different Postgres clusters, populates the databases inside each cluster with test data, installs a fresh copy of Bucardo, and *then* begins the real testing. No way I'm going to wait around for that to happen.- Debugging is greatly aided by having the tests stop where I want them to. Often tests after the failing one will modify data and otherwise destroy the "state" such that I cannot manually duplicate the error right then and there, and thus fix it easily.

For now, my solution is to override some of the methods from Test::More. I have a standard script that does this, and I 'use' this script after I 'use Test::More' inside my test scripts. For example, a test script might look like this:

```perl
#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use Test::More tests =&gt; 356;
use TestOverride;

sub some_function {
       my $arr = [];
       push @$arr =&gt; 4,9;
       return [$arr];
}

my $t = q{Function some_function() returns correct value when called with 'foo'};
my $value = some_function('foo');
my $res = [[3],[5]];
is_deeply( $value, $res, $t);

...

$t = q{Value of baz is 123};
is ($baz, 123, $t);
...
```

In turn, the **TestOverride** file contains this:

```perl
...
use Data::Dumper;
$Data::Dumper::Indent = 1;
$Data::Dumper::Terse = 1;
$Data::Dumper::Pad = '|';

use base 'Exporter';
our @EXPORT = qw{ is_deeply like pass is isa_ok ok };

my $bail_on_error = $ENV{TESTBAIL} || 0;

my $total_errors = 0;

sub is_deeply {

   # Return right away if the test passes
   my $rv = Test::More::is_deeply(@_);
   return $rv if $rv;

   if ($bail_on_error and ++$total_errors &gt;= $bail_on_error) {
       my ($file,$line) = (caller)[1,2];
       Test::More::diag("GOT: ".Dumper $_[0]);
       Test::More::diag("EXPECTED: ".Dumper $_[1]);
       Test::More::BAIL_OUT "Stopping on a failed 'is_deeply' test from line $line of $file.";
   }

   return;

} ## end of is_deeply

sub is {
   my $rv = Test::More::is(@_);
   return $rv if $rv;
   if ($bail_on_error and ++$total_errors &gt;= $bail_on_error) {
       my ($file,$line) = (caller)[1,2];
       Test::More::BAIL_OUT "Stopping on a failed 'is' test from line $line of $file.";
   }
   return;
} ## end of is
```

The **is_deeply** compares two arbitrary Perl structures (such as the arrayref here, but it can do hashes as well), and points out if they differ, and where. The "deeply" is because it will walk through the entire structure to find any differences. Good stuff.

Some things to note about the new is_deeply function: first, we simply pass in our parameters to the "real" is_deeply subroutine - the one found inside the Test::More package. If this passes (by returning true), we simply pass that truth back to the caller, and it's completely as if is_deeply had not been overwritten at all. However, if the test fails, Test::More::is_deeply will output a failure notice, but we check to see if the total number of failures for this test script ($total_errors) is greater than or equal to the threshold ($bail_on_error) that we set via then environment variable TESTBAIL. (Having it as an environment variable that defaults to zero allows the traditional behavior to be easily changed without editing any files).

If the number of failed tests is over our threshhold, we call the **BAIL_OUT** method from Test::More, which not only stops the current test script from running any more scripts, but stops any subsequent test files from running as well.

Before calling BAIL_OUT however, we also take advantage of the overriding to provide a little more detail about the failure. We output the line and file the test came from (because Test::More::is_deeply only sees that we are calling it from within the TestOverride.pm file). Most importantly, we output a complete dump of the expected and actual structures passed to is_deeply to be compared. The regular is_deeply only describes where the first mismatch occurs, but I often need to see the entire surrounding object. So rather than normal output looking like this:

```perl
1..356
not ok 1 - Function some_function() returns correct value when called with 'foo'
#   Failed test 'Function some_function() returns correct value when called with 'foo''
#   at test1.t line 18.
#     Structures begin differing at:
#          $got-&gt;[0] = '4'
#     $expected-&gt;[0] = '3'
# Looks like you planned 356 tests but ran 1.
# Looks like you failed 1 test of 1 run.
```

The new output looks like this:

```perl
1..356
not ok 1 - Function some_function() returns correct value when called with 'foo'
#   Failed test 'Function some_function() returns correct value when called with 'foo''
#   at TestOverride.pm line 23.
#     Structures begin differing at:
#          $got-&gt;[0] = '4'
#     $expected-&gt;[0] = '3'
# GOT: |[
# |  4,
# |  [
# |    9
# |  ]
# |]
# EXPECTED: |[
# |  3
# |]
Bail out!  Stopping on a failed 'is_deeply' test from line 17 of test1.t.
```

Yes, the [Test::Most](http://search.cpan.org/~ovid/Test-Most-0.23/lib/Test/Most.pm) module does some similar things, but I don't use it because it's yet another module dependency, it doesn't allow me to control the number of acceptable failures before bailing, and it doesn't show pretty output for is_deeply.


