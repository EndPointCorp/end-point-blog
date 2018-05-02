---
author: Marco Matarazzo
gh_issue_number: 1297
tags: redhat, ipv6, hosting, networking
title: Linode IPv6 issues with NetworkManager on CentOS 7
---

In End Point, we use different hosting providers based on the specific task needs. One provider we use extensively with good results is [Linode](https://www.linode.com).

During a routine CentOS 7 system update, we noticed a very strange behavior where our IPv6 assigned server address was wrong after restarting the server.

### IPv6 on Linode and SLAAC

Linode is offering IPv6 on all their VPS, and IPv6 dynamic addresses are assigned to servers using [SLAAC](https://en.wikipedia.org/wiki/IPv6#Stateless_address_autoconfiguration_.28SLAAC.29).

In the provided CentOS 7 server image, this is managed by NetworkManager by default. After some troubleshooting, we noticed that during the update the NetworkManager package was upgraded from 1.0.6 to 1.4.0.

This was a major update, and it turned out that the problem was a change in the configuration defaults between the two version.

### Privacy stable addressing

Since 1.2, NetworkManager added the Stable Privacy Addressing feature. This allows for some form of tracking prevention, with the IPv6 address to be stable on a network but changing when entering another network, and still remain unique.

This new interesting feature has apparently become the default after the update, with the ipv6.addr-gen-mode property set to “stable-privacy”. Setting it to “eui64” maintains the old default behavior.

### Privacy Extension

Another feature apparently also caused some problems on our VPS: the Privacy Extension. This is a simple mechanism that somewhat randomizes the network hardware’s (MAC) address, to add another layer of privacy. Alas, this is used in address generation, and that randomization seemed to be part of the problem we were seeing.

This too has become the default, with the ipv6.ip6-privacy property set to 1. Setting it to 0 turns off the feature.

### To sum it up

In the end, after the update, we could restore the old behavior and resolve our issues by running, in a root shell:

```bash
nmcli connection modify "Wired connection 1" ipv6.ip6-privacy 0
nmcli connection modify "Wired connection 1" ipv6.addr-gen-mode eui64
```

After a reboot, the IPv6 address finally matched the one actually assigned by Linode, and everything was working ok again.

If you want to know more on Privacy Extensions and Privacy Stable Addressing, [this great blog post](https://blogs.gnome.org/lkundrak/2015/12/03/networkmanager-and-privacy-in-the-ipv6-internet/) by Lubomir Rintel helped us a lot understanding what was going on.
