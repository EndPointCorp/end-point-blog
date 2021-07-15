---
author: David Christensen
title: PostgreSQL odd checkpoint failure
github_issue_number: 350
tags:
- database
- postgres
date: 2010-09-14
---



Nothing strikes fear into the heart of a DBA like error messages, particularly ones which indicate that there may be data corruption. One such situation happened recently to us, when we ran into a recent unusual situation in an upgrade to PostgreSQL 8.1.21. We had updated the software and manually been running a REINDEX DATABASE command, when we started to notice some errors being reported on the front-end. We decided to dump the database in question to ensure we had a backup to return to, however we still ended up with more messages:

```bash
  pg_dump -Fc database1 > pgdump.database1.archive

  pg_dump: WARNING:  could not write block 1 of 1663/207394263/443523507
  DETAIL:  Multiple failures --- write error may be permanent.
  pg_dump: ERROR:  could not open relation 1663/207394263/443523507: No such file or directory
  CONTEXT:  writing block 1 of relation 1663/207394263/443523507
  pg_dump: SQL command to dump the contents of table "table1" failed: PQendcopy() failed.
  pg_dump: Error message from server: ERROR:  could not open relation 1663/207394263/443523507: No such file or directory
  CONTEXT:  writing block 1 of relation 1663/207394263/443523507
  pg_dump: The command was: COPY public."table1" (id, field1, field2, field3) TO stdout;
```

Looking at the pg_database contents revealed that 207394263 was not even the database in question. I connected to the aforementioned database and looked for a relation that matched that pg_class.oid, and barring that pg_class.relfilenode. This search revealed nothing. So where was the object itself living, and why were we getting this message?

We decided that since it appeared that something was awry with the database system in general, that we should take this opportunity to dump the tables in question. I proceeded to write a quick script to go through the database tables and dump each one individually using pg_dump’s -t option. This worked for some of the tables, but not all of them, which would die with the same error. Looking at the pg_class.relpages field for the non-dumpable tables revealed that these were all the larger tables in the database. Obviously not good, since this is where the bulk of the data lay. However, we also noticed that the message that we got referenced the exact same filesystem path, so it appeared to be something separate from the table that was being dumped.

After some advice on IRC, we reviewed the logs for checkpoint logging, which revealed that checkpoints had been failing. This further meant that the database was in a state such that it could not be shut down cleanly, had we wanted to try to restart to see if that cleared up the flakiness. This further meant that we’d only be able to shutdown via a hard kill, which is definitely something to avoid, WAL or not, particularly since there had not been a checkpoint for some time. A manual CHECKPOINT further failed after a timeout.

Before we went down the road of forcing a hard server shutdown, we ended up just touching the specific relation path in question into existence and then running a CHECKPOINT. This time since the file existed, it was able to complete the checkpoint, and restore working order to the database. We successfully (and quickly) ran a full pg_dump, and went about the task of manually vetting a few of the affected tables, etc.

Our working theory for this is that somehow there was a dirty buffer that referenced a relation that no longer existed, and hence when the there was a checkpoint or other event which attempted to flush shared_buffers (i.e., the loading of a large relation which would require a flush of Least Recently Used pages as in the pg_dump case), the flush attempt for the missing relation failed, which aborted the checkpoint/other action.

After the file existed and PostgreSQL had successfully synched to disk, it was a single two-block file, of which the first block was completely empty and the second block looked like an index page (due to the layout/contents of the data). The most suggestive cause was that had been an interrupted REINDEX earlier in the day. Since this machine was showing no other signs of data corruption and everything else seemed reasonable, our best guess is that there was some race condition that had caused the relation’s data to exist in memory even while the canceled REINDEX ensured that the actual relfile and the pg_class rows did not exist for the buffer.


