---
title: "Migrating from Legacy Networking to systemd-networkd on Ubuntu 24.04"
author: Bharathi Ponnusamy
date: 2025-11-17
github_issue_number: 
featured:
  image_url: /blog/2025/11/legacy-networking-to-systemd-networkd/banner.webp
description: Learn how to migrate from Ubuntu’s legacy ifupdown networking to systemd-networkd for better performance, reliability, and easier management. This article explains the configuration, migration steps, and verification process for modern Ubuntu servers.
tags: 
- Ubuntu
- systemd-networkd
- ifupdown
- Networking
- Server Administration
- Linux
- Ubuntu 24.04
- Migration
- Infrastructure
- DevOps
---

![own image.](/blog/2025/11/legacy-networking-to-systemd-networkd/banner.webp)

<!-- photo by Bharathi Ponnusamy -->

### Introduction

During a recent Ubuntu server upgrade, I migrated a production system from the legacy ifupdown networking stack to the modern systemd-networkd service. This migration was part of preparing the server for a smooth upgrade to Ubuntu 24.04, which relies heavily on systemd-managed components.

In this post, I’ll share why this change is necessary, the steps I followed, and how to verify that everything works correctly afterward.

### Why Migrate to systemd-networkd?

Ubuntu 24.04 uses systemd-networkd as the default backend for network management. The traditional ifupdown scripts (/etc/network/interfaces) are no longer the recommended way to configure networking, especially when using modern features like:

- Predictable network interface naming (e.g., ens3, eth0, etc.)
- Built-in support for bridges, VLANs, and bonds
- Faster boot times with asynchronous network handling
- Unified configuration under /etc/systemd/network
- Migrating now avoids future compatibility issues and takes advantage of systemd’s integrated logging and management.

### Step 1: Check the Current Setup

Before the migration, I confirmed the system was still using ifupdown:


```plain
ls /etc/network/interfaces
cat /etc/network/interfaces

```
Output showed legacy configuration similar to:
```
auto eth0
iface eth0 inet static
    address 10.42.41.1
    netmask 255.255.0.0
```

### Step 2: Install and Enable systemd-networkd

If systemd-networkd wasn’t already active, I installed and enabled it:

```plain
sudo apt install systemd-networkd systemd-resolved -y
sudo systemctl enable systemd-networkd
sudo systemctl enable systemd-resolved

```

Then, I stopped ifupdown to prevent conflicts.

### Step 3: Create a Network Configuration File

I created configuration file under `/etc/systemd/network/`.

DHCP-based interface:
``` plain
# /etc/systemd/network/10-eth0.network
[Match]
Name=eth0

[Network]
DHCP=yes
```
Static interface:
``` plain

# /etc/systemd/network/20-eth1.network
[Match]
Name=eth1

[Network]
Address=10.42.41.1/16
Gateway=10.42.0.1
DNS=8.8.8.8
DNS=1.1.1.1

```

### Step 4: Configure systemd-resolved

This step ensures your system’s DNS resolver works correctly with systemd-networkd.

systemd-resolved listens locally on 127.0.0.53 and handles DNS resolution, caching, and per-interface settings.

Link your system’s `/etc/resolv.conf` to use it:

If we skip this, system might lose DNS resolution after reboot.
Applications like apt, curl, and ping may fail to resolve hostnames even though interfaces are up.

```plain
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

then to verify

resolvectl status
```
### Restart and Verify

Restart both services:
``` plain
sudo systemctl restart systemd-networkd
sudo systemctl restart systemd-resolved
```
Check active links:
``` plain
networkctl list
```

Detailed view for one interface:
``` plain
networkctl status eth0
```

Sample output:
``` plain
● 2: eth0
       Type: ether
      State: routable (configured)
     Address: 10.42.41.1/16
     Gateway: 10.42.0.1
     DNS: 8.8.8.8
```

Test 
``` plain
ping -c 3 8.8.8.8
ping -c 3 google.com

```
### Step 6: Reboot and Confirm

Reboot once to ensure everything persists:

After the reboot,
``` plain
systemctl status systemd-networkd
systemctl status systemd-resolved
```
and confirm interface and DNS are still functional.

### Conclusion

Migrating to systemd-networkd brings Ubuntu servers in line with modern Linux networking practices.
It’s cleaner, faster, and integrates directly into the systemd ecosystem, and also simplifying monitoring, automation, and troubleshooting.

