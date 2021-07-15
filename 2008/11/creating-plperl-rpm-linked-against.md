---
author: Jon Jensen
title: Creating a PL/Perl RPM linked against a custom Perl build
github_issue_number: 78
tags:
- perl
- redhat
- sysadmin
- postgres
date: 2008-11-29
---

I recently needed to refer to [a post I made on March 7, 2007](/blog/2007/03/plperl-rpm-linked-against-custom-perl-build), showing how to build a PL/Perl RPM linked against a custom Perl build. A few things have changed since that time, so I’ve reworked it here, updated for local Perl 5.10.0 built into RPMs:

We sometimes have to install a custom Perl build without thread support, and to have some specific newer and/or older versions of CPAN modules, and we don’t want to affect the standard distribution Perl that lives in /usr/bin/perl and /usr/lib/perl5. We use standard PGDG RPMs to install PostgreSQL. We also use PL/Perl, and want PL/Perl to link against our custom Perl build in /usr/local/bin and /usr/local/lib/perl5.

It’s easy to achieve this with a small patch to the source RPM spec file:

```
--- postgresql-8.3.spec 2008-10-31 17:34:34.000000000 +0000
+++ postgresql-8.3.custom.spec  2008-11-30 02:10:09.000000000 +0000
@@ -315,6 +315,7 @@
 CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

 export LIBNAME=%{_lib}
+export PATH=/usr/local/bin:$PATH
 %configure --disable-rpath \
 %if %beta
    --enable-debug \
@@ -322,6 +323,7 @@
 %endif
 %if %plperl
    --with-perl \
+   --with-libraries=/usr/local/lib64/perl5/5.10.0/x86_64-linux/CORE/libperl.so \
 %endif
 %if %plpython
    --with-python \
```

Since we build RPMs of our local Perl, we want this PL/Perl RPM to depend on them, so we make this additional patch before building:

```
--- postgresql-8.3.spec 2008-10-31 17:34:34.000000000 +0000
+++ postgresql-8.3.custom.spec  2008-11-30 02:10:09.000000000 +0000
@@ -100,7 +100,7 @@
 Patch6:        postgresql-perl-rpath.patch
 Patch8:        postgresql-prefer-ncurses.patch

-Buildrequires: perl glibc-devel bison flex
+Buildrequires: local-perl = 4:5.10.0, glibc-devel, bison, flex
 Requires:  /sbin/ldconfig initscripts

 %if %plpython
@@ -227,7 +227,7 @@
 %package plperl
 Summary:   The Perl procedural language for PostgreSQL
 Group:     Applications/Databases
-Requires:  postgresql-server = %{version}-%{release}
+Requires:  postgresql-server = %{version}-%{release}, local-perl = 4:5.10.0
 %ifarch ppc ppc64
 BuildRequires:  perl-devel
 %endif
```

After applying the patch(es) (adjusted for your own custom Perl build, of course), rebuild the RPM, and install the postgresql-plperl (8.2 or newer) or postgresql-pl (8.1 and earlier) RPM. With a `service postgresql restart`, you’re ready to go.

For pre-built PostgreSQL 8.3 RPMs that link against unthreaded local Perl 5.10.0, for Red Hat Enterprise Linux 5 x86_64, see the [packages.endpoint.com Yum repositories](https://packages.endpoint.com/).
