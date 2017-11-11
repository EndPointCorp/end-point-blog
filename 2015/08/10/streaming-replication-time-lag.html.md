---
author: Josh Williams
gh_issue_number: 1149
tags: monitoring, nagios, postgres, sysadmin
title: Streaming Replication time lag monitoring added to check_postgres
---



<a href="https://www.flickr.com/photos/56278705@N05/8548635299/in/photolist-e2pZrM-5uDPns-71jap-5rbtCP-bua9Dn-p3KzAA-aJh7uD-7bgsx6-nvBRCq-4B2ng3-aSheyH-vADsy-kHby-9pZZVn-fMrcKa-p2egJ5-AnRMU-EXrr-eTYP7U-5ayMi6-sn5ecN-kCFz-bXANVG-46YU7g-gxoMCB-qGxWFt-dY3Cyx-68giiZ-wJ7e7-6SkM1-JZ3a6-a6otTh-9c9xPc-pHcHM2-wQNQD-oUrYYB-bR6BR8-qoAwB6-LzGU1-cjZBEJ-c5WzkQ-4JYvg5-ewJe9D-gVtTRu-U3oT-4gtg8Q-cjFWdQ-7brR3P-7bvDHy-9bTMZN/" title="Clocks at Great Northern in Manchester, UK"><img alt="Clocks at Great Northern in Manchester, UK" height="240" src="/blog/2015/08/10/streaming-replication-time-lag/image-0.jpeg" width="195"/></a>

I almost let this one sneak past!  Guess I need to do some lag monitoring on myself.  About a month or so ago, a new version of [check_postgres](https://bucardo.org/wiki/Check_postgres) was released, and that includes a bit of code I wrote.  While the patch has been available in the git checkout for a while, now that it's in the official release and will start appearing in repos (if it hasn't already) it's probably worth writing up a quick note describing its reasoning and usage.

What's the feature?  [Time-based replication monitoring in the hot_standby_delay action.](https://github.com/bucardo/check_postgres/commit/6b765c839eaf80499f68d412a897f61f11db9bfc)  This was something that had been a long-standing item on my personal TODO list, and happened to scratch the itch of a couple of clients at the time.

Previously it would only take an integer representing how many bytes of WAL data the master could be ahead of a replica before the threshold is crossed:

```
check_hot_standby_delay --dbhost=master,replica1 --critical=16777594
```

This is certainly useful for, say, keeping an eye on whether you're getting close to running over your wal_keep_segments value.  Of course it can also be used to indicate whether the replica is still processing WAL, or has become stuck for some reason.  But for the (arguably more common) problem of determining whether a replica is falling too far behind determining what byte thresholds to use, beyond simply guessing, isn't easy to figure out.

Postgres 9.1 introduced a handy function to help solve this problem: pg_last_xact_replay_timestamp().  It measures a slightly different thing than the pg_last_xlog_* functions the action previously used.  And it's for that reason that the action now has a more complex format for its thresholds:

```
check_hot_standby_delay --dbhost=master,replica1 --critical="16777594 and 5 min"
```

For backward compatibility, of course, it'll still take an integer and work the same as it did before.  Or alternatively if you only want to watch the chronological lag, you could even give it just a time interval, '5 min', and the threshold only takes the transaction replay timestamp into account.  But if you specify both, as above, then both conditions must be met before the threshold activates.

Why?  Well, that gets in to bit about the measurement of slightly different things.  As its name implies, pg_last_xact_replay_timestamp() returns the timestamp of the last transaction it received and replayed.  That's fine if you have a database cluster that's constantly active 24 hours a day.  But not all of them are.  Some have fluctuating periods of activity, perhaps busy during the business day and nearly idle during the night.  In other words, if the master isn't processing any transactions, that last transaction timestamp doesn't change.

Then there's the other end of the scale.  With the SSD's/high speed disk arrays a master server may in a short interval process more transaction data than it can send over a network wire.  For example, we have a system that runs an ETL process between two local databases on a master server, and generates a ton of transaction log data in a short amount of time.  However even if it has many megabytes of WAL data to transmit, the replicas never get any more than a handful of seconds behind and soon catch up.

Both conditions on their own are fine.  It's when both conditions are simultaneously met, when the replica is behind in both transaction log and it hasn't seen a chronologically recent transaction, that's when you know something is going wrong with your replication connection.

Naturally, this updated check also includes the chronological lag metric, so you can feed that into Graphite, or some other system of choice.  Just make sure you're system handles the new metric; our Nagios system seemed to ignore it until the RRD data for the check was cleared and recreated.

Oh, and make sure your clocks are in sync.  The timestamp check executes only on the replica, so any difference between its clock and the master's can show up as skew here.  ntpd is an easy way to keep everything mostly synchronized, but if you really want to be sure, check_postgres also has a timesync action.
