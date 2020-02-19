---
author: Jon Jensen
gh_issue_number: 272
tags: aws, cloud, database, hosting, postgres, scalability
title: PostgreSQL EC2/EBS/RAID 0 snapshot backup
---

One of our clients uses [Amazon Web Services](https://aws.amazon.com/) to host their production application and database servers on EC2 with EBS (Elastic Block Store) storage volumes. Their main database is [PostgreSQL](/technology/postgresql).

A big benefit of Amazon’s cloud services is that you can easily add and remove virtual server instances, storage space, etc. and pay as you go. One known problem with Amazon’s EBS storage is that it is much more I/O limited than, say, a nice SAN.

To partially mitigate the I/O limitations, they’re using 4 EBS volumes to back a Linux software RAID 0 block device. On top of that is the xfs filesystem. This gives roughly 4x the I/O throughput and has been effective so far.

They ship WAL files to a secondary server that serves as warm standby in case the primary server fails. That’s working fine.

They also do nightly backups using pg_dumpall on the master so that there’s a separate portable (SQL) backup not dependent on the server architecture. The problem that led to this article is that extra I/O caused by pg_dumpall pushes the system beyond its I/O limits. It adds both reads (from the PostgreSQL database) and writes (to the SQL output file).

There are several solutions we are considering so that we can keep both binary backups of the database and SQL backups, since both types are valuable. In this article I’m not discussing all the options or trying to decide which is best in this case. Instead, I want to consider just one of the tried and true methods of backing up the binary database files on another host to offload the I/O:

1. Create an atomic snapshot of the block devices
1. Spin up another virtual server
1. Mount the backup volume
1. Start Postgres and allow it to recover from the apparent “crash” the server had (since there wasn’t a clean shutdown of the database before the snapshot
1. Do whatever pg_dump or other backups are desired
1. Make throwaway copies of the snapshot for QA or other testing

The benefit of such snapshots is that you get an exact backup of the database, with whatever table bloat, indexes, statistics, etc. exactly as they are in production. That’s a big difference from a freshly created database and import from pg_dump.

The difference here is that we’re using 4 EBS volumes with RAID 0 striped across them, and there isn’t currently a way to do an atomic snapshot of all 4 volumes at the same time. So it’s no longer “atomic” and who knows what state the filesystem metadata and the file data itself would be in?

Well, why not try it anyway? Filesystem metadata doesn’t change that often, especially in the controlled environment of a Postgres data volume. Snapshotting within a relatively short timeframe would be pretty close to atomic, and probably look to the software (operating system and database) like some kind of strange crash since some EBS volumes would have slightly newer writes than others. But aren’t all crashes a little unpredictable? Why shouldn’t the software be able to deal with that? Especially if we have Postgres make a checkpoint right before we snapshot.

I wanted to know if it was crazy or not, so I tried it on a new set of services in a separate AWS account. Here are the notes and some details of what I did:

1\. Created one EC2 image:

Amazon EC2 Debian 5.0 lenny AMI built by Eric Hammond<br>
Debian AMI ID ami-4ffe1926 (x86_64)<br>
Instance Type: High-CPU Extra Large (c1.xlarge) — 7 GB RAM, 8 CPU cores

2\. Created 4 x 10 GB EBS volumes

3\. Attached volumes to the image

4\. Created software RAID 0 device:

```bash
mdadm -C /dev/md0 -n 4 -l 0 -z max /dev/sdf /dev/sdg /dev/sdh /dev/sdi
```

5\. Created XFS filesystem on top of RAID 0 device:

```bash
mkfs -t xfs -L /pgdata /dev/md0
```

6\. Set up in /etc/fstab and mounted:

```bash
mkdir /pgdata
# edit /etc/fstab, with noatime
mount /pgdata
```

7\. Installed PostgreSQL 8.3

8\. Configured postgresql.conf to be similar to primary production database server

9\. Created empty new database cluster with data directory in /pgdata

10\. Started Postgres and imported a play database (from public domain census name data and Project Gutenberg texts), resulting in about 820 MB in data directory

11\. Ran some bulk inserts to grow database to around 5 GB

12\. Rebooted EC2 instance to confirm everything came back up correctly on its own

13\. Set up two concurrent data-insertion processes:

- 50 million row insert based on another local table (INSERT INTO ... SELECT ...), in a single transaction (hits disk hard, but nothing should be visible in the snapshot because the transaction won’t have committed before the snapshot is taken)

- Repeated single inserts in autocommit mode (Python script writing INSERT statements using random data from /usr/share/dict/words piped into psql), to verify that new inserts made it into the snapshot, and no partial row garbage leaked through

14\. Started those “beater” jobs, which mostly consumed 2-3 CPU cores

15\. Manually inserted a known test row and created a known view that should appear in the snapshot

16\. Started Postgres’s backup mode that allows for copying binary data files in a non-atomic manner, which also does a CHECKPOINT and thus also a filesystem sync:

```sql
SELECT pg_start_backup('raid_backup');
```

17\. Manually inserted a 2nd known test row & 2nd known test view that I don’t want to appear in the snapshot after recovery

18\. Ran snapshot script which calls ec2-create-snapshot on each of the 4 EBS volumes—​during first run, run serially quite slowly taking about 1 minute total; during second run, run in parallel such that the snapshot point was within 1 second for all 4 volumes

19\. Tell Postgres the backup’s over:

```sql
SELECT pg_stop_backup();
```

20\. Ran script to create new EBS volumes derived from the 4 snapshots (which aren’t directly usable and always go into S3), using `ec2-create-volume --snapshot`

21\. Run script to attach new EBS volumes to devices on the new EC2 instance using `ec2-attach-volume`

22\. Then, on the new EC2 instance for doing backups:

- `mdadm --assemble --scan`
- `mount /pgdata`
- Start Postgres
- Count rows on the 2 volatile tables; confirm that the table with the in-process transaction doesn’t show any new rows, and that the table getting individual rows committed to reads correctly
- `VACUUM VERBOSE` — and confirm no errors or inconsistencies detected
- `pg_dumpall` # confirmed no errors and data looks sound

It worked! No errors or problems, and pretty straightforward to do.

Actually before doing all the above I first did a simpler trial run with no active database writes happening, and didn’t make any attempt for the 4 EBS snapshots to happen simultaneously. They were actually spread out over almost a minute, and it worked fine. With the confidence that the whole thing wasn’t a fool’s errand, I then put together the scripts to do lots of writes during the snapshot and made the snapshots run in parallel so they’d be close to atomic.

There are lots of caveats to note here:

- This is an experiment in progress, not a how-to for the general public.
- The data set that was snapshotted was fairly small.
- Two successful runs, even with no failures, is not a very big sample set. :)
- I didn’t use Postgres’s point-in-time recovery (PITR) here at all—​I just started up the database and let Postgres recover from an apparent crash. Shipping over the few WAL logs from the master collected during the pg_backup run *after* the snapshot copying is complete would allow a theoretically fully reliable recovery to be made, not just a practically non-failing recovery as I did above.

So there’s more work to be done to prove this technique viable in production for a mission-critical database, but it’s a promising start worth further investigation. It shows that there *is* a way to back up a database across multiple EBS volumes without adding noticeably to its I/O load by utilizing the Amazon EBS data store’s snapshotting and letting a separate EC2 server offload the I/O of backups or anything else we want to do with the data.
