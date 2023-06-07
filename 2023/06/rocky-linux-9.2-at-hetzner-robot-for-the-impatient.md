---
title: "Rocky Linux 9.2 at Hetzner Robot for the impatient"
author: "Jeffry Johar"
date: 2023-06-07
featured:
  image_url: https://www.pexels.com/photo/17122631/
tags:
- Heztner
- Rocky Linux 9
- Cloud Computing
---

![Arrizq Jeffry on a go-kart](/blog/2023/06/rocky-linux-9.2-at-hetzner-robot-for-the-impatient/arrizqjeffry.webp)
<br>Image: https://www.pexels.com/photo/go-kart-17122631/

### Introduction
Rocky Linux is a free and open-source community-driven operating system designed to be a drop-in replacement for CentOS. CentOS was previously a popular Linux distribution that was based on the same source code as Red Hat Enterprise Linux (RHEL) but offered as a free alternative with community support.

As of to date ( 6th June 2023) , Rocky Linux 9 is not supported by Hetzner Robot to install at its dedicated physical servers. Despite the installimage indicating support, attempting to install it will result in the following error: “We do not yet support rockylinux 9.1 on EFI systems”
![EFI error](/blog/2023/06/rocky-linux-9.2-at-hetzner-robot-for-the-impatient/efi-error.webp)

If you are looking for a workaround, consider installing Rocky Linux 8 and upgrading it to version 9. While it's important to note that this installation approach is still in the testing phase and hasn't undergone comprehensive testing, I'll provide you with the following step-by-step instructions to accomplish it.

### Provisioning the Server
To get started, follow the guide in the following link  to order and provision a server from Hetzner Robot. 
https://docs.hetzner.com/robot/dedicated-server/general-information/root-server-hardware

Once the server has been provisioned, you may proceed to the next step. 


### Enabling Rescue Mode

1. Access the Hetzner Robot interface and navigate to the "Rescue" tab.
2. Choose Linux as the rescue media and select the SSH option to access the server. Alternatively, use the generated root password.
3. Click the "Activate rescue system" button.
![Robot Menu](/blog/2023/06/rocky-linux-9.2-at-hetzner-robot-for-the-impatient/robot-rescue.webp)

### Rebooting the Server

1. Switch to the "Reset" tab.
2. Select the "CTRL+ALT+DEL" option.
3. Click "Send" to reboot the server.
![Robot Menu](/blog/2023/06/rocky-linux-9.2-at-hetzner-robot-for-the-impatient/robot-reset.webp)

### Accessing the Rescue System

After a few minutes, SSH into the server using the `root@[server ip4 or server ipv6]` address to access the rescue system.

### Installing Rocky Linux 8.2:

1. Once in the rescue system, proceed with the installation of Rocky Linux 8.2 using RAID6 and LVM. For the installation, we going to set up the filesystem as follows:

- boot/efi esp: 256MB
- /boot ext4: 1GB
- LVM vg0 (rest of the disk)
- /dev/vg0/root ext4: 50GB
- /dev/vg0/home ext4: 10GB
- /dev/vg0/swap swap: 1GB
- Rest of vg0: Unused

2. Run the command: `imageinstall` and you shoud get the following menu. 
![Robot Menu](/blog/2023/06/rocky-linux-9.2-at-hetzner-robot-for-the-impatient/installimage.webp)

3. Choose "Rocky Linux" -> "Rocky Linux 8.2". After confirming the selection, you will be brought to the configuration file. 

4. In the configuration file, put these values that set up the planned filesystems and LVMs as specified.
```bash
PART /boot ext4 1G
PART /boot/efi esp 256M
PART lvm vg0 all
LV vg0 root / ext4 50G
LV vg0 home /home ext4 50G
LV vg0 swap swap swap 1G
```
5. Press F10 to exit the configuration file editor, and the OS installation will resume.

### Completing the Installation

1. Once the installation is done, reboot the rescue system.
After a few minutes, SSH into the server again using `root@[server ip4 or server ipv6]`. The SSH key and root password will be the same as the rescue system.

2. Execute the following to verify the OS is Rocky Linux 8.2
```bash
cat /etc/os-release
```

### Upgrading to Rocky Linux 9.2:

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
2. Execute the following to change the hostname:
```bash
hostnamectl set-hostname mynewhostname
```

3. Reboot the system to complete the OS upgrade.


### Accessing the Rocky Linux 9.2 System:
1. After a few minutes, SSH into the server again using `root@[server ip4 or server ipv6]

2 Execute the following update the RPM database
```bash
rpm --rebuilddb
```

3 Execute the following to verify the OS is Rocky Linux 9.2
```bash
cat /etc/os-release
```

### Conclusion
That's all folks. By following the step-by-step instructions outlined in this guide, you can overcome the issue you encountered with Rocky Linux by installing version 8 and upgrading it to Rocky Linux 9.2 on Hetzner Robot. Although it's essential to note that this installation approach is still in the testing phase and hasn't undergone comprehensive testing, it provides a potential workaround for those seeking to utilize Rocky Linux 9.2. With these instructions, you'll be able to seamlessly transition to the new and shiny Rocky Linux 9.2 on Hetzner Robot. Enjoy the enhanced features and capabilities of this updated version.

