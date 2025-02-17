---
title: "Resolving iptables Update Issues on Rocky Linux and Other RHEL-Based Systems"
date: 2025-02-17
author: "Jeffry Johar"
feature: 
  image_url: /blog/2025/02/resolving-iptables-update/elevators.webp
description: A step by step how-to to update iptables-legacy to iptables-nft 
tags:
- Red Hat
- Rock Linux
- iptables
- sysadmin
---

![Elevators work in progress.](/blog/2025/02/resolving-iptables-update/elevators.webp)
<!-- https://www.pexels.com/photo/elevator-and-renovation-27595304/ --> 

If you are on iptables-legacy systems, you may encounter errors when attempting to perform an OS update involving iptables-libs-1.8.10-11.el9_5.x86_64 on Rocky Linux or other Red Hat-based operating systems.

### Error example
```bash
Error:
 Problem: cannot install both iptables-libs-1.8.10-11.el9_5.x86_64 from baseos and iptables-libs-1.8.10-4.el9_4.x86_64 from @System
  - package iptables-legacy-1.8.10-4.1.el9.x86_64 from @System requires (iptables-libs(x86-64) = 1.8.10-4.el9 or iptables-libs(x86-64) = 1.8.10-4.el9_4), but none of the providers can be installed
  - cannot install the best update candidate for package iptables-libs-1.8.10-4.el9_4.x86_64
  - cannot install the best update candidate for package iptables-legacy-1.8.10-4.1.el9.x86_64
(try to add '--allowerasing' to command line to replace conflicting packages or '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
```	

### Cause of the Error

The latest package `iptables-libs-1.8.10-11.el9_5.x86_64` is incompatible with iptables-legacy. To proceed with the update, you must remove iptables-legacy and transition to iptables-nft, which uses the nf_tables kernel API while maintaining the same iptables commands and rules.

> **Note:** This guide does not migrate your system to nftables. Your existing iptables rules and commands will still work.

### Step-by-Step Solution
**1. Backup Your iptables and ip6tables Rules**
<br>Before making any changes, ensure your current rules are saved.
```bash
iptables-save > /root/iptables.rules.bak
ip6tables-save > /root/ip6tables.rules.bak
```
**2. Update with --allowerasing**
<br>Use the following command to proceed with the update and automatically remove conflicting packages:
```bash
yum update --allowerasing
```
**3.Ensure iptables-legacy is Removed**
<br>Check if iptables-legacy was removed. If not, manually remove it:
```bash
yum remove iptables-legacy-libs
```
**4. Install the New iptables-nft Services**
<br>Install the updated iptables utilities and its systemd service script. 
```bash
yum install iptables-utils iptables-nft-services
```
**5. Restore Your iptables Rules**
<br>If your rules were backed up during the package update, they may be saved as .rpmsave files. Restore them as follows:
```bash
cd /etc/sysconfig
mv iptables iptables.old
mv iptables.rpmsave iptables
mv ip6tables ip6tables.old
mv ip6tables.rpmsave ip6tables
```

If the .rpmsave files do not exist, restore from your backup:
```bash
cp /root/iptables.rules.bak /etc/sysconfig/iptables
cp /root/ip6tables.rules.bak /etc/sysconfig/ip6tables
```

**6. Enable and Start the iptables Services**
<br>Ensure the iptables services are enabled and running:
```bash
systemctl enable iptables --now
systemctl enable ip6tables --now
```

**7. Verify the iptables Rules**
<br>Confirm that your desired rules are loaded correctly:
```bash
iptables -nL
ip6tables -nL
```

Your system is now updated, and the iptables rules should be functioning as expected. This completes the installation process. 


