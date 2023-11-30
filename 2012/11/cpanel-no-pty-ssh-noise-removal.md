---
author: Jon Jensen
title: cPanel no-pty ssh noise removal
github_issue_number: 719
tags:
- hosting
- redhat
- sysadmin
date: 2012-11-06
---



We commonly use non-interactive ssh for automation of various tasks. This usually involves setting BatchMode=yes in the ~/.ssh/config file or the no-pty option in the ~/.ssh/authorized_keys file, and stops a tty from being assigned for the ssh session so that a job will not wait for interactive input in unexpected places.

When using a RHEL 5 Linux server that has been modified by cPanel, ssh sessions display “stdin: is not a tty” on stderr. For ad-hoc tasks this is merely an annoyance, but for jobs run from cron it means an email is sent because cron didn’t see an empty result from the job and wants an administrator to review the output.

You could quell all output from ssh, but then if any legitimate errors or warnings were sent, you won’t see those. So that is not ideal.

Using bash’s set -v option to trace commands being run on the cPanel server we found that they had modified Red Hat’s stock /etc/bashrc file and added this line:

```bash
mesg y
```

That writes a warning to stderr when there’s no tty because mesg doesn’t make sense in non-interactive environments.

The solution is simple, since we don’t care to hear that warning. We edit that line like this:

```bash
mesg y 2>/dev/null
```

This tip that may only be useful to one or two people ever, if even that many. I hope they enjoy it. :)


