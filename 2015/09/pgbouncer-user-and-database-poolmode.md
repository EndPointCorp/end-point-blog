---
author: Greg Sabino Mullane
title: Pgbouncer user and database pool_mode with Scaleway
github_issue_number: 1160
tags:
- cloud
- database
- postgres
- scalability
date: 2015-09-24
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2015/09/pgbouncer-user-and-database-poolmode/image-0.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" data-original-height="333" data-original-width="500" id="jA0ECgMCcw4XQprbL4Fg0nYB3a6dd1Vi67QwWMs7TvxhnNfGQ2Qze6lTuPNBjKVpfppBeYnI8F9EumHNXWq9EfoO2spSKn/O4L7ls+X8VcOivVg5IRIFusCv9P8fSftPW/Bvkvp/PnC344QZDFpZ0nxEVcqJ0JGnoKGW3em3InqwzIWYXNT7=aYud" src="/blog/2015/09/pgbouncer-user-and-database-poolmode/image-0.jpeg" width="400"/></a><br/><small>(<a href="https://flic.kr/p/nUKQby">Waterfall photo</a> by <a href="https://www.flickr.com/photos/lukeprice88/">Luke Price</a></small>)</div>

The recent release of [PgBouncer 1.6](https://pgbouncer.github.io/), a connection
pooler for Postgres, brought a number of new features. The two I want to demonstrate today are
the per-database and per-use pool_modes. To get this effect
previously, one had to run separate instances of PgBouncer.
As we shall see, a single instance can now run different pool_modes seamlessly.

There are three pool modes available in PgBouncer, representing how aggressive
the pooling becomes: **session mode**, **transaction mode**, and **statement mode**.

**Session pool mode** is the default, and simply allows you to avoid
the startup costs for new connections. PgBouncer connects to Postgres, keeps the
connection open, and hands it off to clients connecting to PgBouncer. This
handoff is faster than connecting to Postgres itself, as no new backends need to
be spawned. However, it offers no other benefits, and many clients/applications
already do their own connection pooling, making this the least useful pool mode.

**Transaction pool mode** is probably the most useful one. It works by
keeping a client attached to the same Postgres backend for the duration of
a transaction only. In this way, many clients can share the same backend
connection, making it possible for Postgres to handle a large number of clients
with a small **max_connections** setting (each of which consumes resources).

**Statement pool mode** is the most interesting one, as it makes no
promises at all to the client about maintaining the same Postgres backend. In
other words, every time a client runs a SQL statement, PgBouncer releases that
connections back to the pool. This can make for some great performance gains,
although it has drawbacks, the primary one being no multi-statement transactions.

To demonstrate the new pool_mode features, I decided to try out a new service
mentioned by a coworker, called [Scaleway](https://www.scaleway.com/). Like Amazon Web Services (AWS), it
offers quick-to-create cloud servers, ideal for testing and demonstrating.
The unique things about Scaleway is the servers are all ARM-based SSDs.
Mini-review of Scaleway: I liked it a lot. The interface was smooth and
uncluttered (looking askance at you, AWS), the setup was very fast, and I had
no problems with it being ARM.

To start a new server (once I entered my billing information, and pasted
my public SSH key in), I simply clicked the create server button, chose
“Debian Jessie (8.1)”, and then create server again. 60 seconds later,
I had an IP address to login as root. The first order of business, as always,
is to make sure things are up to date and install some important tools:

```
root@scw-56578065:~# apt-get update
root@scw-56578065:~# apt-get upgrade
## Only five packages were upgraded, which means things are already very up to date

## Because just plain 'apt-get' only gets you so far:
root@scw-56578065:~# apt-get install aptitude

## To find out the exact names of some critical packages:
root@scw-56578065:~# aptitude search emacs git

## Because a server without emacs is like a jungle without trees:
root@scw-56578065:~# apt-get install emacs-nox git-core

## To figure out what version of Postgres is available:
root@scw-56578065:~# aptitude show postgresql
Package: postgresql
State: not installed
Version: 9.4+165

## Since 9.4 is the latest, we will happily use it for this demo:
root@scw-56578065:~# apt-get install postgresql postgresql-contrib

## Nice to not have to worry about initdb anymore:
root@scw-56578065:~# service postgresql start
```

Postgres 9.4 is now installed, and started up. Time to figure out where
the configuration files are and make a few small changes. We will turn
on some heavy logging via the **postgresql.conf** file, and allow anyone
locally to log in to Postgres, no questions asked, by changing
the **pg_hba.conf** file. Then we restart Postgres, and verify it is working:

```
root@scw-56578065:~# updatedb
root@scw-56578065:~# locate postgresql.conf pg_hba.conf

root@scw-56578065:~# echo "logging_collector = on
log_filename = 'postgres-%Y-%m-%d.log'
log_rotation_size = 0" >> /etc/postgresql/9.4/main/postgresql.conf

## But it already has a nice log_line_prefix (bully for you, Debian)

## Take a second to squirrel away the old version before overwriting:
root@scw-56578065:~# cp /etc/postgresql/9.4/main/pg_hba.conf ~
root@scw-56578065:~# echo "local all all trust" > /etc/postgresql/9.4/main/pg_hba.conf
root@scw-56578065:~# service postgresql restart
root@scw-56578065:~# psql -U postgres -l
                             List of databases
   Name    |  Owner   | Encoding  | Collate | Ctype |   Access privileges
-----------+----------+-----------+---------+-------+-----------------------
 postgres  | postgres | SQL_ASCII | C       | C     |
 template0 | postgres | SQL_ASCII | C       | C     | =c/postgres          +
           |          |           |         |       | postgres=CTc/postgres
 template1 | postgres | SQL_ASCII | C       | C     | =c/postgres          +
           |          |           |         |       | postgres=CTc/postgres
(3 rows)
```

SQL_ASCII? Yuck, how did that get in there?! That’s an absolutely terrible
encoding to be using in 2015, so we need to change that right away. Even
though it won’t affect this demonstration, there is the principle of the matter.
We will create a new database with a sane encoding, then create some test databases
based on that.

```
root@scw-56578065:~# su - postgres
postgres@scw-56578065:~$ createdb -T template0 -E UTF8 -l en_US.utf8 foo
postgres@scw-56578065:~$ for i in {1..5}; do createdb -T foo test$i; done
postgres@scw-56578065:~$ psql -l
                             List of databases
   Name    |  Owner   | Encoding  |  Collate   |   Ctype    |   Access privileges
-----------+----------+-----------+------------+------------+-----------------------
 foo       | postgres | UTF8      | en_US.utf8 | en_US.utf8 |
 postgres  | postgres | SQL_ASCII | C          | C          |
 template0 | postgres | SQL_ASCII | C          | C          | =c/postgres          +
           |          |           |            |            | postgres=CTc/postgres
 template1 | postgres | SQL_ASCII | C          | C          | =c/postgres          +
           |          |           |            |            | postgres=CTc/postgres
 test1     | postgres | UTF8      | en_US.utf8 | en_US.utf8 |
 test2     | postgres | UTF8      | en_US.utf8 | en_US.utf8 |
 test3     | postgres | UTF8      | en_US.utf8 | en_US.utf8 |
 test4     | postgres | UTF8      | en_US.utf8 | en_US.utf8 |
 test5     | postgres | UTF8      | en_US.utf8 | en_US.utf8 |
(9 rows)

## Create some test users as well:
postgres@scw-56578065:~$ for u in {'alice','bob','eve','mallory'}; do createuser $u; done
## First time I tried this I outfoxed myself - so make sure the users can connect!
postgres@scw-56578065:~$ for d in {1..5}; do psql test$d -qc 'grant all on all tables in schema public to public'; done

## Make sure we can connect as one of our new users:
postgres@scw-56578065:~$ psql -U alice test1 -tc 'show effective_cache_size'
 847283
```

Now that Postgres is up and running, let’s install PgBouncer. Since we are
showing off some 1.6 features, it is unlikely to be available via packaging,
but we will check anyway.

```
postgres@scw-56578065:~$ aptitude versions pgbouncer
Package pgbouncer:
p   1.5.4-6+deb8u1            stable            500

## Not good enough! Let's grab 1.6.1 from git:
postgres@scw-56578065:~$ git clone https://github.com/pgbouncer/pgbouncer
postgres@scw-56578065:~$ cd pgbouncer
## This submodule business for such a small self-contained project really irks me :)
postgres@scw-56578065:~/pgbouncer$ git submodule update --init
postgres@scw-56578065:~/pgbouncer$ git checkout pgbouncer_1_6_1
postgres@scw-56578065:~/pgbouncer$ ./autogen.sh
```

The autogen.sh script fails rather quickly with an error about libtool—​which is to be expected,
as PgBouncer comes with a small list of required packages in order to build it. Because monkeying
around with all those prerequisites can get tiresome, apt-get provides an option called “build-dep”
that (in theory!) allows you to download everything needed to build a specific package. Before doing
that, let’s drop back to root and give the postgres user full sudo permission, so we don’t have to
keep jumping back and forth between accounts:

```
postgres@scw-56578065:~/pgbouncer$ exit
## This is a disposable test box - do not try this at home!
## Debian's /etc/sudoers has #includedir /etc/sudoers.d, so we can do this:
root@scw-56578065:~# echo "postgres ALL= NOPASSWD:ALL" > /etc/sudoers.d/postgres
root@scw-56578065:~# su - postgres
postgres@scw-56578065:~ cd postgres
postgres@scw-56578065:~/pgbouncer$ sudo apt-get build-dep pgbouncer
The following NEW packages will be installed:
  asciidoc autotools-dev binutils build-essential cdbs cpp cpp-4.9 debhelper docbook-xml docbook-xsl dpkg-dev g++ g++-4.9 gcc gcc-4.9 gettext
  gettext-base intltool-debian libasan1 libasprintf0c2 libatomic1 libc-dev-bin libc6-dev libcloog-isl4 libcroco3 libdpkg-perl libevent-core-2.0-5
  libevent-dev libevent-extra-2.0-5 libevent-openssl-2.0-5 libevent-pthreads-2.0-5 libgcc-4.9-dev libgomp1 libisl10 libmpc3 libmpfr4 libstdc++-4.9-dev
  libubsan0 libunistring0 libxml2-utils linux-libc-dev po-debconf sgml-data xmlto xsltproc
postgres@scw-56578065:~/pgbouncer$ ./autogen.sh
```

Whoops, another build failure. Well, build-dep isn’t perfect, turns out we still need
a few packages. Let’s get this built, create some needed directories, tweak permissions,
find the location of the installed PgBouncer ini file, and make a few changes to it:

```
postgres@scw-56578065:~/pgbouncer$ sudo apt-get install libtools automake pkg-config
postgres@scw-56578065:~/pgbouncer$ ./autogen.sh
postgres@scw-56578065:~/pgbouncer$ ./configure
postgres@scw-56578065:~/pgbouncer$ make
postgres@scw-56578065:~/pgbouncer$ sudo make install
postgres@scw-56578065:~/pgbouncer$ sudo updatedb
postgres@scw-56578065:~/pgbouncer$ locate pgbouncer.ini
/var/lib/postgresql/pgbouncer/etc/pgbouncer.ini
postgres@scw-56578065:~/pgbouncer$ sudo mkdir /var/log/pgbouncer /var/run/pgbouncer
postgres@scw-56578065:~/pgbouncer$ sudo chown postgres.postgres /var/log/pgbouncer \
 /var/run/pgbouncer /var/lib/postgresql/pgbouncer/etc/pgbouncer.ini
postgres@scw-56578065:~/pgbouncer$ emacs /var/lib/postgresql/pgbouncer/etc/pgbouncer.ini
## Add directly under the [databases] section:
test1 = dbname=test1 host=/var/run/postgresql
test2 = dbname=test2 host=/var/run/postgresql pool_mode=transaction
test3 = dbname=test3 host=/var/run/postgresql pool_mode=statement
test4  = dbname=test3 host=/var/run/postgresql pool_mode=statement auth_user=postgres
## Change listen_port to 5432
## Comment out listen_addr
## Make sure unix_socket_dir is /tmp
```

How are we able to use 5432, when Postgres is using it too? In the unix world, a port relies on a
socket file, which is located somewhere on the file system. Thus, you can use the same port as long
as they are coming from different files. While Postgres has a default **unix_socket_directories** value
of **'/tmp'**, Debian has changed that to **'/var/run/postgresql'**, meaning PgBouncer itself is
free to use **'/tmp'**!
The bottom line is that we can use port 5432 for both Postgres and PgBouncer, and control which one
is used by setting the host parameter when connecting (which, when starting with a slash, is
actually the location of the socket file). However, note that only one of them can be used when
connecting via TCP/IP. Enough of all that, let’s make sure PgBouncer at least
starts up!

```
postgres@scw-56578065:~/pgbouncer$ pgbouncer /var/lib/postgresql/pgbouncer/etc/pgbouncer.ini -d
2000-08-04 02:06:08.371 5555 LOG File descriptor limit: 65536 (H:65536),
 max_client_conn: 100, max fds possible: 230
postgres@scw-56578065:~/pgbouncer$
```

As expected, the pgbouncer program gave us a single line of information before going into background daemon mode, per
the **-d** argument. Since both Postgres and PgBouncer are running on port 5432, let’s make our psql prompt
a little more informative, by having it list the hostname via **%M**. If the hostname matches the unix_socket_directory
value that psql was compiled with, then it will simply show **'[local]'**. Thus, seeing **'/tmp'** indicates we are
connected to PgBouncer, and seeing **'[local]'** indicates we are connected to Postgres (via /var/run/postgresql).

```
## Visit the <a href="http://www.postgresql.org/docs/current/static/app-psql.html#APP-PSQL-PROMPTING">psql docs</a> for explanation of this prompt
postgres@scw-56578065:~/pgbouncer$ echo "\set PROMPT1 '%n@%/:%>%R%x%#%M '" > ~/.psqlrc
```

Let’s confirm that each PgBouncer connection is in the expected mode. Database test1 should be using the
default pool_mode, “session”. Database test2 should be using a “transaction” pool_mode, while “statement” mode
should be used by both test3 and test4. See my previous blog post on
[ways to detect the various pool_modes of pgbouncer](/blog/2015/05/connected-to-pgbouncer-or-postgres/). First, let’s connect to normal Postgres and
verify we are not connected to PgBouncer by trying to change to a non-existent database. **FATAL** means
PgBouncer, and **ERROR** means Postgres:

```
postgres@scw-56578065:~/pgbouncer$ psql test1
psql (9.4.3)
Type "help" for help.

postgres@test1:5432=#[local] \c crowdiegocrow
FATAL:  database "crowdiegocrow" does not exist

postgres@scw-56578065:~/pgbouncer$ psql -h /tmp test1
psql (9.4.3)
Type "help" for help.

postgres@test1:5432=#[local:/tmp] \c sewdiegosew
ERROR:  No such database: sewdiegosew
```

Now let’s confirm that we have database-specific pool modes working. If you recall from above, test2 is set to transaction mode,
and test3 is set to statement mode. We determine the mode by running three tests. First, we do a “BEGIN; ROLLBACK;”—​if this fails,
it means we are in statement mode. Next, we try to PREPARE and EXECUTE a statement. If this fails, it means
we are in a transaction mode. Finally, we try to switch to a non-existent database. If it returns an ERROR, it
means we are in session mode. If it returns a FATAL, it means we are not connected to PgBouncer at all.

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2015/09/pgbouncer-user-and-database-poolmode/image-1-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img alt="Your mnemonic helper" border="0" src="/blog/2015/09/pgbouncer-user-and-database-poolmode/image-1.png"/></a></div>

```
## Mnemonic for this common set of psql options: "axe cutie"
postgres@scw-56578065:~/pgbouncer$ psql -Ax -qt -h /tmp test1
postgres@test1:5432=#[local:/tmp] BEGIN; ROLLBACK;
postgres@test1:5432=#[local:/tmp] PREPARE abc(int) AS SELECT $1::text;
postgres@test1:5432=#[local:/tmp] EXECUTE abc(123);
text|123
postgres@test1:5432=#[local:/tmp] \c rowdiegorow
ERROR:  No such database: rowdiegorow
## test1 is thus running in session pool_mode

postgres@scw-56578065:~/pgbouncer$ psql -Ax -qt -h /tmp test2
postgres@test2:5432=#[local:/tmp] BEGIN; ROLLBACK;
postgres@test2:5432=#[local:/tmp] PREPARE abc(int) AS SELECT $1::text;
postgres@test2:5432=#[local:/tmp] EXECUTE abc(123);
ERROR:  prepared statement "abc" does not exist
## test2 is thus running in transaction pool_mode

postgres@scw-56578065:~/pgbouncer$ psql -Ax -qt -h /tmp test3
postgres@test3:5432=#[local:/tmp] BEGIN; ROLLBACK;
ERROR:  Long transactions not allowed
## test3 is thus running in statement pool_mode
```

So the database-level pool modes are working as expected. PgBouncer now supports user-level
pool modes as well, and these always trump the database-level pool
modes. Recall that our setting for test4 in the pgbouncer.ini file was:

```
test4 = dbname=test3 host=/var/run/postgresql pool_mode=statement auth_user=postgres
```

The addition of the auth_user parameter allows us to specify other users to connect as, without
having to worry about adding them to the PgBouncer auth_file. We added four sample regular users
above: Alice, Bob, Eve, and Mallory. We should only be able to connect with them via auth_user,
so only test4 should work:

```
postgres@scw-56578065:~/pgbouncer$ psql -h /tmp test1 -U alice
psql: ERROR:  No such user: alice
postgres@scw-56578065:~/pgbouncer$ psql -h /tmp test2 -U alice
psql: ERROR:  No such user: alice
postgres@scw-56578065:~/pgbouncer$ psql -h /tmp test3 -U alice
psql: ERROR:  No such user: alice
postgres@scw-56578065:~/pgbouncer$ psql -h /tmp test4 -U alice
psql (9.4.3)
Type "help" for help.

alice@test4:5432=>[local:/tmp] begin;
ERROR:  Long transactions not allowed
```

Let’s see if we can change the pool_mode for Alice to transaction, even if we
are connected to test4 (which is set to statement mode). All it takes is a quick entry
to the **pgbouncer.ini** file, in a section we must create called **[users]**:

```
echo "[users]
alice = pool_mode=transaction
$(cat /var/lib/postgresql/pgbouncer/etc/pgbouncer.ini)" \
> /var/lib/postgresql/pgbouncer/etc/pgbouncer.ini

## Attempt to reload pgbouncer:
postgres@scw-56578065:~/pgbouncer$ kill -HUP `head -1 /run/pgbouncer/pgbouncer.pid`

## Failed, due to a PgBouncer bug:
2001-03-05 02:27:44.376 5555 FATAL @src/objects.c:299 in function
  put_in_order(): put_in_order: found existing elem

## Restart it:
postgres@scw-56578065:~/pgbouncer$ pgbouncer /var/lib/postgresql/pgbouncer/etc/pgbouncer.ini -d

postgres@scw-56578065:~/pgbouncer$ psql -Ax -qt -h /tmp test4 -U alice
alice@test4:5432=>[local:/tmp] BEGIN; ROLLBACK;
alice@test4:5432=>[local:/tmp] PREPARE abc(int) AS SELECT $1::text;
alice@test4:5432=>[local:/tmp] EXECUTE abc(123);
ERROR:  prepared statement "abc" does not exist
## test4 is thus running in transaction pool_mode due to the [users] setting
```

There you have it—​database-specific and user-specific PgBouncer pool_modes. Note that you cannot
yet do user *and* database specific pool_modes, such as if you want Alice to use transaction
mode for database test4 and statement mode for test5.
