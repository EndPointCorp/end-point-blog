---
author: Jon Jensen
gh_issue_number: 36
tags: email, openbsd
title: Switching from Sendmail to Postfix on OpenBSD
---

It's easy to pick on Sendmail, and with good reason. A poor security record, baroque configuration, slowness, painful configuration, monolithic design, and arcane configuration. Once you know Sendmail it's bearable, and long-time experts aren't always eager to give it up, but I wouldn't recommend anyone deploy it for a serious mail server these days. But for a send-only mail daemon or a private, internal mail server, it works fine. Since it's the default mailer for OpenBSD, and I haven't been using OpenBSD as a heavy-traffic mail server, I've usually just left Sendmail in place.

A few years ago some of our clients' internal mail servers running Sendmail were getting heavy amounts of automated output from cron jobs, batch job output, transaction notifications, etc., and they bogged down and sometimes even stopped working entirely under the load. It wasn't *that* much email, though -- the machines should've been able to handle it.

After trying to tune Sendmail to be more tolerant of heavy load and having little success, I finally switched to Postfix (which we had long used elsewhere) and the CPU load immediately dropped from 30+ down to below 1, and mail delivery worked without interruption during busy times.

If I'd known how easy it is to switch OpenBSD from Sendmail to Postfix, I would've done it long ago. I wrongly figured it'd be hard since Sendmail is part of the base system, and none of that seemed very pluggable without hacking on things. I found out it was easy only by finally just trying it myself, following the very simple instructions, and having no trouble. I did this first on OpenBSD 3.9 and now again on OpenBSD 4.3, and the process was the same.

First, pick an [OpenBSD mirror](http://www.openbsd.org/ftp.html), and navigate to the appropriate packages directory. Then set up your environment for easy pkg_add usage. For example:

```
export PKG_PATH=ftp://ftp.openbsd.org/pub/OpenBSD/4.3/packages/i386
```

There are several varying OpenBSD Postfix packages, offering support for lookups in LDAP, MySQL, Postgres, or SASL, or a simple build without any of those dependencies:

```
# pkg_add postfix
Ambiguous: postfix could be postfix-2.5.1p0 postfix-2.5.1p0-ldap postfix-2.5.1p0-mysql postfix-2.5.1p0-pgsql postfix-2.5.1p0-sasl2 postfix-2.6.20080216p1 postfix-2.6.20080216p1-ldap postfix-2.6.20080216p1-mysql postfix-2.6.20080216p1-pgsql postfix-2.6.20080216p1-sasl2
```

We'll use the simple build:

```
pkg_add postfix-2.6.20080216p1
```

The output from the package installation tells you most of what you need to know, but I'll break it down here with a little more detail.

Run crontab -e as root and comment out this Sendmail job:

```
# sendmail clientmqueue runner
#*/30    *       *       *       *       /usr/sbin/sendmail -L sm-msp-queue -Ac -q
```

The sendmail compatibility is implemented by a wrapper script similar to how Debian's alternatives system does it (and which Red Hat borrowed as well). In OpenBSD, the wrapper is a binary that uses the configuration in /etc/mailer.conf to decide what to actually run, as opposed to using symlinks as the alternatives system does. You can see this here:

```
# ls -lFa /usr/sbin/sendmail /usr/bin/newaliases /usr/bin/mailq
lrwxr-xr-x  1 root  wheel  21 Aug  1 14:50 /usr/bin/mailq@ -> /usr/sbin/mailwrapper
lrwxr-xr-x  1 root  wheel  21 Aug  1 14:50 /usr/bin/newaliases@ -> /usr/sbin/mailwrapper
lrwxr-xr-x  1 root  wheel  21 Aug  1 14:51 /usr/sbin/sendmail@ -> /usr/sbin/mailwrapper
```

To make the switch to Postfix, run:

```
/usr/local/sbin/postfix-enable
```

Now you're ready to configure /etc/postfix/main.cf as needed. The defaults should be fine for a server sending outgoing mail only, though if you followed the OpenBSD installer's instructions to use only the short name for the hostname, you need to either set the mydomain parameter manually in main.cf, or else edit /etc/myname to use a fully-qualified domain name instead of the hostname only (and update immediately with the hostname command as well). I do the latter and haven't had any trouble with it before.

Stop Sendmail and start Postfix the same way the boot script will do it:

```
pkill sendmail
/usr/sbin/sendmail -bd
```

Send a test message and make sure you receive it:

```
echo "A special test message" | mail -s testing <em>your_account@the.domain</em>
```

Note that if you send your message to somewhere offsite, spam filters may reject it if your sending server doesn't have a real hostname, a reverse DNS pointer for the IP address, etc. You can just send locally to avoid that, but of course you won't be able to send mail offsite until you deal with those problems.

Add these settings to /etc/rc.conf.local so Postfix will start on boot:

```
sendmail_flags="-bd"
syslogd_flags="-a /var/spool/postfix/dev/log"
```

Now reboot to make sure everything comes up correctly on its own and to get syslogd going right. Send yourself another test message, and you can move on!

Many thanks to the [Postfix](http://www.postfix.org/) developers for the excellent mail server software and to the OpenBSD developers for a nice easy way to switch the system mail daemon.
