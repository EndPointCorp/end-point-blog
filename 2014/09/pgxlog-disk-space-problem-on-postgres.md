---
author: Greg Sabino Mullane
title: Solving pg_xlog out of disk space problem on Postgres
github_issue_number: 1036
tags:
- postgres
date: 2014-09-25
---

<div class="separator" style="clear: both; padding-bottom: 30px; float:right; text-align: center;"><a href="/blog/2014/09/pgxlog-disk-space-problem-on-postgres/image-0-big.png" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/09/pgxlog-disk-space-problem-on-postgres/image-0.png"/></a><br/>
<em>pg_xlog with a dummy file</em><br/>
<small>(<a href="https://flic.kr/p/5Naet5">image</a> by <a href="https://www.flickr.com/photos/andrewmalone/">Andrew Malone</a>)</small></div>

Running out of disk space in the pg_xlog directory is a fairly common Postgres problem. This important directory holds the [WAL](https://www.postgresql.org/docs/current/static/wal-intro.html) (Write Ahead Log) files. (WAL files contain a record of all changes made to the database—​see the link for more details). Because of the near write‑only nature of this directory, it is often put on a separate disk. Fixing the out of space error is fairly easy: I will discuss a few remedies below.

When the pg_xlog directory fills up and new files cannot be written to it, Postgres will stop running, try to automatically restart, fail to do so, and give up. The pg_xlog directory is so important that Postgres cannot function until there is enough space cleared out to start writing files again. When this problem occurs, the Postgres logs will give you a pretty clear indication of the problem. They will look similar to this:

```
PANIC:  could not write to file "pg_xlog/xlogtemp.559": No space left on device
STATEMENT:  insert into abc(a) select 123 from generate_series(1,12345)
LOG:  server process (PID 559) was terminated by signal 6: Aborted
DETAIL:  Failed process was running: insert into abc(a) select 123 from generate_series(1,12345)
LOG:  terminating any other active server processes
WARNING:  terminating connection because of crash of another server process
DETAIL:  The postmaster has commanded this server process to roll back the current transaction and exit, because another server process exited abnormally an
d possibly corrupted shared memory.
HINT:  In a moment you should be able to reconnect to the database and repeat your command.
LOG:  all server processes terminated; reinitializing
LOG:  database system was interrupted; last known up at 2014-09-16 10:36:47 EDT
LOG:  database system was not properly shut down; automatic recovery in progress
FATAL:  the database system is in recovery mode
LOG:  redo starts at 0/162FE44
LOG:  redo done at 0/1FFFF78
LOG:  last completed transaction was at log time 2014-09-16 10:38:50.010177-04
PANIC:  could not write to file "pg_xlog/xlogtemp.563": No space left on device
LOG:  startup process (PID 563) was terminated by signal 6: Aborted
LOG:  aborting startup due to startup process failure
```
  

The “PANIC” seen above is the most severe [log_level Postgres has](https://www.postgresql.org/docs/current/static/runtime-config-logging.html#RUNTIME-CONFIG-SEVERITY-LEVELS), and it basically causes a “full stop right now!”. You will note in the above snippet that a normal SQL command caused the problem, which then caused all other Postgres processes to terminate. Postgres then tried to restart itself, but immediately ran into the same problem (no disk space) and thus refused to start back up. (The “FATAL” line above was another client trying to connect while all of this was going on.)

Before we can look at how to fix things, a little background will help. When Postgres is running normally, there is a finite number of WAL files (roughly twice the value of [checkpoint_segments](https://www.postgresql.org/docs/current/static/runtime-config-wal.html#RUNTIME-CONFIG-WAL-CHECKPOINTS)) that exist in the pg_xlog directory. Postgres deletes older WAL files, so the total number of files never climbs too high. When something prevents Postgres from removing the older files, the number of WAL files can grow quite dramatically, culminating in the out of space condition seen above. Our solution is therefore two-fold: fix whatever is preventing the old files from being deleted, and clear out enough disk space to allow Postgres to start up again.

The first step is to determine why the WAL files are not being removed. The most common case is a failing [archive_command](https://www.postgresql.org/docs/current/static/continuous-archiving.html). If this is the case, you will see archive-specific errors in your Postgres log. The usual causes are a failed network, downed remote server, or incorrect copying permissions. You might see some errors like this:

```
2013-05-06 23:51:35 EDT [19421]: [206-1] user=,db=,remote= LOG:  archive command failed with exit code 14
2013-05-06 23:51:35 EDT [19421]: [207-1] user=,db=,remote= DETAIL:  The failed archive command was: rsync --whole-file --ignore-existing --delete-after -a pg_xlog/000000010000006B00000016 backup:/archive/000000010000006B00000016
rsync: Failed to exec ssh: Permission denied (13)
# the above was from an actual bug report; the problem was SELinux
```
  

There are some other reasons why WAL would not be removed, such as failure to complete a checkpoint, but they are very rare so we will focus on archive_command. The quickest solution is to fix the underlying problem by bringing the remote server back up, fixing the permissions, etc. (To debug, try emulating the archive_command you are using with a small text file, as the postgres user. It is generally safe to ship non-WAL files to the same remote directory). If you cannot easily or quickly get your archive_command working, change it to a dummy command that always returns true:

```
# On Nix boxes:
archive_command = '/bin/true'
# On BSD boxes:
archive_command = '/usr/bin/true'
# On Windows boxes:
archive_command = 'REM'
```
  

This will allow the archive_command to complete successfully, and thus lets Postgres start removing older, unused WAL files. Note that changing the archive_command means you will need to change the archive_command back later and create fresh base backups, so do that as a last resort. Even after changing the archive_command, you cannot start the server yet, because the lack of disk space is still a problem. Here is what the logs would look like if you tried to start it up again:

```
LOG:  database system shutdown was interrupted; last known up at 2014-09-16 10:38:54 EDT
LOG:  database system was not properly shut down; automatic recovery in progress
LOG:  redo starts at 0/162FE44
LOG:  redo done at 0/1FFFF78
LOG:  last completed transaction was at log time 2014-09-16 10:38:50.010177-04
PANIC:  could not write to file "pg_xlog/xlogtemp.602": No space left on device
LOG:  startup process (PID 602) was terminated by signal 6: Aborted
LOG:  aborting startup due to startup process failure
```
  

At this point, you must provide Postgres a little bit of room in the partition/disk that the pg_xlog directory is in. There are four approaches to doing so: removing non-WAL files to clear space, moving the pg_xlog directory, resizing the partition it is on, and removing some of the WAL files yourself.

The easiest solution is to clear up space by removing any non-WAL files that are on the same partition. If you do not have pg_xlog on its own partition, just remove a few files (or move them to another partition) and then start Postgres. You don’t need much space—​a few hundred megabytes should be more than enough.

This problem occurs often enough that I have a best practice: create a dummy file on your pg_xlog partition whose sole purpose is to get deleted after this problem occurs, and thus free up enough space to allow Postgres to start! Disk space is cheap these days, so just create a 300MB file and put it in place like so (on Linux):

```
dd if=/bin/zero of=/pgdata/pg_xlog/DO_NOT_MOVE_THIS_FILE bs=1MB count=300
```
  

This is a nice trick, because you don’t have to worry about finding a file to remove, or determine which WALs to delete—​simply move or delete the file and you are done. Once things are back to normal, don’t forget to put it back in place.

The best way to get more room is to simply move your pg_xlog directory to another partition that has more space. Simply create a directory for it on the other partition, copy over all the files, then make pg_xlog a symlink to this new directory. (thanks to Bruce in the comments below)

Another way to get more space in your pg_xlog partition is to resize it. Obviously this is only an option if your OS/filesystem has been setup to allow resizing, but if it is, this is a quick and easy way to give Postgres enough space to startup again. No example code on this one, as the way to resize disks varies so much.

The final way is to remove some older WAL files. This should be done as a last resort! It is far better to create space, as removing important WAL files can render your database unusable! If you go this route, first determine which files are safest to remove. One way to determine this is to use the [pg_controldata program](https://www.postgresql.org/docs/current/static/app-pgcontroldata.html). Just run it with the location of your data directory as the only argument, and you should be rewarded with a screenful of arcane information. The important lines will look like this:

```
Latest checkpoint's REDO location:    0/4000020
Latest checkpoint's REDO WAL file:    000000010000000000000005
```
  

This second line represents the last WAL file processed, and it should be safe to remove any files older than that one. (Unfortunately, older versions of PostgreSQL will not show that line, and only the REDO location. While the canonical way to translate the location to a filename is with the pg_xlogfile_name() function, it is of little use in this situation, as it requires a live database! Thus, you may need another solution.) 

Once you know which WAL file to keep by looking at the pg_controldata output, you can simply delete all WAL files older than that one. (As Craig points out in the comments below, you can use the [pg_archivecleanup](https://www.postgresql.org/docs/9.3/static/pgarchivecleanup.html) program in standalone mode, which will actually work all the way back to version 8.0). As with all mass deletion actions, I recommend a three-part approach. First, back everything up. This could be as simple as copying all the files in the pg_xlog directory somewhere else. Second, do a trial run. This means seeing what the deletion would do without actually deleting the files. For some commands, this means using a --dry-run or similar option, but in our example below, we can simply leave out the “-delete” argument. Third, carefully perform the actual deletion. In our example above, we could clear the old WAL files by doing:

```
$ cp -r /pgdata/pg_xlog/* /home/greg/backups/
$ find -L /pgdata/pg_xlog -not -newer /pgdata/pg_xlog/000000010000000000000005 -not -samefile /pgdata/pg_xlog/000000010000000000000005| sort | less
$ find -L /pgdata/pg_xlog -not -newer /pgdata/pg_xlog/000000010000000000000005 -not -samefile /pgdata/pg_xlog/000000010000000000000005 -delete
```

It’s worth a mention that to find files **older** than the specific file it’s not sufficient to just do find -not -newer, because this would actually include the file being compared against, so deleting would be **disastrous** for your database cluster. Be sure to include the -not -samefile in the find command. Additionally, if you have a very busy system, it’s possible that the modification timestamps on the WAL files will have the same timestamp, and so might get removed if you just blindly -delete everything. This is why it is **very** important to **always** review the output before actually deleting things.

Once you have straightened out the archive_command and cleared out some disk space, you are ready to start Postgres up. You may want to adjust your pg_hba.conf to keep everyone else out until you verify all is working. When you start Postgres, the logs will look like this:

```
LOG:  database system was shut down at 2014-09-16 10:28:12 EDT
LOG:  database system is ready to accept connections
LOG:  autovacuum launcher started
```
  

After a few minutes, check on the pg_xlog directory, and you should see that Postgres has deleted all the extra WAL files, and the number left should be roughly twice the checkpoint_segments setting. If you adjusted pg_hba.conf, adjust it again to let clients back in. If you changed your archive_command to always return truth, remember to change it back as well as generate a new [base backup](https://www.postgresql.org/docs/current/static/app-pgbasebackup.html)

Now that the problem is fixed, how do you prevent it from happening again? First, you should use the [‘tail_n_mail’](https://bucardo.org/tail_n_mail/) program to monitor your Postgres log files, so that the moment the archive_command starts failing, you will receive an email and can deal with it right away. Making sure your pg_xlog partition has plenty of space is a good strategy as well, as the longer it takes to fill up, the more time you have to correct the problem before you run out of disk space.

Another way to stay on top of the problem is to get alerted when the pg_xlog directory starts filling up. Regardless of whether it is on its own partition or not, you should be using a standard tool like Nagios to alert you when the disk space starts to run low. You can also use the [check_postgres program](https://bucardo.org/check_postgres/check_postgres.pl.html#wal_files) to alert you when the number of WAL files in the pg_xlog directory goes above a specified number.

In summary, things you should do now to prevent, detect, and/or mitigate the problem of running out of disk space in pg_xlog:

1. Move pg_xlog to its own partition. This not only increases performance, but keeps things simple and makes things like disk resizing easier.
1. Create a dummy file in the pg_xlog directory as described above. This is a placeholder file that will prevent the partition from being completely filled with WAL files when 100% disk space is reached.
1. Use tail_n_mail to instantly detect archive_command failures and deal with them before they lead to a disk space error (not to mention the stale standby server problem!)
1. Monitor the disk space and/or number of WAL files (via check_postgres) so that you are notified that the WALs are growing out of control. Otherwise your first notification may be when the database PANICs and shuts down!

In summary, don’t panic if you run out of space. Do the steps above, and rest assured that no data corruption or data loss has occurred. It’s not fun, but there are far worse Postgres problems to run into! :)
