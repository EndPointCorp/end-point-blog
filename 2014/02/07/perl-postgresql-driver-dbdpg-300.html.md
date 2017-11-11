---
author: Greg Sabino Mullane
gh_issue_number: 924
tags: dbdpg, perl, postgres
title: Perl PostgreSQL driver DBD::Pg 3.0.0 released
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2014/02/07/perl-postgresql-driver-dbdpg-300/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/02/07/perl-postgresql-driver-dbdpg-300/image-0.jpeg"/></a><br/><a href="http://www.flickr.com/photos/58505349@N04/11306745055/in/photolist-ie92og-9VGzdh-9VGce5-aeJFwW-AEuKX-5yQqdL-dvL4rC-9bNETo-4wWo81-wMme2-8pkCsJ-7sGZqc-a3P3b9-qndNG-aAUEih-4bwydr-P1JC9-s8waL-kqSSN-a8WSUb-6o5G4p-95a4Dz-3MJRz1-9VGrjs-x5YkV-aKGJzz-82S6jT-hygzDj-7ddteN-bpDuEv-bCVYHG-7x53rc-7x53uz-HMera-9dgTkM-7K2kcz-9egdRk-dxVsaB-bbxy3e-3i16xM-9VGxqE-9VGvdY-9VDmEc-9VGt6Q-5dpTGX-5NA2Jd-x5QcE-x5SLY-62uXRr-dVR2tu-8SPS7k">Nuptse summit</a> by Flickr user <a href="http://www.flickr.com/photos/f514nc0/">François Bianco</a></div>

I am happy to announce that version 3.0.0 of DBD::Pg, the [Perl](http://www.perl.org/) interface to [Postgres](http://www.postgresql.org/), was released on February 3, 2014. This represents a major release, mostly due to the way it now handles [UTF-8](http://perldoc.perl.org/perlunitut.html). I will try to blog soon with more details about that and some other major changes in this version.

The new version is [available from CPAN](http://search.cpan.org/~turnstep/DBD-Pg-3.0.0/). Please make sure that this is the latest version, as new versions may have come out since this post was written.

Checksums for 3.0.0:

58c2613bcb241279aca4c111ba16db48  DBD-Pg-3.0.0.tar.gz

03ded628d453718cbceaea906da3412df5a7137a  DBD-Pg-3.0.0.tar.gz

The complete list of changes is below. Thank you to everyone who sent in patches, helped debug, wrote bug reports, and helped me get this version out the door!

```
Version 3.0.0  Released February 3, 2014 (git commit 9725314f27a8d65fc05bdeda3da8ce9c251f79bd)

  - Major change in UTF-8 handling. If client_encoding is set to UTF-8, 
    always mark returned Perl strings as utf8. See the pg_enable_utf8 docs
    for more information.
    [Greg Sabino Mullane, David E. Wheeler, David Christensen]

  - Bump DBI requirement to 1.614

  - Bump Perl requirement to 5.8.1

  - Add new handle attribute, switch_prepared, to control when we stop 
    using PQexecParams and start using PQexecPrepared. The default is 2: 
    in previous versions, the effective behavior was 1 (i.e. PQexecParams 
    was never used).
    [Greg Sabino Mullane]

  - Better handling of items inside of arrays, particularly bytea arrays.
    [Greg Sabino Mullane] (CPAN bug #91454)

  - Map SQL_CHAR back to bpchar, not char
    [Greg Sabino Mullane, reported by H.Merijn Brand]

  - Do not force oids to Perl ints
    [Greg Sabino Mullane] (CPAN bug #85836)

  - Return better sqlstate codes on fatal errors
    [Rainer Weikusat]

  - Better prepared statement names to avoid bug
    [Spencer Sun] (CPAN bug #88827)

  - Add pg_expression field to statistics_info output to show 
    functional index information
    [Greg Sabino Mullane] (CPAN bug #76608)

  - Adjust lo_import_with_oid check for 8.3
    (CPAN bug #83145)

  - Better handling of libpq errors to return SQLSTATE 08000
    [Stephen Keller]

  - Make sure CREATE TABLE .. AS SELECT returns rows in non do() cases

  - Add support for AutoInactiveDestroy
    [David Dick] (CPAN bug #68893)

  - Fix ORDINAL_POSITION in foreign_key_info
    [Dagfinn Ilmari Mannsåker] (CPAN bug #88794)

  - Fix foreign_key_info with unspecified schema
    [Dagfinn Ilmari Mannsåker] (CPAN bug #88787)

  - Allow foreign_key_info to work when pg_expand_array is off
    [Greg Sabino Mullane and Tim Bunce] (CPAN bug #51780)

  - Remove math.h linking, as we no longer need it
    (CPAN bug #79256)

  - Spelling fixes
    (CPAN bug #78168)

  - Better wording for the AutoCommit docs
    (CPAN bug #82536)

  - Change NOTICE to DEBUG1 in t/02attribs.t test for handle attribute "PrintWarn":
    implicit index creation is now quieter in Postgres.
    [Erik Rijkers]

  - Use correct SQL_BIGINT constant for int8
    [Dagfinn Ilmari Mannsåker]

  - Fix assertion when binding array columns on debug perls &gt;= 5.16
    [Dagfinn Ilmari Mannsåker]

  - Adjust test to use 3 digit exponential values
    [Greg Sabino Mullane] (CPAN bug #59449)

  - Avoid reinstalling driver methods in threads
    [Dagfinn Ilmari Mannsåker] (CPAN bug #83638)

  - Make sure App::Info does not prompt for pg_config location 
    if AUTOMATED_TESTING or PERL_MM_USE_DEFAULT is set
    [David E. Wheeler] (CPAN bug #90799)

  - Fix typo in docs for pg_placeholder_dollaronly
    [Bryan Carpenter] (CPAN bug #91400)

  - Cleanup dangling largeobjects in tests
    [Fitz Elliott] (CPAN bug #92212)

  - Fix skip test counting in t/09arrays.t
    [Greg Sabino Mullane] (CPAN bug #79544)

  - Explicitly specify en_US for spell checking
    [Dagfinn Ilmari Mannsåker] (CPAN bug #91804)

```


