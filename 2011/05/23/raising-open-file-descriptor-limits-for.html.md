---
author: Jon Jensen
gh_issue_number: 457
tags: hosting, redhat
title: Raising open file descriptor limits for Dovecot and nginx
---



Recently we've needed to increase some limits in two excellent open-source servers: [Dovecot](http://www.dovecot.org/), for IMAP and POP email service, and [nginx](http://nginx.org/), for HTTP/HTTPS web service. These are running on different servers, both using Red Hat Enterprise Linux 5.

First, let's look at Dovecot. We have a somewhat busy mail server and as it grew busier, it occasionally hit connection limits when the server itself still has plenty of available capacity.

Raising the number of processes in Dovecot is easy. Edit /etc/dovecot.conf and change from the prior (now commented-out) limits to the new limits:

```nohighlight
#login_max_processes_count = 128
login_max_processes_count = 512
```

and later in the file:

```nohighlight
#max_mail_processes = 512
max_mail_processes = 2048
```

However, then Dovecot won't start at all due to a shortage of available file descriptors. There are various ways to change that, including munging the init scripts, changing the system defaults, etc. The most standard and non-interventive way to do so with this RHEL 5 Dovecot RPM package is to edit /etc/sysconfig/dovecot and add:

```nohighlight
ulimit -n 131072
```

That sets the shell's maximum number of open file descriptors allowed in the init script /etc/init.d/dovecot before the Dovecot daemon is run. The default ulimit -n is 1024, so we here increased it to an arbitrarily big enough number (2 * 64K) to handle the new limits and then some.

Similarly, on another server we needed to increase the number of connections allowed per nginx worker process from the default 1024 for a very high-capacity HTTP caching proxy server.

We edited /etc/nginx/nginx.conf and changed the events block like this:

```nohighlight
events {
    worker_connections  65536;
}
```

But then nginx wouldn't start at all. The same problem and same solution applied. We edited /etc/sysconfig/nginx to add:

```nohighlight
ulimit -n 131072
```

And now nginx has enough file descriptors to start.

Changing the limits this way also has the benefit of surviving an upgrade, because /etc/sysconfig files are marked in RPM as configuration files that should have any changes preserved.


