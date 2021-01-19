---
author: "Jon Jensen"
title: "Creating a PL/Perl RPM linked against a custom Perl build"
tags: postgres, sysadmin, perl
gh_issue_number: 1671
---

We sometimes have to install a custom Perl build without thread support, and to have some specific versions of CPAN modules, and we don’t want to affect the standard distribution Perl that lives in `/usr/bin/perl` and `/usr/lib/perl5`. We use standard PGDG RPMs to install PostgreSQL. We also like PL/Perl, and want PL/Perl to link against our custom Perl build.

It’s easy to achieve this with a small patch to the source RPM spec file:

```
--- postgresql-8.2.spec.before  2007-02-15 11:52:53.000000000 -0700
+++ postgresql-8.2.spec 2007-02-15 12:02:35.000000000 -0700
@@ -306,6 +306,7 @@
 %endif
 %if %plperl
        --with-perl \
+       --with-libraries=/usr/local/lib/perl5/5.8.7/i386-linux/CORE/libperl.so \
 %endif
 %if %plpython
        --with-python \
```

After applying that patch (adjusted for your own custom Perl build, of course), rebuild the RPM, and install the postgresql-plperl (as of PostgreSQL 8.2) or postgresql-pl (8.1 and earlier) RPM. With a `service postgresql restart`, you’re ready to go.

<!-- original version is at https://web.archive.org/web/20071108213916/http://people.planetpostgresql.org/jjensen/index.php?/archives/1-Creating-a-PLPerl-RPM-linked-against-a-custom-Perl-build.html -->
