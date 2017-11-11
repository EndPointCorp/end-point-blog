---
author: David Christensen
gh_issue_number: 506
tags: bucardo, conference, postgres
title: PG West 2011 Re-cap
---



I just recently got back from PG West 2011, and have had some time to ruminate on the experience (do elephants chew a cud?</note-to-self>).  I definitely enjoyed San Jose as the location; it's always neat to visit new places and to meet new people, and I have to say that San Jose's weather was perfect for this time of year.  I was also glad to be able to renew professional relationships and meet others in the PostgreSQL community.

Topic-wise, I noticed that quite a few talks had to do with replication and virtualization; this certainly seems to be a trend in the industry in general, and has definitely been a pet topic of mine for quite a while.  It's interesting to see the various problems that necessitate some form of replication, the tradeoffs/considerations for each specific problem, and wide variety of tools that are available in order to attack each of these problems (e.g. availability, read/write scaling, redundancy, etc).

A few high points from each of the days:

### Tuesday

I had dinner with fellow PostgreSQL contributors; some I knew ahead of time, others I got to know.  This was followed by additional socializing.

### Wednesday

I attended a talk on *PostgreSQL HA*, which covered the use of traditional cluster-level warm/hot standbys, as well as a solution using pg_pool and slony.  This was followed by the keynote address at the conference, given by Charles Fan, Senior Vice President from VMware.  This was a high-level overview of the type of work that VMware had been doing in order to support virtualizing PostgreSQL and optimizing for running multiple PostgreSQL instances on separate VMs efficiently.

I was involved in some "lunch track" discussions, and followed this all up with several more talks covering VMWare's specific offerings in more detail.

Evening was dinner and mandatory socializing.

### Thursday

I went to Robert Hodges' talk about *Tungsten*.  I had only heard of it in general terms, so it was interesting to get more specific details.  Robert's talk covered the basic architecture of Tungsten, as well as how their various adapters between multiple types of databases were used to ensure that the SQL that was executed on heterogeneous clusters would account for differences in datatype representation, encoding, DDL, specific query syntax, etc; for instance when executing a CREATE TABLE statement, MySQL's AUTO_INCREMENT fields would be converted to PostgreSQL's equivalent SERIAL type.  There was lots of good discussion after the presentation, and I spoke with Robert after the talk about different design/architecture choices that they made with Tungsten and we discussed differences between that and Bucardo.

At lunchtime I got to meet David Fetter's wife and baby (who looks [just](http://david.endpoint.com/fetter-baby.jpg) like him!), then gave an updated version of my *Bucardo: More than just Multimaster* talk.  Attendance was good, around 30-35, and the audience asked plenty of questions.

After my talk, I attended one about database optimization.  This is always an interesting topic for me, so I'm glad to hear other's insights on this subject.

This was all followed up by mandatory socializing.

### Friday

I found the talk about *Translattice* to be very interesting, as it highlighted specific problem domains for distributed, redundant, multi-write database clusters for more fault-tolerant applications.  It struck me as utilizing some of the same ideas as Cassandra or other decentralized distributed datastores, but doing so in a way that is transparent to the use of PostgreSQL.  What I found particularly interesting about this system was the use of data access/usage patterns, explicit policy, and locality to specify both the costing algorithm for accessing data as well as distributing knowledge about just where each copy of each piece of data exists.  The talk, while an introduction to the system, did not skimp on the details and the presenter was happy to answer my many specific questions.

The remaining talks were fairly light-hearted.  I went to one called *Redis: Data Bacon* for the title alone.  While I still don't understand why bacon, I walked away with an appreciation of the problem domain Redis addresses and how it could be used in specific cases.  The final talk I attended was about *Schemaverse*, a project which implements a game entirely in SQL.  Each player has their own database user created that they can then use from either the web interface or even via just a regular psql connection.  I can't speak for the game itself other than the overview given in the talk, but creative use/hacking of the game was explicitly encouraged, and seems like an interesting approach for testing things which may not often be stressed enough in (at least my) regular use of PostgreSQL, such as intra-database security/permissions, huge numbers of users, etc.  (It didn't surprise me that this game had been a hit at DEFCON.)

This was followed by the closing session, and final goodbyes, etc.  Oh, and (need I say) mandatory socializing.

### Final Thoughts

I always enjoy going to PostgreSQL events, and continue to be impressed with the community that surrounds PostgreSQL.  Thanks to everyone who attended, and a special thanks to Josh Drake for the work he put into it.  Hope to see ya next time!


