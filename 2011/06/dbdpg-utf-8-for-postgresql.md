---
author: Greg Sabino Mullane
title: DBD::Pg UTF-8 for PostgreSQL server_encoding
github_issue_number: 471
tags:
- database
- dbdpg
- git
- open-source
- perl
- postgres
date: 2011-06-20
---



<a href="/blog/2011/06/dbdpg-utf-8-for-postgresql/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5620313937936840898" src="/blog/2011/06/dbdpg-utf-8-for-postgresql/image-0.png" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 167px; height: 276px;"/></a>

We are preparing to make a major version bump in DBD::Pg, the Perl interface for [PostgreSQL](https://www.postgresql.org/), from the 2.x series to 3.x. This is due to a reworking of how we handle UTF-8. The change is not going to be backwards compatible, but will probably not affect many people. If you are using the pg_enable_utf8 flag, however, you definitely need to read on for the details.

The short version is that DBD::Pg is going return all strings from the Postgres server with the Perl utf8 flag on. The sole exception will be databases in which the server_encoding is SQL_ASCII, in which case the flag will never be turned on.

For backwards compatibility and fine-tuning control, there is a new attribute called **pg_utf8_strings** that can be set at connection time to override the decision above. For example, if you need your connection to return byte-soup, non-utf8-marked strings, despite coming from a UTF-8 Postgres database, you can say:

```perl
  my $dsn = 'dbi:Pg:dbname=foobar';
  my $dbh = DBI->connect($dsn, $dbuser, $dbpass,
    { AutoCommit => 0,
      RaiseError => 0,
      PrintError => 0,
      pg_utf8_strings => 0,
    }
  );
```

Similarly, you can set pg_utf8_strings to 1 and it will force settings returned strings as utf8, even if the backend is SQL_ASCII. You should not be using SQL_ASCII of course, and certainly not forcing the strings returned from it to UTF-8. :)

All Perl variables (be they strings or otherwise) are actually Perl objects, with some internal attributes defined on them. One of those is the utf8 flag, which can be flipped on to indicate that the string should be treated as possibly containing multi-byte characters, or it can be left off, to indicate the string should always be treated on a byte-by-byte basis. This will affect things like the Perl **length** function, and the Perl **\w** regex flag. This is completely unrelated to the Perl pragma **use utf8**, which DBD::Pg has nothing at all to do with. Have I mentioned that UTF-8, and UTF-8 in Perl in particular, can be quite confusing?

There are a few exceptions as to what things DBD::Pg will mark as utf8. Integers and other numbers will not, boolean values will not, and no bytea data will ever have the flag set. When in doubt, assume that it is set.

The old attribute, **pg_enable_utf8**, will be deprecated, and have no effect. We thought about re-using that but it seemed clearer and cleaner to simply create a new variable (pg_utf8_strings), as the behavior has significantly changed.

A beta version of DBD::Pg (2.99.9_1) with these changes has been uploaded to CPAN for anyone to experiment with. Right now, none of this is set in stone, but we did want to get a working version out there to start the discussion and see how it interacts with applications that were making use of the
pg_enable_utf8 flag. You can web search for “dbdpg” and look for the “Latest Dev. Release”, or jump straight to [the page for DBD::Pg 2.99.9_1](https://metacpan.org/release/TURNSTEP/DBD-Pg-2.99.9_1). The trailing underscore is a CPAN convention that indicates this is a development version only, and thus will not replace the latest production version (2.18.1 as of this writing).

As a reminder, DBD::Pg has [switched to using git](/blog/2011/06/dbdpg-moves-to-git), so you can follow along with the development
with:

```bash
git clone git://bucardo.org/dbdpg.git
```

There is also a commits mailing list you can join to receive notifications of commits as they are pushed to the main repo. To sign up, send an email to **dbd-pg-changes-subscribe@perl.org**.


