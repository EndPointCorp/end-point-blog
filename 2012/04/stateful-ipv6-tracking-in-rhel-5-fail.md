---
author: Josh Williams
title: 'Stateful IPv6 tracking in RHEL 5: Fail'
github_issue_number: 582
tags:
- ipv6
- redhat
date: 2012-04-05
---



Are you a RHEL 5 user? Or CentOS or Scientific Linux, for that matter? Have you started deploying IPv6 on RHEL 5? If you’re using ip6tables as a firewall in this environment, you may want to double check its configuration.

The short version: The 2.6.18 kernel RHEL 5 ships doesn’t have a working conntrack module for IPv6. The conntrack module is what ip6tables uses for stateful packet tracking. You may already be familiar with it from the IPv4 version of iptables, looking something like this in your firewall config:

```nohighlight
-m state --state ESTABLISHED,RELATED -j ACCEPT
```

ip6tables will accept that as well, it just doesn’t do much. The rule is effectively skipped, and the processing eventually gets down to where ip6tables is set to drop or reject, unless it matches something else along the way. Thus it appears that outgoing connections are blocked for most servers, but maybe not everywhere, even if you don’t have any rules in your OUTPUT chain.

Incoming connections will of course work fine, as those don’t rely on the state match (at least initially) and instead match explicitly defined rules for public ports, specific source addresses, etc. RHEL 6 is also fine, as the more recent kernel has switched to something different to implement stateful tracking.

See this [Red Hat Bugzilla bug](https://bugzilla.redhat.com/show_bug.cgi?id=232933) for a few details, but essentially this version of the kernel sets all packets to the INVALID state. The SYN packet goes out to the remote server, it just doesn’t match the return SYN/ACK reply. So instead of doing stateful tracking, we have to resort to stateless. We’ll lose that fancy connection tracking which can be useful for protocols like FTP that make multiple connections. Rather, in allowing in anything that’s not starting a new connection, this should do the job:

```nohighlight
-A INPUT -p tcp -m tcp ! --syn -j ACCEPT
```

We encountered this little kernel bug in the course of moving our old employee shell server to an existing server that already had IPv6 enabled, only to find out going connections mysteriously not working. It took a little digging, but I’m sure we won’t be the last to encounter it, so hopefully this will help someone else out.


