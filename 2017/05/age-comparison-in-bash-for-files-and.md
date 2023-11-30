---
author: Kiel Christofferson
title: Age comparison in Bash for files and processes
github_issue_number: 1305
tags:
- shell
date: 2017-05-22
---

You want your script to run a command only if elapsed-time for a given process is greater than *X*?

Well, bash does *not* inherently understand a time comparison like:

```bash
if [ 01:23:45 -gt 00:05:00 ]; then
    foo
fi
```

However, bash *can* compare timestamps of files using -ot and -nt for “older than” and “newer than”, respectively. If the launch of our process includes creation of a PID file, then we are in luck! At the beginning of our loop, we can create a file with a specific age and use that for quick and simple comparison.

For example, if we only want to take action when the process we care about was launched longer than 24 hours ago, try:

```bash
touch -t $(date --date=yesterday +%Y%m%d%H%M.%S) $STAMPFILE
```

Then, within your script loop, compare the PID file with the $STAMPFILE, like this:

```bash
if [ $PIDFILE -ot $STAMPFILE ]; then
    foo
fi
```

And of course if you want to be sure you’re working with the PID file of a process which is actually responding, you can try to send it signal 0 to check:

```bash
if kill -0 `cat $PIDFILE`; then
    foo
fi
```
