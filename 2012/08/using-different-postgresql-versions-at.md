---
author: Szymon Lipiński
title: Using Different PostgreSQL Versions at The Same Time.
github_issue_number: 680
tags:
- postgres
- ubuntu
date: 2012-08-20
---

When I work for multiple clients on multiple different projects, I usually need a bunch of different stuff on my machine. One of the things I need is having multiple PostgreSQL versions installed.

I use Ubuntu 12.04. Installing PostgreSQL there is quite easy. Currently there are available two versions out of the box: 8.4 and 9.1. To install them I used the following command:

```shell
~$ sudo apt-get install postgresql-9.1 postgresql-8.4 postgresql-client-common
```

Now I have the above two versions installed.

Starting the database is also very easy:

```shell
~$ sudo service postgresql restart
 * Restarting PostgreSQL 8.4 database server   [ OK ]
 * Restarting PostgreSQL 9.1 database server   [ OK ]
```

The problem I had for a very long time was using the proper psql version. Both database installed their own programs like pg_dump and psql. Normally you can use pg_dump from the higher version PostgreSQL, however using different psql versions can be dangerous because psql uses a lot of queries which dig deep into the PostgreSQL internal tables for getting information about the database. Those internals sometimes change from one database version to another, so the best solution is to use the psql from the PostgreSQL installation you want to connect to.

The solution to this problem turned out to be quite simple. There is a pg_wrapper program which can take care of the different versions. It is enough to provide information about the PostgreSQL version you want to connect to and it will automatically choose the correct psql version.

Below you can see the results of using psql --version command which prints the psql version. As you can see there are different psql versions chosen according to the --cluster parameter.

```shell
~$ psql --cluster 8.4/main --version
psql (PostgreSQL) 8.4.11
contains support for command-line editing
~$ psql --cluster 9.1/main --version
psql (PostgreSQL) 9.1.4
contains support for command-line editing
```

You can find more information in the program manual using man pg_wrapper or at [pg_wrapper manual](http://manpages.ubuntu.com/manpages/precise/man1/pg_wrapper.1.html)
