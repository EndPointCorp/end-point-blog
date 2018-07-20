---
author: Greg Sabino Mullane
gh_issue_number: 244
tags: database, monitoring, open-source, perl, postgres
title: Monitoring Postgres log files with tail_n_mail
---



We’ve just publically released a useful script named tail_n_mail that keeps an eye on your Postgres log files and mails interesting lines to one or more addresses. It’s released under a BSD license and is available at:

[https://bucardo.org/tail_n_mail/](https://bucardo.org/tail_n_mail/)

Complete documentation is available at the above, but here’s a quick overview. First, it figures out the current log file (it actually works for any file, but it’s primarily aimed at Postgres log files). Then, it finds any lines that match based on the INCLUDE lines in the config file, and finally removes any that do not match the EXCLUDE lines in the config files. It summarizes the results and sends a report to one or more emails.

To use, just specify a a configuration file as the first argument. Typically, the script is run from cron, either for instant reports (e.g. FATAL or PANIC errors), or for daily reports (e.g. all interesting ERRORs in the last 24 hours).

Here’s what a typical config file looks like. In this example, we’ll look for any FATAL or PANIC notices from Postgres, while ignoring a few known errors 
that we don’t care about.

```nohighlight
 ## Config file for the tail_n_mail.pl program
 ## This file is automatically updated
 EMAIL: greg@endpoint.com, postgres@endpoint.com
 
 FILE: /var/log/pg_log/postgres-%Y-%m-%d.log
 INCLUDE: FATAL:  
 INCLUDE: PANIC:  
 EXCLUDE: database ".+" does not exist
 EXCLUDE: database "template0" is not currently accepting connections
 MAILSUBJECT: HOST Postgres fatal errors (FILE)

```

It should be setup to run often from cron:

```bash
  */5 * * * * perl bin/tail_n_mail.pl bin/tnm/tnm.fatals.config
```

The resulting mail message will look like this:

```nohighlight
Matches from /var/log/pg_log/postgres-2010-01-01.log: 42
Date: Fri Jan  1 10:34:00 2010
Host: pollo

[1] Between lines 123005 and 147976, occurs 39 times.
First:  Jan  1 00:00:01 rojogrande postgres[4306]
Last:   Jan  1 10:30:00 rojogrande postgres[16854]
Statement:  user=root,db=rojogrande FATAL:  password authentication failed for user "root"

[2] Between lines 147999 and 148213, occurs 2 times.
First:  Jan  1 10:31:01 rojogrande postgres[3561]
Last:   Jan  1 10:31:10 rojogrande postgres[15312]
Statement: FATAL  main: write to worker pipe failed -(9) Bad file descriptor

[3] (from line 152341)
PANIC:  could not locate a valid checkpoint record
```

There may be false positives, but it’s not designed to be a complete log parser. There are some other command line flags and options for the config file: see the documentation for the full list. This script has been watching over a number of production systems for a while now, but improvements, ideas, and patches are always welcome. It’s tracked via git; you can clone it by running:

```bash
  git clone git://bucardo.org/tail_n_mail.git
```

Bugs and feature requests can be filed and tracked at:

[https://github.com/bucardo/bucardo/issues](https://github.com/bucardo/bucardo/issues)


