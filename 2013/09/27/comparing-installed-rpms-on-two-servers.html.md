---
author: Jon Jensen
gh_issue_number: 859
tags: hosting, redhat, sysadmin
title: Comparing installed RPMs on two servers
---

Sometimes I’m called on to deal with a problem that shows up only on one of two or more servers that are supposed to be configured identically, or nearly identically. One of the first things I do is run ```rpm -qa | sort``` on each machine and diff the output to see which RPM packages may be missing on one or the other server. I’ve never bothered to package this functionality up into a script because it’s so simple.

To exclude minor version differences, you need to specify a custom ```rpm --queryformat``` that leaves the version number off.

To understand what you’re seeing when it appears that some package is different but seems the same, you’re often looking at multiple architectures of packages (e.g. i386 and x86_64) which RPM doesn’t show in its default query format.

Finally, to turn the diff output into a list of RPMs to install via yum, I usually do some combination of grep and sed to pick out the RPMs I need.

After all that the process isn’t entirely simple anymore, and I recently decided it was easier to script it than explain it all to someone else. I first looked around to see what scripts others have come up with, since this is certainly not a new need. I found the [blog post “Compare the RPM Packages Installed on Two Different Servers”](https://major.io/2009/03/10/compare-the-rpm-packages-installed-on-two-different-servers/) which gives a very simple example of the manual labor version I’ve long done.

In that blog post’s comments, people link to various scripts others have done. I checked them out and found that they are all *way* overcomplicated for my needs, and the simple approach I want just needed to be scripted after all. So here is my script:

```bash
#!/bin/sh

test -n "$TMPDIR" || TMPDIR=/tmp
tmpfilebase="$TMPDIR/rpmdb-compare.$$"

if test $# -ne 2
then
    echo "Usage: $0 [user@]server1 [user@]server2" >&2
    echo "Special name localhost means this server, without ssh" >&2
    exit 1
fi

for i in "$@"
do
    tmpfile="$tmpfilebase.$i"
    if test $i = localhost
    then
        rpm -qa --qf '%{NAME}.%{ARCH}\n' | sort > $tmpfile
    else
        ssh $i "rpm -qa --qf '%{NAME}.%{ARCH}\n'" | sort > $tmpfile
    fi
done

echo "RPMs in $1 only:"
comm -23 "$tmpfilebase.$1" "$tmpfilebase.$2"

echo
echo "RPMs in $2 only:"
comm -13 "$tmpfilebase.$1" "$tmpfilebase.$2"

rm -f "$tmpfilebase.$1" "$tmpfilebase.$2"
```

I noticed one of those commenters mentioned using comm instead of diff/grep/sed, and so I used that too. Now the script is easier for me too, and helps avoid copying and leaving temporary files sitting around.

To run it, just do:

```bash
./rpmdb-compare host1 host2 > mylist
```

With the output redirected to file mylist, you can edit it to result in a list of RPMs that need to be installed on one server, then do this on that server:

```bash
< mylist yum -y install
```

It’s a good idea to test it first without the -y option, which will cause yum to abort the installation and gives you a chance to see if any unexpected dependencies will be dragged in.

Also, don’t blindly install every package you don’t know the purpose of. Watch out for RPMs that may not belong everywhere due to hardware differences such as Ethernet firmware, RAID controller, IPMI, etc.
