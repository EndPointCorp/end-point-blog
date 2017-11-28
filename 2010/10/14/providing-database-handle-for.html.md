---
author: Chris Kershaw
gh_issue_number: 367
tags: interchange, perl, testing
title: Providing Database Handle for Interchange Testing
---



I've recently begun using the test driven development approach to my projects using Perl's Test::More module. Most of my projects lately have been with [Interchange](http://www.icdevgroup.org) which has some hurdles to get around as far as test driven development is concerned. Primarily this is because Interchange runs as a daemon and provides some readily available utilites like the database handle. This method is not available to our tests, so they need to be made available as discussed below.

I develop Usertags, GlobalSubs and ActionMaps where applicable as it helps keep the separation of business logic and views clear. I generally organize these to call a function within a Perl module so they can be tested properly. Most of these tags involve some sort of connection with the database to present information to the user in which I uses the Interchange ::database_exists_ref method.

When it comes to testing I want to ensure that the test script invokes the same method. Otherwise, your script will not be testing the code as its used in production.

Let's say you are building a Perl module that looks something like this:

```perl
package YourMagic;
use strict;

sub do_something {
    my ($opt) = @_;

    # some code

    my $dbh = ::database_exists_ref($opt->{table})->dbh
        or return undef;

    # ... more code
    return $output;
}

1;
```

The ::database_exists_ref() method will not be available for a test script and needs to be defined. It should return an object to the dbh method in the test script as it does within Interchange. There is no need to test the method itself, as it is not part of the "what" that is being developed.  The following code needs to be added to the test script so it can handle the correct type of database reference returned by Interchange.

```perl
use lib '/home/user/interchange/custom/lib';
use Test::More tests => 2;
use DBI;

# Here are the methods to provide proper reference to our database handle
################################
sub ::database_exists_ref {
    my $table = shift;
    return undef if !$table;

    # return an object with a dbh method
    return bless({}, __PACKAGE__);
}

sub dbh {
    # define a dbh method
    my $db = DBI->connect('dsn, 'user', 'pass');

    return $db;
}
##################################

use YourMagic;

is(
    YourMagic::do_something(),
    undef,
    'do_something() returns undef when called with no arguments',
);

is(
    YourMagic::do_something(\%opt),
    undef,
    'do_something() returns ...',
);
```

It is also worthwhile to note that you'll need to use the ::database_exists_ref method to look up some information from the existing table that is valuable to test against. Now the do_something() method will call ::database_exists_ref() when invoked.

This approach allows us to use, reuse, and add new tests without worrying about mock data during the intial development. You can be sure that the existing test scripts will function properly against the latest data that is available. 

I will cover some other topics regarding Interchange Test Driven Development in future posts. For more information regarding Unit Testing in general see [this post](/blog/2010/06/23/getting-started-with-unit-testing) by [Ethan](http://www.blogger.com/profile/07543304949984321650).


