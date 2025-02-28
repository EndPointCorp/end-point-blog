---
title: "Resolving iptables Update Issues on Rocky Linux and Other RHEL-Based Systems"
date: 2025-02-28
author: "Jeffry Johar"
featured:
  image_url: /blog/2025/02/resolving-iptables-update/elevators.webp
description: A step-by-step guide on updating iptables-legacy to iptables-nft
github_issue_number: 2097
tags:
- redhat
- iptables
- sysadmin
---

![Two elevators on either side of a hall, with orange construction plastic stretched out in front of the entrances. At the end of a hall is a window looking out over a city.](/blog/2025/02/resolving-iptables-update/elevators.webp)

<!-- Photo by Jeffry Johar: https://www.pexels.com/photo/elevator-and-renovation-27595304/ -->

If you are on iptables-legacy systems, you may encounter errors when attempting to perform an OS update involving `iptables-libs-1.8.10-11.el9_5.x86_64` on Rocky Linux or other Red Hat-based operating systems:

```plain
Error:
 Problem: cannot install both iptables-libs-1.8.10-11.el9_5.x86_64 from baseos and iptables-libs-1.8.10-4.el9_4.x86_64 from @System
  - package iptables-legacy-1.8.10-4.1.el9.x86_64 from @System requires (iptables-libs(x86-64) = 1.8.10-4.el9 or iptables-libs(x86-64) = 1.8.10-4.el9_4), but none of the providers can be installed
  - cannot install the best update candidate for package iptables-libs-1.8.10-4.el9_4.x86_64
  - cannot install the best update candidate for package iptables-legacy-1.8.10-4.1.el9.x86_64
(try to add '--allowerasing' to command line to replace conflicting packages or '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
```

### Cause of the error

The latest package, `iptables-libs-1.8.10-11.el9_5.x86_64`, is incompatible with iptables-legacy. To proceed with the update, you must remove iptables-legacy and transition to iptables-nft, which uses the `nf_tables` kernel API while maintaining the same iptables commands and rules.

> **Note:** This guide does not migrate your system to nftables. Your existing iptables rules and commands will still work.

### Step-by-step solution

#### 1. Back up your iptables and ip6tables rules

Before making any changes, ensure your current rules are saved.

```plain
iptables-save > /root/iptables.rules.bak
ip6tables-save > /root/ip6tables.rules.bak
```

#### 2. Update with `--allowerasing`

Use the following command to proceed with the update and automatically remove conflicting packages.

```plain
dnf update --allowerasing
```

#### 3. Ensure iptables-legacy is removed

Check if iptables-legacy was removed. If not, manually remove it:

```plain
dnf remove iptables-legacy-libs
```

#### 4. Install the new iptables-nft services

Install the updated iptables utilities and its systemd service script.

```plain
dnf install iptables-utils iptables-nft-services
```

#### 5. Restore your iptables rules

If your rules were backed up during the package update, they may be saved as `.rpmsave` files. Restore them as follows:

```plain
cd /etc/sysconfig
mv iptables iptables.old
mv iptables.rpmsave iptables
mv ip6tables ip6tables.old
mv ip6tables.rpmsave ip6tables
```

If the `.rpmsave` files do not exist, restore from your backup:

```plain
cp /root/iptables.rules.bak /etc/sysconfig/iptables
cp /root/ip6tables.rules.bak /etc/sysconfig/ip6tables
```

#### 6. Enable and start the iptables services

Ensure the iptables services are enabled and running:

```plain
systemctl enable iptables --now
systemctl enable ip6tables --now
```

#### 7. Verify the iptables rules

Confirm that your desired rules are loaded correctly:

```plain
iptables -nL
ip6tables -nL
```

Your system is now updated, and the iptables rules should be functioning as expected. This completes the installation process.

