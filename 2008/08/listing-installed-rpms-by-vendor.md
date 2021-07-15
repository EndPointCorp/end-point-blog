---
author: Jon Jensen
title: Listing installed RPMs by vendor
github_issue_number: 41
tags:
- redhat
date: 2008-08-09
---

The other day I wanted to see a list of all RPMs that came from a source other than Red Hat, which were installed on a [Red Hat Enterprise Linux](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) (RHEL) 5 server. This is straightforward with the rpm --queryformat (short form --qf) option:

```
rpm -qa --qf '%{NAME} %{VENDOR}\n' | grep -v 'Red Hat, Inc\.' | sort
```

That instructs rpm to output each package’s name and vendor, then we exclude those from “Red Hat, Inc.” (which is the exact string Red Hat conveniently uses in the “vendor” field of all RPMs they pacakge).

By default, rpm -qa uses the format '%{NAME}-%{VERSION}-%{RELEASE}', and it’s nice to see version and release, and on 64-bit systems, it’s also nice to see the architecture since both 32- and 64-bit packages are often installed. Here’s how I did that:

```
rpm -qa --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH} %{VENDOR}\n' | grep -v 'Red Hat, Inc\.' | sort
```

With that I’ll see output such as:

```
fping-2.4-1.b2.2.el5.rf.x86_64 Dag Apt Repository, http://dag.wieers.com/apt/
git-1.5.6.5-1.x86_64 End Point Corporation
iftop-0.17-1.el5.x86_64 (none)
```

There we see the fping package from the excellent [DAG RPM repository](http://dag.wiee.rs/rpm/), along with a few others.

To see a list of all symbols that can be used:

```
rpm --querytags
```
