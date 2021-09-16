---
author: Jon Jensen
title: Home router problems with .0 IP address
github_issue_number: 474
tags:
- hosting
- networking
date: 2011-07-01
---



In our work the occasional mysterious problem surfaces which makes me appreciate how tractable and sane the majority of the challenges are. Here I’ll tell the story of one of the mysterious problems.

In Internet routing of IPv4 addresses, there’s nothing inherently special about an IP address that ends in .0, .255, or anything else. It all depends on the subnet. In the days before CIDR (Classless Inter-Domain Routing) brought us arbitrary subnet masks, there were classes of routing, most commonly A, B, and C. And the .0 and .255 addresses were special.

That was a long time ago, but it can still cause occasional trouble today. One of our hosting providers assigned us an IP address ending in .0, which we used for hosting a website. It worked fine, and was in service for many months before we heard any reports of trouble.

Then we heard a report from one of our clients that they could not access that website from their home, but they could from their office. We couldn’t ever figure out why.

Next one of our own employees found that he could not access the website from his home, but he could from other locations.

Finally we had enough evidence when a friend from the open source community also could not access that website from his home.

The commonality was in the router they were using:

- Belkin G Wireless Router Model F5D7234-4 v4
- Belkin F5D9231-4 v1
- and the third thought it was a Belkin but they were not able to provide the exact model.

We moved the website to a different IP address on the same server, and they had no problem accessing it.

The routers are obviously broken, but there’s little sense arguing about that. For now we avoid using any .0 IP address because there are going to be some few people who can’t reach it.


