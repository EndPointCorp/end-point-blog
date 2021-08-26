---
author: Jon Jensen
title: Slow Xen virtualization of RHEL 3 i386 guest on RHEL 5 x86_64
github_issue_number: 91
tags:
- environment
- redhat
date: 2009-01-23
---



It seems somehow appropriate that this post so closely follows Ethan’s recent note about patches vs. complaints in free software. Here’s the situation and the complaint (no patch, I’m sorry to say):

We’re migrating an old server into a virtual machine on a new server, because our client needs to get rid of the old server very soon. Then afterwards we will migrate the services piecemeal to run natively on RHEL 5 x86_64 with current versions of each piece of the software stack, so we have time to test compatibility and make adjustments without being in a big hurry.

The old server is running RHEL 3 i386 on 2 Xeon @ 2.8 GHz CPUs (hyperthreaded), 4 GB RAM, 2 SCSI hard disks in RAID 1 on MegaRAID, running Red Hat’s old 2.4.21-4.0.1.ELsmp kernel.

The new server is running RHEL 5 x86_64 on 2 Xeon quad-core L5410 @ 2.33GHz CPUs, 16 GB RAM, 6 SAS hard disks in RAID 10 on LSI MegaRAID, running Red Hat’s recent 2.6.18-92.1.22.el5xen kernel.

The virtual machine is using Xen full virtualization, with 4 virtual CPUs and 4 GB RAM allocated, with a nearly identical copy of the operating system and applications from the old server. And it is bog-slow. Agonizingly slow.

Under the load of even a single repeated web request to web server (Apache) + app server (Interchange) + database server (MySQL), it breathes heavy, and takes 1-2 seconds per request (wildly varying). The old physical machine takes 0.5-0.7 seconds per request under 2 concurrent users. Under heavier load (just a boring day of regular web traffic) the new VM groans and plods along.

The most noticeable metric is that the CPUs get pegged from 50%-90% to more system usage, with under 40% user usage. This is nearly the opposite of the physical machine where system usage was always in the low teens %, and user usage was around 50% per CPU. In both cases there’s almost no I/O wait.

First, I’m really surprised it’s this bad. We’ve done Xen full virtualization of RHEL 5 x86_64 and i386 guests on RHEL 5 x86_64, with no special handling, and it’s always worked quite well with little performance degradation.

So, we know there are paravirtualized drivers you can use to speed up network and disk devices even of otherwise fully virtualized guests. However, apparently you [can’t use the paravirtualized drivers in 32-bit RHEL 3 guest on a 64-bit RHEL 5 host](https://web.archive.org/web/20090209135133/http://www.redhat.com/docs/manuals/enterprise/RHEL-5-manual/en-US/RHEL510/html/Para-Virtualized_Drivers/sect-Para-Virtualized_Drivers-Para_virtualization_Restrictions_and_Support.html). That’s really painful, since in my mind a very common use case for virtualization is loading a bunch of old 32-bit machines on a big 64-bit machine with a lot of RAM. But ... not if you want it to even match the speed of the old servers!

We increased the number of virtual CPUs to 8. That took the edge off the worst slowdowns a bit, but only barely.

We tried upgrading the RHEL 3 guest to the very latest versions of everything from Red Hat Network (Update 9 IIRC) and upgrading the RHEL 5 host to the very latest RHEL 5.3, and saw the wild variation in performance from request to request moderate a lot. Also, performance under heavier concurrency was stable: 2.4-2.6 seconds per request in that scenario.

But that’s still really slow. I hope we’re just missing something obvious here. I’d love to know what the really stupid mistake we’re making is. So far, the search has been fruitless and this seemingly ideal use can for Xen virtualization is barely usable.


