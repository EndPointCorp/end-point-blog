---
author: Jon Jensen
gh_issue_number: 547
tags: debian, linux, redhat, security, sysadmin, ubuntu
title: Linux unshare -m for per-process private filesystem mount points
---

### Private mount points with unshare

Linux offers some pretty interesting features that are either new, borrowed, obscure, experimental, or any combination of those qualities. One such feature that is interesting is the **unshare() function**, which the unshare(2) man page says “allows a process to disassociate parts of its execution context that are currently being shared with other processes. Part of the execution context, such as the mount namespace, is shared implicitly when a new process is created using fork(2) or vfork(2)”.

I’m going to talk here about one option to unshare: **per-process private filesystem mount points**, also described as mount namespaces. This Linux kernel feature has been around for a few years and is easily accessible in the userland command unshare(1) in util-linux-ng 2.17 or newer (which is now simply util-linux again without the "ng" distinction because the fork took over mainline development).

Running `unshare -m` gives the calling process a private copy of its mount namespace, and also unshares file system attributes so that it no longer shares its root directory, current directory, or umask attributes with any other process.

Yes, completely private mount points for each process. Isn’t that interesting and strange?

### A demonstration

Here’s a demonstration on an Ubuntu 11.04 system. In one terminal:

```bash
% su -
Password:
# unshare -m /bin/bash
# secret_dir=`mktemp -d --tmpdir=/tmp`
# echo $secret_dir
/tmp/tmp.75xu4BfiCw
# mount -n -o size=1m -t tmpfs tmpfs $secret_dir
# df -hT
Filesystem    Type    Size  Used Avail Use% Mounted on
/dev/mapper/auge-root
              ext4    451G  355G   74G  83% /
```

There’s no system-wide sign of /tmp/tmp.* there thanks to mount -n which hides it. But it can be seen process-private here:

```bash
# grep /tmp /proc/mounts
tmpfs /tmp/tmp.75xu4BfiCw tmpfs rw,relatime,size=1024k 0 0
# cd $secret_dir
# ls -lFa
total 36
drwxrwxrwt  2 root root    40 2011-11-03 22:10 ./
drwxrwxrwt 21 root root 36864 2011-11-03 22:10 ../
# touch play-file
# mkdir play-dir
# ls -lFa
total 36
drwxrwxrwt  3 root root    80 2011-11-03 22:10 ./
drwxrwxrwt 21 root root 36864 2011-11-03 22:10 ../
drwxr-xr-x  2 root root    40 2011-11-03 22:10 play-dir/
-rw-r--r--  1 root root     0 2011-11-03 22:10 play-file
```

Afterward, in another terminal, and thus a separate process with no visibility into the above-shown terminal process’s private mount points:

```bash
% su -
Password:
# grep /tmp /proc/mounts
# cd /tmp/tmp.75xu4BfiCw
# ls -lFa
total 40
drwx------  2 root root  4096 2011-11-03 22:10 ./
drwxrwxrwt 21 root root 36864 2011-11-03 22:18 ../
```

It’s all secret!

### Use cases

This feature makes it possible for us to create a private temporary filesystem that even other root-owned processes cannot see or browse through, raising the bar considerably for a naive attacker to get access to sensitive files or even see that they exist, at least when they’re not currently open and visible to e.g. lsof.

Of course a sophisticated attacker would presumably have a tool to troll through kernel memory looking for what they need. As always, assume that a sophisticated attacker who has access to the machine will sooner or later have anything they really want from it. But we’d might as well make it a challenge.

Another possible use of this feature is to have a process unmount a filesystem privately, perhaps to reduce the exposure of other files on a system to a running daemon if it is compromised.

### /etc/mtab vs. /proc/mounts

Experimenting with this feature also drew my attention to differences in how popular Linux distributions expose mount points. There are actually traditionally two places that the list of mounts is stored on a Linux system.

First, the classic Unix **/etc/mtab**, which is in essence a materialized view. It is the reason that on the Ubuntu 11.04 example above we see the private mount point everywhere on the system, but it reported different disk sizes. The existence of the mount point was global in /etc/mtab but the sizes are determined dynamically and differ based on process’s view into the mount points themselves. The `mount -n` option tells mount to not put the new mount point into /etc/mtab. And this is what the df(1) command refers to. How repulsive that a file in the normally read-only /etc is written to so nonchalantly!

Second, the Linux-specific **/proc/mounts**, which is real-time, exact, and accurate, and can appear differently to each process. The mount invocation can’t hide anything from /proc/mounts. This is what you would think is the only place to look for mounts, but /etc/mtab is still used some places.

Ubuntu 11.04 still has both, with a separate /etc/mtab. Fedora 16 has done away with /etc/mtab entirely and made it merely a symlink to /proc/mounts, which makes sense, but that is a newer convention and leads to the surprising difference here.

### Linux distributions and unshare

The unshare userland command in util-linux(-ng) comes with RHEL 6, Debian 6, Ubuntu 11.04, and Fedora 16, but *not* on the very common RHEL 5 or CentOS 5. Because we needed it on RHEL 5, I made a simple package that contains only the unshare(1) command and peacefully coexists with the older stock RHEL 5 util-linux. It’s called util-linux-unshare and here are the RPM downloads for RHEL 5:

- x86_64: [util-linux-unshare-2.20.1-3.ep.x86_64.rpm](https://packages.endpoint.com/rhel/5/os/x86_64/util-linux-unshare-2.20.1-3.ep.x86_64.rpm)
- i386: [util-linux-unshare-2.20.1-3.ep.i386.rpm](https://packages.endpoint.com/rhel/5/os/i386/util-linux-unshare-2.20.1-3.ep.i386.rpm)
- SRPM: [util-linux-unshare-2.20.1-3.ep.src.rpm](https://packages.endpoint.com/rhel/5/os/SRPMS/util-linux-unshare-2.20.1-3.ep.src.rpm)

I hope you’ve found this as interesting as I did!

### Further reading

- Karel Zak is the util-linux maintainer and a Red Hat employee; see his [detailed blog post about the unshare command](http://karelzak.blogspot.com/2009/12/unshare1.html)
- [unshare(2)](http://linux.die.net/man/2/unshare) function man page
- [unshare(1)](http://linux.die.net/man/1/unshare) userland command man page
- The difference between /etc/mtab and /proc/mounts is described well in [Karel Zak’s blog post about bind mounts ](http://karelzak.blogspot.com/2011/04/bind-mounts-mtab-and-read-only.html)
- [util-linux overview](http://en.wikipedia.org/wiki/Util-linux)
