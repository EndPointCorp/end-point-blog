---
author: Emanuele “Lele” Calò
title: Give me my /var/log/rpmpkgs back!
github_issue_number: 845
tags:
- redhat
- sysadmin
date: 2013-08-12
---

When switching from RHEL5 to RHEL6 everyone had fears and hopes about things which would have been lost and gained.

One of the lost ones is ***/var/log/rpmpkgs*** which is a nice tool which helps system administrator staying sane when a server rebuild or migration is needed by giving them the list of packages installed up to the day before.

How this feature works is that basically a daily ***cronjob*** dumps the installed packages in the log file /var/log/rpmpkgs, along with various information, for the sake of system maintainers.

What happened is that while this tool was included in the RPM package ’til RHEL5 (and CentOS 5.x), when releasing RHEL6 (and CentOS 6.x) they decided to split it and create a specific package called ***rpm-cron***.

So if you’re among the ones who misses this useful feature, please fire up your SSH connection and type

```
yum install rpm-cron
```

And rejoice of the useful tool being back where it should be.
