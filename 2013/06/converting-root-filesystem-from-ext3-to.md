---
author: Jon Jensen
title: Converting root filesystem from ext3 to ext4 on CentOS and RHEL 5.9
github_issue_number: 818
tags:
- hosting
- redhat
date: 2013-06-12
---

Here’s a quick explanation of the procedure to convert the root / filesystem on RHEL and CentOS 5.9 from ext3 to [ext4](https://en.wikipedia.org/wiki/Ext4), because ext3 wasn’t available during install time.

Note that this is not a configuration Red Hat supports, but it works fine. (I believe you cannot convert the /boot filesystem to ext4 on standard RHEL/CentOS 5 because its GRUB can’t handle it, but you can convert all the other filesystems.)

Ideally do this only on a fairly freshly-installed system you don’t mind losing. Back everything up first unless this is a system you don’t mind destroying! This is a risky operation and (ahem) things can go wrong.

You’ll need direct console or KVM access to the server. You can do without that if you can remount -o ro / but that usually won’t work with sshd or other daemons that keep files open on the / filesystem.

You will of course need to adapt the current kernel version and root filesystem block device path in the examples below.

Now, to live dangerously:

- yum -y install e4fsprogs
- Edit /etc/fstab so that the / filesystem is mounted as ext4 (which works with the existing ext3 filesystem as well). If you’re using a battery-backed RAID controller you may want to add the nobarrier mount option. See man mount to read about what that choice entails.
- mkinitrd --with=ext4 --with=ext3 -f /boot/initrd-2.6.18-348.el5.img 2.6.18-348.el5
- shutdown -r now
- Boot into single-user mode: use GRUB to edit the linux arguments adding “single” to the end
- fsck.ext3 -pf /dev/vg0/lv_root
- tune4fs -O extents,uninit_bg,dir_index /dev/vg0/lv_root
- fsck.ext4 -yfD /dev/vg0/lv_root
- shutdown -r now
- Allow it to boot normally into multi-user mode.

There are lots of articles out there about converting from ext3 to ext4, but none I found that covered RHEL/CentOS 5 specifically and contained all the needed steps and actually worked. This is based on info from [here for Debian](https://www.debian-administration.org/article/Migrating_a_live_system_from_ext3_to_ext4_filesystem) and [here for CentOS](https://web.archive.org/web/20100610195928/http://www.centos.org/modules/newbb/viewtopic.php?topic_id=26309&forum=37).
