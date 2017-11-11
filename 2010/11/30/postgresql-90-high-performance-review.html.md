---
author: David Christensen
gh_issue_number: 386
tags: database, optimization, performance, postgres
title: PostgreSQL 9.0 High Performance Review
---



I recently had the privilege of reading and reviewing the book [PostgreSQL 9.0 High Performance](http://link.packtpub.com/aOSDW3) by Greg Smith.  While the title of the book suggests that it may be relevant only to PostgreSQL 9.0, there is in fact a wealth of information to be found which is relevant for all community supported versions of Postgres.

Acheiving the highest performance with PostgreSQL is definitely something which touches all layers of the stack, from your specific disk hardware, OS and filesystem to the database configuration, connection/data access patterns, and queries in use.  This book gathers up a lot of the information and advice that I've seen bandied about on the IRC channel and the PostgreSQL mailing lists and presents it in one place.

While seemingly related, I believe some of the main points of the book could be summed up as:

1. Measure, don't guess.  From the early chapters which cover the lowest-level considerations, such as disk hardware/configuration to the later chapters which cover such topics as query optimization, replication and partitioning, considerable emphasis is placed on determining the metrics by which to measure performance before/after specific changes.  This is the only way to determine the impact the changes you make have.

1. Tailor to your specific needs/workflows.  While there are many good rules of thumb out there when it comes to configuration/tuning, this book emphasizes the process of determining/refining those more general numbers to tailoring configuration/setup to your specific database's needs.

1. Review the information the database system itself gives you.  Information provided by the pg_stat_* views can be useful in identifying bottlenecks in queries, unused/underused indexes.

This book also introduced me to a few goodies which I had not encountered previously.  One of the more interesting ones is the pg_buffercache contrib module.  This suite of functions allows you to peek at the internals of the shared_buffers cache to get a feel for which relations are heavily accessed on a block-by-block basis.  The examples in the book show this being used to more accurately size shared_buffers based on the actual number of accesses to specific portions of different relations.

I found the book to be well-written (always a plus when reading technical books) and felt it covered quite a bit of depth given its ambitious scope.  Overall, it was an informative and enjoyable read.


