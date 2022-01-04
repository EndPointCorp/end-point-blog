---
author: Josh Williams
title: pg_wrapper’s very symbolic links
github_issue_number: 352
tags:
- database
- postgres
date: 2010-09-22
---



I like pg_wrapper. For a development environment, or testing replication scenarios, it’s brilliant. If you’re not familiar with pg_wrapper and its family of tools, it’s a set of scripts in the postgresql-common and postgresql-client-common packages available in Debian, as well as Ubuntu and other Debian-like distributions. As you may have guessed pg_wrapper itself is a wrapper script that calls the correct version of the binary you’re invoking – psql, pg_dump, etc – depending on the version of the database you want to connect to. Maybe not all that exciting in itself, but implied therein is the really cool bit: This set of tools lets you manage multiple installations of Postgres, spanning multiple versions, easily and reliably.

Well, usually reliably. We were helping a client upgrade their production boxes from Postgres 8.1 to 8.4. This was just before the 9.0 release, otherwise we’d consider moving the directly to that instead. It was going fairly smoothly until on one box we hit this message:

```plain
Could not parse locale out of pg_controldata output
```

Oops, they had pinned the older postgres-common version. An upgrade of those packages and no more error!

```plain
$ pg_lsclusters
Version Cluster   Port Status Owner    Data directory                     Log file
8.1     main      5439 online postgres /var/lib/postgresql/8.1/main       custom
Error: Invalid data directory
```

Hmm, interesting. Okay, so not quite, got a little bit more work to do. This one took some tracing through the code. The pg_wrapper scripts, if they don’t already know it, look for the data directory in a couple of places. The first stop is the postgresql.conf file, specifically /etc/postgresql/<version>/<cluster-name>/postgresql.conf, looking for the data_directory parameter. But, in its transitional state at the time, the postgresql.conf was still a work in progress.

The second place it looks is a symlink in the same /etc/postgresql/<version>/<cluster-name>/ directory. While that’s the old way of doing things, it at least let us get things looking reasonable:

```plain
# ln -s /var/lib/postgresql/8.4/main /etc/postgresql/8.4/main/pgdata
# /etc/init.d/postgresql-8.4 status
8.1     main      5439 online postgres /var/lib/postgresql/8.1/main       custom
8.4     main      5432 online postgres /var/lib/postgresql/8.4/main       custom
```

Voilà! From there we were able to proceed with the upgrade, confident that the instance will behave as expected. And now, everything is running great!

As with most things that provide a simpler experience on the surface, there’s additional complexity under the hood. But for now, we have one more client upgraded. Thanks, Postgres!


