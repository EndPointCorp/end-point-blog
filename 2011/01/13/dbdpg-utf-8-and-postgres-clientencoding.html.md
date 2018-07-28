---
author: Greg Sabino Mullane
gh_issue_number: 395
tags: database, dbdpg, perl, postgres
title: DBD::Pg, UTF-8, and Postgres client_encoding
---

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5561747612884867330" src="/blog/2011/01/13/dbdpg-utf-8-and-postgres-clientencoding/image-0.jpeg"/>Photo by [Roger Smith](https://www.flickr.com/photos/rogersmith/)

I’ve been working on getting DBD::Pg to play nicely with UTF-8, as the current system is suboptimal at best. DBD::Pg is the Perl interface to Postgres, and is the glue code that takes the data from the database (via libpq) and gives it to your Perl program. However, not all data is created equal, and that’s where the complications begin.

Currently, everything coming back from the database is, by default, treated as byte soup, meaning no conversion is done, and no strings are marked as utf8 (Perl strings are actually objects in which one of the attributes you can set is ‘utf8’). If you want strings marked as utf8, you must currently set the pg_enable_utf8 attribute on the database handle like so:

```perl
$dbh->{pg_enable_utf8} = 1;
```

This causes DBD::Pg to scan incoming strings for high bits and mark the string as utf8 if it finds them. There are a few drawbacks to this system:

- It does this for all databases, even SQL_ASCII!
- It doesn’t do this for everything, e.g. arrays, custom data types, xml.
- It requires the user to remember to set pg_enable_utf8.
- It adds overhead as we have to parse every single byte coming back from the database.

Here’s one proposal for a new system. Feedback welcome, as this is a tricky thing to get right.

DBD::Pg will examine the client_encoding parameter, and see if it matches UTF8. If it does, then we can assume everything coming back to us from Postgres is UTF-8. Therefore, we’ll simply flip the utf8 bit on for all strings. The one exception is bytea data, of course, which we’ll read in and dequote into a non-utf8 string. Any non-UTF8 client_encodings (e.g. the monstrosity that is SQL_ASCII) will simply get back a byte soup, with no utf8 markings on our part.

The pg_enable_utf8 attribute will remain, so that applications that do their own decoding, or otherwise do not want the utf8 flag set, can forcibly disable it by setting pg_enable_utf8 to 0. Similarly, it can be forced on by setting pg_enable_utf8 to 1. The flag will always trump the client_encoding parameter.

A further complication is client_encoding: What if it defaults to something else? We can set it ourselves upon first connecting, and then if the program changes it after that point, it’s on them to deal with the issues. (As DBD::Pg will still assume it is UTF-8, as we don’t constantly recheck the parameter.)

Someone also raised the issue of marking ASCII-only strings as utf8. While *technically* this is not correct, it would be nice to avoid having to parse every single byte that comes out of the database to look for high bits. Hopefully, programs requesting data from a UTF-8 database will not be surprised when things come back marked as utf8.

Feel free to comment here or on the [bug that started it all.](https://rt.cpan.org/Public/Bug/Display.html?id=40199) Thanks also to [David Christensen](/team/david_christensen), who has given me great input on this topic.
