---
author: Jon Jensen
title: Trouble with MySQL 4.1 under heavy load
github_issue_number: 12
tags:
- database
- mysql
date: 2006-06-16
---

Two of our customers running high-traffic websites backed by [MySQL](http://www.mysql.com/) (one using [PHP](http://www.php.net/), the other using [Perl](http://www.perl.com/) and [Interchange](/expertise/perl-interchange/)) recently ran into serious problems with their MySQL server getting extremely slow or ceasing to respond altogether. In both cases the problem happened under heavy load, with MySQL 4.1 running on [Red Hat Enterprise Linux](http://www.redhat.com/rhel/) 4 (i386) with the MySQL RPMs built by Red Hat, installed from [Red Hat Network](http://www.redhat.com/rhn/). In both cases, we were unable to find any log output or traffic patterns that indicated the cause of the problem.

When this happened on the first server, we tried numerous MySQL configuration changes, and wrote scripts to monitor the MySQL daemon and restart it when it failed, to give us time to investigate the problem fully. But eventually, out of expediency we simply upgraded to MySQL 5.0 with RPMs provided by the creators of MySQL. Doing so immediately fixed the problem. About a month later when another client encountered the same problem, we went straight for the upgrade path and it fixed things there too.

We haven't had trouble like this with MySQL before, from any source. I [filed a bug report](https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=195745) in Red Hat's bug tracker and Tom Lane quickly pointed me to another similar bug.

Apparently the latest RHN update of MySQL 4.1.20 came just a little too late for our first encounter with this problem, and MySQL 5.0.21 that we upgraded to had the fix in it. It sounds like using the latest MySQL for RHEL 4 from RHN now should work. If you're seeing similar problems, we hope our experience will be of use to you.

At least we can report that the upgrades to MySQL 5.0 were trouble-free. Using nonstandard MySQL client libraries requires you to build new php-mysql, perl-DBD-MySQL, and other dependent RPMs to match, but that's not too hard and is worth the effort if you want to use features from the newer version.
