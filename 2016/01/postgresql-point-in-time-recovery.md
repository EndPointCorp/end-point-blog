---
author: David Christensen
title: 'PostgreSQL Point-in-time Recovery: An Unexpected Journey'
github_issue_number: 1195
tags:
- database
- postgres
- replication
- disaster-recovery
date: 2016-01-15
---

With all the major changes and improvements to PostgreSQL’s native replication system through the last few major releases, it’s easy to forget that there can be benefits to having some of the tried-and-true functionalities from older PostgreSQL versions in place.

In particular, with the ease of setting up hot standby/​streaming replication, it’s easy to get replication going with almost no effort. Replication is great for redundancy, scaling, and backups. However, it does not solve all potential data-loss problems. For best results it should be used in conjunction with [Point-in-time Recovery](https://www.postgresql.org/docs/current/static/continuous-archiving.html) (PITR) and the archiving features of PostgreSQL.

### Background

We recently had a client experience a classic blunder with their database, namely, that of performing a manual UPDATE of the database without wrapping it in a transaction block and validating the changes before committing. The table in question was the main table in the application, and the client had done an unqualified UPDATE, unintentionally setting a specific field to a constant value instead of targetting the specific row they thought they were going for.

Fortunately, the client had backups. Unfortunately the backups themselves would not be enough; being a snapshot of the data earlier in the day, we would have lost all changes made throughout the day.

This resulted in a call to us to help out with the issue. We fortunately had information about precisely when the errant UPDATE took place, so we were able to use this information to help target a PITR-based restore.

### The Approach

Since we did not want to lose other changes made in this database cluster either before or after this mistake, we came up with the following strategy which would let us keep the current state of the database but just recover the field in question:

1. Create a parallel cluster for recovery.
2. Load the WAL until just before the time of the event.
3. Dump the table in question from the recovery cluster.
4. Load the table in the main cluster with a different name.
5. Use UPDATE FROM to update the field values for the table with their old values based on the table’s primary key.

In practice, this worked out pretty well, though of course there were some issues that had to be worked around.

PostgreSQL’s PITR relies on its WAL archiving mechanism combined with taking regular base backups of the data directory. As part of the archive setup, you choose the strategies (such as the frequency of the base backups) and ensure that you can recover individual WAL segment files when desired.

In order for the above strategy to work, you need hardware to run this on. The client had proposed their standby server which was definitely equipped to handle this and did not have much load. The client had initially suggested that we could break the replication, but we recommended against that, due to both having sufficient disk space and being able to avoid future work and risk by having to rebuild the replica after this stage.

We copied over the daily base backup into its own directory/​mount point here, adjusted the recovery.conf file to point to the local WAL directory, and copied the necessary WAL files from the archive location to the pg_xlog directory of the new cluster. We also had to adjust a few parameters in the new cluster, most notably the “port” parameter to run the cluster on a different port. We also used the timestamp of the incident as a target for the recovery.conf’s recovery_target_time setting. After starting up the new cluster and letting things process, we were able to dump the table in question and finish the recovery on the master.

Some issues **did** come up for us that needed expert-level knowledge of the system, as well as having some good luck in the timing if the event. We had to locate several of the WAL files in the initial archive on the primary server due to some issues with the (inherited by us) configuration. Also due to the timing of the event and the amount of time it took to create the parallel cluster, we successfully were able to create the new instance before the next nightly base backup was run, which was fortunate, because it otherwise would have resulted in our inability to resolve this issue. (The client had things configured to keep only a single base backup around.)

### Lessons Learned

With any issue, there is a takeaway, so what are those here?

- Always use explicit transactions when manually modifying data, or modify your production environment’s `~/.psqlrc` to add `\set AUTOCOMMIT off`.
- Not all data-loss situations can be fixed with replication alone—​Point in Time Recovery is absolutely still relevant these days.
- It helps to have a PostgreSQL expert on hand day and night. End Point offers 24x7 PostgreSQL support, which you can engage by getting a hold of us [here](/contact).
