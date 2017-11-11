---
author: Jon Jensen
gh_issue_number: 520
tags: camps, hosting, linux, redhat
title: Semaphore limits and many Apache instances on Linux
---



On some of our development servers, we run many instances of the Apache httpd web server on the same system. By "many", I mean 30 or more separate Apache instances, each with its own configuration file and child processes. This is not unusual on [DevCamps](http://www.devcamps.org/) setups with many developers working on many projects on the same server at the same time, each project having a complete software stack nearly identical to production.

On Red Hat Enterprise Linux 5, with somewhere in the range of 30 to 40 Apache instances on a server, you can run into failures at startup time with this error or another similar one in the error log:

```nohighlight
[error] (28)No space left on device: Cannot create SSLMutex
```

The exact error will depend on what Apache modules you are running. The "space left on device" error does not mean you've run out of disk space or free inodes on your filesystem, but that you have run out of SysV IPC semaphores.

You can see what your limits are like this:

```nohighlight
# cat /proc/sys/kernel/sem
250 32000 32 128
```

I typically double those limits by adding this line to /etc/sysctl.conf:

```nohighlight
kernel.sem = 500 64000 64 256
```

That makes sure you'll get the change at the next boot. To make the change take immediate effect:

```nohighlight
# sysctl -p
```

With those limits I've run 100 Apache instances on the same server.


