---
author: Bryan Berry
title: Cross Release APT Managment aka How to Watch Netflix on Debian 7 Wheezy
github_issue_number: 1100
tags:
- debian
- html
- linux
date: 2015-03-11
---



Native Netflix video streaming has come to GnuLinux! ...if you have the correct library versions.

I am currently running GNU-Linux Debian 7 Wheezy with OpenBox.  I really enjoy this lightweight, speedy and easily customized window manager (OpenBox uses simple XML configuration files). So I was also pretty excited when Netflix added HTML5 streaming support and read that folks were proclaiming success in Google Chrome browsers without necessitating any agent masking workarounds.

However, I found I was still getting errors when attempting to stream video in Chrome. The forums I was reading were reporting that when using the Chrome 36+ browser, Netflix would allow Linux streaming. Most all of these forums were based in a Ubuntu 14.04+ environment. Nevertheless, I found a hint as to how to proceed in Debian after reading [this](http://www.pcworld.com/article/2824623/ubuntu-linux-gets-netflix-without-weird-workarounds.html) article regarding libnss:

> “Netflix streams its video in HTML5, but uses a technology called Encrypted Media Extensions to prevent piracy. These extensions in turn require a set of libraries called Network Security Services that the browser can access.”
> 
> 

Debian Wheezy’s repo list maxed out at libnss3==2:3.14 and I would need libnss3==2:3.16+ in order to pass the DRM tests and securely stream with Netflix’s HTML5 option enabled. In order to allow this libnss upgrade, I would first need to provide APT with instructions to pull from the Debian “jessie” development branch.

This is accomplished by setting repo priorities. I created a “jessie” specific APT sources list and added the Debian repo url’s for jessie:

```plain
$ cat /etc/apt/sources.list.d/jessie.list
## DEBIAN JESSIE
deb ftp://ftp.debian.org/debian/ jessie main
deb-src ftp://ftp.debian.org/debian/ jessie main
```

And set pin priorities for libnss3 to fetch jessie libraries over wheezy while defining a lower priority of all other jessie packages:

```plain
$ cat /etc/apt/preferences
Package: *
Pin: release a=waldorf
Pin-Priority: 1001

Package: *
Pin: release a=wheezy
Pin-Priority: 500

Package: *
Pin: release a=jessie
Pin-Priority: 110

Package: libnss3
Pin: release n=jessie
Pin-Priority: 510
```

Now, update apt and confirm higher libnss3 installation candidates:

```plain
$ sudo apt-get update && sudo apt-cache policy libnss3
libnss3:
  Installed: 2:3.14.5-1+deb7u3
  Candidate: 2:3.17.2-1.1
  Package pin: 2:3.17.2-1.1
  Version table:
    2:3.17.2-1.1 510
        500 ftp://ftp.debian.org/debian/ jessie/main amd64 Packages
*** 2:3.14.5-1+deb7u3 510
        500 http://http.debian.net/debian/ wheezy/main amd64 Packages
        500 http://security.debian.org/ wheezy/updates/main amd64 Packages
        100 /var/lib/dpkg/status

```

Install new libnss3 candidate:

```plain
$ sudo apt-get install libnss3=2:3.17.2-1.1
```

Restart any Chrome instances (and upgrade to 36+ if you haven’t yet) and enjoy Netflix streaming on Debian Linux!


