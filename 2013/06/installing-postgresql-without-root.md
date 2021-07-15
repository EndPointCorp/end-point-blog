---
author: Szymon Lipiński
title: Installing PostgreSQL without Root
github_issue_number: 819
tags:
- postgres
date: 2013-06-12
---

PostgreSQL can be installed using installers prepared for your operation system. However this way you just depend on the installation settings chosen by the packages mainainers. Installation requires root privileges, on some machines programmers are not allowed to do that. What’s more, this way you rather will not install the PostgreSQL beta version.

The only way to install Postgres without root privileges, in home directory, is to compile it from sources. That’s not very difficult.

### Download Sources

First of all you need to download sources. I use GitHub for getting the latest sources. There is a [Postgres GitHub mirror](https://github.com/postgres/postgres). I clone that, but you could just download [zip file](https://github.com/postgres/postgres/archive/master.zip).

Unpack it somewhere, and you have the Postgres sources you need.

### Install Needed Software

For compiling Postgres you will need some libraries and programs. The complete list can be found in [Postgres documentation](https://www.postgresql.org/docs/9.2/static/install-requirements.html).

I’m using Ubuntu, the packages I use for compiling Postgres are:

- gcc — C compiler
- libreadline6, libreadline6-dev — readline support
- zlib1g, zlib1g-dev — compression library used internally by Postgres
- libpython2.7, libpython2.7-dev — for compiling with PL/Python support

If you are using different system, or different system/Postgres version, then your packages/libraries can be named differently.

### Configure

Now you should enter the directory where your sources are and run below command for source configuration:

```
./configure --prefix=$HOME/postgres/ --with-python PYTHON=/usr/bin/python2.7
```

The --prefix parameter shows the path where Postgres will be installed.

The --with-python parameter enables compiling with plpython support.

PYTHON parameter points to current python binary installation.

The configure command should finish without any errors. If you have any errors, most probably you don’t have some needed libraries installed.

### Compile

If configure succeeded, you can compile the sources. It is simple:

```
make -j 4
```

The -j parameter allows for this maximum number of jobs at the same time.

My computer has 4 cores, I want to use all of them, this way compilation time will be much shorter. On my laptop compilation with 4 cores takes 1 minute 26 seconds. Using one core is almost 4 times longer.

### Install

If compilation ended without error, you can install the database. Installation copies all files into the directory from the --prefix parameter. For installation just run:

```
make install
```

This should create four directories in ~/postgres/

```
* bin
* include
* lib
* share
```

### Create database

I’m going to keep the database in the same directory as the installed files. The data will be at ~/postgres/data directory. For this I need to use initdb program, but not this one installed at system level, but this one from ~/postgres/bin/ directory:

```
~/postgres/bin/initdb -D ~/postgres/data/
```

Your output should look like this:

```
The files belonging to this database system will be owned by user "szymon".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.UTF-8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".
Data page checksums are disabled.

creating directory /home/szymon/postgres/data ... ok
creating subdirectories ... ok
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
creating configuration files ... ok
creating template1 database in /home/szymon/postgres/data/base/1 ... ok
initializing pg_authid ... ok
initializing dependencies ... ok
creating system views ... ok
loading system objects' descriptions ... ok
creating collations ... ok
creating conversions ... ok
creating dictionaries ... ok
setting privileges on built-in objects ... ok
creating information schema ... ok
loading PL/pgSQL server-side language ... ok
vacuuming database template1 ... ok
copying template1 to template0 ... ok
copying template1 to postgres ... ok
syncing data to disk ... ok

WARNING: enabling "trust" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or
--auth-local and --auth-host, the next time you run initdb.
```

Success. You can now start the database server using:

/home/szymon/postgres/bin/postgres -D /home/szymon/postgres/data/

or

    /home/szymon/postgres/bin/pg_ctl -D /home/szymon/postgres/data/ -l logfile start

Take a look at the last couple of line. This shows you exact commands needed for running Postgres at this location with this database.

### Run

Let’s run, I will use the first command, the log lines will be printed on console:

```
/home/szymon/postgres/bin/postgres -D /home/szymon/postgres/data/
LOG:  database system was shut down at 2013-06-05 11:08:10 CEST
LOG:  database system is ready to accept connections
LOG:  autovacuum launcher started
```

### Connect

Connect to the database. One important notice, you should use the psql program which you’ve already installed:

```
~/postgres/bin/psql --version
psql (PostgreSQL) 9.3beta1
```

The PostgreSQL installation uses my system username szymon as Postgres admin name. The default database created in Postgres is postgres. To login to this database I use:

```
~/postgres/bin/psql -U szymon postgres
psql (9.3beta1)
Type "help" for help.
```

Let’s also check the database version:

```
postgres=# select version();
                                                    version
---------------------------------------------------------------------------------------------------------------
 PostgreSQL 9.3beta1 on x86_64-unknown-linux-gnu, compiled by gcc (Ubuntu/Linaro 4.7.3-1ubuntu1) 4.7.3, 64-bit
(1 row)
```

And check the data directory:

```
postgres=# show data_directory ;
       data_directory
----------------------------
 /home/szymon/postgres/data
(1 row)
```

### Configuration

All configuration files are stored in the data directory: ~/postgres/data. If you want to run multiple Postgres versions on the same machine, they must have different data directories and different ports. The port number can be changed in ~/postgres/data/postgresql.conf.

### Deleting Installation

If you want to delete the installation—​nothing easier. Just stop the Postgres if it is running, and delete the whole ~/postgres/ directory.

If you want to delete the whole data—​just stop Postgres if it is running, and delete ~/postgres/data directory. Then you can run initdb once again to have a brand new database.

### Summary

I know that there are many ways of installing, and compiling Postgres in local directory. I know that there can be made some more advanced tweaks and automations. I also have my makefile with some default values.

My goal here was to show that it is very easy and there is nothing too difficult for programmers to do it, without asking for root privileges for installation or even starting/stopping database.

This method also works if you need some older Postgres versions and there are no packages for your system, you don’t want to mess with existing packages or the packages require some old libraries you cannot install.
