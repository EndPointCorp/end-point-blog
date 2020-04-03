---
author: Bharathi Ponnusamy
title: How we automated Ubuntu-18.04 install on a different partition from an existing Ubuntu installation
tags: Linux, ubuntu, update, open-source, sysadmin, DevOps, scalability, chef
---

![Clean setup](/blog/2020/04/10/how-we-automated-ubuntu-18.04-install-on-a-different-partition-from-an-existing-ubuntu-installation/banner.jpg)
Photo by [Patryk Grądys](https://unsplash.com/@patrykgradyscom) on [Unsplash](https://unsplash.com/photos/4pPzKfd6BEg)

Our liquid Galaxy systems are running on the physical hardware with Ubuntu 14.04 LTS Operating systems and it’s located on the different remote locations.
We decided to upgrade them to the Ubuntu 18.04 LTS as Ubuntu 14.04 LTS reaches the end of life on April 30, 2019

### Upgrading from Ubuntu 14.04 LTS

Naturally, the recommended way for those on Ubuntu 14.04 LTS is to upgrade to 16.04 LTS and then 16.04 LTS to Upgrade to18.04 LTS, which will continue to receive support until April 2023.
Ubuntu does have LTS -> LTS upgrades, allowing you to skip intermediate non-LTS releases.
But we can’t skip intermediate LTS releases. we have to go via 16.04. 
14.04 LTS -> 16.04 LTS -> 18.04 LTS

Unless you want to do a fresh install of 18.04 LTS.
For a little more longevity, we decided to the fresh install of Ubuntu 18.04 LTS. Not only is this release supported into 2023 but it will offer a direct upgrade route to Ubuntu 20.04 LTS after it’s is released April 2020

### Installing Clean Ubuntu 18.04 LTS from Ubuntu 14.04 LTS
### Install debootstrap
The debootstrap utility installs a very minimal Debian system. debootstrap tool will install Debian-based Linux OS into a sub-directory. You don’t need an installation CD for this purpose. However, you need to have access to the corresponding Linux distribution repository (e.g. Debian or Ubuntu).

```
  /usr/bin/apt-get update
  /usr/bin/apt-get -y install debootstrap
```

### Creating new root partition

Create a logical volume for 12G and format the filesystem to ext4

```
/sbin/lvcreate -L12G -n ROOT_VG/ROOT_VOLUME
/sbin/mkfs.ext4 /dev/ROOT_VG/ROOT_VOLUME
```

### Mounting new root partition

Mount the partition as `/mnt/root18` (the installation point, to be the root (`/`) filesystem on your new system

```
/bin/mkdir -p "/mnt/root18"
/bin/mount /dev/ROOT_VG/ROOT_VOLUME /mnt/root18
```

### Bootstrapping new root partition
Debootstrap can download the needed files directly from the archive when you run it. You can substitute any Ubuntu archive mirror for ports.ubuntu.com/ubuntu-ports in the command example below, preferably a mirror close to you network-wise. Mirrors are listed at http://wiki.ubuntu.com/Archive.
Substitute ARCH in the debootstrap command: amd64, arm64, armhf, i386, powerpc, ppc64el, or s390x.

`/usr/sbin/debootstrap --arch "$ARCH" "$DISTRO" "$ROOT_MOUNTPOINT”`
`/usr/sbin/debootstrap --arch "amd64" "bionic" "/mnt/root18"`

### Installing fstab

 This just changes the root(/) partition path in the new installation also keeping the `/boot` partition intact
	For example `/dev/mapper/headVG-root /`  -> `/dev/mapper/headVG-root18 / `
Why `/boot` uses UUID, because device names are not guaranteed to the same across the reboot or when a new device is connected. So we use UUID(Universally Unique Identifier) to refer the partitions in the fstab. But we don't need to use UUIDs for the logical volumes since it can't be duplicated. 

``` 
OLD_ROOT_PATH="$(awk '$2 == "/" { print $1 }' /etc/fstab)"
/bin/sed "s:^${OLD_ROOT_PATH}\s:/dev/mapper/headVG-root18 :" /etc/fstab > "/mnt/root18/etc/fstab" 
```

### Mounting things in the new root partition
bind mount `/dev` and mount the `/sysfs` `/proc` and `/devpts` from your host system to the target system

```
/bin/mount --bind /dev "/mnt/root18/dev"
/bin/mount -t sysfs none "/mnt/root18/sys"
/bin/mount -t proc none "/mnt/root18/proc"
/bin/mount -t devpts none "/mnt/root18/dev/pts"
```

### Configuring apt
Debootstrap will have created a very basic  `/mnt/root18/etc/apt/sources.list` that will allow installing additional packages. However, it is suggested that you add some additional sources, for example for source packages and security updates:

```
/bin/echo "deb http://us.archive.ubuntu.com/ubuntu bionic main universe
deb-src http://us.archive.ubuntu.com/ubuntu bionic main universe
deb http://security.ubuntu.com/ubuntu bionic-security main universe
deb-src http://security.ubuntu.com/ubuntu bionic-security main universe" > "/mnt/root18/etc/apt/sources.list"
```

Make sure to run **apt update** inside the **chroot** after you have made changes to the target system sources list.

Now we’ve got a real Ubuntu system, though rather lean, on disk. **chroot** into it to set-up the base configurations.
 `LANG=C.UTF-8 chroot /mnt/root18 /bin/bash`

### Installing required packages and running chef-client
As we are maintaining most of the Liquid galaxy configuration and packages via chef, we need to install chef-client and configure it on the new target system and run the chef-client to complete the set-up
 
Copy chef configuration and persistent net udev rules into place 
```
cp -a /etc/chef "/mnt/root18/etc/"
cp /etc/udev/rules.d/70-persistent-net.rules /mnt/root18/etc/udev/rules.d/
```

Install and run chef-client and it create the things to user login
```
/bin/cat << EOF | chroot "/mnt/root18"
/usr/bin/apt-get update && /usr/bin/apt-get install -y curl wget
/usr/bin/curl -L https://omnitruck.chef.io/install.sh | /bin/bash -s -- -v 12.5.1
/usr/bin/chef-client -E production_trusty -o 'recipe[users]'
EOF
```

Chroot and install the required packages 
```
cat << EOF | chroot "$ROOT_MOUNTPOINT"
/bin/mount /boot
/usr/bin/apt-get update && /usr/bin/apt-get install -y --no-install-recommends linux-image-generic lvm2 openssh-server ifupdown net-tools
/usr/sbin/locale-gen en_US.UTF-8
EOF
```

### Set Ubuntu 14.04 to boot default
Backing up the current trusty kernel files into `/boot/trusty` directory and create a custom menu entry configuration for Ubuntu 14.04 on 42_custom_trusty. 
Update the `/etc/default/grub` to set Ubuntu 14.04 as default menu entry and run the update-grub to make it effective on the current system.
 
* This will be useful as a fail-safe method to run the Trusty OS again if there is a problem with the new installation.


```
mkdir -vp /boot/trusty
cp -v /boot/*-generic /boot/trusty/
sed -i 's/GRUB_DEFAULT=.*/GRUB_DEFAULT="TRUSTY"/' /etc/default/grub
update-grub
```

Create the custom menu entry for Ubuntu 14.04 and ubuntu 18.04 on the target system 42_custom_menu_entry 
```
mkdir -p /mnt/root18/etc/grub.d
cat 42_custom_template > /mnt/root18/etc/grub.d/42_custom_menu_entry
```

 chroot into it to the target system and run the update-grub, this will also update the grub configuration to boot Ubuntu 14.04  as default, and update the 0th menu entry as Ubuntu 18.04 (Bionic) 
```
cat << EOF | chroot "/mnt/root18"
update-grub
EOF
```

### Boot into Bionic
To boot into Ubuntu 18.04(Bionic) reboot the system followed by `grub-reboot bionic`  and test the bionic system is working fine as expected 

```
$ grub-reboot bionic
$ reboot 
```

Reboot and test the 0th menu entry followed by `grub-reboot 0`
```
$ grub-reboot 0
$ reboot 
```

Normal reboot returns to the Ubuntu 14.04(Trusty) Because Default menu entry is set to Ubuntu 14.04(Trusty)

### Set Ubuntu 18.04 to boot default
To set the Ubuntu 18.04 as default menu entry, update GRUB_DEFAULT as 0  on  `/etc/default/grub`  and run the update-grub to make it effective.
Next reboot goes to  Ubuntu 18.04

```
sed -i 's/GRUB_DEFAULT=.*/GRUB_DEFAULT=0/‘ /etc/default/grub
update-grub
```

### Congratulations! Here is our newly installed Ubuntu 18.04 system
