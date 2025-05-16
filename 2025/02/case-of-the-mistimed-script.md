---
author: "Josh Williams"
date: 2025-02-19
title: "The Case of the Mistimed Python Script"
github_issue_number: 2094
featured:
  image_url: /blog/2025/02/case-of-the-mistimed-script/clock-tower.webp
  endpoint: true
description: "Solving a mysterious timing issue where a cron job ran 5 hours early, despite everything seeming to be in order…"
tags:
- sysadmin
- linux
- tools
---

![A low-angle view of an old European church clock tower. The square tower with rounded corners is ornamented with gothic styling, and topped with a golden eagle.](/blog/2025/02/case-of-the-mistimed-script/clock-tower.webp)

<!-- Photo by Seth Jensen, 2024. -->

“Time isn’t working right!” said a message from a client on their internal chat.

My efforts to catch a spot as an extra in a Doctor Who episode have thus far been fruitless, so I jumped in to reply to that message. Just in case.

The follow-up had more detail: “I’ve set something to run at 7:30 AM every morning, but it runs at 2:30 AM instead. Time zone is right. I can’t figure out what’s wrong.”

Dang, the screen debut will have to wait. But at least this is a mystery *I* can solve.

The hypothesis offered up was that a Python script was getting the time wrong, but it turns out Python doesn’t do the scheduling here. Rather, it’s just plain ol’ cron, so all eyes are on that now.

First, the obvious: It’s running early, not late. So it’s not a situation where it’s running for about 5 hours and appearing later than desired. I mean, it could possibly be taking 19 hours to run and finishing at 2:30 the next day, but at a glance it’s clearly not taking that long. It's just running at the wrong time.

Let’s double check what cron is actually set to do.

```plain
30 7 * * * python3 /home/data/process/something.py
```

Alright. So clearly cron is set for 7:30 but running that at the wrong time. That’s typically a time zone issue, or potentially in rare cases a hardware clock issue. In fact those are probably about the only possibilities. The message reported the time zone is set correctly, but double checking that:

```plain
$ date
Fri Feb  7 16:23:01 EST 2025
$ cat /etc/timezone
America/New_York
```

We once had a server that somehow had a broken clock. We would log in first thing in the morning and it would report that it’s Tuesday, and by the time we were done in the afternoon the server time said Saturday. Thus far that’s as close as I’ve been able to get to a real TARDIS.

But that `date` above is right on compared to the wall clock. The schedule is exactly 5 hours off, so I can't shake the feeling that it's related to time zone, even though it appears correct. At least, it appears correct right now...

```bash
$ ls -l /etc/timezone
-rw-r--r-- 1 root root 17 Jan 31 06:14 /etc/timezone
```

That modification time is suspiciously recent. How long has this system been running? How long has cron been running?

```plain
$ uptime
 16:47:54 up 96 days, 31 min,  1 user,  load average: 0.00, 0.00, 0.00
$ ps -f -C cron
UID         PID  PPID  C STIME TTY          TIME CMD
root      16544     1  0  2024 ?        00:00:11 /usr/sbin/cron -f -P
```

Ah ha, a smoking sonic screwdriver: Processes usually only read things like the system timezone when starting up, and cron is one of them.

So the suspicion is that the timezone was set to UTC when the system booted and cron started up. Later, the system time zone was changed, but without restarting anything. Old processes keep that old value. New processes (like user sessions) show the updated time zone setting, which only helps confuse the issue.

Looking for a way to prove that, we can actually check the environment for those old processes. If the system had set the $TZ variable when starting up cron it should appear…

```bash
# tr '\0' '\n' < /proc/16544/environ
LANG=en_US.UTF-8
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

… but unfortunately it did not, so we’re left to assume that it read from /etc/timezone like we did, but it was different at the time. So all we can do is work with that assumption and try to make it behave.

I suppose we could have set the `CRON_TZ` variable at the top of the crontab, but we went with a slightly more heavy handed approach: restart it to see if it fixes it!

```plain
$ systemctl restart crond
```

And of course it did. Ideally when changing things like the the time zone setting we should be even more heavy handed and reboot the system afterward. That way *everything* inherits the new value. But this lets us be less disruptive, but still ensure any other cron tabs see the same setting.
