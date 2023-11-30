---
author: Greg Sabino Mullane
title: check_postgres without Nagios (Postgres checkpoints)
github_issue_number: 398
tags:
- database
- monitoring
- open-source
- postgres
date: 2011-01-21
---

<a href="/blog/2011/01/checkpostgres-without-nagios-postgres/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5564861357320644354" src="/blog/2011/01/checkpostgres-without-nagios-postgres/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 320px; height: 200px;"/></a>

Version 2.16.0 of [check_postgres](https://bucardo.org/check_postgres/), a monitoring tool for Postgres, was just released. We’re still trying to keep a “release often” schedule, and hopefully this year will see many releases. In addition to a few minor bug fixes, we added a new check by Nicola Thauvin called [hot_standby_delay](https://bucardo.org/check_postgres/check_postgres.pl.html#hot_standby_delay), which, as you might have guessed from the name, calculates the streaming replication lag between a [master server](https://wiki.postgresql.org/wiki/Hot_Standby) and one of the slaves connected to it. Obviously the servers must be running PostgreSQL 9.0 or better.

Another recently added feature ([in version 2.15.0](https://github.com/bucardo/check_postgres/commit/c54c4d041bb164c201f5da2de217496c9f4e261c)) was the simple addition of a **--quiet** flag. All this does is to prevent any normal output when an OK status is found. I wrote this because sometimes even Nagios is overkill. In the default mode ([Nagios](https://www.nagios.org/), the other major mode is [MRTG](https://oss.oetiker.ch/mrtg/)), check_postgres will exit with one of four states, each with their own exit code: OK, WARNING, CRITICAL, or UNKNOWN. It also outputs a small message, per Nagios conventions, so a txn_idle action might exit with a value of 1 and output something similar to this:

```plain
POSTGRES_TXN_IDLE WARNING: (host:svr1) longest idle in txn: 4638s
```

I had a situation where I wanted to use the functionality of check_postgres (to examine the lag on a warm standby server), but did not want the overhead of adding it into Nagios, and just needed a quick email to be sent if there were any problems. Thus, the use of the quiet flag yielded a quick and cheap Nagios replacement using cron:

```plain
*/10 * * * * bin/check_postgres.pl --action=checkpoint -w 300 -c 600 --datadir=/dbdir --quiet
```

So every 10 minutes the script gathers the number of seconds since the last checkpoint was run. If that number is under five minutes (300 seconds), it exits silently. If it’s over five minutes, it outputs something similar to this, which cron then sends in an email:

```plain
POSTGRES_CHECKPOINT CRITICAL:  Last checkpoint was 842 seconds ago
```

I’m not advocating replacing Nagios of course: there are many other good reasons to use Nagios instead of cron, but this worked well for the situation at hand. Other actions, feature requests, and [patches](https://github.com/bucardo/check_postgres/) for check_postgres are always welcome, either on the [check_postgres GitHub repository](https://github.com/bucardo/check_postgres/issues) or the [mailing list](https://mail.endcrypt.com/mailman/listinfo/check_postgres).
