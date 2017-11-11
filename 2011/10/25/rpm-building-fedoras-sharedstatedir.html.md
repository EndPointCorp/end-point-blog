---
author: Jon Jensen
gh_issue_number: 509
tags: hosting, redhat, sysadmin
title: 'RPM building: Fedora''s _sharedstatedir'
---

When Red Hat Enterprise Linux does not offer packages that we need, [EPEL](http://fedoraproject.org/wiki/EPEL) (Extra Packages for Enterprise Linux) often has what we want, kept compatible with RHEL. When EPEL also doesn't have a package, or we need a newer release than is offered, we rebuild packages from [Fedora](http://fedoraproject.org/), which has consistently high-quality packages even in its "rawhide" development phase. We then distribute our packages in several compatibility-oriented Yum repositories at [packages.endpoint.com](https://packages.endpoint.com/).

Of course some things in the latest Fedora are not compatible with RHEL. In rebuilding the [logcheck](http://logcheck.org/) package (needed as a dependency for another package), I found that Fedora RPM spec files have begun using the _sharedstatedir macro in /usr/lib/rpm/macros, which RHEL has never used before.

On RHEL that macro has been set to /usr/com, a strange nonexistent path that apparently came from the GNU autoconf tools but wasn't used in RHEL. Now in Fedora the macro is set to /var/lib and is being used, as described in [a Fedora wiki page on packaging](https://fedoraproject.org/wiki/Archive:PackagingDrafts/RPMMacros_sharedstatedir_optflags_and_admonitions).

The easiest and most compatible way to make the change without munging the system- or user-wide RPM macros is to add this definition to the top of the spec file where it's needed:

```nohighlight
%define _sharedstatedir /var/lib
```

And then the RPM build is happy.

In related news, alongside the new logcheck package, there are also new [End Point RHEL 5 x86_64 packages](https://packages.endpoint.com/rhel/5/os/x86_64/) for the brand-new [Git](http://git-scm.com/) 1.7.7.1 and [pbzip2](http://compression.ca/pbzip2/) 1.1.5, the multi-CPU core parallel compressor that has had several bugfix releases this year.
