---
author: Szymon Lipiński
gh_issue_number: 590
tags: hosting, linux, ubuntu
title: Easy creating ramdisk on Ubuntu
---

Hard drives are extremely slow compared to RAM. Sometimes it is useful to use a small amount of RAM as a drive.

However, there are some drawbacks to this solution. All the files will be gone when you reboot your computer, so in fact it is suitable only for storing some temporary files—​those which are generated during some process and are not useful later.

I will mount the ramdisk in my local directory. I use Ubuntu 11.10, my user name is ‘szymon’, and my home directory is ‘/home/szymon’.

I create the directory for mounting the ramdisk in my home dir:

```nohighlight
mkdir /home/szymon/ramdisk
```

When creating the ramdisk, I have a couple of possibilities:

- ramdisk—​there are sixteen standard block devices at /dev/ram* (from /dev/ram0 to /dev/ram15) which can be used for storing ram data. I can format it with any of the filesystems I want, but usually this is too much complication
- ramfs—​a virtual filesystem stored in ram. It can grow dynamically, and in fact it can use all available ram, which could be dangerous.
- tmpfs—​another virtual filesystem stored in ram, but because it has a fixed size, it cannot grow like ramfs.

I want to have a ramdisk that won’t be able to use all of my ram, and I want to keep it as simple as possible; therefore, I will use tmpfs.

The following command will mount a simple ramdisk in my new local directory.

```nohighlight
$ sudo mount -t tmpfs -o size=512M,mode=777 tmpfs
/home/szymon/ramdisk
```

I can even unmount it with:

```nohighlight
$ sudo umount /home/szymon/ramdisk
```

Let’s check if the ramdisk is really there. I can do so in a couple of ways.

I can use df -h to check the size of the mounted device:

```nohighlight
$ df -h | grep szymon
tmpfs                 512M     0  512M   0% /home/szymon/ramdisk
```

I can also use mount to report on the mounted devices:

```nohighlight
$ mount | grep ramdisk
tmpfs on /home/szymon/ramdisk type tmpfs (rw,size=512M,mode=777)
```

There is one more thing to do—​make the ramdisk load automatically at machine start. This can be done by adding the following line into /etc/fstab:

```nohighlight
tmpfs    /home/szymon/ramdisk    tmpfs    rw,size=512M,mode=777 0    0
```

Two things to be aware of:

- Data stored in ramdisk will be removed at the machine restart. Creating a script for saving the files to hard drive at machine shutdown won’t persist the data during a machine crash or reset.
- The computer won’t be able to boot normally if the entry in the fstab file has any errors in it. If you do make such an error, you can always boot the computer in recovery mode, so you have the root console and can fix the fstab file.
