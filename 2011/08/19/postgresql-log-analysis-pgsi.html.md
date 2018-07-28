---
author: Greg Sabino Mullane
gh_issue_number: 488
tags: analytics, database, monitoring, performance, postgres
title: PostgreSQL log analysis / PGSI
---



<a href="/blog/2011/08/19/postgresql-log-analysis-pgsi/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5642400584741062274" src="/blog/2011/08/19/postgresql-log-analysis-pgsi/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 320px; height: 221px;"/></a>

Image by [“exfordy” on Flickr](https://www.flickr.com/photos/exfordy/)

End Point recently started working with a new client (a startup in [stealth mode](https://en.wikipedia.org/wiki/Stealth_mode), cannot name names, etc.) who is using [PostgreSQL](https://www.postgresql.org/) because of the great success some of the people starting the company have had with Postgres in previous companies. One of the things we recommend to our clients is a regular look at the database to see where the bottlenecks are. A good way to do this is by analyzing the logs. The two main tools for doing so are [PGSI](https://bucardo.org/Pgsi/) (Postgres System Impact) and [pgfouine](http://pgfoundry.org/projects/pgfouine/). We prefer PGSI for a few reasons: the output is better, it considers more factors, and it does not require you to munge [your log_line_prefix](https://www.postgresql.org/docs/9.0/static/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) setting quite as badly.

Both programs work basically the same: given a large number of log lines from Postgres, normalize the queries, see how long they took, and produce some pretty output.If you only want to look at the longest queries, it’s usually enough to set your log_min_duration_statement to something sane (such as 200), and then run a daily [tail_n_mail](https://bucardo.org/tail_n_mail/) job against it. This is what we are doing with this client, and it sends a daily report that looks like this:

```nohighlight
Date: Mon Aug 29 11:22:33 2011 UTC
Host: acme-postgres-1
Minimum duration: 2000 ms
Matches from /var/log/pg_log/postgres-2011-08-29.log: 7

[1] (from line 227)
2011-08-29 08:36:50 UTC postgres@maindb [25198]
LOG: duration: 276945.482 ms statement: COPY public.sales 
(id, name, region, item, quantity) TO stdout;

[2] (from line 729)
2011-08-29 21:29:18 UTC tony@quadrant [17176]
LOG: duration: 8229.237 ms execute dbdpg_p29855_1: SELECT 
id, singer, track FROM album JOIN artist ON artist.id = 
album.singer WHERE id < 1000 AND track <> 1
```

However, the PGSI program was born of the need to look at ***all*** the queries in the database, not just the slowest-running ones; the cumulative effect of many short queries can have much more of an impact on the server than a smaller number of long-running queries. Thus, PGSI looks not only at how long a query takes to run, but how many times it has run in a certain period, as well as how often it runs. All of this information is put together to give a score to each normalized query, known as the “system impact”. Like the costs on a Postgres explain plan, this is a unit-less number and of little importance in and of itself—​the important thing is to compare it to the other queries to see the relative impact. We also have that report emailed out, it looks similar to this (this is a text version of the HTML produced):

```nohighlight
Log file: /var/log/pg_log/postgres-2011-08-29.log

 * SELECT (24)
 * UPDATE (1)

Query System Impact : SELECT

 Log activity from 2011-08-29 11:00:01 to 2011-08-29 11:15:01

   +----------------------------------+
   |   System Impact: | 0.15          |
   |   Mean Duration: | 1230.95 ms    |
   | Median Duration: | 1224.70 ms    |
   |     Total Count: | 411           |
   |   Mean Interval: | 4195 seconds  |
   |  Std. Deviation: | 126.01 ms     |
   +---------------------------------+

 SELECT *
  FROM albums
  WHERE track <> ? AND artist = ?
  ORDER BY artist, track

```

At this point you may be wondering how we get all the queries into the log. This is done by setting log_min_duration_statement to 0. However, most (but not all!) clients do not want full logging 24 hours a day, as this creates some very large log files. So the solution we use is to analyze a slice of the day, only. It depends on the client, but we try for about 15 minutes during a busy time of day. Thus, the sequence of events is:

1. Turn on “full logging” by dropping log_min_duration_statement to zero1. Some time later, set log_min_duration_statement back to what it was (e.g. 200)1. Extract the logs from the time it was set to zero to when it was flipped back.1. Run PGSI against the log subsection we pulled out1. Mail the results out

All of this is run by cron. The first problem is how to update the postgresql.conf file and have Postgres re-read it, all automatically. As [covered previously](/blog/2011/08/10/changing-postgresqlconf-from-script), we use the [modify_postgres.pl](https://github.com/bucardo/modify_postgres_config) script for this.

The exact incantation looks like this:

```nohighlight
0 11 * * * perl bin/modify_postgres_conf --quiet \
  --pgconf /etc/postgresql/9.0/main/postgresql.conf \
  --change log_min_duration_statement=0
15 11 * * * perl bin/modify_postgres_conf --quiet \
  --pgconf /etc/postgresql/9.0/main/postgresql.conf \
  --change log_min_duration_statement=200 --no-comment
## The above are both one line each, but split for readability here
```

This changes log_min_duration_statement to 0 at 11AM, and then back to 200 15 minutes later. We use the --quiet argument as this is run from cron so we don’t want any output from modify_postgres_conf on success. We do want a comment when we flip it to 0, as this is the temporary state and we want people viewing the postgresql.conf file at that time to realize it (or someone just doing a “git diff”). We don’t want a comment when we flip it back, as the timestamp in the comment would cause git to think the file had changed.

Now for the tricky bit: extracting out just the section of logs that we want and sending it to PGSI. Here’s the recipe I came up with for this client:

```nohighlight
16 11 * * * tac `ls -1rt /var/log/pg_log/postgres*log \
  | tail -1` \
  | sed -n '/statement" changed to "200"/,/statement" changed to "0"/ p' \
  | tac \
  | bin/pgsi.pl --quiet > tmp/pgsi.html && bin/send_pgsi.pl
## Again, the above is all one line
```

What does this do? First, it finds the latest file in the /var/log/pg_log directory that starts with ‘postgres’ and ends with ‘log’. Then it uses the **tac** program to spool the file backwards, one line at a time (‘tac’ is the opposite of ‘cat’). Then it pipes *that* output to the **sed** program, which prints out all lines starting with the one where we changed the log_min_duration_statement to 200, and ending with the one where we changed it to 0 (the reverse of what we actually did, as we are reading it backwards). Finally, we use tac again to put the lines back in the correct order, pipe the output to **pgsi**, write the output to a temporary file, and then call a quick Perl script named **send_pgsi.pl** which mails the temporary HTML file to some interested parties.

Why do we use tac? Because we want to read the file backwards, so as to make sure we get the correct slice of log files as delimited by the log_min_duration_statement changes. If we simply started at the beginning of the file, we might encounter other similar changes that were made earlier and not by us.

All of this is not foolproof, of course, but it does not have to be, as it is very easy to run manually is something (for example the sed recipe) goes wrong, as the log file will still be there. Yes, it’s also possible to grab the ranges in other ways (such as perl), but I find sed the quickest and easiest. As tempting as it was to write Yet Another Perl Script to extract the lines, sometimes a few chained Unix programs can do the job quite nicely.


