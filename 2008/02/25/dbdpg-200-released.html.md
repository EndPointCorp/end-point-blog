---
author: Greg Sabino Mullane
gh_issue_number: 27
tags: database, open-source, postgres, perl
title: DBD::Pg 2.0.0 Released
---

I'm happy to announce that the newest version of DBD::Pg is out! This was a major release, and includes many features and changes from the previous version, 1.49. Releases are back to the "release early, release often" mantra of open source: versions 2.1.0, 2.1.1, 2.1.2, and 2.1.3 were all released within a week of 2.0.0, and 2.2.0 is expected to be released soon.

Many infrastructure changes were done for this change, including moving from CVS to Subversion, moving the [mailing lists](http://www.nntp.perl.org/group/perl.dbd.pg/) and [repository](http://svn.perl.org/modules/DBD-Pg/trunk/) to perl.org, and switching to a three-part "extended" versioning system, similar to the one PostgreSQL uses. Support for versions of Postgres older than 7.4 was dropped, which allowed much of the code to be cleaned up.

Support for asynchronous queries was added, which allows a Perl script to continue doing other things while a long-running query is still being processed by Postgres. Not only can the script check back periodically and see if the query is ready yet, but it can also be cancelled at any point, so at no point does your script get stuck waiting for a query. Another great feature of version 2.0.0 is full support for arrays, both into and out of the database. This allows you to supply an arrayref in your execute queries, and Postgres arrays returned from the database are transformed into Perl arrays.

The previous COPY interface was deprecated and replaced by a newer one, which is based on the new libpq functions. The new interface is simpler to use and does not require that the size of the data be specified beforehand.

In addition to fixing all open bugs and adding numerous other enhancements, the test suite and large parts of the main codebase were cleaned up and rewritten. The next version is expected to introduce advanced tracing flags, which will greatly facilitate debugging of application code.

*(See Greg's [blog post on the release](http://people.planetpostgresql.org/greg/index.php?/archives/122-DBDPg-2.0.0-released.html) for more details.)*
