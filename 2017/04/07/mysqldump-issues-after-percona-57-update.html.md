---
author: Marco Matarazzo
gh_issue_number: 1298
tags: mysql
title: mysqldump issues after Percona 5.7 update
---

During a recent CentOS 7 update, among other packages, we updated our Percona 5.7 installation to version 5.7.17-13.

Quickly after that, we discovered that mysqldump stopped working, thus breaking our local mysql backup script (that complained loudly).

### What happened?

The error we received was:

```bash
mysqldump: Couldn't execute 'SELECT COUNT(*) FROM INFORMATION_SCHEMA.SESSION_VARIABLES WHERE VARIABLE_NAME LIKE 'rocksdb\_skip\_fill\_cache'': The 'INFORMATION_SCHEMA.SESSION_VARIABLES' feature is disabled; see the documentation for 'show_compatibility_56' (3167)
```

After a bit of investigation, we discovered this was caused by [this regression bug](https://bugs.launchpad.net/percona-server/+bug/1676401), apparently already fixed but not yet available on CentOS:

Everything revolves around INFORMATION_SCHEMA being deprecated in version 5.7.6, when Performance Schema tables has been added as a replacement.

Basically, a regression caused mysqldump to try and use deprecated INFORMATION_SCHEMA tables instead of the new Performance Schema.

### How to fix it?

Immediate workaround is to add this line to /etc/my.cnf or (more likely) /etc/percona-server.conf.d/mysqld.cnf, depending on how your configuration files are organized:

```bash
show_compatibility_56=1
```

This flag was both introduced and deprecated in 5.7.6. It will be there for some time to help with the transition.

It seems safe and, probably, good to keep if you have anything still actively using INFORMATION_SCHEMA tables, that would obviously be broken if not updated to the new Performance Schema since 5.7.6.

With this flag, it is possible to preserve the old behavior and keep your old code in a working state, while you upgrade it. Also, according to the documentation, it should not impact or turn off the new behavior with Performance Schema.

More information on how to migrate to the new Performance Schema can be found [here](https://dev.mysql.com/doc/refman/5.7/en/performance-schema-variable-table-migration.html).
