---
author: Jon Jensen
title: Converting RHEL 5.9 and 6.4 to CentOS
github_issue_number: 775
tags:
- hosting
- linux
- redhat
date: 2013-04-04
---

CentOS is, by design, an almost identical rebuild of Red Hat Enterprise Linux (RHEL). Any given version of each OS should behave the same as the other and packages and yum repositories built for one should work for the other unchanged. Any exception I would call a bug.

Because Red Hat is the source or origin of packages that ultimately end up in CentOS, there is an inherent delay between when Red Hat releases new packages and when they appear in CentOS. CentOS is financed by optional donations of work, hosting, and money, while Red Hat Enterprise Linux is financed by requiring customers to purchase entitlements to use the software and get various levels of support from Red Hat.

Thanks to this close similarity and the tradeoff between rapidity of updates vs. cost and entitlement tracking, we find reasons to use both RHEL and CentOS, depending on the situation.

Sometimes we want to convert RHEL to CentOS or vice versa, on a running machine, without the expense and destabilizing effect of having to reinstall the operating system. In the past I’ve written on this blog about [converting from CentOS 6 to RHEL 6](/blog/2011/12/converting-centos-6-to-rhel-6), and earlier about [converting from RHEL 5 to CentOS 5](/blog/2009/10/upgrading-from-rhel-52-to-centos-54).

I recently needed to migrate several servers from RHEL to CentOS, and found an update of the procedure was in order because some URLs and package versions had changed. Here are current instructions on how to migrate from RHEL 5.9 to CentOS 5.9, and RHEL 6.4 to CentOS 6.4.

These commands should of course be run as root, and observed carefully by a human eye to look for any errors or warnings and adapt accordingly.

### RHEL 5.9 to CentOS 5.9 conversion, 64-bit (x86_64)

```bash
cd
mkdir centos
cd centos
wget http://mirror.centos.org/centos/5.9/os/x86_64/RPM-GPG-KEY-CentOS-5
wget http://mirror.centos.org/centos/5.9/os/x86_64/CentOS/centos-release-5-9.el5.centos.1.x86_64.rpm
wget http://mirror.centos.org/centos/5.9/os/x86_64/CentOS/centos-release-notes-5.9-0.x86_64.rpm
wget http://mirror.centos.org/centos/5.9/os/x86_64/CentOS/yum-3.2.22-40.el5.centos.noarch.rpm
wget http://mirror.centos.org/centos/5.9/os/x86_64/CentOS/yum-updatesd-0.9-5.el5.noarch.rpm
wget http://mirror.centos.org/centos/5.9/os/x86_64/CentOS/yum-fastestmirror-1.1.16-21.el5.centos.noarch.rpm
wget http://mirror.centos.org/centos/5.9/os/x86_64/CentOS/gamin-python-0.1.7-10.el5.x86_64.rpm
yum erase yum-rhn-plugin rhn-client-tools rhn-virtualization-common rhn-setup rhn-check rhnsd yum-updatesd
yum clean all
rpm --import RPM-GPG-KEY-CentOS-5
rpm -e --nodeps redhat-release
yum localinstall *.rpm
yum upgrade
shutdown -r now
```

### RHEL 5.9 to CentOS 5.9 conversion, 32-bit (i386)

```bash
cd
mkdir centos
cd centos
wget http://mirror.centos.org/centos/5.9/os/i386/RPM-GPG-KEY-CentOS-5
wget http://mirror.centos.org/centos/5.9/os/i386/CentOS/centos-release-5-9.el5.centos.1.i386.rpm
wget http://mirror.centos.org/centos/5.9/os/i386/CentOS/centos-release-notes-5.9-0.i386.rpm
wget http://mirror.centos.org/centos/5.9/os/i386/CentOS/yum-3.2.22-40.el5.centos.noarch.rpm
wget http://mirror.centos.org/centos/5.9/os/i386/CentOS/yum-updatesd-0.9-5.el5.noarch.rpm
wget http://mirror.centos.org/centos/5.9/os/i386/CentOS/yum-fastestmirror-1.1.16-21.el5.centos.noarch.rpm
wget http://mirror.centos.org/centos/5.9/os/i386/CentOS/gamin-python-0.1.7-10.el5.i386.rpm
yum erase yum-rhn-plugin rhn-client-tools rhn-virtualization-common rhn-setup rhn-check rhnsd yum-updatesd
yum clean all
rpm --import RPM-GPG-KEY-CentOS-5
rpm -e --nodeps redhat-release
yum localinstall *.rpm
yum upgrade
shutdown -r now
```

### RHEL 6.4 to CentOS 6.4 conversion, 64-bit (x86_64)

```bash
cd
mkdir centos
cd centos
wget http://mirror.centos.org/centos/6.4/os/x86_64/RPM-GPG-KEY-CentOS-6
wget http://mirror.centos.org/centos/6.4/os/x86_64/Packages/centos-release-6-4.el6.centos.10.x86_64.rpm
wget http://mirror.centos.org/centos/6.4/os/x86_64/Packages/yum-3.2.29-40.el6.centos.noarch.rpm
wget http://mirror.centos.org/centos/6.4/os/x86_64/Packages/yum-utils-1.1.30-14.el6.noarch.rpm
wget http://mirror.centos.org/centos/6.4/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.30-14.el6.noarch.rpm
yum erase yum-rhn-plugin rhn-client-tools rhn-virtualization-common rhn-setup rhn-check rhnsd yum-updatesd subscription-manager
yum clean all
rpm --import RPM-GPG-KEY-CentOS-6
rpm -e --nodeps redhat-release-server
yum localinstall *.rpm
yum upgrade
shutdown -r now
```

We don’t use 32-bit (i386) RHEL or CentOS 6, so you’re on your own with that, but it should be very straightforward to adapt the x86_64 instructions.

If during the yum localinstall you get an error like this that references a URL containing %24releasever:

```plain
[Errno 14] PYCURL ERROR 22 - "The requested URL returned error: 404 Not Found"
Error: Cannot retrieve repository metadata (repomd.xml) for repository
```

Then you need to temporarily disable that add-on yum repository until after the conversion is complete by editing /etc/yum.repos.d/*name*.repo to change enabled=1 to enabled=0. The problem here is caused by the repo configuration using the releasever yum variable which is undefined mid-conversion because we forcibly removed the redhat-release* package that defines it. We can’t expect the OS to know what kind it is in the middle of its identity crisis and change!

If all goes well, nothing will look any different at all, except you’ll now see:

```plain
# cat /etc/redhat-release
CentOS release 5.9 (Final)
```

or:

```plain
# cat /etc/redhat-release
CentOS release 6.4 (Final)
```
