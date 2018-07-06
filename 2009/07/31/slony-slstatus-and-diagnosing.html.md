---
author: Selena Deckelmann
gh_issue_number: 179
tags: postgres
title: Slony, sl_status and diagnosing a particular type of lag
---



During some routine checking on a [slony](http://www.slony.info/) cluster, Greg noticed something curious. Replication was still happening between the master and a couple slaves, but we were seeing our indicator for lag inside of slony increasing. 

To check out the status of slony replication, you will typically take a look at the view ‘sl_status’: 

```sql
mydatabase=# select * from sl_status; 
 st_origin | st_received | st_last_event |      st_last_event_ts      | st_last_received |    st_last_received_ts     | st_last_received_event_ts | st_lag_num_events |       st
_lag_time       
-----------+-------------+---------------+----------------------------+------------------+----------------------------+---------------------------+-------------------+---------
----------------
         2 |           1 |       2697511 | 2008-04-30 02:40:06.034144 |          2565031 | 2008-04-14 15:31:32.897165 | 2008-04-14 16:24:08.81738 |            132480 | 15 days 
10:16:03.060499
(1 row)
```

This view pulls data out of sl_event and sl_confirm, two tables that keep track of the forward progress of replication. Every time there is an event—​SYNCs, DDL changes, slony administrative events—​a row is added to sl_event. Slony is very chatty and so all of the slaves send events to each other, as well as the master. (That statement is a simplification, and it is possible to make some configuration changes that reduce the traffic, but in general, this is what people who set up slony will see.)

Broken down, the columns are: 

**st_origin**: the local slony system

**st_received**: the slony instance that sent an event

**st_last_event**: the sequence number of the last event received from that origin/received pair

**st_last_event_ts**: the timestamp on the last event received

**st_last_received**: the sequence number of the last sl_event + sl_confirm pair received

**st_last_received_ts**: the timestamp on the sl_confirm in that pair

**st_last_received_event_ts**: the timestamp on the sl_event in that pair

**st_lag_num_events**: difference between st_last_event and st_last_received

**st_lag_time**: difference between st_last_event_ts and st_last_received_ts

Depending on the type of event, a row might be added to sl_confirm immediately (by the same thread that created the event), or this may be created separately by another process. The important thing here is that there is a separation between sl_event and sl_confirm, so it is possible for sl_event SYNCs (replication events) to continue to come through and be applied to the server, without the sl_confirm rows being eventually created.

We have a monitor which checks the status of replication by looking at a recently added value on the master and comparing that to what is on the slave. This works well for workloads that are primarily append-only. So, that monitor thought replication was working fine, even though the lag was increasing steadily.

sl_event and sl_confirm tables are periodically cleaned up by cleanupEvent(), automatically by slony. Typically, this function is run every 100 seconds. When the slon process kicks it off, it checks to see what the newest confirmed events are, deletes old event records, and old confirm rows. 

When confirms stop coming through, sl_events can’t be cleaned up on the affected server (because they haven’t been confirmed!). Depending on how active your servers are, this will eat up disk space. But you’ve got disk space monitors in place, right? :)

So, how do you fix the problem when the confirms stop coming through? 

I had a look at process tables on all the slon slaves, and noticed that on the two lagged systems, there was no incoming connection from the master slony system. The fix: restart slony on the master so that it could reconnect.

There’s a couple things I wished that slony would have told me: 

- Notification on the slave that it no longer had its connection back to the master. We’ll set up our own monitors to detect that this connection no longer exists, but it would be much nicer for slony to warn about this. Additionally, it would be nice to be able to re-connect to a single slave without restarting slon entirely.
- More explanation about sl_confirm and likely causes of failed confirmations. I hope I’ve shed a little light with this blog post.

The [documentation for setting up slony](http://www.slony.info/documentation/addthings.html) is very good, but the troubleshooting information is lacking around events and confirmations, and how each type of event and confirmation actually happens. I’m happy to be proven wrong—​so please leave pointers in the comments!


