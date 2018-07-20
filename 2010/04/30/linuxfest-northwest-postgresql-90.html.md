---
author: Selena Deckelmann
gh_issue_number: 297
tags: postgres
title: 'LinuxFest Northwest: PostgreSQL 9.0 upcoming features'
---



Once again, LinuxFest Northwest provided a full track of PostgreSQL talks during their two-day conference in Bellingham, WA.

Gabrielle Roth and I presented [our favorite features in 9.0](https://github.com/gorthx/pg9_preso), including a live demo of Hot Standby with streaming replication! We also demonstrated features like:

- the newly improved ‘[set storage MAIN](https://www.postgresql.org/docs/8.4/static/sql-altertable.html)’ behavior ([TOAST related](https://www.postgresql.org/docs/8.4/static/storage-toast.html))
- ‘samehost’ and ‘samenet’ designations to [pg_hba.conf](https://www.postgresql.org/docs/devel/static/auth-pg-hba-conf.html) (see CIDR-address section)
- Log changed parameter values when postgresql.conf is reloaded
- Allow [EXPLAIN output](https://www.postgresql.org/docs/devel/static/sql-explain.html) in XML, JSON, and YAML formats (which our own Greg Sabino Mullane worked on!
- Allow [NOTIFY](https://www.postgresql.org/docs/devel/static/sql-notify.html) to pass an optional string to listeners
- And of course—​[Hot Standby](https://www.postgresql.org/docs/devel/static/hot-standby.html) and [Streaming Replication](https://www.postgresql.org/docs/devel/static/warm-standby.html#STREAMING-REPLICATION)

The [full feature list](https://www.postgresql.org/docs/devel/static/release-9-0.html) is available at on the developer site right now!


