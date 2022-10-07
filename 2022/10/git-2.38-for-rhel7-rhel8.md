---
author: "Jon Jensen"
date: 2022-10-05
title: "Git 2.38 packages for RHEL, CentOS, Rocky Linux, AlmaLinux, Oracle Linux 7 and 8"
github_issue_number: 1902
tags:
- git
- sysadmin
- linux
---

![Photo of a wilderness footpath over stone with scattered evergreen trees alongside a clear lake, with a blue sky](/blog/2022/10/git-2.38-for-rhel7-rhel8/20220903-162550-sm.webp)

<!-- photo by Jon Jensen -->

Git 2.38 was released 2 days ago, and it has some interesting new features. Let's look at a couple of them, which you may find make upgrading worthwhile.

### Scalar

Git now includes a new command-line tool called `scalar` which is adapted to working with very large Git repositories. It reminds me of Google's "repo" tool used to manage a group of multiple large Git repositories for the Android project, but unlike that, Scalar focuses on a single repository.

By default it makes a partial clone so that you need far less network transfer and local disk space to work with a large repository. One of our clients has a repository whose `.git` directory for a complete clone takes 7.1 GB, but when using `scalar clone` the partial clone of that repository uses only 46 MB. That's only 0.6% the size! Your experience will vary based on how much of the repository data is in history vs. currently checked-out files.

I use SSH agent confirmation with `ssh-add -c` (on Linux; see references below for tips on doing it on Windows and macOS). Because of that, I am aware of every SSH connection that uses my SSH secret key, and noticed that Scalar had Git make 3 network connections to the origin server rather than just 1.

During later Git operations, having only the most recent commit stored locally leads to some interesting new network calls. For example, when you do plain `git log` to see commits, there's no remote access needed. But doing `git log -p` to see the diffs per commit causes 1 SSH request per commit, quite a bundle of SSH agent confirmations for even a small handful of commits!

Cloning with Scalar also leaves some warnings for your enjoyment, which currently happen no matter which remote Git server I'm cloning from, but maybe these will go away later when servers gain support for some new features being used here:

```plain
warning: filtering not recognized by server, ignoring
warning: filtering not recognized by server, ignoring
warning: fetch normally indicates which branches had a forced update,
but that check has been disabled; to re-enable, use '--show-forced-updates'
flag or run 'git config fetch.showForcedUpdates true'
warning: fetch normally indicates which branches had a forced update,
but that check has been disabled; to re-enable, use '--show-forced-updates'
flag or run 'git config fetch.showForcedUpdates true'
```

Another default feature of Scalar is scheduled background maintenance. On a Linux system with systemd during your first `scalar clone` operation you'll see:

```plain
Created symlink /home/someuser/.config/systemd/user/timers.target.wants/git-maintenance@hourly.timer → /home/someuser/.config/systemd/user/git-maintenance@.timer.
Created symlink /home/someuser/.config/systemd/user/timers.target.wants/git-maintenance@daily.timer → /home/someuser/.config/systemd/user/git-maintenance@.timer.
Created symlink /home/someuser/.config/systemd/user/timers.target.wants/git-maintenance@weekly.timer → /home/someuser/.config/systemd/user/git-maintenance@.timer.
```

showing that it set up systemd timers to maintain your Git clones.

### Rebasing dependent branches

This is a really helpful new feature!

In short, when rebasing, you can now use `git rebase --update-refs` and Git will update other branches that are affected by the changed commit hashes you are currently rebasing.

You probably only want to do that when you're dealing with local private branches of your own, or you're working against a repository where you can force-push branch history rewrites for multiple branches.

### And more ...

There are several other great new features too. This was just to whet your appetite.

The [GitHub blog highlights from Git 2.38](https://github.blog/2022-10-03-highlights-from-git-2-38/) gives an accessible overview of the major new features.

### New Git on an older Enterprise Linux OS

But how soon will you be able to use the new Git? On your own development computer, hopefully soon.

If you're using a server running Red Hat Enterprise Linux or its derivatives CentOS, Rocky Linux, AlmaLinux, or Oracle Linux, you probably only have an old version of Git there that the distribution won't upgrade beyond that major version to avoid introducing incompatibilities.

We have packaged Git 2.38 for RHEL 7 and 8 so anyone can upgrade and use a modern Git version.

Follow [our instructions for installing newer Git](/blog/2021/12/installing-git-2-on-centos-7/). That write-up highlights Git 2.34.1, but since our repositories now include Git 2.38.0, you'll get that newer version.

Enjoy!

### Reference

* [Installing Git 2 on CentOS 7](/blog/2021/12/installing-git-2-on-centos-7/)
* [End Point package repositories](https://packages.endpointdev.com/) for EL 8 also include Git 2.38
* [Git website](https://git-scm.com/)
* [Highlights from Git 2.38](https://github.blog/2022-10-03-highlights-from-git-2-38/) on the GitHub blog
* SSH agent confirmation:
  * On Linux and other Unixes: `ssh-add -c`
  * On Windows, see [Windows SSH key agent confirmation](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/)
  * On macOS, you can use [ssh-askpass for macOS](https://github.com/theseal/ssh-askpass) for normal keys or [Secretive](https://github.com/maxgoedjen/secretive) for keys generated in and stored in Apple's Secure Enclave.
* [Scalar](https://github.com/microsoft/scalar) project website
* [Get up to speed with partial clone and shallow clone](https://github.blog/2020-12-21-get-up-to-speed-with-partial-clone-and-shallow-clone/) on the GitHub blog
* [repo](https://android.googlesource.com/tools/repo) multi-repository tool for Git
