---
author: Josh Williams
gh_issue_number: 436
tags: database, performance, postgres
title: Annotating Your Logs
---



We recently did some PostgreSQL performance analysis for a client with an application having some scaling problems. In essence, they wanted to know where Postgres was getting bogged down, and once we knew that we’d be able to target some fixes. But to get to that point, we had to gather a whole bunch of log data for analysis while the test software hit the site.

This is on Postgres 8.3 in a rather locked down environment, by the way. Coordinated pg_rotate_logfile() was useful, but occasionally it would seem to devolve to something resembling: “Okay, we’re adding 60 more users ... now!” And I’d write down the time stamp, and figure out an appropriate place to slice the log file later.

Got me thinking, what if we could just drop an entry into the log file, and use it to filter things out later? My first instinct was to start looking at seeing if a patch would be accepted, maybe a wrapper for ereport(), something easy. Turns out, it’s even easier than that...

```nohighlight
pubsite=# DO $$BEGIN RAISE LOG 'MARK: 60 users'; END;$$;
DO
Time: 0.464 ms
pubsite=# DO $$BEGIN RAISE LOG 'MARK: 120 users'; END;$$;
DO
Time: 0.378 ms
pubsite=# DO $$BEGIN RAISE LOG 'MARK: 360 users'; END;$$;
DO
Time: 0.700 ms
```

Of course the above will only work on version 9.0 and up (eventually). Previous versions that have PL/pgSQL turned can just create a function that does the same thing. The “LOG” severity level is an informational message that’s supposed to always make it into the log files. So with those in place, a grep through the log can reveal just where they appear, and sed can extract the sections of log between those lines and feed them into your favorite analysis utility:

```nohighlight
postgres@mothra:~$ grep -n 'LOG:  MARK' /var/log/postgresql/postgresql-9.0-main.log 
19180:2011-03-31 20:20:37 EDT LOG:  MARK: 60 users
19478:2011-03-31 20:25:48 EDT LOG:  MARK: 120 users
20247:2011-03-31 20:32:15 EDT LOG:  MARK: 360 users
postgres@mothra:~$ sed -n '19180,19478p' /var/log/postgresql/postgresql-9.0-main.log | bin/pgsi.pl > 60users.html
```

Oh, and the performance problem? Turns out it wasn’t Postgres at all, every single query average execution time was shown to vary minimally as the concurrent user count was scaled higher and higher. But that’s another story.


