---
author: Adam Vollrath
title: Estimating overlayfs File Space Usage on Ubuntu 12.04 LiveCD
github_issue_number: 791
tags:
- google-earth
- linux
- liquid-galaxy
- sysadmin
- ubuntu
date: 2013-04-24
---

End Point’s [Liquid Galaxy](http://liquidgalaxy.endpoint.com/) platform is a cluster of computers distributing the rendering load of Google Earth and other visualization applications. Each of these “display nodes” boots the same disk image distributed over the local network. Our disk image is based on the Ubuntu 12.04 LiveCD, and uses the same [overlayfs](https://git.kernel.org/cgit/linux/kernel/git/mszeredi/vfs.git/tree/Documentation/filesystems/overlayfs.txt?h=overlayfs.current) to combine a read-only ISO with a writeable ramdisk. This [Union mount](http://en.wikipedia.org/wiki/Union_mount) uses [Copy-on-write](http://en.wikipedia.org/wiki/Copy-on-write) to copy files from the read-only “lower” filesystem to the virtual “upper” filesystem whenever those files or directories are opened for writing.

We often allocate 4GB of system memory to the ramdisk containing the “upper” filesystem. This allows 4GB of changed files on the / filesystem, most of which are often Google Earth cache files. But sometimes the ramdisk fills up with other changes and it’s difficult to track down which files have changed unexpectedly.

The df command properly displays total usage for the overlayfs “upper” filesystem mounted at /.

```plain
$ df -h
Filesystem              Size  Used Avail Use% Mounted on
/cow                    3.9G  2.2G  1.8G  55% /
/dev/loop0              833M  833M     0 100% /cdrom
/dev/loop1              808M  808M     0 100% /rofs
```

But how can we identify which files are consuming that space? Because the root device has been pivoted by the casper scripts at boot, the /cow device is not readily available. We often use the du tool to estimate disk usage, but in this case it cannot tell the difference between files in the “upper” ramdisk and the “lower” read-only filesystem. To find the files filling our /cow device, we need a way to enumerate only the files in the “upper” filesystem, and then estimate only their disk usage.

The `mount` command shows the / filesystem is type “overlayfs”.

```plain
$ mount
/cow on / type overlayfs (rw)
/dev/loop0 on /cdrom type iso9660 (ro,noatime)
/dev/loop1 on /rofs type squashfs (ro,noatime)
```

The find command does indicate that most directories exist in the filesystem of type “overlayfs”, and most unmodified files are on the “lower” filesystem, in this case “squashfs”.

```plain
$ sudo find / -printf '%F\t%D\t%p\n' | head -n 7 ### fstype, st_dev, filename
overlayfs 17 /
overlayfs 17 /bin
squashfs 1793 /bin/bash
squashfs 1793 /bin/bunzip2
squashfs 1793 /bin/bzcat
squashfs 1793 /bin/bzcmp
squashfs 1793 /bin/bzdiff
```

However, the modified files are reported to be on an “unknown” filesystem on a device 16. These are the files that have been copied to the “upper” filesystem upon writing.

```plain
$ find /home/lg/ -printf '%F\t%D\t%p\n' | head -n 33
overlayfs 17 /home/lg/
squashfs 1793 /home/lg/.Xresources
unknown  16 /home/lg/.bash_history
squashfs 1793 /home/lg/.bash_logout
squashfs 1793 /home/lg/.bashrc
overlayfs 17 /home/lg/.config
overlayfs 17 /home/lg/.config/Google
unknown  16 /home/lg/.config/Google/GoogleEarthPlus.conf
unknown  16 /home/lg/.config/Google/GECommonSettings.conf
```

I couldn’t quickly discern how find is identifying the filesystem type, but it can use the -fstype test to reliably identify files that have been modified and copied. (Unfortunately find does not have a test for device number so if you have more than one overlayfs filesystem this solution may not work for you.)

Now that we have a reliable list of which files have been written to and copied, we can see which are consuming the most disk space by piping that list to du. We’ll pass it a null-terminated list of files to accommodate any special characters, then we’ll sort the output to identify the largest disk space hogs.

```plain
$ sudo find / -fstype unknown -print0 | du --files0-from=- --total | sort -nr | head -n 4
2214228 total
38600 /var/cache/apt/pkgcache.bin
38576 /var/cache/apt/srcpkgcache.bin
17060 /var/log/daemon.log
```

We included a total in this output, and notice that total is exactly the 2.2GB indicated by the df output above, so I believe this is measuring what we intend.

Of course five hundred 2MB Google Earth cache files consume more space than a single 38MB apt cache file, so we’d like to list the directories whose files are consuming the most ramdisk space. Unfortunately giving find and du depth arguments won’t work: the “unknown” filesystem doesn’t have any directories that we can see. We’ll have to parse the output, and that’s left as an exercise for the reader for now.

I just realized I could’ve simply looked for files modified after boot-time and gotten very similar results, but that’s not nearly as fun. There may be a way to mount only the “upper” filesystem, but I was disappointed by the lack of documentation around overlayfs, which will [likely be included](http://lkml.indiana.edu/hypermail/linux/kernel/1303.1/02476.html) in the mainline 3.10 Linux kernel.
