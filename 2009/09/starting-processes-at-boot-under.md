---
author: Jon Jensen
title: Starting processes at boot under SELinux
github_issue_number: 197
tags:
- hosting
- redhat
date: 2009-09-07
---

There are a few common ways to start processes at boot time in Red Hat Enterprise Linux 5 (and thus also CentOS 5):

1. Standard init scripts in /etc/init.d, which are used by all standard RPM-packaged software.

1. Custom commands added to the /etc/rc.local script.

1. @reboot cron jobs (for vixie-cron, see `man 5 crontab`—​it is not supported in some other cron implementations).

Custom standalone /etc/init.d init scripts become hard to differentiate from RPM-managed scripts (not having the separation of e.g. /usr/local vs. /usr), so in most of our hosting we’ve avoided those unless we’re packaging software as RPMs.

rc.local and @reboot cron jobs seemed fairly equivalent, with crond starting at #90 in the boot order, and local at #99. Both of those come after other system services such as Postgres & MySQL have already started.

To start up processes as various users we’ve typically used su - $user -c "$command" in the desired order in /etc/rc.local. This was mostly for convenience in easily seeing in one place what all would be started at boot time. However, when running under SELinux this runs processes in the init_t context which usually prevents them from working properly.

The cron @reboot jobs don’t have that SELinux context problem and work fine, just as if run from a login shell, so now we’re using those. Of course they have the added advantage that regular users can edit the cron jobs without system administrator intervention.
