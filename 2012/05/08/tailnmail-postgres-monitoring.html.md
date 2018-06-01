---
author: Greg Sabino Mullane
gh_issue_number: 610
tags: monitoring, postgres
title: Monitoring many Postgres files at once with tail_n_mail
---



<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/05/08/tailnmail-postgres-monitoring/image-0-big.png" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="258" src="/blog/2012/05/08/tailnmail-postgres-monitoring/image-0.png" width="250"/></a></div>

*This post discusses version 1.25.0 of tail_n_mail, which can be downloaded at [https://bucardo.org/tail_n_mail/](https://bucardo.org/tail_n_mail/)*

One of our clients recently had one of their Postgres servers 
crash. In technical terms, it issued a 
[PANIC](https://www.postgresql.org/docs/current/static/runtime-config-logging.html#RUNTIME-CONFIG-SEVERITY-LEVELS) because it tried to commit a transaction that had already been committed. We 
are using **tail_n_mail** for this client, and while we got notified 
six ways to Sunday about the server being down (from Nagios, 
tail_n_mail, and other systems), I was curious as to why the actual PANIC had 
not gotten picked up by tail_n_mail and mailed out to us.

The tail_n_mail program at its simplest is a Perl script that 
greps through log files, finds items of interest, and mails them out. 
It does quite a bit more than that, of course, including normalizing 
SQL, figuring out which log files to scan, and analyzing the data 
on the fly. This particular client of ours consolidates all of their logs to some central 
logging boxes via rsyslog. For the host in question that issued the PANIC, we had two 
tail_n_mail config files that looked like this:

```nohighlight
## Config file for the tail_n_mail program
## This file is automatically updated
## Last updated: Fri Apr 27 18:00:01 2012
MAILSUBJECT: Groucho fatals: NUMBER

INHERIT: tail_n_mail.fatals.global.txt

FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-err.log
LASTFILE: /var/log/2012/groucho/04/27/18/pgsql-err.log
OFFSET: 10199
```

```nohighlight
## Config file for the tail_n_mail program
## This file is automatically updated
## Last updated: Fri Apr 27 18:00:01 2012
MAILSUBJECT: Groucho fatals: NUMBER

INHERIT: tail_n_mail.fatals.global.txt

FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-warning.log
LASTFILE: /var/log/2012/groucho/04/27/18/pgsql-warning.log
OFFSET: 7145

```

The reason for two files was that rsyslog was splitting the 
incoming Postgres logs into multiple files. Which is normally a 
very handy thing, because the main file, **pgsql-info.log**, 
is quite large, and it’s nice to have the mundane things filtered 
out for us already. Because rsyslog also splits things based on the timestamp, 
we don’t give it an exact file name, but use a POSIX template 
instead, e.g. /var/log/apps/%Y/groucho/%m/%d/%H/pgsql-warning.log. 
By doing this, tail_n_mail knows where to find the latest file. 
It also uses the LASTFILE and OFFSET to know exactly where it stopped 
last time, and then walks through all files from LASTFILE until 
the current one.

So why did we miss the PANIC? Because it was in a heretofore unseen 
and untracked log file known as **pgsql-crit.log**. (Which goes 
to show how rarely Postgres crashes: this was the first time in well over 
700,000 log files generated that a PANIC had occurred!) At this point, the 
solution was to either create yet another set of config files for each host 
to watch for and parse any pgsql-crit.log files, or to 
give tail_n_mail some more brains and allow it to handle multiple 
FILE entries in a single config file. Obviously, I chose the latter.

After some period of coding, testing, debugging, and caffeine consumption, 
a new tail_n_mail was ready. This one (version 1.25.0) allows multiple values of the FILE parameter 
inside of a single config. Thus, for the above, I was able to combine everything into a single 
tail_n_mail config file like so:

```nohighlight
MAILSUBJECT: Groucho fatals: NUMBER

INHERIT: tail_n_mail.fatals.global.txt

FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-warning.log
FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-err.log
FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-crit.log
```

The INHERIT file is a way of keeping common config items in a 
single file: in this case, groucho and a bunch of other similar 
hosts all use it. It contains the rules on what tail_n_mail 
should care about, and looks similar to this:

```nohighlight
## Global behavior for all "fatals" configs
EMAIL: acme-alerts@endpoint.com
FROM: postgres@endpoint.com
FIND_LINE_NUMBER: 0
STATEMENT_SIZE: 3000
INCLUDE: FATAL:
INCLUDE: PANIC:
INCLUDE: ERROR:

## Client specific exceptions:
EXCLUDE: ERROR:  Anvils cannot be delivered via USPS
EXCLUDE: ERROR:  Jetpack fuel quantity missing
EXCLUDE: ERROR:  Iron Carrots and Giant Magnets must go to different addresses
EXCLUDE: ERROR:  Rocket Powered Rollerskates no longer available

## Postgres excceptions:
EXCLUDE: ERROR:  aggregates not allowed in WHERE clause
EXCLUDE: ERROR:  negative substring length not allowed
EXCLUDE: ERROR:  there is no escaped character
EXCLUDE: ERROR:  operator is not unique
EXCLUDE: ERROR:  cannot insert multiple commands into a prepared statement
EXCLUDE: ERROR:  value "\d+" is out of range for type integer
EXCLUDE: ERROR:  could not serialize access due to concurrent update
```

Thus, we only have one file per host to worry about, in addition to a common 
shared file across all hosts. So now tail_n_mail can handle multiple files over a time 
dimension (by walking forward from LASTFILE to the present), as well as over a vertical 
dimension (by forcing together the files split by rsyslog). However, there is no reason we 
cannot handle multiple files over a horizontal dimension as well. In other words, 
putting multiple hosts into a single file. In this client’s case, there were other 
hosts very similar to “groucho” that had files we wanted to monitor. Thus, the 
config file was changed to look like this:

```nohighlight
MAILSUBJECT: Acme fatals: NUMBER

INHERIT: tail_n_mail.fatals.global.txt

FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-warning.log
FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-err.log
FILE: /var/log/%Y/groucho/%m/%d/%H/pgsql-crit.log

FILE: /var/log/%Y/dawson/%m/%d/%H/pgsql-warning.log
FILE: /var/log/%Y/dawson/%m/%d/%H/pgsql-err.log
FILE: /var/log/%Y/dawson/%m/%d/%H/pgsql-crit.log

FILE: /var/log/%Y/cosby/%m/%d/%H/pgsql-warning.log
FILE: /var/log/%Y/cosby/%m/%d/%H/pgsql-err.log
FILE: /var/log/%Y/cosby/%m/%d/%H/pgsql-crit.log
```

We’ve just whittled nine config files down to a single one. Of course, the config file cannot stay like that, as the LASTFILE and OFFSET entries need to be applied to specific files. Thus, when tail_n_mail 
does its first rewrite of the config file, it will assign numbers to 
each FILE, and the file will then look something like this:

```nohighlight
FILE1: /var/log/%Y/groucho/%m/%d/%H/pgsql-warning.log
LASTFILE1: /var/log/2012/groucho/04/27/18/pgsql-warning.log
OFFSET1: 100

FILE2: /var/log/%Y/groucho/%m/%d/%H/pgsql-err.log
LASTFILE2: /var/log/2012/groucho/04/27/18/pgsql-err.log
OFFSET2: 2531

FILE3: /var/log/%Y/groucho/%m/%d/%H/pgsql-crit.log

FILE4: /var/log/%Y/dawson/%m/%d/%H/pgsql-warning.log
LASTFILE4: /var/log/2012/dawson/04/27/18/pgsql-warning.log
OFFSET4: 42

# etc.
```

By using this technique, we were able to reduce a slew of 
config files (the actual number was around 60), and their crontab entries, 
into a single config file and a single cron call. We also have a daily “error” report 
that mails a summary of all ERROR/FATAL calls in the last 24 hours. 
These were consolidated into a single email, rather than the half 
dozen that appeared before.

While tail_n_mail has a lot of built-in intelligence to handle 
Postgres logs, it is ultimately regex-based and can be used on 
any files which you want to track and receive alerts when certain 
items appear inside of them, so feel free to use it for more than just Postgres!


