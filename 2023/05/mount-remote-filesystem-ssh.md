---
author: "Trevor Slocum"
title: "Mount a remote filesystem over SSH using SSHFS"
github_issue_number: 0
date: 2023-05-02
tags:
- ssh
- tips
---

<!-- TODO Photo -->

While creating and debugging software, it is important to reduce the amount of
friction between each iteration of making a change to the software and then
testing that change. Over time, even small amounts of friction can lead to
fatigue and decreased performance. Because of this, we should take every
opportunity to make our workflow as smooth and comfortable as possible.

A common source of friction when developing software running on remote systems
is the separation between your personal computer and the server. Your personal
computer likely has an IDE configured just the way you like. The server, on the
other hand, is likely configured to be easily available to everyone on your team.

You could copy files back and forth between systems using SFTP or some other
file transfer protocol. This works for quick one-off changes, but for
development requiring multiple iterations you would likely want a more
streamlined workflow.

If only there was a way to use the software installed on your personal system
to edit files on a remote system, without copying the files back and forth...

There is! [SSHFS](https://en.wikipedia.org/wiki/SSHFS) is a tool for mounting
and interacting with remote directories over [SSH](https://en.wikipedia.org/wiki/Secure_Shell).

### Installation

This guide contains installation instructions for macOS and Linux systems only.

If you are using Windows, check out [sshfs-win](https://github.com/winfsp/sshfs-win).

#### macOS instructions

Download the macFUSE and SSHFS packages from [this website](https://osxfuse.github.io)
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

Let's say we want to mount the remote directory `/var/www/html` on the remote
system at `example.com` as the remote user `wildfly`. We want to mount this
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
