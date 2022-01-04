---
author: "Jon Jensen"
date: 2021-12-09
title: "Installing Git 2 on CentOS 7"
github_issue_number: 1806
tags:
- git
- sysadmin
- linux
---

![Photo of a room with colorful translucent glass windows; wooden beams, walls, and ceiling; and heating vents](/blog/2021/12/installing-git-2-on-centos-7/20210718-174926-sm.jpg)

<!-- photo by Jon Jensen -->

### Git-ing a bit stale?

RHEL/CentOS 7 is starting to feel a somewhat dated, but it still has over 2½ years before it reaches the end of its support lifetime that Red Hat has set for the end of June 2024.

One component that is far enough outdated to cause serious annoyance is Git.

Git is by far the most-used version control system in the world. It popularized the distributed model of tracking changes to source code files and greatly simplified collaboration by multiple developers. It is open source and free software and is used by most public and many internal software projects, and also by solo developers. IDEs such as VS Code and IntelliJ idea integrate with it. SaaS code hosting providers GitHub, GitLab, Bitbucket, and others are built around it. We have been using and [advocating Git since 2007](/blog/2007/12/better-git-it-in-your-soul/) — see [our blog posts about Git](/blog/tags/git/) for a variety of helpful articles.

CentOS/RHEL 7 includes Git version 1.8.3, which was released in May 2013. There have been 2 major, 36 minor, and **216** patch releases of Git in the 8½ years between then and the current version 2.34.1!

The makers of CentOS/RHEL have good reasons to stick with versions they shipped with for the lifetime of the operating system: compatibility, stability, predictability. They only want to release updates that are entirely compatible, mostly for bugfixes and security updates.

Using a newer version will likely have some differences, but for software primarily used interactively by humans who can adapt to change, this is often worth the tradeoff of more features vs. occasional unexpected change.

### We help you freshen up

To relieve the pain of aging software, we here at End Point Dev package up newer Git versions for RHEL 7 as needed for ourselves and our clients. You can use it too! Our current packaged version as of today is the latest Git, version 2.34.1, which was released on 24 November 2021.

Why not just build the latest version from source? That works well on a single developer workstation if you don't mind staying abreast of each new Git release on your own, and doing a bit of work to build them.

We recommend using packages specific to your OS because it is faster, easier, and fits well with automation tools such as Ansible, Salt, Chef, and Puppet. And when you configure a Yum repository that includes ongoing package updates, the updates are automatically applied to all your systems as part of your routine OS maintenance.

Here are instructions showing how you can install the latest Git package we built, on CentOS/RHEL 7 systems.

### Check your version of git

First, see what version you have installed:

```bash
$ git --version
git version 1.8.3.1
```

Now see where it is installed:

```bash
$ which git
/usr/bin/git
```

If you have `git` installed somewhere else, such as `/usr/local/bin/git`, it was probably built from source and installed there, and you should consider deleting that other installation before you install this new packaged one.

To make sure it was installed from an RPM using yum:

```plain
$ rpm -qi git
Name        : git
Version     : 1.8.3.1
Release     : 23.el7_8
Source RPM  : git-1.8.3.1-23.el7_8.src.rpm
Build Date  : Thu 28 May 2020 08:37:56 PM UTC
Build Host  : x86-02.bsys.centos.org
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
```

(I omitted a few uninteresting lines from that output so we can focus on the essentials.)

If instead of the above you see this from `rpm` and/or don't have `git` installed at all:

```bash
$ rpm -qi git
package git is not installed
$ which git
/usr/bin/which: no git in (/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin)
```

That's fine. In that case you will just be installing Git on this system for the first time.

### Add the End Point Yum repository

Now install the End Point package repository Yum repo package:

```bash
$ sudo yum install https://packages.endpointdev.com/rhel/7/os/x86_64/endpoint-repo.x86_64.rpm
```

That adds two important files to your system:

#### Yum repo config file

The first is `/etc/yum.repos.d/endpoint.repo` which is configuration for `yum`, an extension to its main `/etc/yum.conf` configuration file. Here is where we point your Yum setup to our [packages.endpointdev.com](https://packages.endpointdev.com/) repository to look for packages in the future.

#### GnuPG key

The second is `/etc/pki/rpm-gpg/RPM-GPG-KEY-endpoint-7` which is the PGP/GnuPG public key matching the secret key we use to sign packages in our repository, so your `yum` can verify the packages have not been corrupted, either accidentally during transmission, or intentionally by Bad Folks.

### Install or upgrade git

Now installing or upgrading to the new version of Git is as simple as:

```bash
$ sudo yum install git
```

You can use `yum upgrade git` if you already have it installed, but `yum install git` works in either case.

You should see output similar to this:

```plain
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: centos.mirror.constant.com
 * epel: d2lzkl7pfhq30w.cloudfront.net
 * extras: bay.uchicago.edu
 * updates: ftp.usf.edu
Resolving Dependencies
--> Running transaction check
---> Package git.x86_64 0:1.8.3.1-23.el7_8 will be updated
--> Processing Dependency: git = 1.8.3.1-23.el7_8 for package: perl-Git-1.8.3.1-23.el7_8.noarch
---> Package git.x86_64 0:2.34.1-1.ep7 will be an update
--> Processing Dependency: git-core = 2.34.1-1.ep7 for package: git-2.34.1-1.ep7.x86_64
--> Processing Dependency: git-core-doc = 2.34.1-1.ep7 for package: git-2.34.1-1.ep7.x86_64
--> Processing Dependency: emacs-filesystem >= 24.3 for package: git-2.34.1-1.ep7.x86_64
--> Running transaction check
---> Package emacs-filesystem.noarch 1:24.3-23.el7 will be installed
---> Package git-core.x86_64 0:2.34.1-1.ep7 will be installed
--> Processing Dependency: libpcre2-8.so.0()(64bit) for package: git-core-2.34.1-1.ep7.x86_64
---> Package git-core-doc.noarch 0:2.34.1-1.ep7 will be installed
---> Package perl-Git.noarch 0:1.8.3.1-23.el7_8 will be updated
---> Package perl-Git.noarch 0:2.34.1-1.ep7 will be an update
--> Running transaction check
---> Package pcre2.x86_64 0:10.23-2.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

===============================================================
 Package            Arch     Version         Repository   Size
===============================================================
Updating:
 git                x86_64   2.34.1-1.ep7    endpoint     69 k
Installing for dependencies:
 emacs-filesystem   noarch   1:24.3-23.el7   base         58 k
 git-core           x86_64   2.34.1-1.ep7    endpoint    5.7 M
 git-core-doc       noarch   2.34.1-1.ep7    endpoint    2.7 M
 pcre2              x86_64   10.23-2.el7     base        201 k
Updating for dependencies:
 perl-Git           noarch   2.34.1-1.ep7    endpoint     43 k

Transaction Summary
===============================================================
Install             ( 4 Dependent packages)
Upgrade  1 Package  (+1 Dependent package)

Total download size: 8.7 M
Is this ok [y/d/N]: y
```

If you don't see the new `git` version available, you may need to clear your Yum caches with:

```bash
$ sudo yum clean all
```

In the install/upgrade output above from `yum`, notice the question: "Is this ok"? As long as what you see is similar to the above, everything should be fine. But investigate further before proceeding if it proposed any unexpected package upgrades or removals.

If you agree to continue, you'll see something like:

```plain
Downloading packages:
Delta RPMs disabled because /usr/bin/applydeltarpm not installed.
(1/6): emacs-filesystem-24.3-23.el7.noarch.rpm  |  58 kB  00:00:00
(2/6): git-2.34.1-1.ep7.x86_64.rpm              |  69 kB  00:00:00
(3/6): pcre2-10.23-2.el7.x86_64.rpm             | 201 kB  00:00:00
(4/6): git-core-doc-2.34.1-1.ep7.noarch.rpm     | 2.7 MB  00:00:00
(5/6): perl-Git-2.34.1-1.ep7.noarch.rpm         |  43 kB  00:00:00
(6/6): git-core-2.34.1-1.ep7.x86_64.rpm         | 5.7 MB  00:00:01
-------------------------------------------------------------------
Total                                  6.9 MB/s | 8.7 MB  00:00:01
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : 1:emacs-filesystem-24.3-23.el7.noarch  1/8
  Installing : pcre2-10.23-2.el7.x86_64               2/8
  Installing : git-core-2.34.1-1.ep7.x86_64           3/8
  Installing : git-core-doc-2.34.1-1.ep7.noarch       4/8
  Updating   : perl-Git-2.34.1-1.ep7.noarch           5/8
  Updating   : git-2.34.1-1.ep7.x86_64                6/8
  Cleanup    : perl-Git-1.8.3.1-23.el7_8.noarch       7/8
  Cleanup    : git-1.8.3.1-23.el7_8.x86_64            8/8
  Verifying  : pcre2-10.23-2.el7.x86_64               1/8
  Verifying  : 1:emacs-filesystem-24.3-23.el7.noarch  2/8
  Verifying  : git-core-2.34.1-1.ep7.x86_64           3/8
  Verifying  : git-2.34.1-1.ep7.x86_64                4/8
  Verifying  : git-core-doc-2.34.1-1.ep7.noarch       5/8
  Verifying  : perl-Git-2.34.1-1.ep7.noarch           6/8
  Verifying  : git-1.8.3.1-23.el7_8.x86_64            7/8
  Verifying  : perl-Git-1.8.3.1-23.el7_8.noarch       8/8

Dependency Installed:
  emacs-filesystem.noarch 1:24.3-23.el7  git-core.x86_64 0:2.34.1-1.ep7
  git-core-doc.noarch 0:2.34.1-1.ep7     pcre2.x86_64 0:10.23-2.el7

Updated:
  git.x86_64 0:2.34.1-1.ep7

Dependency Updated:
  perl-Git.noarch 0:2.34.1-1.ep7

Complete!
```

Now check again which version of `git` is installed, and what the RPM database contains:

```plain
$ git --version
git version 2.34.1
$ rpm -qi git
Name        : git
Version     : 2.34.1
Release     : 1.ep7
Architecture: x86_64
Source RPM  : git-2.34.1-1.ep7.src.rpm
Build Date  : Thu 09 Dec 2021 01:15:52 AM UTC
Build Host  : rhel7-build64.epinfra.net
Packager    : End Point Hosting Team <hosting@endpointdev.com>
Vendor      : End Point Dev - https://packages.endpointdev.com/
```

(Again I removed a few uninteresting lines.)

We can see that this new version came from the End Point repository and is very fresh as of the time of this writing.

### Bonus: Newer tmux!

You may also be interested in our much newer tmux 3.2a vs. the tmux 1.8 that comes with CentOS 7.

If you want it, now that you have the End Point Yum repository configured, you can simply do:

```bash
$ sudo yum install tmux
```

### Reference

* [End Point package repositories](https://packages.endpointdev.com/)
* [pkgs.org](https://pkgs.org/) makes it easy to find RPM packages across the various Linux distros, architectures, and repositories. We often use it to find source RPMs from Fedora Rawhide and other distros that we can rebuild for RHEL.
* [CentOS Linux](https://centos.org/centos-linux/)
* [Git website](https://git-scm.com/)
* [GitHub blog Highlights from Git 2.34](https://github.blog/2021-11-15-highlights-from-git-2-34/) is a good exploration of important changes in the most recent version of Git. GitHub's articles about each Git release are worth reading.
* [tmux on Wikipedia](https://en.wikipedia.org/wiki/Tmux)
