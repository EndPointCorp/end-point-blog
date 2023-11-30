---
author: Josh Williams
title: WAL-based Estimates For When a Record Was Changed
github_issue_number: 1238
tags:
- database
- postgres
date: 2016-07-01
---

I originally titled this: *Inferring Record Timestamps by Analyzing PITR Streams for Transaction Commits and Cross-Referencing Tuple xmin Values*. But that seemed a little long, though it does sum up the technique.

In other words, it’s a way to approximate an updated_at timestamp column for your tables when you didn’t have one in the first place.

PostgreSQL stores the timestamp of a transaction’s commit into the transaction log. If you have a hot standby server, you can see the value for the most-recently-applied transaction as the output of the pg_last_xact_replay_timestamp() function. That’s useful for estimating replication lag. But I hadn’t seen any other uses for it, at least until I came up with the hypothesis that all the available values could be extracted wholesale, and matched with the transaction ID’s stored along with every record.

If you’re on 9.5, there’s track_commit_timestamps in postgresql.conf, and combined with the pg_xact_commit_timestamp(xid) function has a similar result. But it can’t be turned on retroactively.

This can -- sort of. So long as you have those transaction logs, at least. If you’re doing Point-In-Time Recovery you’re likely to at least have some of them, especially more recent ones.

I tested this technique on a pgbench database on stock PostgreSQL 9.4, apart from the following postgresql.conf settings that (sort of) turn on WAL archival -- or at least make sure the WAL segments are kept around:

```plain
wal_level = archive
archive_mode = on
archive_command = '/bin/false'
```

We’ll be using the **pg_xlogdump** binary to parse those WAL segments, available from 9.3 on. If you’re on an earlier version, the [older xlogdump code](https://github.com/snaga/xlogdump) will work.

Once pgbench has generated some traffic, then it’s time to see what’s contained in the WAL segments we have available. Since I have them all I went all the way back to the beginning.

```shell
$ pg_xlogdump -p pg_xlog/ --start 0/01000000 --rmgr=Transaction
rmgr: Transaction len (rec/tot):     12/    44, tx:          3, lsn: 0/01006A58, prev 0/01005CA8, bkp: 0000, desc: commit: 2016-05-15 22:32:32.593404 EDT
rmgr: Transaction len (rec/tot):     12/    44, tx:          4, lsn: 0/01008BC8, prev 0/01008A60, bkp: 0000, desc: commit: 2016-05-15 22:32:32.664374 EDT
rmgr: Transaction len (rec/tot):     12/    44, tx:          5, lsn: 0/01012EA8, prev 0/01012E58, bkp: 0000, desc: commit: 2016-05-15 22:32:32.668813 EDT
(snip)
rmgr: Transaction len (rec/tot):     12/    44, tx:       1746, lsn: 0/099502D0, prev 0/099501F0, bkp: 0000, desc: commit: 2016-05-15 22:55:12.711794 EDT
rmgr: Transaction len (rec/tot):     12/    44, tx:       1747, lsn: 0/09951530, prev 0/09951478, bkp: 0000, desc: commit: 2016-05-15 22:55:12.729122 EDT
rmgr: Transaction len (rec/tot):     12/    44, tx:       1748, lsn: 0/099518D0, prev 0/099517F0, bkp: 0000, desc: commit: 2016-05-15 22:55:12.740823 EDT
pg_xlogdump: FATAL:  error in WAL record at 0/99518D0: record with zero length at 0/9951900
```

The last line just indicates that we’ve hit the end of the transaction log records, and it’s written to stderr, so it can be ignored. Otherwise, that output contains everything we need, we just need to shift around the components so we can read it back into Postgres. Something like this did the trick for me, and let me import it directly:

```sql
$ pg_xlogdump -p pg_xlog/ --start 0/01000000 --rmgr=Transaction | awk -v Q=\' '{sub(/;/, ""); print $8, Q$17, $18, $19Q}' > xids

postgres=# CREATE TABLE xids (xid xid, commit timestamptz);
CREATE TABLE
postgres=# \copy xids from xids csv
COPY 1746
```

At which point it’s a simple join to pull in the commit timestamp records:

```sql
postgres=# select xmin, aid, commit from pgbench_accounts inner join xids on pgbench_accounts.xmin = xids.xid;
 xmin |  aid   |            commit             
------+--------+-------------------------------
  981 | 252710 | 2016-05-15 22:54:34.03147-04
 1719 | 273905 | 2016-05-15 22:54:35.622406-04
 1183 | 286611 | 2016-05-15 22:54:34.438701-04
 1227 | 322132 | 2016-05-15 22:54:34.529027-04
 1094 | 331525 | 2016-05-15 22:54:34.26477-04
 1615 | 383361 | 2016-05-15 22:54:35.423995-04
 1293 | 565018 | 2016-05-15 22:54:34.688494-04
 1166 | 615272 | 2016-05-15 22:54:34.40506-04
 1503 | 627740 | 2016-05-15 22:54:35.199251-04
 1205 | 663690 | 2016-05-15 22:54:34.481523-04
 1585 | 755566 | 2016-05-15 22:54:35.368891-04
 1131 | 766042 | 2016-05-15 22:54:34.33737-04
 1412 | 777969 | 2016-05-15 22:54:34.953517-04
 1292 | 818934 | 2016-05-15 22:54:34.686746-04
 1309 | 940951 | 2016-05-15 22:54:34.72493-04
 1561 | 949802 | 2016-05-15 22:54:35.320229-04
 1522 | 968516 | 2016-05-15 22:54:35.246654-04
```

