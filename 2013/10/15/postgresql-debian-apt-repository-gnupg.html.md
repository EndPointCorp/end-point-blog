---
author: Jon Jensen
gh_issue_number: 863
tags: debian, postgres, sysadmin
title: PostgreSQL Debian apt repository GnuPG key update
---

The excellent PGDG (PostgreSQL Global Development Group) apt repositories provide current point releases of supported PostgreSQL versions for Debian and Ubuntu LTS Linux. If you'd like to use a newer version of PostgreSQL than ships with your Linux distribution, or need to use an older Postgres release, you should take a look at [http://wiki.postgresql.org/wiki/Apt](http://wiki.postgresql.org/wiki/Apt).

A minor housekeeping matter arose just a few days ago: The GnuPG key used to sign the PostgreSQL packages expired on October 13. During a run of apt-get update && apt-get upgrade that leads to errors such as those seen here:

```
Get:1 http://security.debian.org wheezy/updates Release.gpg [836 B]
Get:2 http://security.debian.org wheezy/updates Release [102 kB]
Get:3 http://apt.postgresql.org wheezy-pgdg Release.gpg [836 B]
Get:4 http://ftp.de.debian.org wheezy Release.gpg [1,672 B]
Get:5 http://apt.postgresql.org wheezy-pgdg Release [29.2 kB]
Get:6 http://ftp.de.debian.org wheezy-updates Release.gpg [836 B]
Get:7 http://ftp.de.debian.org wheezy Release [168 kB]
Err http://apt.postgresql.org wheezy-pgdg Release

Get:8 http://security.debian.org wheezy/updates/main Sources [61.2 kB]
Get:9 http://security.debian.org wheezy/updates/main amd64 Packages [113 kB]
Get:10 http://security.debian.org wheezy/updates/main Translation-en [66.5 kB]
Get:11 http://ftp.de.debian.org wheezy-updates Release [124 kB]
Get:12 http://ftp.de.debian.org wheezy/main Sources [5,959 kB]
Get:13 http://ftp.de.debian.org wheezy/main amd64 Packages [5,848 kB]
Get:14 http://ftp.de.debian.org wheezy/main Translation-en [3,851 kB]
Get:15 http://ftp.de.debian.org wheezy-updates/main Sources [1,995 B]
Hit http://ftp.de.debian.org wheezy-updates/main amd64 Packages/DiffIndex
Hit http://ftp.de.debian.org wheezy-updates/main Translation-en/DiffIndex
Fetched 16.3 MB in 5s (3,094 kB/s)
Reading package lists... Done
W: A error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error:
http://apt.postgresql.org wheezy-pgdg Release: The following signatures were invalid: KEYEXPIRED 1381654177

W: Failed to fetch http://apt.postgresql.org/pub/repos/apt/dists/wheezy-pgdg/Release

W: Some index files failed to download. They have been ignored, or old ones used instead.
```

And, fair enough, the [PostgreSQL apt wiki page](http://wiki.postgresql.org/wiki/Apt) mentions this in its news section:

> 2013-10-10: New pgdg-keyring version extending the key expiration date. The old expiration date is 2013-10-13.

Updating the key to quell the error may not be quite as simple as expected, though. If you follow the instructions on the page, you would do this:

```
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
```

Indeed that imports the new key. However, you may still see errors from apt. Why? It's possible to have apt trusted keys installed in more than one place:

```
# apt-key list
/etc/apt/trusted.gpg
--------------------
pub   4096R/ACCC4CF8 2011-10-13 [expires: 2016-02-24]
uid                  PostgreSQL Debian Repository

/etc/apt/trusted.gpg.d//apt.postgresql.org.gpg
----------------------------------------------
pub   4096R/ACCC4CF8 2011-10-13 [expired: 2013-10-13]
uid                  PostgreSQL Debian Repository
```

A script is referenced from the apt setup page but it doesn't do the exact same thing as the instructions show. Instead, it installs the GPG key in /etc/apt/sources.list.d/pgdg.list, and unless we update or remove that file, apt will continue to see the expired key and complain about it.

In our example above, we have already imported the new key into the main /etc/apt/trusted.gpg keystore, so let's just remove the original key that was in its own file in /etc/apt/trusted.gpg.d/ like this:

```
rm -f /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
```

Afterward, apt happily proceeds with its work.
