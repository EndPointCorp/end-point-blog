---
author: Jon Jensen
title: cPanel Exim false positive failure & restart fix
github_issue_number: 673
tags:
- hosting
- redhat
- sysadmin
date: 2012-07-24
---

I’m not a big fan of add-on graphical control panels for Linux such as cPanel, Webmin, Ensim, etc. They deviate from the distributor’s standard packages and locations for files, often simultaneously tightening security in various ways and weakening security practically by making several more remotely accessible administration logins.

On one of the few servers we maintain that has [cPanel](https://cpanel.net/) on it, today we did a routine Red Hat Network update and reboot to load the latest RHEL 5 kernel, and all seemed to go well.

However, within a few minutes we started getting emailed reports from the cPanel service monitor saying that the Exim mail server had failed and been restarted. These emails began coming in at roughly 5-minute intervals:

```
Date: Tue, 24 Jul 2012 14:21:05 -0400
From: cPanel ChkServd Service Monitor <cpanel@[SNIP]>
To: [SNIP]
Subject: exim on [SNIP] status: failed

exim failed @ Tue Jul 24 14:21:04 2012. A restart was attempted automagically.

Service Check Method:  [socket connect]

Reason: TCP Transaction Log:
<< 220-[SNIP] ESMTP Exim 4.77 #2 Tue, 24 Jul 2012 14:21:04 -0400
<<
<<
>> EHLO localhost
<< 250-[SNIP] Hello localhost.localdomain [127.0.0.1]
<<
<<
<<
<<
<<
>> AUTH PLAIN
[SNIP]=
<< 535 Incorrect authentication data
exim: ** [535 Incorrect authentication data != 2]
: Died at /usr/local/cpanel/Cpanel/TailWatch/ChkServd.pm line 689, <$socket_scc> line 10.

Number of Restart Attempts: 1

Startup Log: Starting exim: [  OK  ]
```

And the relevant entry in /var/log/exim_mainlog was:

```
2012-07-24 14:08:05 fixed_plain authenticator failed for localhost.localdomain (localhost) [127.0.0.1]:48454: 535 Incorrect authentication data (set_id=__cpane
l__service__auth__exim__[SNIP])
```

I wasn’t able to find a way to fix this in any reasonable amount of time, so I opened a trouble ticket with cPanel support and they had asked for server access, logged in, and fixed the problem within a little over an hour. It was about as painless as tech support ever gets, so kudos to cPanel for that!

The solution was to run this as root:

```
/scripts/upcp --force
```

Which resyncs cPanel so that chkservd reports Exim as up and the unwanted service restarts no longer happen.

Here’s to responsive tech support.
