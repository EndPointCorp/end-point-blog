---
author: Jon Jensen
title: RHEL 5 SELinux initscripts problem
github_issue_number: 442
tags:
- hosting
- linux
- redhat
- security
- selinux
date: 2011-04-22
---



I ran into a strange problem updating Red Hat Enterprise Linux 5 a few months ago, and just ran into it again and this time better understood what went wrong.

The problem was serious: After a `yum upgrade` of a RHEL 5 x86_64 server with SELinux enforcing, it never came back after a reboot. Logging into the console I could see that it was stuck in single user mode because there were no init scripts! Investigation showed that indeed the initscripts package was completely missing.

I searched on [bugzilla.redhat.com](https://bugzilla.redhat.com/) looking for any reported problems and didn’t find any. I reinstalled initscripts, rebooted, and the server was fine, but it was not happytimes to have that unexpected downtime.

Tonight I ran into the problem again, this time on a build server where downtime didn’t matter so I could investigate more leisurely.

The error from yum looked like this (the same problem affected the screen package as affected initscripts):

```nohighlight
Downloading Packages:
screen-4.0.3-4.el5.i386.rpm          | 559 kB      00:00
Running rpm_check_debug
Running Transaction Test
Finished Transaction Test
Transaction Test Succeeded
Running Transaction
groupadd: unable to open group file
error: %pre(screen-4.0.3-4.el5.i386) scriptlet failed, exit status 10
error:   install: %pre scriptlet failed (2), skipping screen-4.0.3-4.el5

Updated:
  screen.i386 0:4.0.3-4.el5

Complete!
# cat /selinux/enforce
1
```

The way I dealt with this initially was to temporarily disable SELinux enforcing, update the package, then reboot (to also load a kernel update):

```nohighlight
# setenforce 0
# yum -y upgrade
# shutdown -r now
```

But following up on the specific error message showed:

```nohighlight
# ls -lFaZ /etc/group
-rw-r--r--  root root system_u:object_r:file_t:s0      /etc/group
```

Aha! The SELinux context is wrong. Given that this has happened a couple of different machines, I’m guessing some past upgrade broke the context. What should it be? Let’s check /etc/passwd for reference:

```nohighlight
# ls -lFaZ /etc/passwd
-rw-r--r--  root root system_u:object_r:etc_t:s0       /etc/passwd
```

That’s confirmed the correct context for /etc/group on another working server. To fix:

```nohighlight
# chcon system_u:object_r:etc_t:s0 /etc/group
```

Then the updates proceed fine. It would be nice to find out what past action set the context wrong on /etc/group.


