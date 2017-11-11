---
author: Selena Deckelmann
gh_issue_number: 173
tags: postgres
title: pgGearman 0.1 release!
---



Yesterday, [Brian Aker](http://brian.krow.net) and [Eric Day](http://oddments.org) presented [pgGearman: A distributed worker queue for PostgreSQL](http://wiki.postgresql.org/wiki/PgDaySanJose2009#pgGearman:_A_distributed_worker_queue_for_PostgreSQL) during the OSCON/SFPUG PgDay. 

[Gearman](http://gearman.org) is a distributed worker queuing system that allows you to farm work out to a collection of servers, and basically run arbitrary operations. The example they presented was automating and distributing the load of image processing for Livejournal. For example, everyone loves to share pictures of their kittens, but once an image is uploaded, it may need to be scaled or cropped in different ways to display in different contexts. Gearman is a tool you can use to farm these types of jobs out.

So, in anticipation of the talk, I worked with Eric Day on a set of C-language user defined functions for Postgres that allow client connections to a Gearman server.

You can try out the [pgGearman 0.1](https://launchpad.net/pggearman/trunk/0.1) release on Launchpad!


