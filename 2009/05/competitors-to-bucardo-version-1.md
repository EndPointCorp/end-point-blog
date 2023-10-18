---
author: Jon Jensen
title: Competitors to Bucardo version 1
github_issue_number: 147
tags:
- database
- postgres
- bucardo
date: 2009-05-18
---

Last time I described [the design and major functions of Bucardo version 1](/blog/2009/05/design-of-bucardo-version-1/) in detail. A natural question to ask about Bucardo 1 is, why didn’t I use something else already out there? And that’s a very good question.

I had no desire to create a new replication system and work out the inevitable kinks that would come with that. However, nothing then available met our needs, and today still nothing I’m familiar with quite would. So writing something new was necessary. Writing an asynchronous multimaster replications system for Postgres was not trivial, but turned out to be easier than I had expected thanks to Postgres itself—​with the caveats noted in the last post.

But, back to the landscape. What follows is a survey of the Postgres replication landscape as it looked in mid-2002 when I first needed multimaster replication for PostgreSQL 7.2.

### [pgreplicator](http://pgreplicator.sourceforge.net/)

PostgreSQL Replicator is probably the most similar project to Bucardo 1. It was released in 2001 and does not appear to have had any updates since October 2001. I don’t recall why I didn’t use this, but from reviewing the documentation I suspect it was because it hadn’t been updated for PostgreSQL 7.2, it used PL/Tcl, and required a daemon to run on every node. But the asynchronous store-and-forward approach, the use of triggers and data storage tables is similar to Bucardo 1.

### dbmirror

I don’t remember whether this was around in 2002, but it’s part of PostgreSQL contrib now. It is master/slave replication only.

### [Slony-I](http://slony.info/)

I don’t think Slony-I existed in 2002—​version 1.0 was released in 2004. But in any case, it only does master/slave replication.

### Slony2

There has been no code released from this project and the website is now gone.

### erserver

Master/slave replication, abandoned in favor of Slony-I. Website is now gone.

### [Postgres-R](http://www.postgres-r.org/)

This was a research project that worked with PostgreSQL 6.4. Some [Postgres-R design documents](https://web.archive.org/web/20090426075330/http://www.cs.mcgill.ca/~kemme/disl/replication.html) were published. An effort to port it to PostgreSQL 7.2 (the pgreplication project) did not appear to have gotten very far. In 2008 it seems to have been partially revived. I don’t know what the current status is.

### [PGCluster](http://pgfoundry.org/projects/pgcluster/)

This didn’t exist in 2002. I’m not sure where it’s at now. I believe it uses synchronous replication.

### [pgpool](http://pgpool.net/mediawiki/index.php/Main_Page)

This isn’t the kind of “replication” I wanted; it’s database load balancing and multiplexing. The pgpool listener is a single point of failure, and all databases must be accessible or data will be lost on a database server that is down.

### [Usogres](https://web.archive.org/web/20090310025931/http://usogres.good-day.net/)

Master/slave replication for backup purposes.

### [Mammoth PostgreSQL + Replication](https://web.archive.org/web/20090207185119/http://www.commandprompt.com/products/mammothreplicator/)

This didn’t exist in 2002. It is only master/slave replication. It began as proprietary software but I believe is open source now.

### EnterpriseDB Replication Server

A proprietary offering that came out in 2005 or 2006, for master/slave replication only. Has apparently been replaced by Slony, or perhaps was always rebranded Slony.

### [pgComparator](https://web.archive.org/web/20090505043719/http://pg-comparator.projects.postgresql.org/)

An rsync-like tool for comparing databases. Didn’t exist in 2002. Probably much better than Bucardo 1’s compare operation.

### [DBBalancer](https://sourceforge.net/projects/dbbalancer/)

Kind of like pgpool, more of a connection pooler. Hasn’t been updated since 2002.

### DRAGON

“Database Replication based on Group Communication.” Links to this project were defunct.

### [DBI-Link](http://pgfoundry.org/projects/dbi-link/)

DBI-Link isn’t about replication.

### (Summary)

I assembled this list some time back and have made some updates to it. I’m sure there are more to consider today. Please comment if you have any corrections or additions.
