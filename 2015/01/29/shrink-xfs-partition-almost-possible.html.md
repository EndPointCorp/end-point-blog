---
author: Emanuele “Lele” Calò
gh_issue_number: 1080
tags: redhat, linux, storage, sysadmin, virtualization
title: 'Shrink XFS partition: Almost possible with LVM'
---

If you happen to have reached this page because you’re trying to shrink an XFS filesystem let’s put things straight: sorry, that’s not possible.

But before you go away you should know there’s still hope and I’d like to show you how I used a little workaround to avoid reinstalling a Red Hat Enterprise Linux 7 or CentOS 7 VM using XFS dump/restore on-the-fly and LVM capabilities, both standard choices for the regular RHEL/CentOS 7 setup.

First of all let’s clarify the situation I found myself in. For various reasons I had a CentOS 7 VM with everything already configured and working, installed not many days ago to test new software we’re evaluating.

The VM itself is hosted on a dedicated server we manage on our own, so I had a certain degree of freedom to what I could do without the need of paying any additional fee. You may not be in this same situation, but you can probably try some similar solution for little money if you’re using an “hourly-billed” VPS provider.

The problem was that, even if everything was working and configured, the virtual hard disk device attached to the machine was *too big* and *on the wrong storage area of the virtualization hosting server*.

There was also another minor glitch: The VM itself was using an old virtualization device driver (IDE-based) instead of the new VIRTIO one. Since I knew that the virtualized OS CentOS 7 is capable of using VIRTIO based devices I also took the chance to fix this.

Unfortunately, XFS is not capable of being shrunk at the moment (and for the foreseeable future) so what I needed to do was to:

1. add a new virtual device correctly using VIRTIO and stored in the right storage area of the virtualization host server
2. migrate all the filesystems to the new virtual device
3. set the VM OS to be working from the newly-built partition
4. dismiss the old virtual device

In my specific case this translated to connect to the virtualization hosting server, create a new LVM logical volume to host the virtual disk device for the VM and then add the new virtual device to the VM configuration. Unfortunately in order to have the VM see the new virtual device I had to shut it down.

While connected to the virtualization host server I also downloaded and attached to the VM the latest ISO of [SysRescueCD](http://www.system-rescue-cd.org/) which is a data rescue specialized Linux distribution. I’m specifically using this distro since it’s one of the few which offers the XFS dump/restore tools on the live ISO.

Now the VM was ready to be booted with the SysRescueCD Live OS and then I could start working my way through all the needed fixes. If you’re doing something similar, of course please make sure you have **offsite backups** and have double-checked that they’re readable before doing anything else.

First of all inspect your *dmesg* output and find what is the source virtual device and what’s the new target virtual device. In my case the source was /dev/sda and the target was /dev/vda

```bash
dmesg | less
```

Then create a partition on the new device (eg: /dev/vda1) as Linux type for the /boot partition; this should be of the same size as the source /boot partition (eg: /dev/sda1) and dedicate all the remaining space to a new LVM type partition (eg: /dev/vda2)

```bash
fdisk /dev/vda
# [create /boot and LVM partitions]
```

You could also mount and copy the /boot files or re-create them entirely if you need to change the /boot partition size. Since I kept /boot exactly the same so I could use *ddrescue* (a more verbose version of classic Unix *dd*).

```bash
ddrescue /dev/sda1 /dev/vda1
```

The next step is supposed to migrate the MBR and should be working but in my case the boot phase kept failing so I also needed to reinstall the bootloader via the CentOS 7 rescue system (not covered in this tutorial but briefly mentioned near the end of the article).

```bash
ddrescue -i0 -s512 /dev/sda /dev/vda
```

Then create the target LVM volumes.

```bash
pvcreate /dev/vda2
vgcreate fixed_centos_VG /dev/vda2
lvcreate -L 1G -n swap fixed_centos_VG
lvcreate -l 100%FREE -n root fixed_centos_VG
vgchange -a y fixed_centos_VG
```

Create the target XFS filesystem.

```bash
mkfs.xfs -L root /dev/fixed_centos_VG/root
```

And then create the swap partition.

```bash
mkfs.swap /dev/fixed_centos_VG/swap
```

Next create the needed mountpoints and mount the old source and the new empty filesystems.

```bash
mkdir /mnt/disk_{wrong,fixed}
mount /dev/fixed_centos_VG/root /mnt/disk_fixed
vgchange -a y wrong_centos_VG
mount /dev/centos_VG/root /mnt/disk_wrong
```

Now here’s the real XFS magic. We’ll use **xfsdump** and **xfsrestore** to copy the filesystem content (files, directory, special files) without having to care about files permission, type, extended ACLs or anything else. Plus since it’s only moving *the content* of the filesystem we won’t need to have a partition of the same size and it won’t take as long as copying the entire block device as the process will just have to go through real used space.

```bash
xfs_dump -J - /mnt/disk_wrong | xfs_restore -J - /mnt/disk_fixed
```

If you want a more verbose output, leave out the *-J* option. After the process is done, be sure to **carefully verify** that everything is in place in the new partition.

```bash
ls -lhtra /mnt/disk_fixed/
```

Then unmount the disks and deactivate the LVM VGs.

```bash
umount /mnt/disk_{old,fixed}
vgchange -a n centos_VG
vgchange -a n fixed_centos_VG
```

At this point in order to avoid changing anything inside the virtualized OS (fstab, grub and so on), let’s remove the old VG and rename the newer one with the same name the old one had.

```bash
vgremove centos_VG
pvremove /dev/sda2
vgrename {fixed_,}centos_VG
```

You should be now able to shutdown the VM again, detach the old disk and start the new VM which will be using the new smaller virtual device.

If the boot phase keeps failing, boot the CentOS installation media in **rescue** mode and after **chroot**-ing inside your installation run **grub-install /dev/vda** (targeting your new main device) to reinstall grub.

Only after everything is working as expected, proceed to remove the old unneeded device and remove it from the virtualization host server.
