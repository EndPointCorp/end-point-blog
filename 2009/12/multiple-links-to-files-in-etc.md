---
author: Jon Jensen
title: Multiple links to files in /etc
github_issue_number: 235
tags:
- hosting
- redhat
- security
date: 2009-12-11
---

I came across an unfamiliar error in /var/log/messages on a RHEL 5 server the other day:

```nohighlight
Dec  2 17:17:23 <em>X</em> restorecond: Will not restore a file with more than one hard link (/etc/resolv.conf) No such file or directory
```

Sure enough, ls showed the inode pointed to by /etc/resolv.conf having 2 links. What was the other link?

```bash
# find /etc -samefile resolv.conf
/etc/resolv.conf
/etc/sysconfig/networking/profiles/default/resolv.conf
# ls -lai /etc/resolv.conf /etc/sysconfig/networking/profiles/default/resolv.conf
1526575 -rw-r--r-- 2 root root 69 Nov 30  2008 /etc/resolv.conf
1526575 -rw-r--r-- 2 root root 69 Nov 30  2008 /etc/sysconfig/networking/profiles/default/resolv.conf
```

I’ve worked with a lot of RHEL/CentOS 5 servers and hadn’t ever dealt with these network profiles. Kiel guessed it was probably a system configuration tool that we never use, and he was right: Running system-config-network (part of the system-config-network-tui RPM package) creates the hardlinks for the default profile.

/etc/hosts gets the same treatment as /etc/resolv.conf.

I suppose SELinux’s restorecond doesn’t want to apply any context changes because its rules are based on filesystem paths, and the paths of the multiple links are different and could result in conflicting context settings.

Since we don’t use network profiles, we can just delete the extra links in /etc/sysconfig/networking/profiles/default/.
