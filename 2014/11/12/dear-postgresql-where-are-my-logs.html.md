---
author: Josh Tolley
gh_issue_number: 1053
tags: postgres
title: 'Dear PostgreSQL: Where are my logs?'
---



<div class="separator" style="clear: both; text-align: center;"><span style="float: right"><a href="https://www.flickr.com/photos/jitze1942/2335756492/in/photostream/" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/11/12/dear-postgresql-where-are-my-logs/image-0.jpeg"/></a><p><small>From Flickr user <a href="https://www.flickr.com/photos/jitze1942/">Jitze Couperus</a></small></p></span></div>

When debugging a problem, it's always frustrating to get sidetracked hunting down the relevant logs. PostgreSQL users can select any of several different ways to handle database logs, or even choose a combination. But especially for new users, or those getting used to an unfamiliar system, just finding the logs can be difficult. To ease that pain, here's a key to help dig up the correct logs.

## Where are log entries sent?

First, connect to PostgreSQL with psql, pgadmin, or some other client that lets you run SQL queries, and run this:

```nohighlight
foo=# show log_destination ;
 log_destination 
-----------------
 stderr
(1 row)
```
The log_destination setting tells PostgreSQL where log entries should go. In most cases it will be one of four values, though it can also be a comma-separated list of any of those four values. We'll discuss each in turn.

### SYSLOG

Syslog is a complex beast, and if your logs are going here, you'll want more than this blog post to help you. Different systems have different syslog daemons, those daemons have different capabilities and require different configurations, and we simply can't cover them all here. Your syslog may be configured to send PostgreSQL logs anywhere on the system, or even to an external server. For your purposes, though, you'll need to know what "ident" and "facility" you're using. These values tag each syslog message coming from PostgreSQL, and allow the syslog daemon to sort out where the message should go. You can find them like this:

```nohighlight
foo=# show syslog_facility ;
 syslog_facility 
-----------------
 local0
(1 row)

foo=# show syslog_ident ;
 syslog_ident 
--------------
 postgres
(1 row)
```
Syslog is often useful, in that it allows administrators to collect logs from many applications into one place, to relieve the database server of logging I/O overhead (which may or may not actually help anything), or any number of other interesting rearrangements of log data.

### EVENTLOG

For PostgreSQL systems running on Windows, you can send log entries to the Windows event log. You'll want to tell Windows to expect the log values, and what "event source" they'll come from. You can find instructions for this operation in the [PostgreSQL documentation discussing server setup](http://www.postgresql.org/docs/9.3/static/event-log-registration.html).

### STDERR

This is probably the most common log destination (it's the default, after all) and can get fairly complicated in itself. Selecting "stderr" instructs PostgreSQL to send log data to the "stderr" (short for "standard error") output pipe most operating systems give every new process by default. The difficulty is that PostgreSQL or the applications that launch it can then redirect this pipe to all kinds of different places. If you start PostgreSQL manually with no particular redirection in place, log entries will be written to your terminal:

```nohighlight
[josh@eddie ~]$ pg_ctl -D $PGDATA start
server starting
[josh@eddie ~]$ LOG:  database system was shut down at 2014-11-05 12:48:40 MST
LOG:  database system is ready to accept connections
LOG:  autovacuum launcher started
LOG:  statement: select syntax error;
ERROR:  column "syntax" does not exist at character 8
STATEMENT:  select syntax error;
```
In these logs you'll see the logs from me starting the database, connecting to it from some other terminal, and issuing the obviously erroneous command "select syntax error". But there are several ways to redirect this elsewhere. The easiest is with pg_ctl's -l option, which essentially redirects stderr to a file, in which case the startup looks like this:

```nohighlight
[josh@eddie ~]$ pg_ctl -l logfile -D $PGDATA start
server starting
```
Finally, you can also tell PostgreSQL to redirect its stderr output internally, with the logging_collector option (which older versions of PostgreSQL named "redirect_stderr"). This can be on or off, and when on, collects stderr output into a configured log directory.

So if you end see a log_destination set to "stderr", a good next step is to check logging_collector:

```nohighlight
foo=# show logging_collector ;
 logging_collector 
-------------------
 on
(1 row)
```
In this system, logging_collector is turned on, which means we have to find out where it's collecting logs. First, check log_directory. In my case, below, it's an absolute path, but by default it's the relative path "pg_log". This is relative to the PostgreSQL data directory. Log files are named according to a pattern in log_filename. Each of these settings is shown below:

```nohighlight
foo=# show log_directory ;
      log_directory      
-------------------------
 /home/josh/devel/pg_log
(1 row)

foo=# show data_directory ;
       data_directory       
----------------------------
 /home/josh/devel/pgdb/data
(1 row)

foo=# show log_filename ;
          log_filename          
--------------------------------
 postgresql-%Y-%m-%d_%H%M%S.log
(1 row)
```
Documentation for each of these options, along with settings governing log rotation, is available [here](http://www.postgresql.org/docs/9.3/static/runtime-config-logging.html).

If logging_collector is turned off, you can still find the logs using the /proc filesystem, on operating systems equipped with one. First you'll need to find the process ID of a PostgreSQL process, which is simple enough:

```nohighlight
foo=# select pg_backend_pid() ;
 pg_backend_pid 
----------------
          31950
(1 row)
```
Then, check /proc/YOUR_PID_HERE/fd/2, which is a symlink to the log destination:

```nohighlight
[josh@eddie ~]$ ll /proc/31113/fd/2
lrwx------ 1 josh josh 64 Nov  5 12:52 /proc/31113/fd/2 -> /var/log/postgresql/postgresql-9.2-local.log
```

### CSVLOG

The "csvlog" mode creates logs in CSV format, designed to be easily machine-readable. In fact, [this section of the PostgreSQL documentation](http://www.postgresql.org/docs/9.3/static/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-CSVLOG) even provides a handy table definition if you want to slurp the logs into your database. CSV logs are produced in a fixed format the administrator cannot change, but it includes fields for everything available in the other log formats. For these to work, you need to have logging_collector turned on; without logging_collector, the logs simply won't show up anywhere. But when configured correctly, PostgreSQL will create CSV format logs in the log_directory, with file names mostly following the log_filename pattern. Here's my example database, with log_destination set to "stderr, csvlog" and logging_collector turned on, just after I start the database and issue one query:

```nohighlight
[josh@eddie ~/devel/pg_log]$ ll
total 8
-rw------- 1 josh josh 611 Nov 12 16:30 postgresql-2014-11-12_162821.csv
-rw------- 1 josh josh 192 Nov 12 16:30 postgresql-2014-11-12_162821.log
```
The CSV log output looks like this:

```nohighlight
[josh@eddie ~/devel/pg_log]$ cat postgresql-2014-11-12_162821.csv 
2014-11-12 16:28:21.700 MST,,,2993,,5463ed15.bb1,1,,2014-11-12 16:28:21 MST,,0,LOG,00000,"database system was shut down at 2014-11-12 16:28:16 MST",,,,,,,,,""
2014-11-12 16:28:21.758 MST,,,2991,,5463ed15.baf,1,,2014-11-12 16:28:21 MST,,0,LOG,00000,"database system is ready to accept connections",,,,,,,,,""
2014-11-12 16:28:21.759 MST,,,2997,,5463ed15.bb5,1,,2014-11-12 16:28:21 MST,,0,LOG,00000,"autovacuum launcher started",,,,,,,,,""
2014-11-12 16:30:46.591 MST,"josh","josh",3065,"[local]",5463eda6.bf9,1,"idle",2014-11-12 16:30:46 MST,2/10,0,LOG,00000,"statement: select 'hello, world!';",,,,,,,,,"psql"
```

