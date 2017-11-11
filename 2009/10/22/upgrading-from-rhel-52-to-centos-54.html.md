---
author: Jon Jensen
gh_issue_number: 210
tags: hosting
title: Upgrading from RHEL 5.2 to CentOS 5.4
---



I have a testing server that was running RHEL 5.2 (x86_64) but its RHN entitlement ran out and I wanted to upgrade it to CentOS 5.4. I found a few tips online about how to do that, but they were a little dated so here are updated instructions showing the steps I took:

```bash
yum clean all
mkdir ~/centos
cd ~/centos
wget http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-5
wget http://mirror.centos.org/centos/5/os/x86_64/CentOS/centos-release-5-4.el5.centos.1.x86_64.rpm
wget http://mirror.centos.org/centos/5/os/x86_64/CentOS/centos-release-notes-5.4-4.x86_64.rpm
wget http://mirror.centos.org/centos/5/os/x86_64/CentOS/yum-3.2.22-20.el5.centos.noarch.rpm
wget http://mirror.centos.org/centos/5/os/x86_64/CentOS/yum-updatesd-0.9-2.el5.noarch.rpm
wget http://mirror.centos.org/centos/5/os/x86_64/CentOS/yum-fastestmirror-1.1.16-13.el5.centos.noarch.rpm
rpm --import RPM-GPG-KEY-CentOS-5 
rpm -e --nodeps redhat-release
rpm -e yum-rhn-plugin yum-updatesd
rpm -Uvh *.rpm
yum -y upgrade
# edit /etc/grub.conf to point to correct new kernel (with Xen, in my case)
shutdown -r now
```

It has worked well so far.


