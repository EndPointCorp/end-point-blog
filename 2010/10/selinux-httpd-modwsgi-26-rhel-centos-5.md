---
author: Adam Vollrath
title: Red Hat SELinux policy for mod_wsgi
github_issue_number: 366
tags:
- django
- hosting
- python
- redhat
- security
- selinux
date: 2010-10-13
---



Using SELinux, you can safely grant a process only the permissions it needs to perform its function, and no more.  Linux distributions provide policies to enforce these limits on most software they package, but many aren’t covered. We’ve made allowances for [mod_wsgi](https://code.google.com/archive/p/modwsgi/) on RHEL and CentOS 5 by extending Apache httpd’s SELinux policy.

It seems the SELinux policy for Apache httpd is twice as large as any other package’s.  The folks at Red Hat have put a lot of work into making sure that attackers who manage to exploit httpd can’t break out to the rest of your system, while still allowing the flexibility to serve most applications.  Consult the [httpd_selinux man page](https://linux.die.net/man/8/httpd_selinux) if messages in audit.log coincide with your error.

###  File Contexts 

If you’ve created files and/or directories in /etc/httpd, make sure they have the proper file contexts so the daemon can read them:

```bash
  # restorecon -vR /etc/httpd
```

httpd can only serve files with an explicitly allowed file context.  Configure the context of files and directories within your production code base using the semanage command:

```bash
  # semanage fcontext --add --ftype -- --type httpd_sys_content_t "/home/projectname/live(/.*)?"
  # semanage fcontext --add --ftype -d --type httpd_sys_content_t "/home/projectname/live(/.*)?"
  # restorecon -vR /home/projectname/live
```

View file contexts with ls -Z.  Changes should be generally accomplished with semanage and restorecon -vR.

###  Booleans 

The httpd policy provides several boolean options for easy run-time configuration:

- **httpd_can_network_connect** — Allows httpd to make network connections, including the local ones you’ll be making to a database
- **httpd_enable_homedirs** — Allows httpd to access /home/

Booleans are persistently set using the setsebool command with the -P flag:

```bash
  # setsebool -P httpd_can_network_connect on
```

###  WSGI Socket 

When running in daemon mode, httpd and the mod_wsgi daemon communicate via a UNIX socket file. This should usually have a context of httpd_var_run_t. The standard Red Hat SELinux policy includes an entry for /var/run/wsgi.* to use this context, so it makes sense to put the socket there using the WSGISocketPrefix directive within your httpd configuration:

```bash
  WSGISocketPrefix run/wsgi
```

(Note that run/wsgi translates to /etc/httpd/run/wsgi which is symlinked to /var/run/wsgi.)

If socket communication fails, httpd returns a 503 “Temporarily Unavailable” error response.

###  SELinux Policy Module 

In the course of our testing SELinux denials like the following appeared:

```nohighlight
  host=example.com type=AVC msg=audit(1262803154.315:1851): avc:  denied  { execmem } for  pid=5337 comm="httpd" scontext=root:system_r:httpd_t:s0 tcontext=root:system_r:httpd_t:s0 tclass=process
```

Unusual behavior like this is usually best allowed by [creating application-specific SELinux policy modules](https://fedoraproject.org/wiki/SELinux/LoadableModules/Audit2allow). If you cannot resolve these AVC errors by manipulating file contexts or booleans, collect all the errors into a single file and feed that into the audit2allow utility:

```bash
  # yum install policycoreutils
  # mkdir ~/tmp  # if this doesn't exist already
  # audit2allow --module wsgi < ~/tmp/pile_of_auditd_output > ~/tmp/wsgi.te
```

This will output source for a new policy module. You might review the .te file before compiling. Ours looks like this:

```nohighlight
module wsgi 1.0;

require {
      type httpd_t;
      class process execmem;
}

#============= httpd_t ==============
allow httpd_t self:process execmem;
```

Compile this source into a new policy module and package it:

```bash
  # checkmodule -M -m -o ~/tmp/wsgi.mod ~/tmp/wsgi.te
  # semodule_package --outfile ~/tmp/wsgi.pp --module ~/tmp/wsgi.mod
```

Once created, the module may be installed permanently into any compatible system’s SELinux configuration:

```bash
  # semodule --install ~/tmp/wsgi.pp
```

There’s plenty of room for improvement here. The file contexts we assigned with semanage should be defined in a .fc source file and included within the policy module. And creating a new context just for the WSGI daemon to transition into would restrict it further, allowing only a subset of Apache httpd’s abilities. Writing your own policy like this allows you much finer tuning of your processes’ limits, while allowing their needed functionality.


