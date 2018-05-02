---
author: Greg Sabino Mullane
gh_issue_number: 1332
tags: postgres, monitoring
title: Using tail_n_mail after hours
---

<a href="/blog/2017/10/23/using-tailnmail-after-hours/image-0-big.jpeg" imageanchor="1"><img border="0" data-original-height="313" data-original-width="500" src="/blog/2017/10/23/using-tailnmail-after-hours/image-0.jpeg"/></a>   
<small>(Photo of [Turtle Island](https://flic.kr/p/bz2Vb4) by [Edwin Poon](https://www.flickr.com/photos/edwinpoon_gz/))</small>

Someone recently asked me something about
[tail_n_mail](https://bucardo.org/tail_n_mail/), a program that watches over your log files, scans for certain patterns,
and sends out an email if matches are found. It is frequently used to watch over
Postgres logs so you can receive an automatic email alert when Bad Things start happening
to your database. The questioner wanted to know if it was possible
for tail_n_mail to change its behavior based on the time of day — would it be able
to do things differently outside of “business hours”? Although tail_n_mail cannot
do so directly, a simple solution is to use alternate configuration files — which
get swapped by cron — and the `INHERIT` keyword.

To demonstrate the solution, let’s spin up a Postgres 10 instance, route the logs to syslog,
setup tail_n_mail, and then create separate configuration files for different times of the week.
First, some setup:

```text
$ initdb --version
initdb (PostgreSQL) 10.0
$ initdb --data-checksums data
$ cat >> data/postgresql.conf << EOT
log_line_prefix=''
log_destination='syslog'
EOT
$ echo 'local0.*  /var/log/postgres.log' | sudo tee -a /etc/rsyslog.conf > /dev/null
$ sudo systemctl restart rsyslog
$ pg_ctl start -D data -l logfile
```

Grab the latest version of tail_n_mail and verify it:

```text
$ wget --no-verbose https://bucardo.org/downloads/tail_n_mail{,.asc}
2017-03-03 10:00:33 URL:https://bucardo.org/downloads/tail_n_mail [98767/98767] -> "tail_n_mail" [1]
2017-03-03 10:00:33 URL:https://bucardo.org/downloads/tail_n_mail.asc [163/163] -> "tail_n_mail.asc" [1]
FINISHED --2017-03-03 10:00:33--
Total wall clock time: 0.3s
Downloaded: 2 files, 96K in 0.1s (702 KB/s)
$ gpg --verify tail_n_mail.asc
gpg: assuming signed data in `tail_n_mail'
gpg: Signature made Sun 01 Oct 2017 11:14:07 AM EDT using DSA key ID 14964AC8
gpg: Good signature from "Greg Sabino Mullane <greg@turnstep.com>"
gpg:                 aka "Greg Sabino Mullane (End Point Corporation) <greg@endpoint.com>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 2529 DF6A B8F7 9407 E944  45B4 BC9B 9067 1496 4AC8
```

The main way to configure tail_n_mail is through its configuration file, which is always the
first argument given to the program. This file describes where the log files are, what to look
for, and a few other important items. In addition, it automatically updates itself each time
tail_n_mail is run to keep track of where the last run left of, so the next run can start at
the exact same file, and the correct place within that file. In this example, let’s
assume the DBA wants to get email for every error that pops up in the database (in practice,
this means any severity levels that are
ERROR, FATAL, or PANIC). The configuration file
would look like this:

```
$ cat > tnm.conf << EOT
FILE: /var/log/postgres.log
PGLOG: syslog
EMAIL: greg@example.com
MAILSUBJECT: HOST Postgres errors NUMBER
INCLUDE: PANIC:
INCLUDE: FATAL:
INCLUDE: ERROR:
## Okay, we don't want to get emailed on *every* error:
EXCLUDE: could not serialize access due to concurrent update
EXCLUDE: canceling statement due to user request
EOT
```

To test it out, we will generate some errors, and then run tail_n_mail from the command line.
If all goes well, it sends out an email and then rewrites the configuration file to indicate
how far along it got. The --dry-run option can be used to view the email without actually sending it.

```text
$ for i in 2 4 6 8; do psql -tc "select $i/0"; done
ERROR:  division by zero
ERROR:  division by zero
ERROR:  division by zero
ERROR:  division by zero
```

```text
$ perl tail_n_mail tnm.conf --dry-run
Subject: localhost.localdomain Postgres errors 4
Auto-Submitted: auto-generated
Precedence: bulk
X-TNM-VERSION: 1.30.0
To: greg@example.com

Date: Tue Oct  3 03:19:22 2017 EDT
Host: localhost.localdomain
Unique items: 1
Matches from /var/log/postgres.log: 4

[1] (between lines 139 and 142, occurs 4 times)
First: Oct   3 03:19:00 localhost postgres[28483]: [6-1]
Last:  Oct   3 03:19:00 localhost postgres[28495]: [6-1]
ERROR: division by zero
STATEMENT: select ?/0
-
ERROR: division by zero
STATEMENT: select 2/0

  DRYRUN: /usr/sbin/sendmail 'greg@example.com' < tnmBWaG6QA1.tnm2
```

Running it in normal mode rewrites the configuration file:

```text
$ perl tail_n_mail tnm.conf
$ cat tnm.conf
## Config file for the tail_n_mail program
## This file is automatically updated
## Last updated: Mon Oct  2 12:09:29 2017
PGLOG: syslog
EMAIL: greg@example.com
MAILSUBJECT: HOST Postgres errors NUMBER

INCLUDE: PANIC:
INCLUDE: FATAL:
INCLUDE: ERROR:
## Okay, we don't want to get emailed on *every* error:
EXCLUDE: could not serialize access due to concurrent update
EXCLUDE: canceling statement due to user request

FILE1: /var/log/postgres.log
LASTFILE1: /var/log/postgres.log
OFFSET1: 333
```

Note how the file was rewritten to include state information about the files we are tracking, but
leaves the exclusion rules and their comments in place. Tail_n_mail also attempts to “flatten”
similar queries, which is why the four division-by-zero errors all appear as “SELECT ?/0”. A
sample of one of the literal errors appears below the normalized version.

You are not limited to a single configuration file, however, as the main config file can read in
other configuration files via the INHERITS keyword. This allows you to import one or more
other configuration files. Not only does this allow different
tail_n_mail invocations to share common items to search for, but (as you will see in a bit) can solve the problem
at the top of this post: how to change what is being looked for based on the time of day.

Using INHERITS also allows us to store files in version control, without worrying about
them getting rewritten on each invocation, as we can store the ephemeral data in one
file, and the constant data in a separate, version controlled file. Let’s apply that idea to
our example:

```text
$ cat > tnm.global.conf << EOT
PGLOG: syslog
EMAIL: greg@example.com
INCLUDE: PANIC:
INCLUDE: FATAL:
INCLUDE: ERROR:
## Okay, we don't want to get emailed on *every* error:
EXCLUDE: could not serialize access due to concurrent update
EXCLUDE: canceling statement due to user request
EOT
$ git add tnm.global.conf && git commit tnm.global.conf \
  -m "Global config for tail_n_mail"
[master 2441df8] Global config for tail_n_mail
 1 file changed, 7 insertions(+)
 create mode 100644 tnm.global.conf
$ cat > tnm.conf << EOT
FILE: /var/log/postgres.log
MAILSUBJECT: HOST Postgres errors NUMBER
INHERIT: tnm.global.conf
EOT
```

After another run, we observe that the inherited file does not change:

```text
$ perl tail_n_mail tnm.conf
$ git status
On branch master
nothing to commit, working tree clean
$ cat tnm.conf

## Config file for the tail_n_mail program
## This file is automatically updated
## Last updated: Mon Oct  2 12:28:10 2017
MAILSUBJECT: HOST Postgres errors NUMBER

INHERIT: tnm.global.conf

FILE1: /var/log/postgres.log
LASTFILE1: /var/log/postgres.log
OFFSET1: 13219
```

Another advantage to moving common items to another file is that we can run multiple tail_n_mails,
with slightly different purposes, but all sharing some of the same underlying rules.
A common usage is to get an immediate email about almost all database problems, as
well as a daily report about all problems. To do this, we create two configuration
files and set them up in cron:

```text
$ cp tnm.conf tnm.fatals.conf
$ mv tnm.conf tnm.errors.conf
$ perl -pi -e 's/Postgres errors/Postgres fatals/' tnm.fatals.conf
$ crontab -e
## Every five minutes, check for important problems
*/5 * * * * perl tail_n_mail tnm.fatals.conf
## Once every morning, generate a report of all errors in the last 24 hours.
30 6 * * * perl tail_n_mail tnm.errors.conf
## Note: it is usually easier to have separate "fatals" and "errors" exclusions.
```

What if we want to change the rules depending on the time of day, per the question that started this article?
Simple enough — we just create two “inherited” configuration files, then have cron swap things around as needed.
For example, let’s say that after 5pm on weekdays, and all weekend, we do not want to receive emails
about “division by zero” errors. First, create files named tnm.global.hometime.conf and tnm.global.workday.conf:

```text
$ cp tnm.global.conf tnm.global.workday.conf
$ cp tnm.global.conf tnm.global.hometime.conf
$ ln -sf tnm.global.workday.conf tnm.global.conf
$ echo "EXCLUDE: ERROR:  division by zero" >> tnm.global.hometime.conf
```

Finally, have cron swap the files around at the start and end of business hours:

```text
$ crontab -e
## May need to use 1-5 instead of Mon-Fri on some systems
0 9 * * Mon-Fri ln -sf tnm.global.workday.conf tnm.global.conf
0 17 * * Mon-Fri ln -sf tnm.global.hometime.conf tnm.global.conf
```

Voila! We’ve changed the way tail_n_mail runs depending on the time of day. There are
many other tricks you can do with tail_n_mail — check out [the documentation](https://bucardo.org/tail_n_mail/) or post to [the mailing list](https://mail.endcrypt.com/mailman/listinfo/tnm)
for more help and/or inspiration.
