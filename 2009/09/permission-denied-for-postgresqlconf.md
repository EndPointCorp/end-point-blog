---
author: Greg Sabino Mullane
title: Permission denied for postgresql.conf
github_issue_number: 202
tags:
- database
- postgres
- security
date: 2009-09-21
---

I recently saw a problem in which Postgres would not startup when called via the standard 'service’ script, /etc/init.d/postgresql. This was on a normal Linux box,   Postgres was installed via yum, and the startup script had not been altered at all. However, running this as root:

```bash
 service postgresql start
```

...simply gave a "**FAILED**".

Looking into the script showed that output from the startup attempt should be going to /var/lib/pgsql/pgstartup.log. Tailing that file showed this message:

```plain
  postmaster cannot access the server configuration file
  "/var/lib/pgsql/data/postgresql.conf": Permission denied
```


However, the postgres user *can* see this file, as evidenced by an su to the account and viewing the file. What’s going on? Well, anytime you see something odd when using Linux, especially if permissions are involved, you should suspect [SELinux](http://fedoraproject.org/wiki/SELinux/FAQ). The first thing to check is if SELinux is running, and in what mode:

```plain
# sestatus

SELinux status:                 enabled
SELinuxfs mount:                /selinux
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 21
Policy from config file:        targeted
```


Yes, it is running and most importantly, in 'enforcing’ mode. SELinux logs to /var/log/audit/ by default on most distros, although some older ones may log directly to /var/log/messages. In this case, I quickly found the problem in the logs:

```plain
# grep postgres /var/log/audit/audit.log | grep denied | tail -1

type=AVC msg=audit(1234567890.334:432): avc:  denied  { read } for
pid=1234 comm="postmaster" name="pgsql" dev=newpgdisk ino=403123
scontext=user_u:system_r:postgresql_t:s0
tcontext=system_u:object_r:var_lib_t:s0 tclass=lnk_file
```

Looks like SELinux did not like a symlink, and sure enough:

```bash
# ls -ld /var/lib/pgsql /var/lib/pgsql/data /var/lib/pgsql/data/postgresql.conf

lrwxrwxrwx. 1 postgres postgres 18 1999-12-31 23:55 /var/lib/pgsql -> /mnt/newpgdisk
drwx------. 2 postgres postgres  4096 1999-12-31 23:56 /var/lib/pgsql/data
-rw-------. 1 postgres postgres 16816 1999-12-31 23:57 /var/lib/pgsql
/data/postgresql.conf
```

Here we see that although the postgres user owns the symlink, owns the data directory at /var/lib/pgsql/data, and owns the file in question, /var/lib/pgsql/data/postgresql.conf, the conf file is no longer really on /var/lib/pgsql, but is on /mnt/newpgdisk. SELinux did not like the fact that the postmaster process was trying to read across that symlink.

Now that we know SELinux is the problem, what can we do about it? There are four possible solutions at this point to get Postgres working again:

First, we can simply edit the PGDATA assignment within the /etc/init.d/postgresql file to point to the actual data dir, and bypass the symlink. In this case, we’d change the line as follows:

```plain
#PGDATA=/var/lib/pgsql/data
PGDATA=/mnt/newpgdisk/data
```

The second solution is to simply turn SELinux off. Unless you are specifically using it for something, this is the quickest and easiest solution.

The third solution is to change the SELinux mode. Switching from "enforcing" to "permissive" will keep SELinux on, but rather than denying access, it will log the attempt and still allow it to proceed. This mode is a good way to debug things while you attempt to put in new enforcement rules or change existing ones.

The fourth solution is the most correct one, but also the most difficult. That of course is to carve out an SELinux exception for the new symlink. If you move things around again, you’ll need to tweak the rules again, or course.
