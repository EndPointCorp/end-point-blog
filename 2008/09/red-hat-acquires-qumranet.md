---
author: Jon Jensen
title: Red Hat acquires Qumranet
github_issue_number: 64
tags:
- redhat
date: 2008-09-17
---



I missed the news a week and a half ago that [Red Hat has acquired Qumranet](https://web.archive.org/web/20080910063001/http://www.redhat.com/promo/qumranet/), makers of the Linux KVM virtualization software. They say they’ll be focusing on KVM for their virtualization offerings in future versions of Red Hat Enterprise Linux, though still supporting Xen for the lifespan of RHEL 5 at least. (KVM is already in Fedora.)

Given that [Ubuntu also chose KVM](https://www.cnet.com/news/ubuntu-picks-kvm-over-xen-for-virtualization/) as their primary virtualization technology a while back, this should mean even easier use of KVM all around, perhaps making it the default choice on Linux. (Ubuntu [supports other virtualization](https://help.ubuntu.com/lts/serverguide/virtualization.html) as well.)

Also, something helpful to note for RHEL virtualization users: Red Hat Network entitlements for up to 4 Xen guests carry no extra charge if [entitled the right way](https://web.archive.org/web/20090501032453/http://magazine.redhat.com/2008/09/11/tips-and-tricks-registering-xen-guests-with-rhn/).

In even older Red Hat news, [Dag Wieers wrote](http://dag.wieers.com/blog/rhel-backported-one-additional-year) about Red Hat [lengthening its support lifespan for RHEL](https://access.redhat.com/support/policy/updates/errata/) by one year for RHEL 4 and 5.

That means RHEL 5 (and thus also CentOS 5) will have full support until March 2011, new media releases until March 2012, and security updates until March 2014. And RHEL 4, despite its aging software stack, will receive security updates until February 2012!

That’s very helpful in making it easier to choose the time of migration without being pushed too soon due to lack of support.


