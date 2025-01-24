---
title: "Rocky Linux 9 via Hetzner Robot for the impatient"
author: "Jeffry Johar"
github_issue_number: 1982
date: 2023-06-12
tags:
- cloud
- hosting
- linux
- sysadmin
- redhat
featured:
  image_url: /blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/arrizqjeffry.webp
---

![Arrizq Jeffry on a go-kart](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/arrizqjeffry.webp)<br>
Image: https://www.pexels.com/photo/go-kart-17122631/

### Update: A Better Way to Install Rocky Linux 9 at Hetzner Cloud

Hey everyone, I wanted to share an update regarding the installation process of Rocky Linux 9 at Hetzner Cloud.

After input from Brian Clemens of the Rocky Linux project and some further exploration and testing, I have a more efficient and straightforward method to get Rocky Linux up and running on the Hetzner platform. You can check out the new method in [my second blog post here](/blog/2023/07/rocky-linux-9-at-hetzner-robot-made-quick-and-easy/).

### About Rocky Linux

Rocky Linux is a free and open-source community-driven operating system designed to be a drop-in replacement for Red Hat Enterprise Linux (RHEL).

Rocky fills the gap left by the end of CentOS, which was a popular Linux distribution based on the same source code as RHEL but offered as a free alternative with community support. CentOS Stream is their new offering, but it is just different enough to not be entirely compatible with RHEL.

Another alternative is AlmaLinux, and everything mentioned here applies to Alma with some adaptation.

### Rocky 9 on Hetzner

Hetzner is a popular hosting company offering bare metal and virtual servers at very affordable prices. It is based in Germany and also has datacenters in Finland and the U.S.

At the time of this writing (June 2023), Rocky Linux 9 is not supported by Hetzner Robot to install on its dedicated physical servers. Despite Hetzner's the `installimage` software indicating support, attempting to install it will result in the following error, at least on some of its servers:

![EFI error](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/efi-error.webp)
“ERROR: We do not yet support rockylinux 91 on EFI systems”

If you are looking for a workaround, consider installing Rocky Linux 8 and upgrading it to version 9.

While it's important to note that this installation approach hasn't undergone comprehensive vendor testing, we have used it and I'll provide you with the following step-by-step instructions to accomplish it.

### Provisioning the Server

To get started, follow [Hetzner's guide](https://docs.hetzner.com/robot/dedicated-server/general-information/root-server-hardware) to order and provision a server from Hetzner Robot.

Once the server has been provisioned, you may proceed to the next step.

### Enabling Rescue Mode

1. Access the Hetzner Robot interface and navigate to the "Rescue" tab.
2. Choose Linux as the rescue media and select the SSH key option to access the server. Alternatively, use the generated root password.
3. Click the "Activate rescue system" button.

![Robot Menu](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/robot-rescue.webp)

### Rebooting the Server

1. Switch to the "Reset" tab.
2. Select the "CTRL+ALT+DEL" option.
3. Click "Send" to reboot the server.

![Robot Menu](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/robot-reset.webp)

### Accessing the Rescue System

After a few minutes, SSH into the server using `root@[server IPv4 or server IPv6 address]` to access the rescue system.

### Installing Rocky Linux 8:

1. Once in the rescue system, proceed with the installation of Rocky Linux 8. For this installation, we're going to configure the disk storage to use RAID 6 and LVM, with filesystems as follows:

- /boot/efi ESP: 256MB
- /boot ext4: 1GB
- LVM vg0 (rest of the disk)
- /dev/vg0/root ext4: 50GB
- /dev/vg0/home ext4: 100GB
- /dev/vg0/swap swap: 1GB
- Rest of vg0: unallocated, for future use

2. Run the command: `imageinstall` and you should get the following menu.

![Robot Menu](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/installimage.webp)

3. Choose "Rocky Linux" → "Rocky Linux 8.2". After confirming the selection, you will be brought to the configuration file.

4. In the configuration file, put these values that set up the planned filesystems and LVMs as specified.

```bash
PART /boot ext4 1G
PART /boot/efi esp 256M
PART lvm vg0 all
LV vg0 root / ext4 50G
LV vg0 home /home ext4 100G
LV vg0 swap swap swap 1G
```
5. Press F10 to exit the configuration file editor, and the OS installation will resume.

### Completing the Installation

1. Once the installation is done, reboot the rescue system.
After a few minutes, SSH into the server again using `root@[server IPv4 or server IPv6 address]`. The SSH key and root password will be the same as the rescue system.

2. Execute the following to verify the OS is Rocky Linux 8:

```bash
cat /etc/os-release
```

### Upgrading to Rocky Linux 9:

1. Execute the following commands to upgrade the OS to Rocky Linux 9.2:

```bash
export REPO_URL="https://download.rockylinux.org/pub/rocky/9/BaseOS/x86_64/os/Packages/r"
export RELEASE_PKG="rocky-release-9.2-1.5.el9.noarch.rpm"
export REPOS_PKG="rocky-repos-9.2-1.5.el9.noarch.rpm"
export GPG_KEYS_PKG="rocky-gpg-keys-9.2-1.5.el9.noarch.rpm"
dnf install $REPO_URL/$RELEASE_PKG $REPO_URL/$REPOS_PKG $REPO_URL/$GPG_KEYS_PKG
rm -rf /usr/share/redhat-logos
dnf --releasever=9 --allowerasing --setopt=deltarpm=false distro-sync -y
```
2. Execute the following to change the hostname to whatever you want it to be:

```bash
hostnamectl set-hostname mynewhostname
```

3. Reboot the system to complete the OS upgrade.

### Accessing the Rocky Linux 9 System:

1. After a few minutes, SSH into the server again using `root@[server IPv4 or server IPv6 address]`.

2. Remove dnf modules from Rocky Linux 8.

```bash
dnf module disable python36 virt
```

3. Execute the following to update the RPM database.

```bash
rpm --rebuilddb
```

4. Execute the following to verify the OS is Rocky Linux 9.

```bash
cat /etc/os-release
```

### Conclusion

That's all, folks.

You can get past the EFI issue you encountered by installing Rocky Linux 8 on Hetzner Robot and upgrading it in-place to Rocky Linux 9.

With these instructions, you can transition to the new and shiny Rocky Linux 9 without waiting for specific support by Hetzner Robot. Enjoy the enhanced features and capabilities of this updated version.
