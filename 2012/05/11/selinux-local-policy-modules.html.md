---
author: Jon Jensen
gh_issue_number: 613
tags: hosting, redhat, security, selinux, sysadmin
title: SELinux Local Policy Modules
---

If you don't want to use SELinux, fair enough. But I find many system administrators would like to use it but get flustered at the first problem it causes, and disable it. That's unfortunate, because often it's simple to customize SELinux policy by creating what's known as a local policy module. That way you allow the actions you need while retaining the added security SELinux brings to the system as a whole.

A few years ago my co-worker [Adam Vollrath](/team/adam_vollrath) wrote an [article on this same subject](/blog/2010/10/13/selinux-httpd-modwsgi-26-rhel-centos-5) for Red Hat Enterprise Linux (RHEL) 5, and went into more detail on SELinux file contexts, booleans, etc. I recently went through the process of building an SELinux local policy module on RHEL 6 and RHEL 7 mail servers and found a few differences and want to document some of the details here. This applies to RHEL 5, RHEL 6, and RHEL 7, and near relatives CentOS, Scientific Linux, et al.

## When under pressure …

If you're tempted to disable SELinux, consider leaving it on, but in "permissive" mode. That will leave it running but stop it from blocking disallowed actions until you have time to deal with them properly. It's as simple as:

```nohighlight
setenforce 0
```

That will last until you reboot, unless otherwise changed manually. You can edit /etc/sysconfig/selinux and set:

```nohighlight
SELINUX=permissive
```

To keep permissive mode even after a reboot. To see what mode SELinux is in, you can do either of:

```nohighlight
getenforce
# or
cat /selinux/enforce
```

## Prerequisites

First make sure you have installed:

```nohighlight
yum install policycoreutils
yum install policycoreutils-python   # also needed on RHEL 6
yum install policycoreutils-devel    # also needed on RHEL 7
```

You must have SELinux enabled, though enforcing isn't required; permissive mode is fine. If it's not enabled, edit /etc/sysconfig/selinux for permissive mode and reboot.

You'll need an up-to-date file /var/lib/sepolgen/interface_info, which is created by /usr/sbin/sepolgen-ifgen for the specific machine you're running it on. That should be done automatically, but be aware of it in case it somehow got stale. If you run into any unexpected problems, make sure the timestamp on interface_info is recent, or just regenerate it, which is harmless.

## Making the policy module

Choose a unique name for your local policy module. It's better to use something specific to your organization, or the hostname, rather than just "postfix" or "dovecot" or something similar which may conflict with existing vendor policy modules.

Run semodule -l to list the existing modules. For this example I'll use "epmail".

Create a directory for your new policy module:

```nohighlight
mkdir -p /root/local-policy-modules/epmail
cd /root/local-policy-modules/epmail
```

Copy relevant error messages verbatim from /var/log/audit/audit.log to a new file. Here for example are two denials of a script called by Postfix as a transport agent, which needed to connect to PostgreSQL locally:

```nohighlight
type=AVC msg=audit(1335581974.308:69047): avc:  denied  { write } for  pid=14649 comm=F9616121202873696E676C65206D65 name=".s.PGSQL.5432" dev=sda2 ino=79924 scontext=system_u:system_r:postfix_pipe_t:s0 tcontext=system_u:object_r:postgresql_tmp_t:s0 tclass=sock_file
type=AVC msg=audit(1335581974.308:69047): avc:  denied  { connectto } for  pid=14649 comm=F9616121202873696E676C65206D65 path="/tmp/.s.PGSQL.5432" scontext=system_u:system_r:postfix_pipe_t:s0 tcontext=system_u:system_r:postgresql_t:s0 tclass=unix_stream_socket
```

In the logs you want to look for "AVC", which stands for Access Vector Cache and is how SELinux logs denials. You can grab all the recent denials with:

```nohighlight
grep ^type=AVC /var/log/audit/audit.log > epmail.log
```

and then filter it manually to contain just what you need.

You can see a usually more informative explanation of each error by piping it into audit2why:

```nohighlight
audit2why < epmail.log
```

Now you're ready to create your policy module:

```nohighlight
audit2allow -m epmail < epmail.log > epmail.te
checkmodule -M -m -o epmail.mod epmail.te
semodule_package -o epmail.pp -m epmail.mod
semodule -i epmail.pp
```

That's a somewhat longwinded way to do things, but that's how I learned it from my co-worker Kiel Christofferson, and it's easy once put into a script. See the man page of each program for more details on what that step is doing, and various options.

A more streamlined way that has audit2allow performing the functions of checkmodule and semodule_package is:

```nohighlight
audit2allow -M $module_name -R -i epmail.log
semodule -i epmail.pp
```

## Wrap-up

You will of course need to keep an eye on the audit log to look for any more AVC denials, as you exercise all the functions of the system. For a production system it may be best to leave SELinux permissive for a few weeks, and once you're confident you've allowed all the actions needed, you can switch it to enforcing mode.

Finally, I have not normally had to do this, but if you need to force reload the SELinux policy on the server, you can do it with:

```nohighlight
semodule -R
```

Have fun with the extra security SELinux offers!
