---
author: Greg Sabino Mullane
gh_issue_number: 1059
tags: postgres
title: When Postgres will not start
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2014/11/24/when-postgres-will-not-start/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/11/24/when-postgres-will-not-start/image-0.jpeg"/></a><br/><small>
<a href="https://flic.kr/p/7BA6ND">Photo</a>
 by <a href="https://www.flickr.com/photos/archetypefotografie/">Vincent_AF</a></small></div>

One of the more frightening things you can run across as a DBA (whether using Postgres or a lesser system) is a crash followed by a complete failure of the database to start back up. Here's a quick rundown of the steps one could take when this occurs.

The first step is to look at why it is not starting up by examining the logs. Check your normal Postgres logs, but also check the filename passed to the **--log** argument for
[pg_ctl](http://www.postgresql.org/docs/current/static/app-pg-ctl.html), as Postgres may not have even gotten far enough to start normal logging. Most of the time these errors are not serious, are fairly self-explanatory, and can be cured easily - such as
[running out of disk space](/blog/2014/09/25/pgxlog-disk-space-problem-on-postgres). When in doubt, search the web or ask in the
[#postgresql IRC channel](http://www.postgresql.org/community/irc/) and you will most likely find a solution.

Sometimes the error is more serious, or the solution is not so obvious. Consider this problem someone had in the #postgresql channel a while back:

```
LOG: database system was interrupted while in recovery at 2014-11-03 12:43:09 PST
HINT: This probably means that some data is corrupted and you will have to use the last backup for recovery.
LOG: database system was not properly shut down; automatic recovery in progress
LOG: redo starts at 1883/AF9458E8
LOG: unexpected pageaddr 1882/BAA7C000 in log file 6275, segment 189, offset 10993664
LOG: redo done at 1883/BDA7A9A8
LOG: last completed transaction was at log time 2014-10-25 17:42:53.836929-07
FATAL: right sibling's left-link doesn't match: block 6443 links to 998399 instead of expected 6332 in index "39302035"
```

As you can see, Postgres has already hinted you may be in deep trouble with its suggestion to use a backup. The Postgres daemon completely fails to start because an index is corrupted. Postgres has recognized that the [B-tree](https://en.wikipedia.org/wiki/B-tree) index no longer looks like a B-tree should and bails out.

For many errors, the next step is to attempt to start Postgres in single-user mode. This is similar to “Safe mode” in Windows - it starts Postgres in a simplified, bare-bones fashion, and is intended primarily for debugging issues such as a failed startup. This mode is entered by running the [“postgres” executable](http://www.postgresql.org/docs/current/static/app-postgres.html) directly (as opposed to having pg_ctl do it), and passing specific arguments. Here is an example:

```
$ /usr/bin/postgres --single -D /var/lib/pgsql93/data -P -d 1
```

This starts up the “postgres” program (used to be “postmaster”), enters single-user mode, specifies where the data directory is located, turns off system indexes, and sets the debug output to 1. After it is run, you will have a simple prompt. From here you can fix your problem, such as reindexing bad indexes, that may have caused a normal startup to fail. Use CTRL-d to exit this mode:

```
$ /usr/bin/postgres --single -D /var/lib/pgsql93/data -P -d 1
NOTICE:  database system was shut down at 2014-11-20 16:51:26 UTC
DEBUG:  checkpoint record is at 0/182B5F8
DEBUG:  redo record is at 0/182B5F8; shutdown TRUE
DEBUG:  next transaction ID: 0/1889; next OID: 12950
DEBUG:  next MultiXactId: 1; next MultiXactOffset: 0
DEBUG:  oldest unfrozen transaction ID: 1879, in database 1
DEBUG:  oldest MultiXactId: 1, in database 1
DEBUG:  transaction ID wrap limit is 2147485526, limited by database with OID 1
DEBUG:  MultiXactId wrap limit is 2147483648, limited by database with OID 1

PostgreSQL stand-alone backend 9.3.5
backend> [CTRL-d]
NOTICE:  shutting down
NOTICE:  database system is shut down
```

If you are not able to fix things with single-user mode, it's time to get serious. This would be an excellent time to make a complete file-level backup. Copy the entire data directory to a different server or at least a different partition. Make sure you get everything in the pg_xlog directory as well, as it may be symlinked elsewhere.

Time to use pg_resetxlog, right? No, not at all. Use of the [pg_resetxlog utility](http://www.postgresql.org/docs/current/static/app-pgresetxlog.html) should be done as an absolute last resort, and there are still some things you should try first. Your problem may have already been solved - so the next step should be to upgrade Postgres to the latest revision. With Postgres, a revision (the last number in the version string) is always reserved for bug fixes only. Further, changing the revision is almost always as simple as installing a new binary. So if you are running Postgres version 9.0.3, upgrade to the latest in the 9.0 series (9.0.18 as of this writing). Check the release notes, make the upgrade, and try to start up Postgres.

Still stumped? Consider asking for help. For fast, free help, try the #postgresql IRC channel. For slightly slower free help, try the [pgsql-general mailing list](http://www.postgresql.org/list/). For both of these options, the majority of the subscribers are clustered near the US Eastern time zone, so response times will be faster at 3PM New York time versus 3AM New York time. For paid help, you can find a Postgres expert (such as [End Point!](/technology/postgresql)) at the [list of professional services](http://www.postgresql.org/support/professional_support/) at postgresql.org,

The next steps depend on the error, but another route is to hack the source code for Postgres to work around the error preventing the startup. This could mean, for example, changing a FATAL exception to an WARNING, or other trickery. This is expert-level stuff, to be sure, but done carefully can still be safer than pg_resetxlog. If possible, try this on a copy of the data!

If you have done everything else, it is time to attempt using pg_resetxlog. Please make sure you read the manual page about it before use. Remember this is a non-reversible, possibly data-destroying command! However, sometimes it is the only thing that will work.

If you did manage to fix the problem - at least enough to get Postgres to start - the very next item is to make a complete logical backup of your database. This means doing a full pg_dump right away. This is especially important if you used pg_resetxlog. Dump everything, then restore it into a fresh Postgres cluster (upgrading to the latest revision first if needed!). The pg_dump will not only allow you to create a clean working version of your database, but is a great way to check on the integrity of your data, as it by necessity examines every row of data you have. It will *not* check on the sanity of your indexes, but there are other ways to do that, the simplest being to do a
[REINDEX DATABASE](http://www.postgresql.org/docs/current/static/sql-reindex.html) on each database in your cluster.

All of these steps, including pg_resetxlog, may or may not help. In the “left-link doesn't match” example at the top, nothing was able to fix the problem (not single-user mode, nor a more recent revision, nor pg_resetxlog). It's possible that the data could have been recovered by hacking the source code or using tools to extract the data directly, but that was not necessary as this was a short-lived AWS experiment. The consensus was it was probably a hardware problem. Which goes to show that you can never totally trust your hardware or software, so always keep tested, frequent, and multiple backups nearby!
