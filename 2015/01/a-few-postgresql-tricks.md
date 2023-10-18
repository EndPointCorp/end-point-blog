---
author: Josh Tolley
title: A few PostgreSQL tricks
github_issue_number: 1081
tags:
- postgres
date: 2015-01-30
---

We ran into a couple of interesting situations recently, and used some helpful tricks to solve them, which of course should be recorded for posterity.

### Unlogged tables

One of our customers needed a new database, created as a copy of an existing one but with some data obscured for privacy reasons. We could have done this with a view or probably any of several other techniques, but in this case, given the surrounding infrastructure, a new database, refreshed regularly from the original, was the simplest method. Except that with this new database, the regular binary backups became too large for the backup volume in the system. Since it seemed silly to re-provision the backup system (and talk the client into paying for it) to accommodate data we could throw away and recalculate at any time, we chose unlogged tables as an alternative.

“Unlogged,” in this case, means changes to this table aren’t written in WAL logs. This makes for better performance, but also means if the database crashes, these tables can’t be recovered in the usual way. As a side effect, it also means these tables aren’t copied via WAL-based replication, so the table won’t show up in a hot standby system, for instance, nor will the table appear in a system restored from a WAL-based backup (pg_dump will still find them). Unlogged tables wouldn’t give our application much of a performance boost in this case—​the improved performance applies mostly to queries that modify the data, and ours were meant to be read-only. But before this change, the regular refresh process generated all kinds of WAL logs, and now they’ve all disappeared. The backups are therefore far smaller, and once again fit within the available space. Should the server crash, we’ll have a little more work to do, regenerating these tables from their sources, but that’s a scripted process and simple to execute.

### Stubborn vacuum

Another fairly new customer has a database under a heavy and very consistent write load. We’ve had to make autovacuum very aggressive to keep up with bloat in several tables. When the vacuum process happens to clean all the tuples from the end of a table file, it tries to shrink the file and reclaim disk space, but it has to obtain a brief exclusive lock to do it. If it can’t get one, it gives up, and emits a log message you’ll see if you are vacuuming in verbose mode:

```plain
INFO:  "some_big_table": stopping truncate due to conflicting lock request
```

Note that though the log message calls this process “truncating”, it should not be confused with the “TRUNCATE TABLE” command, which (locks permitting) would reclaim quite a bit more disk space than we want it to. Anyway, when the shrinking operation succeeds, there is no log message, so if VACUUM VERBOSE doesn’t say anything about “stopping truncate”, it’s because it was able to get its lock and shrink the table, or the table didn’t need it in the first place. Because of this database’s tendency to bloat, we’d like vacuum to be able to shrink tables regularly, but the query load is such that for some tables, it never gets the chance. We’re working on mitigating that, but in the meantime, one stop-gap solution is to run VACUUM VERBOSE in a tight loop until you don’t see one of those “stopping truncate” messages. In our case we do it like this:

```bash
#!/bin/bash
 
timeout="8m"
problematic_tables="
one_bloated_table
another_bloated_table
and_one_more_bloated_table
"
my_database="foo"
 
for table in $problematic_tables; do
    echo "Vacuuming $table"
    ( timeout $timeout bash <<VACUUM
        while :; do
            vacuumdb -v -t $table $my_database 2>&1 | grep "stopping truncate" || break
        done
VACUUM
) || echo "Timed out on table $table"
done
```

This script iterates through a list of tables we’d like to shrink, and vacuums each repeatedly, as quickly as possible, until the vacuum process fails to emit a “stopping truncate” message, or it finds it has spent eight minutes trying. Of course this whole technique is only useful in a few limited cases, but for our purposes we’ve found it helpful for managing bloat while we continue to work on the query patterns to reduce locking overall.

1. In version 9.0 and before, it simply tries to obtain the lock once. In 9.1 and later versions, it tries every few milliseconds for up to five seconds to obtain the lock.
2. There’s nothing magic about eight minutes, it just works out well enough for our purposes.
