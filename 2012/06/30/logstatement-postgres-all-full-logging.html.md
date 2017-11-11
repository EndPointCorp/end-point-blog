---
author: Greg Sabino Mullane
gh_issue_number: 664
tags: database, postgres
title: Postgres log_statement='all' should be your default
---



<div class="separator" style="clear: both; float:right; text-align: center;">
<a href="/blog/2012/06/30/logstatement-postgres-all-full-logging/image-0-big.jpeg" imageanchor="1" style="clear:right; margin-left:1em; margin-bottom:1em"><img border="0" height="281" src="/blog/2012/06/30/logstatement-postgres-all-full-logging/image-0.jpeg" width="400"/></a><br/>Modified version of <a href="http://www.flickr.com/photos/ellesmerefnc/3869313993/">image</a> by Flickr user <a href="http://www.flickr.com/photos/ellesmerefnc/">Ellesmere FNC</a></div>

Setting the PostgreSQL **log_statement** parameter to **'all'** is always your best choice; this article will explain why. PostgreSQL does not have many knobs to control logging. The main one is 
[log_statement](http://www.postgresql.org/docs/current/static/runtime-config-logging.html#GUC-LOG-STATEMENT), which can be set to **'none'** (do not ever set it to this!), **'ddl'** or **'mod'** (decent but flawed values), or **'all'**, which is what you should be using. In addition, you probably 
want to set **log_connections = on**, **log_disconnections = on**, and **log_duration = on**. 
Of course, if you do set all of those, don't forget to set **log_min_duration_statement = -1**
to turn it off completely, as it is no longer needed.

The common objections to setting log_statement to 'all' can be summed up as 
 ***Disk Space***,   ***Performance***, and  ***Noise***. Each will be 
explained and countered below. The very good reasons for having it set to 'all' 
will be covered as well:  ***Troubleshooting***,   ***Analytics***, and   
***Forensics/Auditing***.

### **Objection: *Disk Space***

The most common objection to logging all of your SQL statements is disk space. 
When log_statement is set to all, every action against the database is logged, 
from a simple **SELECT 1;** to a gigantic data warehousing query that is 300 lines long and takes seven hours to complete. As one can imagine, logging all queries generates large logs, very quickly. How much depends on your particular system of course. Luckily, the amount of space is very easy to test: just flip log_statement='all' in your postgresql.conf, and reload your database (no restart required!). Let it run for 15 minutes or so and you will have a decent starting point for extrapolating daily disk space usage. For most of our clients, the median is probably around 30MB per day, but we have some as low as 1MB and some over 50GB! Disk space is cheap, but if it is really an issue to save everything, one solution is to dynamically ship the logs to a different box via syslog (see below). Another not-as-good option is to simply purge older logs, or at least ship the older logs to a separate server, or perhaps to tape. Finally, you could write a quick script to remove common and uninteresting lines (say, all selects below 10 milliseconds) from older logs.

### **Objection: *Performance***

Another objection is that writing all those logs is going to harm the performance 
of the server the database is on. A valid concern, although the actual impact can 
be easily measured by toggling the value temporarily. The primary performance issue
is I/O, as all those logs have to get written to a disk. The first solution is to 
make sure the logs are going to a different hard disk, thus reducing contention with 
anything else on the server. Additionally, you can configure this disk differently, 
as it will be heavy write/append with little to no random read access. The best 
filesystems for handling this sort of thing seem to be ext2 and ext4.
A better solution is to trade the I/O hit for a network hit, and use syslog (or 
better, [rsyslog](http://en.wikipedia.org/wiki/Rsyslog)) to ship the logs to a different server. Doing this is usually as simple as setting **log_destination = 'syslog'** in your postgresql.conf and adjusting your [r]syslog.conf. This has many advantages: if shipping to a local server, you can often go over a non-public network interface, and thus not impact the database server at all. This other server can also be queried at will, without affecting the performance of the database server. This means heavy analytics, e.g. running [pgsi](http://bucardo.org/wiki/Pgsi) or 
[pgfouine](http://pgfouine.projects.postgresql.org/), can 
run without fear of impacting production. It can also be easier to provision this other server with larger disks than to mess around with the production database server.

### **Objection: *Noise***

A final objection is that the log files get so large and noisy, they are hard to read. Certainly, if you are used to reading sparse logs, this will be a change that will take some getting used to. One should not be reading logs manually anyway: there are tools to do that. If all your logs were showing before was log_min_duration_statement, you can get the same effect (in a prettier format!) by using the 'duration' mode of [the tail_n_mail program](http://bucardo.org/wiki/Tail_n_mail), which also lets you pick your own minimum duration and then sorts them from longest to shortest.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/06/30/logstatement-postgres-all-full-logging/image-1-big.jpeg" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" height="299" src="/blog/2012/06/30/logstatement-postgres-all-full-logging/image-1.jpeg" width="400"/></a><br/><a href="http://www.flickr.com/photos/7682623@N02/2535217848/">Image</a> by Flickr user <a href="http://www.flickr.com/photos/7682623@N02/">auntjojo</a></div>

### **Advantage: *Troubleshooting***

When things go wrong, being able to see exactly what is happening in your database 
can be crucial. Additionally, being able to look back and see what *was* 
going on can be invaluable. I cannot count the number of times that full logging 
has made debugging a production issue easier. Without this logging, the only 
option sometimes is to switch log_statement to all and then wait for the error 
to pop up again! Don't let that happen to you - log heavy preemptively. This is 
not just useful for tracking direct database problems; often the database 
trail can enable a DBA to work with application developers to see exactly what their 
application is doing and where things started to go wrong. On that note, it is a good 
idea to log as verbosely as you can for everything in your stack, from the database 
to the application to the httpd server: you never know which logs you may need at a 
moment's notice when major problems arise.

### **Advantage: *Analytics***

If the only logging you are doing is those queries that happen to be longer 
than you log_min_duration_statement, you have a very skewed and incomplete view 
of your database activity. Certainly one can view the slowest queries and try to speed them up, but tools like [pgsi](http://bucardo.org/wiki/Pgsi) are designed to parse full logs: the impact of thousands of "fast" queries can often be more stressful on your server than a few long-running queries, but without full logging you will never know. You also won't know if those long-running queries sometimes (or often!) run faster than log_min_duration_statement.

We do have some clients that cannot do log_statement = 'all', but we still want 
to use pgsi, so what we do is turn on full logging for a period of time via cron 
(usually 15 minutes, during a busy time of day), then turn it off and run pgsi 
on that slice of full logging. Not ideal, but better than trying to crunch numbers 
using incomplete logs.

### **Advantage: *Forensics/Auditing***

Full logging via log_statement='all' is extremely important if you need to know exactly what commands a particular user or process has run. This is not just relevant to 
[SQL injection attacks](http://blog.endpoint.com/2012/06/detecting-postgres-sql-injection.html), but for rogue users, lost laptops, and any situation 
in which someone has done something unknown to your database. Not every one of 
these situations will be noticeable, such as the infamous **DROP TABLE students;**: 
often it involves updating a few critical rows, modifying some functions, or 
simply copying a table to disk. The *only* way to know exactly what was done is 
to have log_statement = 'all'. Luckily, this parameter cannot be turned off 
by clients: one must edit the postgresql.conf file and then reload the server.

The advantages of complete logging should outweigh the disadvantages, except in the most extreme cases. Certainly, it is better to start from a position of setting Postgres' log_statement to **'all'** and defending any change to a lesser setting. Someday it may save your bacon. Disagreements welcome in the comment section!


