---
author: Emanuele “Lele” Calò
gh_issue_number: 793
tags: iptables, sysadmin
title: Rackspace Load Balancers network issues and "desperate" solution
---



Most people in IT already know the common "Have you tried turning it off and on again?" joke and about all of them also know that sometimes *it just works*.

In a sense that's what I experienced with *Rackspace Load Balancers* when after a day of networking troubleshooting, which involved (but was not limited to):

- iptables rules proof-reading
- overlapping network mask checks
- tcpdump network traffic troubleshooting
- software functionality testing both via localhost and different hosts

I had an enlightenment moment when I realized that while I was waiting for the next desperate solution to pop out some remote areas of my brain I could just remove all nodes from the load balancer (via the web interface) and then add them back, without actually making any other change. Well it turns out that *this was the solution* that I was looking for after a day of reckless debugging.

So lesson learned: before hurting yourself, try once again the most simple, obvious and possibly silly answers... and just a second before considering the impossible become possible, try "turning it off and on once again".


