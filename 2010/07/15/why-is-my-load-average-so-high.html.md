---
author: Josh Tolley
gh_issue_number: 326
tags: environment, hosting, monitoring, optimization
title: Why is my load average so high?
---



One of the most common ways people notice there’s a problem with their server is when Nagios, or some other monitoring tool, starts complaining about a high load average. Unfortunately this complaint carries with it very little information about what might be causing the problem. But there are ways around that. On Linux, where I spend most of my time, the load average represents the average number of process in either the "run" or "uninterruptible sleep" states. This code snippet will display all such processes, including their process ID and parent process ID, current state, and the process command line:

```bash
#!/bin/sh

ps -eo pid,ppid,state,cmd |\
    awk '$3 ~ /[RD]/ { print $0 }'
```

Most of the time, this script has simply confirmed what I already anticipated, such as, "PostgreSQL is trying to service 20 times as many simultaneous queries as normal." On occasion, however, it’s very useful, such as when it points out that a backup job is running far longer than normal, or when it finds lots of "[pdflush]" operations in process, indicating that the system was working overtime to write dirty pages to disk. I hope it can be similarly useful to others.


