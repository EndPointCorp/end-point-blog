---
author: Jon Jensen
gh_issue_number: 144
tags: environment, open-source
title: Operating system upgrades
---



This won't be earth-shattering news to anyone, I hope, but I'm pleased to report that two recent operating system upgrades went very well.

I upgraded a laptop from Ubuntu 8.10 to 9.04, and it's the smoothest I've ever had the process go. The only problem of any kind was that the package download process stalled on the last of 1700+ files downloaded, and I had to restart the upgrade, but all the cached files were still there and on reboot everything worked including my two-monitor setup, goofy laptop audio chipset, wireless networking, crypto filesystem, and everything else.

I also upgraded an OpenBSD 4.3 server that is a firewall, NAT router, DHCP server, and DNS server, to OpenBSD 4.5. It was the first time I used the in-place upgrade with no special boot media and fetching packages over the network, as per [the bsd.rd instructions](http://www.openbsd.org/faq/faq4.html#bsd.rd), and it went fine. Then the extra packages that were there before had to be upgraded separately as per the [FAQ on pkg updates](http://www.openbsd.org/faq/faq15.html#PkgUpdate). I initially scripted some munging of pkg_info's output, not realizing I could simply run pkg_add -u and it updates all packages.

There was one hangup upgrading zsh, which I just removed and reinstalled. Everything else went fine, and all services worked fine after reboot.

How pleasant.


