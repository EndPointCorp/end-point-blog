---
author: Cas Rusnov
title: Installing CentOS 5 on a 3 TB Drive
github_issue_number: 874
tags:
- redhat
- devops
date: 2013-11-06
---

In collaboration with Spencer Christensen and Lele Calo.

The everyday problem: Set up a remotely-hosted machine with a 3 TB drive.

The bigger problem: *It must be CentOS 5*.

While this would be a trivial task with a newer OS, CentOS 5 only supports MBR style partitioning, which itself only supports drives less than 2 TB in size; well let us be clear, the installer and GRUB shipped with the installation disk only support MBR normally, the kernel supports the GPT format. GPT is a newer partition format that was introduced by EFI standard, which can support booting from large devices. From various documents and postings on the internet it seemed possible to still use MBR with more than 2TB, but in practice this turned out to be completely unsuccessful. So we moved on with a plan to use GPT.

Since the CentOS 5 installer cannot work with GPT partition tables, we needed to use something else to create the partitions we wanted. We did this by using a rescue CD, like SystemRescue CD from here [http://www.sysresccd.org/Download](http://www.sysresccd.org/Download).

- Boot into the rescue CD
- Use gdisk to first delete the old partition table to make sure you start cleanly.

        - gdisk, then x (for extended commands), then z to delete.

- Then go through the process to create the partitions as desired. We wanted:

        - /boot 500M
        - 1.5TB LVM physical disk
        - remaining space LVM physical disk

- Save the partition table and quit gdisk
- Create LVM group and volumes as desired. Here’s what we did:

        - pvcreate /dev/sda2, then pvcreate /dev/sda3
        - vgcreate vg0 /dev/sda2 /dev/sda3
        - lvcreate -L 32G -n swap vg0
        - lvcreate -L 100G -n root vg0

- Then make the file systems for those volumes.

        - mkfs.ext3 /dev/sda1 (the /boot partition)
        - mkswap /dev/vg0/swap
        - mkfs.ext4 /dev/vg0/root

Once the partitioning is set up as required, we boot the CentOS 5 rescue CD for the installation process. The installation disc also incidentally contains a rescue mode which can be used by typing linux rescue at the boot prompt. Follow the instructions to get to the rescue prompt. If the network install CD image is used, follow the menus until a choice as to how to load the rescue image is given, then select the appropriate method. We used the HTTP method, and specified vault.centos.org as the server name, and /5.10/os/x86_64 as the path (use your favorite mirror as needed); this step involves loading the rescue image which may take some time, at the end of which you will be prompted to find your existing OS, since there is none, select Skip and this will result in being dropped to the rescue prompt. Once at the rescue prompt, we can proceed to the OS installation step.

The first installation step at this stage is to modify anaconda so that it doesn’t produce an unskippable error due to there being an “unsupported” GPT. First create a ramdisk to contain a copy of the anaconda libraries:

```plain
mkdir /mnt/anacondalib
mount -t tmpfs none /mnt/anacondalib
cp -R /mnt/runtime/usr/lib/anaconda/* /mnt/anacondalib/
```

Now edit the python file at /mnt/anacondalib/partitions.py, and on line 1082 (vi and nano are present in the rescue image for editing), change the word “*errors*” to the word “*warnings*”—​this little change allows anaconda to install despite the fact that we’ve setup the partitions using GPT for the /boot partition, which is what will normally cause the install to fail.

Now we mount the changed library directory over the read-only version from the installation media:

```plain
mount -o bind /mnt/anacondalib/ /mnt/runtime/usr/lib/anaconda/
```

Now we have to move /sbin out of way otherwise anaconda will fail complaining that /sbin already exists:

```plain
export PATH=$PATH:/sbin.bak
mv /sbin /sbin.bak
mkdir /sbin
```

Now we can start anaconda:

```plain
centos_mirror="http://vault.centos.org/5.10/os/x86_64/"
anaconda --dmraid --selinux -T -m $centos_mirror
```

You may of course replace $centos_mirror with your preferred mirror.

You may then walk through the Anaconda installation menus, proceeding until you get to the “Partitioning Type” step at which point the Create custom layout should be selected. This will take you to a Partitioning screen showing the partition scheme created during the GPT partition creation steps above. After setting your large main logical volume to mount as / (root) and your boot partition to mount as /boot, you should visually confirm the layout and proceed. After accepting the warning about using unsupported GPT partitioning, you will be prompted for several screens about grub options, all of which should be correct so may be accepted at their defaults. After this, the installation should be able to proceed as normal.

Once the OS installation is complete, you will be prompted to eject any media and reboot the machine. You can go ahead and try (we did), but you should run into an error similar to “No bootable media found.” and the system is unable to boot. This is because the version of grub that is installed doesn’t know how to deal with GPT partition tables. So the next step is to install a newer version of grub. We found some instructions at the bottom of this page: [http://www.sysresccd.org/Sysresccd-Partitioning-EN-The-new-GPT-disk-layout](http://www.sysresccd.org/Sysresccd-Partitioning-EN-The-new-GPT-disk-layout). We didn’t follow those exactly, so here is what we did:

- Download SystemRescue CD from here: http://www.sysresccd.org/Download
- Boot the SystemRescue CD

Then:

```plain
mkdir /mnt/boot
mount /dev/sda1 /mnt/boot   # mount your /boot partition to /mnt/boot
cp /lib/grub/x86_64/* /mnt/boot/grub/
umount /mnt/boot
grub  # no arguments, entered grub shell
root (hd0,0)
setup (hd0,0)
^D # exit grub shell
```

Now reboot the machine (without the SystemRescue CD)

At this point the machine successfully booted for us. Yay! Problem solved.

References:

- [http://oliverpelz.blogspot.it/2010/09/how-to-install-centos-55-on-any-gpt.html](http://oliverpelz.blogspot.it/2010/09/how-to-install-centos-55-on-any-gpt.html)
- [http://richardjh.org/blog/install-centos-large-partitions-using-gpt-disk-layout/](http://richardjh.org/blog/install-centos-large-partitions-using-gpt-disk-layout/)
- [http://www.sysresccd.org/Sysresccd-Partitioning-EN-The-new-GPT-disk-layout](http://www.sysresccd.org/Sysresccd-Partitioning-EN-The-new-GPT-disk-layout)
