---
author: Jon Jensen
gh_issue_number: 232
tags: hosting, redhat, security
title: Cisco PIX mangled packets and iptables state tracking
---

Kiel and I had a fun time tracking down a client’s networking problem the other day. Their scp transfers from their application servers behind a Cisco PIX firewall failed after a few seconds, consistently, with a connection reset.

The problem was easily reproducible with packet sizes of 993 bytes or more, not just with TCP but also ICMP (bloated ping packets, generated with ping -s 993 $host). That raised the question of how this problem could go undetected for their heavy web traffic. We determined that their HTTP load balancer avoided the problem as it rewrote the packets for HTTP traffic on each side.

Kiel narrowed the connect resets down to iptables’ state-tracking considering packets INVALID, not ESTABLISHED or RELATED as they should be.

Then he found via tcpdump that the problem was easily visible in scp connections when TCP window scaling adjustments were made by either side of the connection. We tried disabling window scaling but that didn’t help.

We tried having iptables allow packets in state INVALID when they were also ESTABLISHED or RELATED, and that reduced the frequency of terminated connections, but still didn’t eliminate them entirely. (And it was a kludge we weren’t eager to keep in place anyway.)

We wanted to avoid some unpleasant possibilities: (1) turn off stateful firewalling or (2) perform risky updates or configuration changes on the Cisco PIX, which may or may not fix the problem, in the middle of the busy holiday ecommerce season.

Finally, Kiel found [this netfilter mailing list post](http://lists.netfilter.org/pipermail/netfilter/2006-September/066840.html) which describes how to enable a Linux kernel workaround for the mangled packets the Cisco generates:

```bash
echo 1 > /proc/sys/net/ipv4/netfilter/ip_conntrack_tcp_be_liberal
```

Of course saving that in /etc/sysctl.conf so it persists after a reboot.

So we have reliable long-running scp connections with TCP window scaling working and iptables doing its job. I love it when a plan comes together.
