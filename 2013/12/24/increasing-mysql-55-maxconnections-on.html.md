---
author: Jon Jensen
gh_issue_number: 906
tags: database, mysql, redhat
title: Increasing MySQL 5.5 max_connections on RHEL 5
---



Busy database-backed websites often hit scalability limits in the database first. In tuning MySQL, one of the first things to look at is the max_connections parameter, which is often too low. (Of course another thing to look at is appropriate fragment caching in your app server, HTTP object caching in your web server, and a CDN in front of it all.)

When using MySQL 5.5 from Oracle's RPMs through cPanel (MySQL55-server-5.5.32-1.cp1136) on RHEL 5.10 x86_64, there is an interesting problem if you try to increase the max_connections setting beyond 214 in /etc/my.cnf. It will silently be ignored, and the limit remains 214:

```nohighlight
mysql> show variables like 'max_connections';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 214   |
+-----------------+-------+
1 row in set (0.00 sec)
```

The problem is that the maximum number of open files allowed is too small, by default 1024, to increase max_connections beyond 214.

There are plenty of online guides that explain how to handle this, including increasing the kernel fs.file-max setting, which may be necessary by editing /etc/sysctl.conf, in this example to double the default:

```nohighlight
fs.file-max = 2459688
```

Then run sysctl -p to make the change take immediate effect. (It'll remain after reboot too.)

There are also many guides that say you need to change /etc/security/limits.conf along these lines:

```nohighlight
mysql           soft    nofile         4096
mysql           hard    nofile         4096
```

However, the /etc/security/limits.conf change does not actually work when mysqld is started via the init script in /etc/init.d/mysql or via service mysql restart.

With standard Red Hat mysql-server (5.1) package that provides /etc/init.d/mysqld (not /etc/init.d/mysql as the Oracle and Percona versions do), you could create a file /etc/sysconfig/mysqld containing ulimit -n 4096 and that setting will take effect for each restart of the MySQL daemon.

But the ulimit -n setting hacked into the init script or put into /etc/sysconfig/mysqld isn't really needed after all, because you can simply set open_files_limit in /etc/my.cnf:

```nohighlight
[mysqld]
open_files_limit = 8192
max_connections = 1000
# etc.
```

... and mysqld_safe will increase the ulimit on its own before invoking the actual mysqld daemon.

After service mysql restart you can verify the new open file limit in the running process, like this:

```nohighlight
# cat /var/lib/mysql/*.pid
30697
# ps auxww | grep 30697
mysql    30697 97.8  9.8 6031872 1212224 pts/1 Sl   13:09   3:01 /usr/sbin/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib64/mysql/plugin --user=mysql --log-error=/var/lib/mysql/some.hostname.err --open-files-limit=8192 --pid-file=/var/lib/mysql/some.hostname.pid
# cat /proc/30697/limits
Limit                     Soft Limit           Hard Limit           Units
Max cpu time              unlimited            unlimited            seconds
Max file size             unlimited            unlimited            bytes
Max data size             unlimited            unlimited            bytes
Max stack size            10485760             unlimited            bytes
Max core file size        0                    unlimited            bytes
Max resident set          unlimited            unlimited            bytes
Max processes             96086                96086                processes
Max open files            8192                 8192                 files
Max locked memory         32768                32768                bytes
Max address space         unlimited            unlimited            bytes
Max file locks            unlimited            unlimited            locks
Max pending signals       96086                96086                signals
Max msgqueue size         819200               819200               bytes
Max nice priority         0                    0
Max realtime priority     0                    0
```

And the running MySQL server will reveal the desired max_connections setting stuck this time:

```nohighlight
mysql> show variables like 'max_connections';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 1000  |
+-----------------+-------+
1 row in set (0.00 sec)
```

The relevant code in /usr/bin/mysqld_safe is here:

```nohighlight
if test -w / -o "$USER" = "root"
then
  # ... [snip] ...
  if test -n "$open_files"
  then
    ulimit -n $open_files
  fi
fi

if test -n "$open_files"
then
  append_arg_to_args "--open-files-limit=$open_files"
fi
```

I have found that some newer versions of either MySQL55-server or cPanel or some intersection of the two has made manually specifying a higher open_files_limit in /etc/my.cnf no longer necessary, although it does not do any harm.

But in conclusion, if you find yourself hitting the mysterious max_connections = 214 limit, just add the appropriately-sized open_files_limit to the [mysqld] section of /etc/my.cnf and restart the server with service mysql restart, and your problem should be solved!


