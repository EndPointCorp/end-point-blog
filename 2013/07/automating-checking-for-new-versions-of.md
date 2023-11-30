---
author: Greg Sabino Mullane
title: Automating checking for new versions of PostgreSQL
github_issue_number: 828
tags:
- monitoring
- nagios
- postgres
- sysadmin
date: 2013-07-03
---

<div class="separator" style="clear: both; text-align: center; float:right"><a href="/blog/2013/07/automating-checking-for-new-versions-of/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/07/automating-checking-for-new-versions-of/image-0.jpeg"/></a><br/><small>Hubble image by <a href="https://www.flickr.com/photos/77954350@N07/">castielstar</a></div>

It is important to run the latest revision of the major branch of Postgres you are using. While [the pgsql-announce mailing list](https://www.postgresql.org/list/pgsql-announce/) is often touted as a canonical way to become aware of new releases, a better method is to use [the check_postgres program](https://bucardo.org/check_postgres/), which will let you know if the version you are running needs to be upgraded or not. An example usage:

```bash
$ check_postgres.pl --action=new_version_pg --dbhost=iroh
POSTGRES_NEW_VERSION_PG CRITICAL:  Please upgrade to version 9.2.4 of Postgres. You are running 9.2.2
```

Postgres version numbers come in three sections. The first two indicate the “major version” 
of Postgres that you are running. The third number indicates the revision. You always want 
to be using the highest revision available for your version. In the example above, Postgres 
version 9.2 is being used, and it should be upgraded from revision 2 to revision 4. A change 
in the revision number is known as a minor release; these are only done for important reasons, 
such as security or important bug fixes. Read 
[the versioning policy page](https://www.postgresql.org/support/versioning/) for more information.

When a new version of PostgreSQL is made, there are two general ways of communicating this 
fact: the pgsql-announce mailing list, and 
[the versions.rss file](https://postgresql.org/versions.rss) on the postgresql.org 
web site. While the mailing list is 
[low volume](https://www.postgresql.org/list/pgsql-announce/2013-06/), it is not ideal as it contains posts about 
conferences, and about other Postgres-related software. A better solution is to track 
the versions.rss file. You could simply subscribe to it, but this will only tell you when the 
file has been changed. The check_postgres program parses this file and compares the latest 
revision to the version of Postgres that you are using.

To use it, simply call check_postgres and pass **new_version_pg**
as the **action** argument, as well as telling check_postgres which PostgreSQL 
instance you are checking. For example, to check that the Postgres running on 
your internal host “zuko” is up to date, just run:

```bash
check_postgres.pl --action=new_version_pg --dbhost=zuko
```

Here is what the default output looks like, for both a matching and 
a non-matching version:

```bash
$ check_postgres.pl --action=new_version_pg --dbhost=appa
POSTGRES_NEW_VERSION_PG CRITICAL:  Please upgrade to version 9.2.4 of Postgres. You are running 9.2.2

$ check_postgres.pl --action=new_version_pg --dbhost=toph
POSTGRES_NEW_VERSION_PG OK:  Version 9.2.4 is the latest for Postgres
```

Those examples are very Nagios specific, of course, as evidenced by those uppercase strings at the beginning 
of the output. If you are using Nagios, it’s a good idea to run this, perhaps once a day or more often. If 
you are not using Nagios, you can make the output a little cleaner with the **--simple** argument:

```bash
$ check_postgres.pl --action=new_version_pg --dbhost=azula
Please upgrade to version 9.2.4 of Postgres. You are running 9.2.2

$ check_postgres.pl --action=new_version_pg --dbhost=sokka
Version 9.2.4 is the latest for Postgres
```

One quick and simple trick is to make this into a cron job and add the **--quiet** argument, which 
prevents all output if the check was “OK”. In this way, cron will only send outout (e.g. mail 
someone) when a new revision has been released. A cron example:

```plain
## Twice a day, check that we are running the latest Postgres:
0 7,18 * * * check_postgres.pl --action=new_version_pg --dbhost=cabbage --quiet
```

Once this alarm goes off, you should strive to update your clusters as soon as possible. 
If you are using a packaging system, then it may be as simple as relying on it to 
do the right thing, e.g. “yum update postgresql”. If you are installing from source, 
you will need the new tarball and can simply “make install” onto the existing 
Postgres, and then restart it. Always check the release notes for the new revision—​once in a blue 
moon the update requires some other action, such as a reindex of certain types of indexes.

The check_postgres program can verify versions of some 
[other programs](https://bucardo.org/check_postgres/check_postgres.pl.html#new_version_bc) as well, including 
[Bucardo](https://bucardo.org/Bucardo/), 
[tail_n_mail](https://bucardo.org/tail_n_mail/), and check_postgres itself.
