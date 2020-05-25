---
author: Josh Williams
gh_issue_number: 848
tags: performance, postgres
title: 'Log Jam: Be careful with local syslog'
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="http://www.flickr.com/photos/shauntarlton/336510796/" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img alt="Elephant" border="0" height="190" src="/blog/2013/08/22/log-jam-be-careful-with-local-syslog/image-0.jpeg" width="240"/></a><br/>
<small><a href="http://www.flickr.com/photos/gadl/">Elephant by Shaun Tarlton</a></small></div>

All they really wanted to do is log any query that takes over 10 seconds. Most of their queries are very simple and fast, but the application generates a few complicated queries for some actions. Recording anything that took longer than 10 seconds allowed them to concentrate on optimizing those. Thus, the following line was set in postgresql.conf:

```
log_min_duration_statement = 10
```

### Log Everything

A little while back, Greg wrote about configuring Postgres to [log everything, and the really good reasons to do so](/blog/2012/06/30/logstatement-postgres-all-full-logging). That isn’t what they intended to to here, but is effectively what happened. The integer in log_min_duration_statement represents milliseconds, not seconds. With a 10ms threshold it wasn’t logging everything the database server was doing, but enough that this performance graph happened:

<div class="separator" style="clear: both; float: left; text-align: center; width: 305px"><img alt="Reconstructed I/O Utilization" height="183" src="/blog/2013/08/22/log-jam-be-careful-with-local-syslog/image-1.png" title="Reconstructed I/O Utilization" width="295"/><p class="wp-caption-text">Reconstructed I/O Utilization</p></div>

That is, admittedly, a fabricated performance plot. But it’s pretty close to what we were seeing at the time. The blue is the fast SAS array where all the Postgres data resides, showing lower than normal utilization before recovering after the configuration change. The maroon behind it is the SATA disk where the OS (and /var/log) resides, not normally all that active, showing 100% utilization and dropping off sharply as soon as we fixed log_min_duration_statement.

It took a few minutes to track down, as we were originally alerted to application performance problems, but once we spotted the disk I/O metrics it didn’t take long to track down the errant postgresql.conf setting. That the disk jumped to 100% with so much log activity isn’t surprising, but the database resides entirely on separate disks. So why did it affect that so much?

### syslog() and the surprise on the socket

If you’re used to using syslog to send your log messages off to a separate server, you may be rather surprised by the above. At least I was; by default it’ll use UDP to transmit the messages, so an overloaded log server will simply result in the messages being dropped. Not ideal from a logging perspective, but it keeps things running if there’s a problem on that front. Locally, messages are submitted to a dgram UNIX socket at /dev/log for the syslog process to pick up and save to disk or relay off to an external system.

The AF_UNIX SOCK_DGRAM socket, it turns out, doesn’t behave just like its AF_INET UDP counterpart. Ordering of the datagrams is preserved and, more importantly here, a full buffer will block rather than drop the messages. As a result in the case above, between syslog’s file buffer and the log socket buffer, once the syslog() calls started blocking, each Postgres backend stopped handling traffic until its log messages made it out toward that slow SATA disk.

As of now, this system has the Postgres logs on the faster array, to mitigate it if there’s any logging problems in the future. But if you’re looking at leaning on syslog to help manage high volumes of log entries, just be aware that it doesn’t solve everything.
