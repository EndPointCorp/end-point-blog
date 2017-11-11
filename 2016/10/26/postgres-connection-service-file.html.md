---
author: Greg Sabino Mullane
gh_issue_number: 1264
tags: postgres
title: Postgres connection service file
---



<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2016/10/26/postgres-connection-service-file/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/10/26/postgres-connection-service-file/image-0.jpeg"/></a><br/><small>(<a href="https://flic.kr/p/fMYx1K">Photo</a> by<a href="https://www.flickr.com/photos/francisco-javier-garcia-orts/">Francisco Javier Garcia Orts</a>)</small></div>

[Postgres](http://postgres.org) has a wonderfully helpful (but often overlooked) feature called the 
connection service file (its [documentation](https://www.postgresql.org/docs/current/static/libpq-pgservice.html) is quite sparse).
In a nutshell, it defines connection aliases you can use from any client. These connections 
are given simple names, which then map behind the scenes to specific connection parameters, 
such as host name, Postgres port, username, database name, and many others. This can be an 
extraordinarily useful feature to have.

The connection service file is named pg_service.conf and is setup in a known 
location. The entries inside are in the common "INI file" format: a named section, followed by its 
related entries below it, one per line. To access a named section, just use the 
service=*name* string in your application.

```
## Find the file to access by doing:
$ echo `pg_config --sysconfdir`/pg_service.conf
## Edit the file and add a sections that look like this:
[foobar]
host=ec2-76-113-77-116.compute-2.amazonaws.com
port=8450
user=hammond
dbname=northridge

## Now you can access this database via psql:
$ psql service=foobar

## Or in your Perl code:
my $dbh = DBI-&gt;connect('dbi:Pg:service=foobar');

## Other libpq based clients are the same. JDBC, you are out of luck!
```

So what makes this feature awesome? First, it can save you from extra typing. No more 
trying to remember long hostnames (or copy and paste them). Second, it is better than 
a local shell alias, as the service file can be made globally available to all users. It also 
works similar to DNS, in that it insulates you from the details of your connections. Your 
hostname has changed because of a failover? No problem, just edit the one file, 
and no clients need to change a thing.

As seen above, the format of the file is simple: a named section, followed by 
connection parameters in a name=value format. Among the connection parameters one may use, the most common and useful are 
host, port, 
user, and dbname. 
Although you can set a password, I recommend against it, as that belongs in the 
more secure, per-user [.pgpass file](https://www.postgresql.org/docs/current/static/libpq-pgpass.html).

The complete list of what may be set can be found in the middle of the [database connection documentation page](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS). Most of them will seldom, if ever, 
be used in a connection service file.

The connection service file is not just limited to basic connections. You can 
have sections that only differ by user, for example, or in their SSL requirements, 
making it easy to switch things around by a simple change in the service name. It's also 
handy for pgbouncer connections, which typically run on non-standard ports. Be creative 
in your service names, and keep them distinct from each other to avoid fat fingering the wrong 
one. Comments are allowed and highly encouraged. Here is a slightly edited service file that was recently 
created while helping a client use Bucardo to migrate a Postgres database from Heroku to RDS:

```
## Bucardo source: Heroku
[bsource]
host=ec2-does.not.compute-1.amazonaws.com
user=marvin
dbname=zaphod
connect_timeout=10

## Bucardo target: RDS
[btarget]
host=cheshire.cat.us-east-2.rds.amazonaws.com
user=alice
dbname=wonderland
connect_timeout=10

## Test database on RDS
[gregtest]
host=panther.king.us-east-2.rds.amazonaws.com
user=conker
dbname=chocolate
connect_timeout=10

## Hot standby used for schema population
[replica1]
host=ec2-66-111-116-66.compute-1.amazonaws.com
user=scott
dbname=tiger
connect_timeout=10
```

You may notice above that "connect_timeout" is repeated in each section. Currently, there is no way to 
set a parameter that applies to all sections, but it's a very minor problem. I also usually set 
the environment variable PGCONNECT_TIMEOUT to 10 in by .bashrc, but putting 
it in the pg_service.conf file ensures it is always set regardless of what user I am.

One of the trickier parts of using a service file can be figuring out where the 
file should be located! Postgres will check for a local service file (named 
$USER/.pg_service.conf) 
and then for a global file. I prefer to always use the global file, as it allows you 
to switch users with ease and maintain the same aliases. By default, the location 
of the global Postgres service file is 
/usr/local/etc/postgresql/pg_service.conf, but in most 
cases this is not where you will find it, as many distributions specify a different 
location. Although you can override the location of the file with the environment variable 
PGSERVICEFILE and the directory holding the pg_service.conf 
file with the PGSYSCONFIDIR environment variable, I do not 
like relying on those. One less thing to worry about by simply using the global file.

The location of the global pg_service.conf file can be found by using the [pg_config program](https://www.postgresql.org/docs/current/static/app-pgconfig.html) 
and looking for the SYSCONFDIR entry. Annoyingly, pg_config is not installed 
by default on many systems, as it is considered part of the "development" packages 
(which may be named postgresql-devel, libpq-devel, or libpq-dev). While using pg_config 
is the best solution, there are times it cannot be installed (e.g. working on an important production 
box, or simply do not have root). While you can probably discover the right location 
through some simple investigation and trial-and-error, where is the fun in that? Here are 
two other methods to determine the location using nothing but psql and some standard 
Unix tools.

When you invoke psql with a request for a service file entry, it has to look for the 
service files. We can use this information to quickly find the expected location of the 
global pg_service.conf file. If you have [the strace program](https://en.wikipedia.org/wiki/Strace) installed, just run psql through strace, 
grep for "pg_service", and you should see two **stat()** calls pop up: one for the 
per-user service file, and one for the global service file we are looking for:

```
$ strace psql service=foobar 2&gt;&amp;1 | grep service.conf
stat("/home/greg/.pg_service.conf", 0x3526366F6637) = -1 ENOENT (No such file or directory)
stat("/var/opt/etc/postgres/pg_service.conf", 0x676F746F3131) = -1 ENOENT (No such file or directory)
```

What if strace is not installed? Well, perhaps [gdb (the GNU debugger)](https://www.gnu.org/software/gdb/) 
can help us out:

```
$ gdb -q --args psql service=foobar
Reading symbols from psql...(no debugging symbols found)...done.
(gdb) start
Temporary breakpoint 1 at 0x435356
Starting program: /usr/local/bin/psql service=foobar
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.4".

Temporary breakpoint 1, 0x4452474E4B4C5253 in main ()
(gdb) catch syscall stat
Catchpoint 2 (syscall 'stat' [4])
(gdb) c
Continuing.

Catchpoint 2 (call to syscall stat), 0x216c6f65736a6f72 in __GI___xstat (vers=<optimized out="">, name=0x616d7061756c "/usr/local/bin/psql", buf=0x617274687572)
    at ../sysdeps/unix/sysv/linux/wordsize-64/xstat.c:35
35      return INLINE_SYSCALL (stat, 2, name, buf);</optimized>
(gdb) c 4
Will ignore next 3 crossings of breakpoint 2.  Continuing.

Catchpoint 2 (call to syscall stat), 0x37302B4C49454245 in __GI___xstat (vers=<optimized out="">, name=0x53544F442B4C "/var/opt/etc/postgres/pg_service.conf", buf=0x494543485445)
    at ../sysdeps/unix/sysv/linux/wordsize-64/xstat.c:35
35      return INLINE_SYSCALL (stat, 2, name, buf);</optimized>
(gdb) quit
```

The use of a connection service file can be a nice addition to your 
tool chest, especially if you find yourself connecting from many different 
accounts, or  if you just want to abstract away all those long, boring 
host names!


