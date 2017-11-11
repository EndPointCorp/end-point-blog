---
author: Greg Sabino Mullane
gh_issue_number: 929
tags: dbdpg, perl, postgres, unicode
title: DBD::Pg 3.0.0 and the utf8 flag
---



One of the major changes in the recently released [3.0 version of DBD::Pg (the Perl driver for PostgreSQL)](http://blog.endpoint.com/2014/02/perl-postgresql-driver-dbdpg-300.html) was the handling of UTF-8 strings. Previously, you had to make sure to always set the mysterious "pg_enable_utf8" attribute. Now, everything should simply work as expected without any adjustments.

When using an older DBD::Pg (version 2.x), any data coming back from the database was treated as a plain old string. Perl strings have an internal flag called "utf8" that tells Perl that the string should be treated as containing UTF-8. The only way to get this flag turned on was to set the **pg_enable_utf8** attribute to true before fetching your data from the database. When this flag was on, each returned string was scanned for high bit characters, and if found, the utf8 flag was set on the string. The Postgres server_encoding and client_encoding values were never consulted, so this one attribute was the only knob available. Here is a sample program we will use to examine the returned strings. The handy [Data::Peek module](http://search.cpan.org/~hmbrand/Data-Peek/Peek.pm) will help us see if the string has the utf8 flag enabled.

```
#!perl
use strict;
use warnings;
use utf8;
use charnames ':full';
use DBI;
use Data::Peek;
use lib 'blib/lib', 'blib/arch';

## Do our best to represent the output faithfully
binmode STDOUT, ":encoding(utf8)";

my $DSN = 'DBI:Pg:dbname=postgres';
my $dbh = DBI->connect($DSN, '', '', {AutoCommit=>0,RaiseError=>1,PrintError=>0})
  or die "Connection failed!\n";                                            
print "DBI is version $DBI::VERSION, DBD::Pg is version $DBD::Pg::VERSION\n";

## Create some Unicode strings (perl strings with the utf8 flag enabled)
my %dm = (
    dotty  => "\N{CADUCEUS}",
    chilly => "\N{SNOWMAN}",
    stuffy => "\N{DRAGON}",
    lambie => "\N{SHEEP}",
);

## Show the strings both before and after a trip to the database
for my $x (sort keys %dm) {
    print "\nSending $x ($dm{$x}) to the database. Length is " . length($dm{$x}) . "\n";                                                                    
    my $SQL = qq{SELECT '$dm{$x}'::TEXT};             
    my $var = $dbh->selectall_arrayref($SQL)->[0][0];
    print "Database gave us back ($var) with a length of " . length($var) . "\n";
    print DPeek $var;
    print "\n";
}
```

Let's checkout an older version of DBD::Pg and run the script:

```
$ cd dbdpg.git; git checkout 2.18.1; perl Makefile.PL; make
$ perl dbdpg_unicode_test.pl
DBI is version 1.628, DBD::Pg is version 2.18.1

Sending chilly (☃) to the database. Length is 1
Database gave us back (â) with a length of 3
PV("\342\230\203"\0)

Sending dotty (☤) to the database. Length is 1
Database gave us back (â¤) with a length of 3
PV("\342\230\244"\0)

Sending lambie (🐑) to the database. Length is 1
Database gave us back (ð) with a length of 4
PV("\360\237\220\221"\0)

Sending stuffy (🐉) to the database. Length is 1
Database gave us back (ð) with a length of 4
PV("\360\237\220\211"\0)

```

The first thing you may notice is that not all of the Unicode symbols appear as expected. They should be tiny but legible versions of a snowman, a caduceus, a sheep, and a dragon. The fact that they do not appear properly everywhere indicates we have a way to go before the world is Unicode ready. When writing this, only chilly and dotty appeared correctly on my terminal. The blog editing textarea showed chilly, dotty, and lambie. The final blog in Chrome showed only chilly and dotty! Obviously, your mileage may vary, but all of those are all legitimate Unicode characters.

The second thing to notice is how badly the length of the string is computed once it comes back from the database. Each string is one character long, and goes in that way, but comes back longer. Which means the utf8 flag is off - this is confirmed by a lack of a UTF8 section in the DPeek output. We can get the correct output by setting the pg_enable_utf8 attribute after connecting, like so:

```
...
my $dbh = DBI->connect($DSN, '', '', {AutoCommit=>0,RaiseError=>1,PrintError=>0})
  or die "Connection failed!\n";
## Needed for older versions of DBD::Pg.
## This is the same as setting it to 1 for DBD::Pg 2.x - see below
$dbh->{pg_enable_utf8} = -1;
...
```

Once we do that, DBD::Pg will add the utf8 flag to any returned string, regardless of the actual encoding, as long as there is a high bit in the string. The output will now look like this:

```

Sending chilly (☃) to the database. Length is 1
Database gave us back (☃) with a length of 1
PVMG("\342\230\203"\0) [UTF8 "\x{2603}"]

```

Now our snowman has the correct length, and Data::Peek shows us that it has a UTF8 section. However, it's not a great solution, because it ignores client_encoding, has to scan every single string, and because it means having to always remember  to set an obscure attribute in your code every time you connect. Version 3.0.0 and up will check your [client_encoding](http://www.postgresql.org/docs/9.3/static/multibyte.html), and as long as it is UTF-8 (and it really ought to be!), it will automatically return strings with the utf8 flag set. Here is our snowman test on 3.0.0 with no explicit setting of pg_enable_utf8:

```
$ git checkout 3.0.0; perl Makefile.PL; make
$ perl dbdpg_unicode_test.pl
DBI is version 1.628, DBD::Pg is version 3.0.0

Sending chilly (☃) to the database. Length is 1
Database gave us back (☃) with a length of 1
PVMG("\342\230\203"\0) [UTF8 "\x{2603}"]

```

This new automatic detection is the same as setting pg_enable_utf8 to -1. Setting it to 0 will prevent the utf8 flag from ever being set, while setting it to 1 will cause the flag to always be set. Setting it to anything but -1 should be extremely rare in production and used with care.

### Common Questions

#### What happens if I set pg_enable_utf8 = -1 on older versions of DBD::Pg?

Prior to DBD::Pg 3.0.0, the pg_enable_utf8 attribute was a simple boolean, so that setting to anything than **0** will set it to true. In other words, setting it to -1 is the same as setting it to 1. If you must support older versions of DBD::Pg, setting it to -1 is a good setting.

#### Why does DBD::Pg flag everything as utf8, including simple ASCII strings with no high bit characters?

The lovely thing about the UTF-8 scheme is that ASCII data fits nicely inside it with no changes. However, a bare ASCII string is still valid UTF-8, it simply doesn't have any high-bit characters. So rather than read each string as it comes back from the database and determine if it *must* be flagged as utf8, DBD::Pg simply flags every string as utf8 because it *can*. In other words, every string may or may not contain actual non-ASCII characters, but either way we simply flag it because it *may* contain them, and that is good enough. This saves us a bit of time and effort, as we no longer have to scan every single byte coming back from the database. This decision to mark everything as utf8 instead of only non-ASCII strings was the most contentious decision when this new version was being developed.

#### Why is only UTF-8 the only client_encoding that is treated special?

There are two important reasons why we only look at UTF-8. First, the utf8 flag is the only flag Perl strings have, so there is no way of marking a string as any other type of encoding. Second, UTF-8 is unique inside Postgres as it is the universal client_encoding, which has a mapping from nearly every supported server_encoding. In other words, no matter what your server_encoding is set to, setting your client_encoding to UTF-8 is always a safe bet. It's pretty obvious at this point that UTF-8 has won the encoding wars, and is the de-facto encoding standard for Unicode.

#### When is the client_encoding checked? What if I change it?

The value of client_encoding is only checked when DBD::Pg first connects. Rechecking this seldom-changed attribute would be quite costly, but there is a way to signal DBD::Pg. If you really want to change the value of client_encoding after you connect, just set the pg_enable_utf8 attribute to -1, and it will cause DBD::Pg to re-read the client_encoding and start setting the utf8 flags accordingly.

#### What about arrays?

Arrays are handled as expected too. Arrays are unwrapped and turned into an array reference, in which the individual strings within it have the utf8 flag set. Example code:

```
...
for my $x (sort keys %dm) {

    print "\nSending $x ($dm{$x}) to the database. Length is " . length($dm{$x}) . "\n";
    my $SQL = qq{SELECT ARRAY['$dm{$x}']};
    my $var = $dbh->selectall_arrayref($SQL)->[0][0];
    print "Database gave us back ($var) with a length of " . length($var) . "\n";
    $var = pop @$var;
    print "Inner array ($var) has a length of " . length($var) . "\n";
    print DPeek $var;
    print "\n";
}

DBI is version 1.628, DBD::Pg is version 3.0.0

Sending chilly (☃) to the database. Length is 1
Database gave us back (ARRAY(0x90c555c)) with a length of 16
Inner array (☃) has a length of 1
PVMG("\342\230\203"\0) [UTF8 "\x{2603}"]

```

#### Why is Unicode so hard?

Partly because human languages are a vast and complex system, and partly because we painted ourselves into a corner a bit in the early days of computing. Some of the statements presented above have been over-simplified. Unicode is much more than just using UTF-8 properly. The utf8 flag in Perl strings does not mean quite the same thing as a UTF-8 encoding. Interestingly, Perl even makes a distinction between "UTF8" and "UTF-8". It's quite a mess, but at the end of the day. Unicode support is far better [in Perl](http://perldoc.perl.org/perlunicode.html) than [any other language](http://dheeb.files.wordpress.com/2011/07/gbu.pdf).


