---
author: "Trevor Slocum"
title: "Mount a remote filesystem over SSH using SSHFS"
github_issue_number: 1965
date: 2023-05-25
tags:
- ssh
- tips
featured:
  image_url: /blog/2023/05/mount-remote-filesystem-sshfs/estuary_at_days_end_crop.webp
---

![A painting of a Dutch port at the end of the day. On the left, sunlight peeks out from clouds low on the horizon, casting rays of light into the light blue sky of the fading day. Trading ships sail the waters, with some disappearing into the horizon. In the foreground, a smaller boat of people and barrels is rowed to an outcropping of land, on which is a boat being tarred by two sailors. A small fire heats a pot next to wooden dock equipment which protrudes into the air.](/blog/2023/05/mount-remote-filesystem-sshfs/estuary_at_days_end_crop.webp)

<!-- Image: Simon de Vlieger, Estuary at Day's End, c. 1640/1645 (cropped from original). Public domain via CC0 -->

While creating and debugging software, it is important to reduce the amount of
friction between each iteration of making a change to the software and then
testing that change. Over time, even small amounts of friction can lead to
fatigue and decreased performance of a developer. Because of this, we should take every
opportunity to make our workflow as smooth and comfortable as possible.

A common source of friction when developing software running on remote systems
is the separation between your personal computer and the server. Your personal
computer likely has an IDE configured just the way you like. The server, on the
other hand, is likely configured to be easily available to everyone on your team.

You could copy files back and forth between systems using SFTP or some other
file transfer protocol. This works for quick one-off changes, but for
development requiring multiple iterations you likely want a more
streamlined workflow.

If only there was a way to use the software installed on your personal system
to edit files on a remote system, without copying the files back and forth...

There is! [SSHFS](https://en.wikipedia.org/wiki/SSHFS) is a tool for mounting
and interacting with remote directories over [SSH](https://en.wikipedia.org/wiki/Secure_Shell).

### Notice

The [SSHFS repository](https://github.com/libfuse/sshfs) has been archived for around a year at the time of writing; the latest release was on May 26, 2022. The repository now has a note about being orphaned and inviting other developers to take over the project. While there are a few forks (most notably [deadbeefsociety's](https://github.com/deadbeefsociety/sshfs) and [stephenxxiu's](https://github.com/stevenxxiu/sshfs)) with some traction, none is a definitive replacement yet.

One alternative suggested by the ArchWiki is using [rclone's mount feature](https://rclone.org/commands/rclone_mount/).

For macOS users, it's important to note that macFUSE is [no longer open-source](https://colatkinson.site/macos/fuse/2019/09/29/osxfuse/) as of 2017.

### Installation

This guide contains installation instructions for macOS and Linux systems only.

If you are using Windows, check out [sshfs-win](https://github.com/winfsp/sshfs-win).

#### macOS instructions

Download the macFUSE and SSHFS packages from [the osxfuse website](https://osxfuse.github.io)
and install them as an administrator.

#### Linux instructions

SSHFS is available from the package repositories of most distributions. This is
usually the preferred way to install software on Linux.

On Debian and Ubuntu systems, the following command will install the latest
version of SSHFS available:

```shell
sudo apt update && sudo apt install sshfs
```

### Usage

After installation you may interact with SSHFS via the `sshfs` command.

Before we mount a remote directory, let's create a local directory that will
serve as the local mount point:

```shell
mkdir /tmp/remote
```

Let's say we want to mount the remote directory `/var/www/html` of the remote
system at `example.com` while connected as the remote user `wildfly`. We want to mount this
remote directory at the local directory `/tmp/remote`. To accomplish this, we
would execute the following command:

```shell
sshfs -o compression=no,cache=yes,cache_timeout=20,auto_cache,idmap=user wildfly@example.com:/var/www/html /tmp/remote
```

The following mount options are given using the `-o` argument:

- `compression=no` - Disable compression. The performance impact of enabling 
compression is not worth the minimal bandwidth savings.
- `cache=yes` - Enable caching. Files that are repeatedly accessed within a
certain period of time will only be retrieved once.
- `cache_timeout=20` - Set cache timeout, in seconds.
- `auto_cache` - Enable caching based on file modification times.
- `idmap=user` - Translate between UID of connecting user and remote user. This
causes remote files to appear to be owned by you, even though they are actually 
owned by the remote user on the remote system.

To unmount on linux, run `fusermount -u /tmp/remote`. On macOS, run `umount /tmp/remote`.
