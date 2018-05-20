---
author: Jon Jensen
gh_issue_number: 669
tags: ipv6, linux, redhat, sysadmin
title: RHEL 6 glibc IPv6 DNS resolution bug
---



We ran into an unpleasant bug in a Red Hat Enterprise Linux 6 glibc update a couple of weeks ago. It since has made its way into CentOS 6 as well.

The problem manifested itself in our particular case with this error from the Postfix mailer:

```
Jun 29 01:55:23 sl37 kernel: smtp[7093]: segfault at 1 ip 00007ffc0e455596 sp 00007fff99948f60 error 6 in libresolv-2.12.so[7ffc0e449000+16000]
```

But it affects all DNS resolution on the host, not just for mail.

If you have any IPv6 resolvers at all listed in /etc/resolv.conf, all your DNS resolution is likely to be broken with this version of glibc:

```
glibc-2.12-1.80.el6.x86_64
```

To work around the problem, you can either:

- Use only IPv4 DNS resolvers (comment out the IPv6 resolvers for now)
- or downgrade to the previous version of glibc using yum downgrade

Red Hat is aware of the bug and you can track progress toward a resolution in [Bugzilla bug #835090](https://bugzilla.redhat.com/show_bug.cgi?id=835090).

If you’re using IPv6, watch out for this! If not, you’re fine.


