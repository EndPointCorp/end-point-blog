---
author: Josh Williams
gh_issue_number: 997
tags: apache, ipv6, nginx, sysadmin
title: DAD Trouble
---



I never thought I’d say it, but these days technology is simply moving too fast for DAD. It’s just the way it is. Of course it’s not DAD’s fault, it’s just the world doesn’t want to wait.

Before I get to that, I want to mention some trouble we’d recently started seeing with nginx failing to start on boot. It’s just been on our most recently obtained servers, both Debian-based (including Ubuntu) and RHEL-based installations. Some were Linode VM’s, others were bare metal hardware systems. After boot and once we got in to try and see what was happening, nginx would happily start manually. The only clue was one line that had been left in the error log:

```nohighlight
2014/06/14 23:33:20 [emerg] 2221#0: bind() to [2607:f0d0:2001:103::8]:80 failed (99: Cannot assign requested address)
```

And it wasn’t just nginx; Apache httpd in one instance gave us similar trouble:

```nohighlight
Starting httpd: (99)Cannot assign requested address: make_sock: could not bind to address [2600:3c00::f03c:91ff:fe73:687f]:80
no listening sockets available, shutting down
```

As an interim fix, since at the moment these systems only had one IPv6 each, we told nginx or httpd to listen on all addresses. But not liking to leave a mystery unsolved, once we were able to schedule a long enough maintenance window on a system to reboot it a few times and see what’s going on, we found that the interface was in a “tentative” state for a short interval.

That was the clue we needed. For some reason, the boot process was allowed to continue before DAD (Duplicate Address Detection) has a chance to decide that if the interface is allowed to use the provided IPv6 address. It’s probably been doing this all along, but the servers that were affected just didn’t boot fast enough to try binding before the interface was ready. Now, things are faster, and service start-up was winning the race.

For us, the addresses are either static or autoconfigured, and we’re confident that a duplicate address situation won’t be a problem. So we turned off dad_transmits by setting this in sysctl.conf:

```
net.ipv6.conf.all.dad_transmits = 0
```

Success! No more bind problems on boot preventing a service from starting.

Incidentally, I believe this [has been solved in Debian](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=705996) by making the interface wait until it’s out of the “tentative” state, but it doesn’t look like it’s been backported to current stable. It should be in Ubuntu as of the current LTS (14.04) however.

Happy Father’s Day!


