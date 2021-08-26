---
author: Greg Sabino Mullane
title: 'Bucardo: Replication for PostgreSQL'
github_issue_number: 24
tags:
- database
- open-source
- perl
- postgres
date: 2007-10-10
---

### Overview

Bucardo, an asynchronous multi-master replication system for [PostgreSQL](/technology/postgresql), was recently released by [Greg Sabino Mullane](/blog/authors/greg-sabino-mullane). First previewed at this year's PostgreSQL Conference in Ottawa, this program was developed for Backcountry.com to help with their complex database needs.

Bucardo allows a Postgres database to be replicated to another Postgres database, by grouping together tables in transaction-safe manner. Each group of tables can be set up in one of three modes:

1. The table can be set as master-master to the other database, so that any changes to either side are then propagated to the other one.
1. The table can be set up as master-slave, so that all changes made to one database are replicated to the second one.
1. It can be set up in "fullcopy" mode, which simply makes a full copy of the table from the master to the slave, removing any data already on the slave.

Master-master replication is facilitated by standard conflict resolution routines, as well as the ability to drop in your own by writing small Perl routines. This custom code can alse be written to handle exceptions that often occur in master-master replication situations, such as a unique constraint on a non-primary key column.

### History

[Backcountry.com](https://www.backcountry.com/), an online retailer of high-end outdoor gear, needed a way to keep their complex, high-volume, Postgres databases in sync with each other in near real-time, and turned to End Point for a solution. In 2002, the first version of Bucardo was rolled out live, and reliably replicated billions of rows. In 2006, Bucardo was rewritten to employ new features, including a robust daemon model, more flexible configuration and logging, custom conflict and exception handling routines, much faster replication times, and a higher level of self-maintenance. This new version has been in production at Backcountry.com since November 2006.

In September 2007, the source code for Bucardo version 3.0.6 was released under the same license as Postgres itself, the flexible BSD license. A website and mailing lists were created to help foster Bucardo's development. The website can be found at [bucardo.org](https://bucardo.org/).
