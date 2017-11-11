---
author: Emanuele “Lele” Calò
gh_issue_number: 829
tags: debian, ipv6, sysadmin
title: Proxmox and the fun maze of IPv6 connectivity
---



While working on the Proxmox machine setup and specifically on the IPv6 connectivity I found a problem where after a reboot I always kept getting the *** net.ipv6.conf.all.forwarding*** and all related variable set to ***0***, thus giving lots of IPv6 network connectivity issues on the guests.

While brainstorming with a colleague on this, we discovered in the boot logs these few messages which are quite indicative of something horrible happening at boot:

```
# less /var/log/boot.0
[..]
Mon Jul  8 18:38:59 2013: Setting kernel variables ...sysctl: cannot stat /proc/sys/net/ipv6/conf/all/forwarding: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/forwarding: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/autoconf: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_dad: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_ra: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_ra_defrtr: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_ra_rtr_pref: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_ra_pinfo: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_source_route: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/default/accept_redirects: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/autoconf: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_dad: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_ra: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_ra_defrtr: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_ra_rtr_pref: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_ra_pinfo: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_source_route: No such file or directory
Mon Jul  8 18:38:59 2013: sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_redirects: No such file or directory
Mon Jul  8 18:38:59 2013: done.
[..]
```

The following steps would be to either crawl through the "inextricable" maze of the ProxMox (PVE) boot initrd image and probably came up with the solution or find a quick way to deal with this in a clean way without touching the boot process.

Since it was all due to ***sysctl*** being called too early in the boot process and then not finding proper IPv6 module already loaded calling it again *later* would suffice. So I simply added the following line to ***/etc/network/interfaces***

```
iface eth0 inet6 static
address    YOUR:IPV6:IS:HERE
netmask    64
up ip -6 route add default via fe80::1 dev eth0
up sysctl -p # <------ ADDED THIS LINE TO FIX IPv6 CONNECTIVITY ISSUES
```

And there it goes. Reboot once again to verify and you should be all set.


