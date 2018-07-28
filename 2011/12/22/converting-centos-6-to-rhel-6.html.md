---
author: Jon Jensen
gh_issue_number: 532
tags: hosting, open-source, redhat, sysadmin, tips
title: Converting CentOS 6 to RHEL 6
---



A few years ago I needed to convert a [Red Hat Enterprise Linux](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) (RHEL) 5 development system to [CentOS](https://www.centos.org/) 5, as our customer did not actively use the system any more and no longer wanted to renew the Red Hat Network entitlement for it. Making the conversion was surprisingly straightforward.

This week I needed to make a conversion in the opposite direction: from CentOS 6 to RHEL 6. I didn’t find any instructions on doing so, but found a [RHEL 6 to CentOS 6 conversion guide](https://ivo.livejournal.com/75008.html) with roughly these steps:

```bash
yum clean all
mkdir centos
cd centos
wget http://mirror.centos.org/centos/6.0/os/x86_64/RPM-GPG-KEY-CentOS-6
wget http://mirror.centos.org/centos/6.0/os/x86_64/Packages/centos-release-6-0.el6.centos.5.x86_64.rpm
wget http://mirror.centos.org/centos/6.0/os/x86_64/Packages/yum-3.2.27-14.el6.centos.noarch.rpm
wget http://mirror.centos.org/centos/6.0/os/x86_64/Packages/yum-utils-1.1.26-11.el6.noarch.rpm
wget http://mirror.centos.org/centos/6.0/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.26-11.el6.noarch.rpm
rpm --import RPM-GPG-KEY-CentOS-6
rpm -e --nodeps redhat-release-server
rpm -e yum-rhn-plugin rhn-check rhnsd rhn-setup rhn-setup-gnome
rpm -Uhv --force *.rpm
yum upgrade
```

I then put together a plan to do more or less the opposite of that. The high-level overview of the steps is:

1. Completely upgrade the current CentOS and reboot to run the latest kernel, if necessary, to make sure you’re starting with a solid system.
1. Install a handful of packages that will be needed by various RHN tools.
1. Log into the Red Hat Network web interface and search for and download onto the server the most recent version of these packages for RHEL 6 x86_64:

        <ul>
          <li>redhat-release-server-6Server</li>
          <li>rhn-check</li>
          <li>rhn-client-tools</li>
          <li>rhnlib</li>
          <li>rhnsd</li>
          <li>rhn-setup</li>
          <li>yum</li>
          <li>yum-metadata-parser</li>
          <li>yum-rhn-plugin</li>
          <li>yum-utils</li>
        </ul>

1. Install the Red Hat GnuPG signing key.
1. Forcibly remove the package that identifies this system as CentOS.
1. Forcibly upgrade to the downloaded RHEL and RHN packages.
1. Register the system with Red Hat Network.
1. Update any packages that now need it using the new Yum repository.

The exact steps I used today to convert from CentOS 6.1 to RHEL 6.2 (with URL session tokens munged):

```bash
yum upgrade
shutdown -r now
yum install dbus-python libxml2-python m2crypto pyOpenSSL python-dmidecode python-ethtool python-gudev usermode
mkdir rhel
cd rhel
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/redhat-release-server/6Server-6.2.0.3.el6/x86_64/redhat-release-server-6Server-6.2.0.3.el6.x86_64.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/rhn-check/1.0.0-73.el6/noarch/rhn-check-1.0.0-73.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/rhn-client-tools/1.0.0-73.el6/noarch/rhn-client-tools-1.0.0-73.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/rhnlib/2.5.22-12.el6/noarch/rhnlib-2.5.22-12.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/rhnsd/4.9.3-2.el6/x86_64/rhnsd-4.9.3-2.el6.x86_64.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/rhn-setup/1.0.0-73.el6/noarch/rhn-setup-1.0.0-73.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/yum/3.2.29-22.el6/noarch/yum-3.2.29-22.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/yum-metadata-parser/1.1.2-16.el6/x86_64/yum-metadata-parser-1.1.2-16.el6.x86_64.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/yum-rhn-plugin/0.9.1-36.el6/noarch/yum-rhn-plugin-0.9.1-36.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget 'https://content-web.rhn.redhat.com/rhn/public/NULL/yum-utils/1.1.30-10.el6/noarch/yum-utils-1.1.30-10.el6.noarch.rpm?__gda__=XXX_YYY&ext=.rpm'
wget https://www.redhat.com/security/fd431d51.txt
rpm --import fd431d51.txt
rpm -e --nodeps centos-release
rpm -e centos-release-cr
rpm -Uhv --force *.rpm
rpm -e yum-plugin-fastestmirror
yum clean all
rhn_register
yum upgrade
```

I’m expecting to use this process a few more times in the near future. It is very useful when working with a hosting provider that does not directly support RHEL, but provides CentOS, so we can get the new servers set up without needing to request a custom operating system installation that may add a day or two to the setup time.

Given the popularity of both RHEL and CentOS, it would be neat for Red Hat to provide a tool that would easily switch, at least “upgrading” from CentOS to RHEL to bring more customers into their fold, if not the other direction!


