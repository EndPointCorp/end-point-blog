---
author: Jon Jensen
gh_issue_number: 30
tags: perl, redhat
title: Building Perl on 64-bit RHEL/Fedora/CentOS
---

When building Perl from source on 64-bit Red Hat Enterprise Linux, Fedora, CentOS, or derivatives, Perl’s Configure command needs to be told about the “multilib” setup Red Hat uses.

The multilib arrangement allows both 32-bit and 64-bit libraries to exist on the same system, and leaves the “non-native” 32-bit libraries in /lib and /usr/lib while the “native” 64-bit libraries go in /lib64 and /usr/lib64. That allows the same 32-bit RPMs to be used on either i386 or x86_64 systems. The downside of this is that 64-bit applications have to be told where to look for, and put, libraries, or they usually won’t work.

For Perl, to compile from a source tarball with the defaults:

```
./Configure -des -Dlibpth="/usr/local/lib64 /lib64 /usr/lib64"
```

Then build as normal:

```
make && make test && sudo make install
```

I hope this information will come in handy for someone. I believe I learned it from Red Hat’s source RPM for Perl.
