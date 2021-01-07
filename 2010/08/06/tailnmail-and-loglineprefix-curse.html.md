---
author: Greg Sabino Mullane
gh_issue_number: 336
tags: monitoring, open-source, perl, postgres
title: Tail_n_mail and the log_line_prefix curse
---

<a href="/blog/2010/08/06/tailnmail-and-loglineprefix-curse/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5502309252316445506" src="/blog/2010/08/06/tailnmail-and-loglineprefix-curse/image-0.jpeg" style="float:right; margin:60px 0 10px 10px;cursor:pointer; cursor:hand;width: 132px; height: 74px;"/></a>

One of the problems I had when writing [tail_n_mail](https://bucardo.org/tail_n_mail/) (a program that parses log files and mails interesting lines to you) was getting the program to understand the format of the Postgres log files. There are quite a few options inside of postgresql.conf that control where the logging goes, and what it looks like. The basic three options are to send it to a rotating logfile with a custom prefix at the start of each line, to use [syslog](https://en.wikipedia.org/wiki/Syslog), or to write it in [CSV format](https://www.postgresql.org/docs/current/static/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-CSVLOG). I’ll save a discussion of all the logging parameters for another time, but the important one for this story is **log_line_prefix**. This is what gets prepended to each log line when using ‘stderr’ mode (e.g. regular log files and not syslog or csvlog). By default, log_line_prefix is an empty string. This is a very useless default.

What you can put in the log_line_prefix parameter is a string of sprintf style escapes, which Postgres will expand for you as it writes the log. There are a large number of escapes, but only a few are commonly used or useful. Here’s a log_line_prefix I commonly use:

```nohighlight
log_line_prefix = '%t [%p] %u@%d '
```

This tells Postgres to print out the timestamp, the PID aka process id (inside of square brackets), the current username and database name, and finally a single space to help separate the prefix visually from the rest of the line. The above will generate lines that look like this:

```nohighlight
2010-08-06 09:24:57.714 EDT [7229] joy@joymail LOG: execute dbdpg_p7228_5: SELECT count(id) FROM joymail WHERE folder = $1
2010-08-06 09:24:57.714 EDT [7229] joy@joymail DETAIL:  parameters: $1 = '4'
```

As you might imagine, the customizability of log_line_prefix makes parsing the log files all but impossible without some prior knowledge. I didn’t want to go the pgfouine route and make people change their log_line_prefix to a specific setting. I think it’s kind of rude to force your database to change its logging to accommodate your tools :). The original quick solution I came up with was to have a set of predefined regular expressions and the user would pick one that most closely matched their logs. For tail_n_mail to work properly, it needs to pick up at least the PID so it can tell when one statement ends a new one begins. For example, if you chose “regex #1”, the log parsing regex would look like this:

```nohighlight
(\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d).+?(\d+)
```

This works fine on the example above, and gets us the timestamp and the PID from each line. The stock regexes worked for many different log_line_prefixes I came across that our clients were using, but I was never very happy with this solution. Not only was it susceptible to failing completely when a client was using a log_line_prefix not fitting into the current list of regexes, but there was no way to know exactly where the prefix ended and the statement began, which is important for the formatting of the output and the canonicaliztion of similar queries.

Enter the current solution: building a regex on the fly. Since we don’t have a connection to the database at all, merely to the the log files, this requires that the user enter in their current log_line_prefix. This is a simple entry into the **tailnmailrc** file that looks just like the entry in postgresql.conf, e.g.:

```nohighlight
log_line_prefix = '%t [%p] %u@%d '
```

The tail_n_mail script uses that variable to build a custom regex specifically tailored to that log_line_prefix and thus to the Postgres logs being used. Not only can we grab whatever bits we want (currently we only care about the timestamp (%t and %m) and the PID (%p)), but we can now cleanly break apart each line in the log into the prefix and the actual statement. This means the canonicalization/flattening of the queries is more effective, and allows us to only output the prefix information once. The output of tail_n_mail looks something like this:

```nohighlight
Date: Fri Aug  6 11:01:03 2010 UTC
Host: whale.example.com
Unique items: 7
Total matches: 85
Matches from [A] /var/log/pg_log/postgresql-2010-08-05.log: 61
Matches from [B] /var/log/pg_log/postgresql-2010-08-06.log: 24

[1] From files A to B (between lines 14,205 of A and 527 of B, occurs 64 times)
First: [A] 2010-08-05 16:52:11 UTC [1602]  postgres@mydb
Last:  [B] 2010-08-06 01:18:14 UTC [20981] postgres@mydb
ERROR: syntax error at or near ")"
STATEMENT: INSERT INTO mytable (id, foo, bar) VALUES (?,?,?))
-
ERROR: syntax error at or near ")"
STATEMENT: INSERT INTO mytable (id, foo, bar) VALUES (123,'chocolate','donut'));

[2] From file A (line 12,172)
2010-08-05 12:27:48 UTC [2906] bob@otherdb
ERROR: invalid input syntax for type date: "May"
STATEMENT: UPDATE personnel SET birthdate='May' WHERE id = 1234;

(plus five other entries)
```

For the entry in the above example, we are able to show the complete prefix of the log lines where the error first occurred and where it most recently occurred. The next two lines show the “flattened” version of the query that tail_n_mail uses to group together similar errors. We then show a non-flattened example of an actual query from that group. In this case, someone added an extra closing paren in their application somewhere, which gives the same error each time, although the exact output changes depending on the values used. In the second example, because there is only one match, we don’t bother to show the flattened version at all.

So in theory tail_n_mail should be now be able to handle any Postgres log you care to throw at it (yes, it can read syslog and csvlog format as well). As my coworker Ethan Rowe pointed out, parsing log files in this way is something that should probably be abstracted into a common module so other tools like [pgsi](https://bucardo.org/Pgsi/) can take advantage of it as well.
