---
author: Greg Sabino Mullane
gh_issue_number: 1150
tags: database, postgres, replication
title: Bucardo replication from Postgres to sqlite and mariadb using pgbench
---



<div class="separator" style="margin: 0 0 20px 20px; clear: both; float: right; text-align: center;"><a href="/blog/2015/08/12/bucardo-postgres-replication-pgbench/image-0-big.png" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/08/12/bucardo-postgres-replication-pgbench/image-0.png"/></a><br/><small><a href="https://flic.kr/p/rwPy8">"Apples and oranges" image</a><br/> by
<a href="https://www.flickr.com/people/mukluk/">Dan McKay</a></small></div>

While [Bucardo](https://bucardo.org/) is known for doing “multi-master” Postgres replication,  it can do a lot more than simple “master to master” replication (better known as “source to source” replication). As people have been asking for simple Bucardo [Bucardo 5](/blog/2014/06/23/bucardo-5-multimaster-postgres-released) recipes based on [pgbench](http://www.postgresql.org/docs/devel/static/pgbench.html), I decided to present a few here. Since Bucardo allows any number of sources and targets, I will demonstrate a source-source-source-target replication. Targets do not have to be Postgres, so let’s also show that we can do source—[MariaDB](https://mariadb.org/)—[SQLite](https://sqlite.org/) replication. Because my own boxes are so customized,  I find it easier and more honest when writing demos to start with a fresh system, which also allows you to follow along at home. For this example, I decided to fire up [Amazon Web Services](https://aws.amazon.com/ec2) (AWS) again.

After logging in at [https://aws.amazon.com](http://aws.amazon.com/), I visited the AWS Management Console, selected “EC2”, clicked on “Launch Instance”, and picked the Amazon Linux AMI (in this case, “Amazon Linux AMI 2015.03 (HVM), SSD Volume Type—ami-1ecae776”). Demos like this require very little resources,  so choosing the smallest AMI (t2.micro) is more than sufficient. After waiting a couple of minutes for it to start up, I was able to SSH in and begin. The first order of business is always updating the box and installing some standard tools. After that I make sure we can install the most recent version of Postgres. I’ll skip the initial steps and jump to the Major Problem I encountered:

```
$ sudo yum install postgresql94-plperl
Error: Package: postgresql94-plperl-9.4.4-1PGDG.rhel6.x86_64 (pgdg94)
           Requires: perl(:MODULE_COMPAT_5.10.1)
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
```

Well, that’s not good (and the “You could try” are useless in this case). Although all the other Postgres packages installed without a problem (postgresql94, postgresql94-server, and postgresql94-libs), there is a major incompatibility preventing Pl/Perl from working. Basically, the rpm was compiled against Perl version 5.10, but Amazon Linux is using 5.16! There are many solutions to this problem, from using perlbrew, to downgrading the system Perl, to compiling Postgres manually. However, this is the Age of the Cloud, so a simpler solution is to ditch this AMI and pick a different one. I decided to try a RHEL (Red Hat Enterprise Linux) AMI. Again, I used a t2.micro instance and launched RHEL-7.1 (AMI ID RHEL-7.1_HVM_GA-20150225-x86_64-1-Hourly2-GP2). As always when starting up an instance, the first order of business when logging in is to update the box. Then I installed some important tools, and set about getting the latest and greatest version of Postgres up and running:

```
$ sudo yum update
$ sudo yum install emacs-nox mlocate git perl-DBD-Pg
```

Checking the available Postgres version reveals,  as expected, that it is way too old:

```
$ sudo yum list postgresql*-server
Loaded plugins: amazon-id, rhui-lb
Available Packages
postgresql-server.x86_64        9.2.13-1.el7_1        rhui-REGION-rhel-server-release
```

Luckily, there is excellent support for Postgres packaging on most distros. The first step is to find a rpm to use to get the “pgdg” yum repository in place. Visit [http://yum.postgresql.org/](https://yum.postgresql.org/) and choose the latest version (as of this writing, 9.4). Then find your distro, and copy the link to the rpm. Going back to the AWS box,  add it in like this:

```
$ sudo yum localinstall http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-redhat94-9.4-1.noarch.rpm
```

This installs a new entry in the **/etc/yum.repos.d/** directory named **pgdg-94-redhat.repo**. However, we want to make sure that we never touch the old, stale versions of Postgres provided by the native yum repos. Keeping it from appearing is as simple as finding out which repo it is in,  and adding an exclusion to that repository section by writing **exclude=postgres***. Finally, we verify that all yum searches for Postgres return only the 9.4 items:

```
## We saw above that repo was "rhui-REGION-rhel-server-release"
## Thus, we know which file to edit
$ sudo emacs /etc/yum.repos.d/redhat-rhui.repo
## At the end of the [rhui-REGION-rhel-server-releases] section, add this line:
exclude=postgres*

## Now we can retry the exact same command as above
$ sudo yum list postgresql*-server
Loaded plugins: amazon-id, rhui-lb
Installed Packages
postgresql94-server.x86_64        9.4.4-1PGDG.rhel7        pgdg94
```

Now it is time to install Postgres 9.4. Bucardo currently needs to use Pl/Perl, so we will install that package (which will also install the core Postgres packages for us). As we are going to need the [pgbench utility](https://wiki.postgresql.org/wiki/Pgbench),  we also need to install the **postgresql-contrib** package.

```
$ sudo yum install postgresql-plperl postgresql-contrib
```

This time it went fine—and Perl is at 5.16.3. The next step is to start Postgres up. Red Hat has gotten on the 
[systemd](https://en.wikipedia.org/wiki/Systemd#Criticism) bandwagon, for better or for worse, so gone is the familiar 
**/etc/init.d/postgresql** script. Instead, we need to use **systemctl**. We will find the exact service name, enable it, then try to start it up:

```
$ systemctl list-unit-files | grep postgres
## postgresql-9.4.service                      disabled

$ sudo systemctl enable postgresql-9.4
ln -s '/usr/lib/systemd/system/postgresql-9.4.service' '/etc/systemd/system/multi-user.target.wants/postgresql-9.4.service'
$ sudo systemctl start postgresql-9.4
Job for postgresql-9.4.service failed. See 'systemctl status postgresql-9.4.service' and 'journalctl -xn' for details.
```

As in the pre-systemd days, we need to run initdb before we can start Postgres. However, the simplicity of the init.d script is gone (e.g. “service postgresql initdb”). Poking in the systemd logs reveals the solution:

```
$ sudo systemctl -l status postgresql-9.4.service
<small id="a22428324754587579849612518418719320321423323528228631933334960571973678780180384284685886187995896299299310201044107210931116111811751176117711861245125412631279162416251626z">postgresql-9.4.service - PostgreSQL 9.4 database server
   Loaded: loaded (/usr/lib/systemd/system/postgresql-9.4.service; enabled)
   Active: failed (Result: exit-code) since Wed 2015-08-03 10:15:25 EDT; 1min 21s ago
  Process: 11916 ExecStartPre=/usr/pgsql-9.4/bin/postgresql94-check-db-dir ${PGDATA} (code=exited, status=1/FAILURE)

Aug 03 10:15:25 ip-12.15.22.5.ec2.internal systemd[1]: Starting PostgreSQL 9.4 database server...
Aug 03 10:15:25 ip-12.15.22.5.ec2.internal postgresql94-check-db-dir[11916]: "/var/lib/pgsql/9.4/data/" is missing or empty.
Aug 03 10:15:25 ip-12.15.22.5.ec2.internal postgresql94-check-db-dir[11916]: Use "/usr/pgsql-9.4/bin/postgresql94-setup initdb" to initialize the database cluster.
Aug 03 10:15:25 ip-12.15.22.5.ec2.internal postgresql94-check-db-dir[11916]: See %{_pkgdocdir}/README.rpm-dist for more information.
Aug 03 10:15:25 ip-12.15.22.5.ec2.internal systemd[1]: postgresql-9.4.service: control process exited, code=exited status=1
Aug 03 10:15:25 ip-12.15.22.5.ec2.internal systemd[1]: Failed to start PostgreSQL 9.4 database server.
Aug 03 10:15:25 ip-12.15.22.5.ec2.internal systemd[1]: Unit postgresql-9.4.service entered failed state.</small>
```

That’s ugly output, but what can you do? Let’s run initdb, start things up, and create a test database. As I really like to use 
[Postgres with checksums](http://paquier.xyz/postgresql-2/postgres-9-3-feature-highlight-data-checksums/), 
we can set the environment variables to pass that flag to initdb. After that completes, we can startup Postgres.

```
$ sudo PGSETUP_INITDB_OPTIONS=--data-checksums /usr/pgsql-9.4/bin/postgresql94-setup initdb
Initializing database ... OK

$ sudo systemctl start postgresql-9.4
```

Now that Postgres is up and running, it is time to create some test databases and populate them via the pgbench utility. First, a few things to make life easier. Because pgbench installs into **/usr/pgsql-9.4/bin**, which is certainly not in anyone’s PATH, we will put it in a better location. We also want to loosen the Postgres login restrictions,  and reload Postgres so it takes effect:

```
$ sudo ln -s /usr/pgsql-9.4/bin/pgbench /usr/local/bin/
$ sudo sh -c 'echo "local all all trust" > /var/lib/pgsql/9.4/data/pg_hba.conf'
$ sudo systemctl reload postgresql-9.4
```

Now we can create a test database, put the pgbench schema into it, and then give the pgbench_history table a 
primary key, which Bucardo needs in order to replicate it:

```
$ export PGUSER=postgres
$ createdb test1
$ pgbench -i --foreign-keys test1
NOTICE:  table "pgbench_history" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_branches" does not exist, skipping
creating tables...
100000 of 100000 tuples (100%) done (elapsed 0.10 s, remaining 0.00 s).
vacuum...
set primary keys...
set foreign keys...
done.
$ psql test1 -c 'alter table pgbench_history add column hid serial primary key'
ALTER TABLE
```

We want to create three copies of the database we just created, but without the data:

```
$ createdb test2
$ createdb test3
$ createdb test4
$ pg_dump --schema-only test1 | psql -q test2
$ pg_dump --schema-only test1 | psql -q test3
$ pg_dump --schema-only test1 | psql -q test4
```

Next up is installing Bucardo itself. We shall grab version 5.4.0 from the git repository, after cryptographically 
verifying the tag:

```
$ git clone http://bucardo.org/bucardo.git
Cloning into 'bucardo'...
$ cd bucardo
$ gpg --keyserver pgp.mit.edu --recv-keys 2529DF6AB8F79407E94445B4BC9B906714964AC8

$ git tag -v 5.4.0
object f1f8b0f6ed0be66252fa203c20a3f03a9382cd98
type commit
tag 5.4.0
tagger Greg Sabino Mullane <greg@endpoint.com> 1438906359 -0400

Version 5.4.0, released August 6, 2015
gpg: Signature made Thu 06 Aug 2015 08:12:39 PM EDT using DSA key ID 14964AC8
gpg: please do a --check-trustdb
gpg: Good signature from "Greg Sabino Mullane <greg@turnstep.com>"
gpg:                 aka "Greg Sabino Mullane (End Point Corporation) <greg@endpoint.com>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 2529 DF6A B8F7 9407 E944  45B4 BC9B 9067 1496 4AC8</greg@endpoint.com></greg@turnstep.com></greg@endpoint.com>

$ git checkout 5.4.0
```

Before Bucardo can be fully installed, some dependencies must be installed. What you need will depend on what your particular OS already has. 
For RHEL 7.1, this means a few things via yum, as well as some things via the cpan program:

```
$ sudo yum install perl-Pod-Parser perl-Sys-Syslog perl-Test-Simple perl-ExtUtils-MakeMaker cpan
$ echo y | cpan
$ (echo o conf make_install_make_command "'sudo make'"; echo o conf commit) | cpan
$ cpan boolean DBIx::Safe

## Now we can install the Bucardo program:
$ perl Makefile.PL
$ make
$ sudo make install

## Setup some directories we will need
$ sudo mkdir /var/run/bucardo /var/log/bucardo
$ sudo chown $USER /var/run/bucardo /var/log/bucardo

## Install the Bucardo database:
$ bucardo install ## hit "P" twice
```

Now that Bucardo is ready to go, let’s teach it about our databases and tables, then 
setup a three-source, one-target database sync (aka multimaster or master-master-master-slave)

```
$ bucardo add db A,B,C,D dbname=test1,test2,test3,test4
Added databases "A","B","C","D"

$ bucardo add all tables relgroup=bench
Creating relgroup: bench
Added table public.pgbench_branches to relgroup bench
Added table public.pgbench_tellers to relgroup bench
Added table public.pgbench_accounts to relgroup bench
Added table public.pgbench_history to relgroup bench
New tables added: 4

$ bucardo add all sequences relgroup=bench
Added sequence public.pgbench_history_hid_seq to relgroup bench
New sequences added: 1

$ bucardo add sync btest relgroup=bench dbs=A:source,B:source,C:source,D:target
Added sync "btest"
Created a new dbgroup named "btest"

$ bucardo start
Checking for existing processes
Starting Bucardo
```

Time to test that it works. The initial database, “test1”, should have many rows in the pgbench_accounts table, while the other databases should have none. Once we update some of the rows in the test1 database, it should replicate to all the others. Changes in test2 and test3 should go everywhere as well,  because they are source databases. Changes made to the database test4 should stay in test4, as it is only a target.

```
$ psql test1 -xtc 'select count(*) from pgbench_accounts'
count | 100000

$ for i in {2,3,4}; do psql test$i -xtc 'select count(*) from pgbench_accounts'; done
count | 0
count | 0
count | 0

## We want to "touch" these four rows to make sure they replicate out:
$ psql test1 -c 'UPDATE pgbench_accounts set aid=aid where aid <= 4'
UPDATE 4

$ for i in {2,3,4}; do psql test$i -xtc 'select count(*) from pgbench_accounts'; done
count | 4
count | 4
count | 4

$ for i in {1,2,3,4}; do psql test$i -xtc "update pgbench_accounts set abalance=$i*100 where aid=$i"; done
UPDATE 1
UPDATE 1
UPDATE 1
UPDATE 1
```

```
$ psql test1 -tc 'select aid, abalance from pgbench_accounts where aid <= 4 order by aid'
   1 |      100
   2 |      200
   3 |      300
   4 |        0
$ psql test2 -tc 'select aid, abalance from pgbench_accounts where aid <= 4 order by aid'
   1 |      100
   2 |      200
   3 |      300
   4 |        0
$ psql test3 -tc 'select aid, abalance from pgbench_accounts where aid <= 4 order by aid'
   1 |      100
   2 |      200
   3 |      300
   4 |        0
$ psql test4 -tc 'select aid, abalance from pgbench_accounts where aid <= 4 order by aid'
   1 |      100
   2 |      200
   3 |      300
   4 |      400
```

What happens if we change aid '4' on one of the sources? The local changes to test4 will 
get overwritten:

```
$ psql test1 -c 'update pgbench_accounts set abalance=9999 where aid = 4'
UPDATE 1
$ psql test4 -tc 'select aid, abalance from pgbench_accounts where aid <= 4 order by aid'
   1 |      100
   2 |      200
   3 |      300
   4 |     9999
```

Let’s create one more sync—this time, we want to replicate our Postgres data to a MariaDB and a SQLite database. 
(Bucardo can also do systems like Oracle, but getting it up and running is NOT an easy task for a quick 
demo like this!). The first step is to get both systems up and running,  and provide them with a copy of the pgbench schema:

```
## The program 'sqlite3' is already installed, but we still need the Perl module:
$ sudo yum install perl-DBD-SQLite

## MariaDB takes a little more effort
$ sudo yum install mariadb-server ## this also (surprisingly!) installs DBD::MySQL!

$ systemctl list-unit-files | grep maria
mariadb.service                             disabled
$ sudo systemctl enable mariadb
ln -s '/usr/lib/systemd/system/mariadb.service' '/etc/systemd/system/multi-user.target.wants/mariadb.service'
$ sudo systemctl start mariadb

$ sudo mysql
mysql> create user 'ec2-user'@'localhost' identified by 'sixofone';
mysql> grant all on *.* TO 'ec2-user'@'localhost';
mysql> quit

## Store the MariaDB / MySQL password so we don't have to keep entering it:
$ cat > ~/.my.cnf 
[client]
password = sixofone
```

Now we can create the necessary tables for both. Note that SQLite does not allow you to change a table's structure once it has been created, so we cannot use the MySQL/Postgres way of using ALTER TABLE after the fact to add the primary keys. Knowing this,  we can put everything into the CREATE TABLE statement. This schema will work on all of our systems:

```
CREATE TABLE pgbench_accounts (
    aid      integer NOT NULL PRIMARY KEY,
    bid      integer,
    abalance integer,
    filler   character(84)
);
CREATE TABLE pgbench_branches (
    bid      integer NOT NULL PRIMARY KEY,
    bbalance integer,
    filler   character(88)
);
CREATE TABLE pgbench_history (
    hid    integer NOT NULL PRIMARY KEY,
    tid    integer,
    bid    integer,
    aid    integer,
    delta  integer,
    mtime  datetime,
    filler character(22)
);
CREATE TABLE pgbench_tellers (
    tid      integer NOT NULL PRIMARY KEY,
    bid      integer,
    tbalance integer,
    filler   character(84)
);

$ mysql
msyql> create database pgb;
mysql> use pgb
pgb> ## add the tables here
pgb> quit

$ sqlite3 pgb.sqlite
sqlite> ## add the tables here
sqlite> .q
```

Teach Bucardo about these new databases, then add them to a new sync. As we do not want changes to get immediately replicated, we set this sync to “autokick off”. This will ensure that the sync will only run when it is manually started via the “bucardo kick” command. Since database C is also part of another Bucardo sync and may get rows written to it that way,  we need to set it as a “makedelta” database, which ensures that the replicated rows from the other sync are replicated onwards in our new sync.

```
## Teach Bucardo about the MariaDB database
$ bucardo add db M dbname=pgb type=mariadb user=ec2-user dbpass=fred
Added database "M"

## Teach Bucardo about the SQLite database
$ bucardo add db S dbname=pgb.sqlite type=sqlite
Added database "S"

## Create the new sync, replicating from C to our two non-Postgres databases:
$ bucardo add sync abc relgroup=bench dbs=C:source,M:target,S:target autokick=off
Added sync "abc"
Created a new dbgroup named "abc"

## Make sure any time we replicate to C, we create delta rows for the other syncs
$ bucardo update db C makedelta=on
Changed bucardo.db makedelta from off to on

$ bucardo restart
Creating /var/run/bucardo/fullstopbucardo ... Done
Checking for existing processes
Removing file "/var/run/bucardo/fullstopbucardo"
Starting Bucardo
```

For the final test, all changes to A, B, or C should end up on M and S!

```
$ for i in {1,2,3,4}; do psql test$i -xtc "update pgbench_accounts set abalance=$i*2222 where aid=$i"; done
UPDATE 1
UPDATE 1
UPDATE 1
UPDATE 1

$ psql test4 -tc 'select aid, abalance from pgbench_accounts where aid <= 4 order by aid'
   1 |     2222
   2 |     4444
   3 |     6666
   4 |     8888

$ sqlite3 pgb.sqlite 'select count(*) from pgbench_accounts'
0

$ mysql pgb -e 'select count(*) from pgbench_accounts'
+----------+
| count(*) |
+----------+
|        0 |
+----------+
```

```
$ bucardo kick abc 0
Kick abc: [1 s] DONE!

$ sqlite3 pgb.sqlite 'select count(*) from pgbench_accounts'
3

$ mysql pgb -e 'select count(*) from pgbench_accounts'
+----------+
| count(*) |
+----------+
|        3 |
+----------+

$ sqlite3 pgb.sqlite 'select aid,abalance from pgbench_accounts where aid <=4 order by aid'
1|2222
2|4444
3|6666

$ mysql pgb -e 'select aid,abalance from pgbench_accounts where aid <=4 order by aid'
+-----+----------+
| aid | abalance |
+-----+----------+
|   1 |     2222 |
|   2 |     4444 |
|   3 |     6666 |
+-----+----------+
```

Excellent. Everything is working as expected. Note that the changes from the test4 database were not replicated onwards, as test4 is not a source database. Feel free to ask any questions in the comments below, or better still, on the [Bucardo mailing list](https://mail.endcrypt.com/mailman/listinfo/bucardo-general).


