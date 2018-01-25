---
author: Josh Williams
gh_issue_number: 1289
tags: linux, sysadmin
title: Become A File Spy With This One Easy Trick! Sys Admins Love This!
---

We had an interesting problem to track down. (Though I suppose I wouldn’t be writing about it if it weren’t, yes?) Over the years a client had built up quite the collection of scripts executed by cron to maintain some files on their site. Some of these were fairly complex, taking a long while to run, and overlapping with each other.

One day, the backup churn hit a tipping point and we took notice. Some process, we found, seemed to be touching an increasing number of image files: The contents were almost always the same, but the modification timestamps were updated. But digging through the myriad of code to figure out what was doing that was proving to be somewhat troublesome.

Enter auditd, already present on the RHEL host. This allows us to attach a watch on the directory in question, and track down exactly what was performing the events. — Note, other flavors of Linux, such as Ubuntu, may not have it out of the box. But you can usually install it via the the auditd package.

```shell
(output from a test system for demonstration purposes)
# auditctl -w /root/output
# tail /var/log/audit/audit.log
type=SYSCALL msg=audit(1487974252.630:311): arch=c000003e syscall=2 success=yes exit=3 a0=b51cf0 a1=241 a2=1b6 a3=2 items=2 ppid=30272 pid=30316 auid=0 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts2 ses=1 comm="script.sh" exe="/usr/bin/bash" key=(null)
type=CWD msg=audit(1487974252.630:311):  cwd="/root"
type=PATH msg=audit(1487974252.630:311): item=0 name="output/files/" inode=519034 dev=fd:01 mode=040755 ouid=0 ogid=0 rdev=00:00 objtype=PARENT
type=PATH msg=audit(1487974252.630:311): item=1 name="output/files/1.txt" inode=519035 dev=fd:01 mode=0100644 ouid=0 ogid=0 rdev=00:00 objtype=CREATE
```
The most helpful logged items include the executing process’s name and path, the file’s path, operation, pid and parent pid. But there’s a good bit of data there per syscall.

Don’t forget to auditctl -W /root/output to remove watch. auditctl -l will list what’s currently out there:

```shell
# auditctl -l
-w /root/output -p rwxa
```
That’s the short version. auditctl has a different set of parameters that are a little bit more verbose, but have more options. The equivalent of the above would be: auditctl -a always,exit -F dir=/root/output -F perm=rwxa ... with options for additional rule fields/filters on uid, gid, pid, whether or not the action was successful, and so on.
