---
author: Josh Tolley
gh_issue_number: 111
tags: postgres
title: pg_controldata
---



PostgreSQL ships with several utility applications to administer the server life cycle and clean up in the event of problems. I spent some time lately looking at what is probably one of the least well known of these, [pg_controldata](http://www.postgresql.org/docs/current/static/app-pgcontroldata.html). This useful utility dumps out a number of useful tidbits about a database cluster, given the data directory it should look at. Here's an example from a little-used 8.3.6 instance:

```nohighlight
josh@eddie:~$ pg_controldata
pg_control version number:            833
Catalog version number:               200711281
Database system identifier:           5291243377389434335
Database cluster state:               in production
pg_control last modified:             Mon 09 Mar 2009 04:05:23 PM MDT
Latest checkpoint location:           0/B70E5B9C
Prior checkpoint location:            0/B70E5B5C
Latest checkpoint's REDO location:    0/B70E5B9C
Latest checkpoint's TimeLineID:       1
Latest checkpoint's NextXID:          0/307060
Latest checkpoint's NextOID:          37410
Latest checkpoint's NextMultiXactId:  1
Latest checkpoint's NextMultiOffset:  0
Time of latest checkpoint:            Fri 06 Mar 2009 02:27:02 PM MST
Minimum recovery ending location:     0/0
Maximum data alignment:               4
Database block size:                  8192
Blocks per segment of large relation: 131072
WAL block size:                       8192
Bytes per WAL segment:                16777216
Maximum length of identifiers:        64
Maximum columns in an index:          32
Maximum size of a TOAST chunk:        2000
Date/time type storage:               floating-point numbers
Maximum length of locale name:        128
LC_COLLATE:                           en_US.UTF-8
LC_CTYPE:                             en_US.UTF-8
```

I can't claim to speak with authority on all these data, but leave it as an exercise to the reader to determine the meaning of those that appear most captivating. One of pg_controldata's more interesting features is that it doesn't have to actually connect to anything; it reads everything from the disk. That means you can use it on databases in the middle of WAL recovery, even though you can't actually query the recovering database. The [check_postgres.pl](http://bucardo.org/check_postgres/) script uses this unique capability to make inferences about the health of a WAL replica, specifically by making sure checkpoints happen fairly regularly. pg_controldata requires only one argument, the data directory of the PostgreSQL instance you're interested in, and that only if you haven't already set the PGDATA environment variable.


