---
author: Greg Sabino Mullane
gh_issue_number: 511
tags: database, monitoring, performance, postgres
title: Finding PostgreSQL temporary_file problems with tail_n_mail
---

<a href="/blog/2011/11/10/postgres-temporary-files-workmem-and/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5673407150243656402" src="/blog/2011/11/10/postgres-temporary-files-workmem-and/image-0.jpeg"/></a>

Image by Flickr user [dirkjanranzijn](https://www.flickr.com/photos/dirkscircusimages/)

PostgreSQL does as much work as it can in RAM, but sometimes it needs to (or thinks that it needs to) write things temporarily to disk. Typically, this happens on large or complex queries in which the required memory is greater than the [work_mem](https://www.postgresql.org/docs/current/static/runtime-config-resource.html#GUC-WORK-MEM) setting.

This is usually an unwanted event: not only is going to disk much slower than keeping things in memory, but it can cause I/O contention. For very large, not-run-very-often queries, writing to disk can be warranted, but in most cases, you will want to adjust the **work_mem** setting. Keep in mind that this is very flexible setting, and can be adjusted globally (via the postgresql.conf file), per-user (via the ALTER USER command), and dynamically within a session (via the SET command). A good rule of thumb is to set it to something reasonable in your postgresql.conf (e.g. 8MB), and set it higher for specific users that are known to run complex queries. When you discover a particular query run by a normal user requires a lot of memory, adjust the work_mem for that particular query or set of queries.

How do you tell when you work_mem needs adjusting, or more to the point, when Postgres is writing files to disk? The key is the setting in postgresql.conf called [log_temp_files](https://www.postgresql.org/docs/current/static/runtime-config-logging.html#GUC-LOG-TEMP-FILES). By default it is set to **-1**, which does no logging at all. Not very useful. A better setting is **0**, which is my preferred setting: it logs *all* temporary files that are created. Setting **log_temp_files** to a positive number will only log entries that have an on-disk size greater than the given number (in kilobytes). Entries about temporary files used by Postgres will appear like this in your log file:

```nohighlight
2011-01-12 16:33:34.175 EST LOG:  temporary file: path "base/pgsql_tmp/pgsql_tmp16501.0", size 130220032
```

The only important part is the size, in bytes. In the example above, the size is 124 MB, which is not that small of a file, especially as it may be created many, many times. So the question becomes, how can we quickly parse the files and get a sense of which queries are causing excess writes to disk? Enter the [tail_n_mail program](https://bucardo.org/wiki/Tail_n_mail), which I recently tweaked to add a “tempfile” mode for just this purpose.

To enter this mode, just name your config file with “tempfile” in its name, and have it find the lines containing the temporary file information. It’s also recommended you make use of the tempfile_limit parameter, which limits the results to the “top X” ones, as the report can get very verbose otherwise. An example config file and an example invocation via cron:

```nohighlight
$ cat tail_n_mail.tempfile.myserver.txt

## Config file for the tail_n_mail program
## This file is automatically updated
## Last updated: Thu Nov 10 01:23:45 2011
MAILSUBJECT: Myserver tempfile sizes
EMAIL: greg@endpoint.com
FROM: postgres@myserver.com
INCLUDE: temporary file
TEMPFILE_LIMIT: 5

FILE: /var/log/pg_log/postgres-%Y-%m-%d.log

$ crontab -l | grep tempfile

## Mail a report each morning about tempfile usage:
0 5 * * * bin/tail_n_mail tnm/tail_n_mail.tempfile.myserver.txt --quiet
```

For the client I wrote this for, we run this once a day and it mails us a nice report giving the worst tempfile offenders. The queries are broken down in three ways:

- Largest overall temporary file size
- Largest arithmetic mean (average) size
- Largest total size across all the same query

Here is a slightly edited version of an actual tempfile report email:

```nohighlight
Date: Mon Nov  7 06:39:57 2011 EST
Host: myserver.example.com
Total matches: 1342
Matches from [A] /var/log/pg_log/2011-11-08.log: 1241
Matches from [B] /var/log/pg_log/2011-11-09.log:  101
Not showing all lines: tempfile limit is 5

  Top items by arithmetic mean    |   Top items by total size
----------------------------------+-------------------------------
    860 MB (item 5, count is 1)   |   17 GB (item 4, count is 447)
    779 MB (item 1, count is 2)   |    8 GB (item 2, count is 71)
    597 MB (item 7, count is 1)   |    6 GB (item 334, count is 378)
    597 MB (item 8, count is 1)   |    6 GB (item 46, count is 104)
    596 MB (item 9, count is 1)   |    5 GB (item 3, count is 63)

[1] From file B Count: 2
Arithmetic mean is 779.38 MB, total size is 1.52 GB
Smallest temp file size: 534.75 MB (2011-11-08 12:33:14.312 EST)
Largest temp file size: 1024.00 MB (2011-11-08 16:33:14.121 EST)
First: 2011-11-08 05:30:12.541 EST
Last:  2011-11-09 03:12:22.162 EST
SELECT ab.order_number, TO_CHAR(ab.creation_date, 'YYYY-MM-DD HH24:MI:SS') AS order_date,
FROM orders o
JOIN order_summary os ON (os.order_id = o.id)
JOIN customer c ON (o.customer = c.id)
ORDER BY creation_date DESC

[2] From file A Count: 71
Arithmetic mean is 8.31 MB, total size is 654 MB
Smallest temp file size: 12.12 MB (2011-11-08 06:12:15.012 EST)
Largest temp file size: 24.23 MB (2011-11-08 19:32:45.004 EST)
First: 2011-11-08 06:12:15.012 EST
Last:  2011-11-09 04:12:14.042 EST
CREATE TEMPORARY TABLE tmp_sales_by_month AS SELECT * FROM sales_by_month_view;

```

While it still needs a little polishing (such as showing which file each smallest/largest came from), it has already been an indispensible tool forfinding queries that causing I/O problems via frequent and/or large temporary files.
