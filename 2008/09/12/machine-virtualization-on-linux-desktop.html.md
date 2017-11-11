---
author: Jon Jensen
gh_issue_number: 61
tags: environment, hosting
title: Machine virtualization on the Linux desktop
---



In the past I've used virtualization mostly in server environments: Xen as a sysadmin, and VMware and Virtuozzo as a user. They have worked well enough. When there've been problems they've mostly been traceable to network configuration trouble.

Lately I've been playing with virtualization on the desktop, specifically on Ubuntu desktops, using Xen, kvm, and VirtualBox. Here are a few notes.

**[Xen](http://www.xen.org/xen/):** Requires hardware virtualization support for full virtualization, and paravirtualization is of course only for certain types of guests. It feels a little heavier on resource usage, but I haven't tried to move beyond lame anecdote to confirm that.

**[kvm](http://kvm.qumranet.com/kvmwiki):** Rumored to have been not ready for prime time, but when used from libvirt with virt-manager, has been very nice for me. It requires hardware virtualization support. One major problem in kvm on Ubuntu 8.04 is with [the CD/DVD driver when using RHEL/CentOS guests](https://bugs.launchpad.net/ubuntu/+source/kvm/+bug/239355). To work around that, I used the net install and it worked fine.

**[VirtualBox](http://www.virtualbox.org/):** This was for me the simplest of all for desktop stuff. I've used both the OSE (Open Source Edition) in Ubuntu and Sun's cost-free but proprietary package on Windows Vista. The current release of VirtualBox only emulates i386 32-bit machines at the moment, though! (No 64-bit guests, though a 64-bit host is fine.) It's also been a little buggy at times -- I've had a few machine crashes when running both an OpenBSD 4.3 and a RHEL 5 guest, though I wasn't able to reproduce the problem and it's possible it wasn't a VirtualBox issue.

I should note that some manufacturers have a BIOS option to disable hardware virtualization, and that it is sometimes disabled by default. When booting a new machine, check for that, especially in servers you won't necessarily want to take down later.

A final note about RHEL 5's net install: Why, oh why, does the installer ask for an HTTP install location as separate web site and directory entries, instead of a universally used and easy URL? And further, when the install source I'm using goes down (as download mirrors occasionally do), why are my only options to reboot or retry? Would it have been so hard to allow me the option of entering a new download URL? Yes, I know, I need to send in a patch.


