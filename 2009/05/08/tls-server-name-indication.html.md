---
author: Jon Jensen
gh_issue_number: 142
tags: environment
title: TLS Server Name Indication
---



I came across a few discussions of the TLS extension "Server Name Indication", which would allow hosting more than one "secure" (https) website per IP address/TCP port combination. The best summary of the state of things is (surprise, surprise) the [Wikipedia Server Name Indication article](http://en.wikipedia.org/wiki/Server_Name_Indication). There are more details about client and server software support for SNI in [Zachary Schneider's blog post](http://www.sigil.us/?p=60) and [Daniel Lange's blog post](http://daniel-lange.com/archives/2-Multiple-Apache-VHosts-on-the-same-IP-and-port.html).

I don't recall hearing about this before, but if I did I probably dismissed as being irrelevant at the time because there would've been almost no support in either clients or servers. But now that all major browsers on all operating systems support SNI **except some on Windows XP** it may be worth keeping an eye on this.

Yes, IE on Windows XP is still a huge contingent and thus a huge hurdle. But maybe Microsoft will backport SNI support to XP. Even if just for IE 7 and later. Or maybe we'll have to wait a few more years till the next Windows operating system (hopefully) displaces XP. Here's a case where the low popularity of Vista (which supports SNI) is hurting the rest of us.

I'm really looking forward to the flexibility of name-based virtual hosting for https that we've had for 10+ years with plain http. It could really change the setup and ongoing infrastructure costs for secure websites, such as ecommerce sites.


