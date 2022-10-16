---
author: "Jon Jensen"
date: 2022-10-14
title: "Upgrading PostgreSQL 14 to 15 on Fedora, RHEL, CentOS, Rocky, Alma Linux with PGDG RPM packages"
github_issue_number: 1909
tags:
- postgres
- sysadmin
- linux
---

![White-haired Labrador dog sitting in mountain field with boulders, and mountain rock wall behind](/blog/2022/10/upgrading-postgresql-14-to-15-on-fedora-centos-rocky-alma-linux/20220903-233459-sm.webp)

<!-- photo by Jon Jensen -->

### PostgreSQL 15 changes

Yesterday PostgreSQL 15 was released! It includes a number of headline features since version 14 that make it worth upgrading your databases running earlier versions of PostgreSQL:

* Improved sort performance
* In-memory statistics collection (removing the statistics collector process)
* SQL-standard `MERGE` syntax that can include `INSERT`, `UPDATE`, and `DELETE` actions in a single statement
* Logical replication publisher options to include all tables in a schema (including those added in the future), row filtering and column lists, and simplified conflict management
* JSON format log output (to files only, not syslog)
* Optional LZ4 and Zstandard compression for WAL (write-ahead log) files, especially useful for those not using btrfs or zfs filesystem built-in compression
* New regular expression functions `regexp_count`, `regexp_instr`, `regexp_like`, and `regexp_substr`
* And many other performance improvements and feature enhancements

Thanks to the PostgreSQL developers for the continuing amazing work!

### Prerequisites for upgrading

This article shows how to upgrade to PostgreSQL 15 if you:

* are running one of the Red Hat family of Linux operating systems, including Fedora, Red Hat Enterprise Linux (RHEL), Rocky Linux, AlmaLinux, Oracle Linux, or CentOS
* have PostgreSQL 14 installed
* are not using `dnf` modularity or the stock distribution `postgresql` RPMs, but rather the PostgreSQL Global Development Group (PGDG) `postgresql14` RPMs that allow simultaneous coexistence of multiple major Postgres versions

My examples are done on the Fedora 36 x86_64 OS. Things will be very similar on other Red Hat family members.

We are doing system administration work here, so let's act as system administrators and work as the `root` user rather than using `sudo` repetitively:

```plain
$ su -
Password:
[root@yourhost ~]#
```

### Stop PostgreSQL 14

Stop your existing PostgreSQL 14 database server, if it is running, and prevent it from starting automatically at boot in the future:

```plain
[root@yourhost ~]# systemctl disable --now postgresql-14
```

### Update your system

Make sure your packages are fully updated:

```plain
[root@yourhost ~]# dnf upgrade
Last metadata expiration check: 2:28:40 ago on Fri 14 Oct 2022 09:01:38 AM MDT.
Dependencies resolved.
Nothing to do.
Complete!
```

If there were updates pending, apply them. If the Linux kernel, glibc, systemd, or other core packages were updated, reboot to load the latest of all parts of your system.

### Install PostgreSQL 15

We will here use a basic set of PostgreSQL client, server, development, and extra contributed packages.

You may also want some of the other available packages for procedural languages such as PL/Perl and PL/Python, PostGIS, or other packages. See the [Yum repository index](https://download.postgresql.org/pub/repos/yum/15/fedora/fedora-36-x86_64/).

Now install PostgreSQL 15, which happily coexists alongside PostgreSQL 14 (and possibly other versions) thanks to the way the PGDG RPMs are designed and where they install files:

```plain
[root@yourhost ~]# dnf install postgresql15-server postgresql15-devel postgresql15-contrib
Last metadata expiration check: 2:29:14 ago on Fri 14 Oct 2022 09:01:38 AM MDT.
Dependencies resolved.
==========================================================================
 Package                  Architecture  Version         Repository   Size
==========================================================================
Installing:
 postgresql15-contrib     x86_64        15.0-1PGDG.f36  pgdg15      708 k
 postgresql15-devel       x86_64        15.0-1PGDG.f36  pgdg15      5.2 M
 postgresql15-server      x86_64        15.0-1PGDG.f36  pgdg15      5.9 M
Installing dependencies:
 postgresql15             x86_64        15.0-1PGDG.f36  pgdg15      1.5 M
 postgresql15-libs        x86_64        15.0-1PGDG.f36  pgdg15      290 k

Transaction Summary
==========================================================================
Install  5 Packages

Total download size: 14 M
Installed size: 54 M
Is this ok [y/N]: y
Downloading Packages:
(1/5): postgresql15-contrib-15.0-1PGDG.f36.x86_64.rpm  412 kB/s | 708 kB     00:01
(2/5): postgresql15-libs-15.0-1PGDG.f36.x86_64.rpm     171 kB/s | 290 kB     00:01
(3/5): postgresql15-15.0-1PGDG.f36.x86_64.rpm          435 kB/s | 1.5 MB     00:03
(4/5): postgresql15-devel-15.0-1PGDG.f36.x86_64.rpm    1.0 MB/s | 5.2 MB     00:05
(5/5): postgresql15-server-15.0-1PGDG.f36.x86_64.rpm   1.7 MB/s | 5.9 MB     00:03
-----------------------------------------------------------------------------------
Total                                                  2.0 MB/s |  14 MB     00:06
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                             1/1
  Installing       : postgresql15-libs-15.0-1PGDG.f36.x86_64     1/5
  Running scriptlet: postgresql15-libs-15.0-1PGDG.f36.x86_64     1/5
  Installing       : postgresql15-15.0-1PGDG.f36.x86_64          2/5
  Running scriptlet: postgresql15-15.0-1PGDG.f36.x86_64          2/5
  Running scriptlet: postgresql15-server-15.0-1PGDG.f36.x86_64   3/5
  Installing       : postgresql15-server-15.0-1PGDG.f36.x86_64   3/5
  Running scriptlet: postgresql15-server-15.0-1PGDG.f36.x86_64   3/5
  Installing       : postgresql15-contrib-15.0-1PGDG.f36.x86_64  4/5
  Installing       : postgresql15-devel-15.0-1PGDG.f36.x86_64    5/5
  Running scriptlet: postgresql15-devel-15.0-1PGDG.f36.x86_64    5/5
  Verifying        : postgresql15-15.0-1PGDG.f36.x86_64          1/5
  Verifying        : postgresql15-contrib-15.0-1PGDG.f36.x86_64  2/5
  Verifying        : postgresql15-devel-15.0-1PGDG.f36.x86_64    3/5
  Verifying        : postgresql15-libs-15.0-1PGDG.f36.x86_64     4/5
  Verifying        : postgresql15-server-15.0-1PGDG.f36.x86_64   5/5

Installed:
  postgresql15-15.0-1PGDG.f36.x86_64         postgresql15-contrib-15.0-1PGDG.f36.x86_64
  postgresql15-devel-15.0-1PGDG.f36.x86_64   postgresql15-libs-15.0-1PGDG.f36.x86_64
  postgresql15-server-15.0-1PGDG.f36.x86_64

Complete!
```

### Create the new PostgreSQL 15 database cluster

Now that we have the new PostgreSQL version installed, we can create the new database cluster.

You need to use the same Postgres `initdb` options that were used when you ran `initdb` for Postgres 14.

For example, if you used the helpful [data checksums feature](https://www.postgresql.org/docs/current/checksums.html), you need to pass the `-k` option to `initdb`, which is done indirectly via the RPM-specific `postgresql-15-setup` script like this:

```plain
[root@yourhost ~]# PGSETUP_INITDB_OPTIONS=-k /usr/pgsql-15/bin/postgresql-15-setup initdb
Initializing database ... OK
```

If you used the default `initdb` options, just omit the `PGSETUP_INITDB_OPTIONS` environment variable:

```plain
[root@yourhost ~]# /usr/pgsql-15/bin/postgresql-15-setup initdb
Initializing database ... OK
```

### Migrate your data with pg_upgrade

At this point you could start the PostgreSQL 15 server and use `psql` to connect to it, if you want to start with an empty database or otherwise load your data by the usual means such as with `psql` or `pg_restore` using output from `pg_dump`.

But if you want to convert all of your existing PostgreSQL 14 cluster's data so everything comes over as is, you can now run `pg_upgrade`.

For any important system, back up your data before doing anything else, and read through the whole [pg_upgrade manual](https://www.postgresql.org/docs/current/pgupgrade.html). It contains several important points to consider:

* Use compatible `initdb` flags that match the old cluster. (Already discussed.)

* Install extension shared object files. (Some may be contained in the `contrib` package, while others are separate, such as PostGIS.)

* Set authentication to `peer` in `pg_hba.conf` for both old and new Postgres versions. This is the default for the new cluster, but your old PostgreSQL 14 cluster may need to be adjusted so `pg_update` can access it.

We will run `pg_upgrade` as the `postgres` OS user and specify the standard PGDG RPM locations for Postgres 14 &amp; 15:

```plain
[root@yourhost ~]# su - postgres
[postgres@yourhost ~]$ /usr/pgsql-15/bin/pg_upgrade -b /usr/pgsql-14/bin -B /usr/pgsql-15/bin -d /var/lib/pgsql/14/data -D /var/lib/pgsql/15/data -j 4
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok

old cluster does not use data checksums but the new one does
Failure, exiting
```

Oops! `pg_upgrade` can't convert an old cluster that didn't have data checksums into a new one that did, so in this case we need to delete our new cluster and recreate it without the `initdb -k` option for checksums.

Exit back to your root shell and re-run a suitable `initdb` command like those shown above:

```plain
[postgres@yourhost ~]$ exit
logout
[root@yourhost ~]# rm -rf ~postgres/15/data/*
[root@yourhost ~]# /usr/pgsql-15/bin/postgresql-15-setup initdb
Initializing database ... OK
```

Now let's try running `pg_upgrade` again:

```plain
[root@yourhost ~]# su - postgres
[postgres@yourhost ~]$ /usr/pgsql-15/bin/pg_upgrade -b /usr/pgsql-14/bin -B /usr/pgsql-15/bin -d /var/lib/pgsql/14/data -D /var/lib/pgsql/15/data -j 4
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok
Checking database user is the install user                  ok
Checking database connection settings                       ok
Checking for prepared transactions                          ok
Checking for system-defined composite types in user tables  ok
Checking for reg* data types in user tables                 ok
Checking for contrib/isn with bigint-passing mismatch       ok
Creating dump of global objects                             ok
Creating dump of database schemas
                                                            ok
Checking for presence of required libraries                 ok
Checking database user is the install user                  ok
Checking for prepared transactions                          ok
Checking for new cluster tablespace directories             ok

If pg_upgrade fails after this point, you must re-initdb the
new cluster before continuing.

Performing Upgrade
------------------
Analyzing all rows in the new cluster                       ok
Freezing all rows in the new cluster                        ok
Deleting files from new pg_xact                             ok
Copying old pg_xact to new server                           ok
Setting oldest XID for new cluster                          ok
Setting next transaction ID and epoch for new cluster       ok
Deleting files from new pg_multixact/offsets                ok
Copying old pg_multixact/offsets to new server              ok
Deleting files from new pg_multixact/members                ok
Copying old pg_multixact/members to new server              ok
Setting next multixact ID and offset for new cluster        ok
Resetting WAL archives                                      ok
Setting frozenxid and minmxid counters in new cluster       ok
Restoring global objects in the new cluster                 ok
Restoring database schemas in the new cluster
                                                            ok
Copying user relation files
                                                            ok
Setting next OID for new cluster                            ok
Sync data directory to disk                                 ok
Creating script to delete old cluster                       ok
Checking for extension updates                              ok

Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade.
Once you start the new server, consider running:
    /usr/pgsql-15/bin/vacuumdb --all --analyze-in-stages


Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh
```

That's better!

### Start PostgreSQL 15

You may want to manually migrate over any configuration in `postgresql.conf` and `pg_hba.conf` from your old PostgreSQL 14 cluster to your new PostgreSQL 15 cluster, using `diff` or similar tools.

Once you're ready, exit back to your root shell, then start your new PostgreSQL 15 database and set it to start automatically at boot:

```plain
[postgres@yourhost ~]$ exit
logout
[root@yourhost ~]# systemctl enable --now postgresql-15
Created symlink /etc/systemd/system/multi-user.target.wants/postgresql-15.service → /usr/lib/systemd/system/postgresql-15.service.
```

Let's take the advice of `pg_upgrade` to analyze our freshly imported databases so the query planner has statistics it needs to plan wisely. We aren't in any hurry to get the database back online, so we won't bother analyzing in stages, and will just do it all at once:

```plain
[root@yourhost ~]# su - postgres
[postgres@yourhost ~]$ /usr/pgsql-15/bin/vacuumdb -a -Z
vacuumdb: vacuuming database "funtimes"
vacuumdb: vacuuming database "postgres"
vacuumdb: vacuuming database "template1"
```

### Try it out

Now we can try our new installation, and check that some of those neat new PostgreSQL 15 features are really available:

```plain
[postgres@yourhost ~]$ psql
psql (15.0)
Type "help" for help.

postgres=# select version();
                                                 version
----------------------------------------------------------------------------------------------------------
 PostgreSQL 15.0 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 12.2.1 20220819 (Red Hat 12.2.1-2), 64-bit
(1 row)

postgres=# select regexp_count('the quick brown fox jumped over the lazy', ' ');
 regexp_count
--------------
            7
(1 row)
postgres=# \h merge
Command:     MERGE
Description: conditionally insert, update, or delete rows of a table
Syntax:
[ WITH with_query [, ...] ]
MERGE INTO target_table_name [ [ AS ] target_alias ]
USING data_source ON join_condition
when_clause [...]

where data_source is:

{ source_table_name | ( source_query ) } [ [ AS ] source_alias ]

and when_clause is:

{ WHEN MATCHED [ AND condition ] THEN { merge_update | merge_delete | DO NOTHING } |
  WHEN NOT MATCHED [ AND condition ] THEN { merge_insert | DO NOTHING } }

and merge_insert is:

INSERT [( column_name [, ...] )]
[ OVERRIDING { SYSTEM | USER } VALUE ]
{ VALUES ( { expression | DEFAULT } [, ...] ) | DEFAULT VALUES }

and merge_update is:

UPDATE SET { column_name = { expression | DEFAULT } |
             ( column_name [, ...] ) = ( { expression | DEFAULT } [, ...] ) } [, ...]

and merge_delete is:

DELETE

URL: https://www.postgresql.org/docs/15/sql-merge.html
```


### Remove PostgreSQL 14

There is likely no urgency for you to do this, but later after you're convinced PostgreSQL 15 is working well for you, you can remove the old PostgreSQL 14 packages and data.

First we'll run this command without agreeing, to see what the package manager plans to do:

```plain
[root@yourhost ~]# rpm -qa postgresql14\* | xargs dnf erase
Dependencies resolved.
======================================================================
 Package              Architecture  Version         Repository   Size
======================================================================
Removing:
 postgresql14         x86_64        14.5-1PGDG.f36  @pgdg14     7.7 M
 postgresql14-devel   x86_64        14.5-1PGDG.f36  @pgdg14      19 M
 postgresql14-libs    x86_64        14.5-1PGDG.f36  @pgdg14     935 k
 postgresql14-server  x86_64        14.5-1PGDG.f36  @pgdg14      24 M

Transaction Summary
======================================================================
Remove  4 Packages

Freed space: 51 M
Is this ok [y/N]: Operation aborted.
```

If it proposes to remove only what you want, and not any other dependencies you want to keep, you can give `dnf` the go-ahead with the `-y` (yes) option:

```plain
[root@yourhost ~]# rpm -qa postgresql14\* | xargs dnf erase -y
```

And you can run the script that `pg_upgrade` left you to delete the old cluster's data files:

```plain
[root@yourhost ~]# su - postgres
[postgres@yourhost ~]$ ./delete_old_cluster.sh
```

Enjoy!

### Reference

* [PostgreSQL 15 release announcement](https://www.postgresql.org/about/news/postgresql-15-released-2526/)
* [PostgreSQL 15 release notes](https://www.postgresql.org/docs/release/15.0/)
* [PostgreSQL Red Hat family Linux downloads](https://www.postgresql.org/download/linux/redhat/)
* [PostgreSQL Global Development Group (PGDG) Yum Repository](https://yum.postgresql.org/)
