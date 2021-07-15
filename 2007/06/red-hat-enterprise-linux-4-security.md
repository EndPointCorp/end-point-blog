---
author: Jon Jensen
title: Red Hat Enterprise Linux 4 Security Report
github_issue_number: 21
tags:
- redhat
- linux
date: 2007-06-05
---

Mark Cox, director of the Red Hat Security Reponse Team, has published a [security report of the first two years of Red Hat Enterprise Linux 4](http://www.redhatmagazine.com/2007/04/18/risk-report-two-years-of-red-hat-enterprise-linux-4/), which was released in February 2005. He discusses the vulnerabilities, threats, time to release of updates, and mitigation techniques the operating system uses.

It is interesting to note that the vast majority of security vulnerabilities affected software not used on servers: The Mozilla browser/email suite, Gaim instant messenger, xpdf, etc. Some of the server vulnerabilities would require certain user input to be exploited, such as running Links or Lynx, calling libtiff, or running a malicious binary. Others require less common setups such as Perl's suidperl or Bluetooth drivers, or local shell access.

Nothing is completely secure, but Red Hat Enterprise Linux, configured well and kept updated, has a very good track record so far.
