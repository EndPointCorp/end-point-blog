---
author: David Christensen
title: PostgreSQL Autovacuum Issues In EOL Postgres
github_issue_number: 836
tags:
- postgres
date: 2013-07-17
---



We recently had a web application shut down and start throwing PostgreSQL errors such as the following:

`
ERROR:  database is shut down to avoid wraparound data loss in database "postgres"
`

`
HINT:  Stop the postmaster and use a standalone backend to vacuum database "postgres"
`

This is of course the dreaded error message that occurs when you get close to the transaction wraparound point, and PostgreSQL refuses to continue to run in server mode.

This is a situation which occurs when vacuuming is not run regularly (or at all, considering that autovacuum has been enabled by default since PostgreSQL 8.2), so this is rare to see in actual usage.

The particular installation we were looking at was an older one, running PostgreSQL 8.1, which had been included as the base PostgreSQL version with RHEL 5. (To stave off the inevitable comments: yes, upgrading is a good idea, considering 8.1 has been End-Of-Life’d for years now. This isn’t the point of this article.)

After running postgres in single-user mode and running VACUUM FULL on all of the databases, I started the cluster back up and started to see why we ran into the wraparound issue.

Using psql, I verified that the autovacuum setting was off (the immediate source of the wraparound issue). However when I went to enable that in the postgresql.conf file, I saw that the postgresql.conf setting showed `autovacuum = on`. This contradicted my expectations; based on the pg_settings view this was being set in the config file, and this was the only instance of this directive in the file, so it was clearly not being overwritten.

Resorting to the documentation for the autovacuum setting, it appears that in addition to autovacuum being enabled, you also need to enable stats_start_collector (enabled) and stats_row_level (disabled). After ensuring these were both enabled, I restarted the cluster and verified that the autovacuum setting had the expected value.

Just hoping to save someone some time if they have to deal with an older version of PostgreSQL and run into this same issue.


