---
author: Bharathi Ponnusamy
title: Installing Ubuntu 18.04 to a different partition from an existing Ubuntu installation
tags: linux, ubuntu, update, sysadmin, devops, chef
gh_issue_number: 1617
---

![Clean setup](/blog/2020/04/06/install-ubuntu-to-different-partition/banner.jpg)

[Photo](https://unsplash.com/photos/4pPzKfd6BEg) by [Patryk Grądys](https://unsplash.com/@patrykgradyscom) on [Unsplash](https://unsplash.com)

Our Liquid Galaxy systems are running on Ubuntu 14.04 LTS (Trusty). We decided to upgrade them to Ubuntu 18.04 LTS (Bionic) since Ubuntu 14.04 LTS reached its end of life on April 30, 2019.

### Upgrading from Ubuntu 14.04 LTS

The recommended way to upgrade from Ubuntu 14.04 LTS is to first upgrade to 16.04 LTS, then to 18.04 LTS, which will continue to receive support until April 2023:

14.04 LTS → 16.04 LTS → 18.04 LTS

Ubuntu has LTS → LTS upgrades, allowing you to skip intermediate non-LTS releases, but we can’t skip intermediate LTS releases; we have to go via 16.04, unless we want to do a fresh install of 18.04 LTS.

For a little more longevity, we decided to do a fresh install of Ubuntu 18.04 LTS. Not only is this release supported into 2023 but it will offer a direct upgrade route to Ubuntu 20.04 LTS when it’s released in April 2020.

### Installing Clean Ubuntu 18.04 LTS from Ubuntu 14.04 LTS

#### Install debootstrap

The [debootstrap](https://linux.die.net/man/8/debootstrap) utility installs a very minimal Debian system. Debootstrap will install a Debian-based OS into a sub-directory. You don’t need an installation CD for this. However, you need to have access to the corresponding Linux distribution repository (e.g. Debian or Ubuntu).

```bash
apt-get update
apt-get -y install debootstrap
```

#### Creating a new root partition

Create a logical volume with size 12G and format the filesystem to ext4:

```bash
lvcreate -L12G -n ROOT_VG/ROOT_VOLUME
mkfs.ext4 /dev/ROOT_VG/ROOT_VOLUME
```

#### Mounting the new root partition

Mount the partition at `/mnt/root18`. This will be the root (/) of your new system.

```bash
mkdir -p /mnt/root18
mount /dev/ROOT_VG/ROOT_VOLUME /mnt/root18
```

#### Bootstrapping the new root partition

Debootstrap can download the necessary files directly from the repository. You can substitute any Ubuntu archive mirror for `ports.ubuntu.com/ubuntu-ports` in the command example below. Mirrors are listed [here](https://wiki.ubuntu.com/Mirrors).

Replace $ARCH below with your architecture: amd64, arm64, armhf, i386, powerpc, ppc64el, or s390x.

```bash
debootstrap --arch $ARCH $DISTRO $ROOT_MOUNTPOINT
debootstrap --arch amd64 bionic /mnt/root18
```

#### Installing fstab

This just changes the root (/) partition path in the new installation while keeping the `/boot` partition intact. For example, `/dev/mapper/headVG-root /` → `/dev/mapper/headVG-root18 /`. Since device names are not guaranteed to be the same after rebooting or when a new device is connected, we use UUIDs (Universally Unique Identifiers) to refer to partitions in fstab. We don’t need to use UUIDs for logical volumes since their device names won’t change.

```bash
OLD_ROOT_PATH="$(awk '$2 == "/" { print $1 }' /etc/fstab)"
sed "s:^${OLD_ROOT_PATH}\s:/dev/mapper/headVG-root18 :" /etc/fstab > /mnt/root18/etc/fstab
```

#### Mounting things in the new root partition

Bind `/dev` to the new location, then mount `/sys`, `/proc`, and `/dev/pts` from your host system to the target system.

```bash
mount --bind /dev /mnt/root18/dev
mount -t sysfs none /mnt/root18/sys
mount -t proc none /mnt/root18/proc
mount -t devpts none /mnt/root18/dev/pts
```

#### Configuring apt

Debootstrap will have created a very basic `/mnt/root18/etc/apt/sources.list` that will allow installing additional packages. However, I suggest that you add some additional sources, such as the following, for source packages and security updates:

```bash
echo "deb http://us.archive.ubuntu.com/ubuntu bionic main universe
deb-src http://us.archive.ubuntu.com/ubuntu bionic main universe
deb http://security.ubuntu.com/ubuntu bionic-security main universe
deb-src http://security.ubuntu.com/ubuntu bionic-security main universe" > /mnt/root18/etc/apt/sources.list
```

Make sure to run `apt update` with `chroot` after you have made changes to the target system sources list.

Now we’ve got a real Ubuntu system, if a rather small one, on disk. `chroot` into it to set up the base configurations.

```bash
LANG=C.UTF-8 chroot /mnt/root18 /bin/bash
```

### Installing required packages and running chef-client

As we are maintaining most of the Liquid Galaxy configuration and packages with [Chef](https://www.chef.io/), we need to install chef-client, configure it on the new target system, and run chef-client to complete the setup.

Copy the chef configuration and persistent net udev rules into place:

```bash
cp -a /etc/chef /mnt/root18/etc/
cp /etc/udev/rules.d/70-persistent-net.rules /mnt/root18/etc/udev/rules.d/
```

Install and run chef-client and let it set up our user login:

```bash
cat <<EOF | chroot /mnt/root18
apt-get update && apt-get install -y curl wget
curl -L https://omnitruck.chef.io/install.sh | bash -s -- -v 12.5.1
chef-client -E production_trusty -o 'recipe[users]'
EOF
```

Next, chroot and install the required packages:

```bash
cat <<EOF | chroot /mnt/root18
mount /boot
apt-get update && apt-get install -y --no-install-recommends linux-image-generic lvm2 openssh-server ifupdown net-tools
locale-gen en_US.UTF-8
EOF
```

### Set Ubuntu 14.04 to boot default

Create file `42_custom_template_trusty`:

```bash
#!/bin/sh
# Entry for trusty system
menuentry 'TRUSTY' --class liquid --class gnu-linux --class gnu --class os {
        # Skipped lines
        linux   /trusty/vmlinuz-$trusty_kernel_version root=/dev/mapper/headVG-root ro nomodeset biosdevname=0 modprobe.blacklist=gma500_gfx quiet
        initrd  /trusty/initrd.img-$trusty_kernel_version
}
```

Create file `42_custom_template_bionic`:

```bash
#!/bin/sh
# Entry for bionic system
menuentry 'BIONIC' --class liquid --class gnu-linux --class gnu --class os {
        # Skipped lines
        linux   /vmlinuz-$bionic_kernel_version-generic root=/dev/mapper/headVG-root18 ro nomodeset net.ifnames=0 biosdevname=0 modprobe.blacklist=gma500_gfx quiet
        initrd  /initrd.img-$bionic_kernel_version-generic
}
```

#### On the Current system (Trusty):

Back up the current Trusty kernel files into `/boot/trusty` and create a custom menu entry configuration for Ubuntu 14.04 on `42_custom_trusty`. Update `/etc/default/grub` to set Ubuntu 14.04 as the default menu entry and run `update-grub` to apply it to the current system. This will be used as a fail-safe method to run Trusty again if there is a problem with the new installation.

```bash
mkdir -vp /boot/trusty
cp -v /boot/*-generic /boot/trusty/

envsubst '${trusty_kernel_version}' < 42_custom_template_trusty > /etc/grub.d/42_custom_template_trusty
chmod +x /etc/grub.d/42_custom_template_trusty

sed -i 's/GRUB_DEFAULT=.*/GRUB_DEFAULT="TRUSTY"/' /etc/default/grub
update-grub
```

#### On the target system (Bionic):

Create the custom menu entry for Ubuntu 14.04 and Ubuntu 18.04 on the target system.

```bash
mkdir -p /mnt/root18/etc/grub.d
envsubst '${trusty_kernel_version}' < 42_custom_template_trusty > /mnt/root18/etc/grub.d/42_custom_template_trusty
envsubst '${bionic_kernel_version}' < 42_custom_template_bionic > /mnt/root18/etc/grub.d/42_custom_template_bionic
chmod +x /mnt/root18/etc/grub.d/42_custom_template_{trusty,bionic}
```

`chroot` into the target system and update `/etc/default/grub` to set Ubuntu 14.04 as the default menu entry and run `update-grub`. This will also update the GRUB configuration to boot Ubuntu 14.04 as default and update the 0th menu entry to Ubuntu 18.04 (Bionic).

```bash
cat <<EOF | chroot /mnt/root18
sed -i 's/GRUB_DEFAULT=.*/GRUB_DEFAULT="TRUSTY"/' /etc/default/grub
update-grub
EOF
```

### Boot into Bionic

To boot into Ubuntu 18.04 (Bionic), reboot the system after `grub-reboot bionic` and test if the bionic system is working as expected.

```bash
$ grub-reboot bionic
$ reboot
```

Reboot and test our new 0th GRUB entry:

```bash
$ grub-reboot 0
$ reboot
```

A normal reboot returns to Ubuntu 14.04 (Trusty) since the default menu entry is still set to Ubuntu 14.04 (Trusty).

### Set Ubuntu 18.04 to boot default

To set our new Ubuntu 18.04 installation as the default menu entry, change GRUB_DEFAULT to 0 in `/etc/default/grub` and run `update-grub` to apply it. The next reboot will boot into Ubuntu 18.04.

```bash
sed -i 's/GRUB_DEFAULT=.*/GRUB_DEFAULT=0/' /etc/default/grub
update-grub
```

Congratulations! You now have a freshly installed Ubuntu 18.04 system.
