---
author: David Christensen
title: PgConf 2015 NYC Recap
github_issue_number: 1110
tags:
- conference
- postgres
date: 2015-04-06
---

I recently just got back from PGConf 2015 NYC. It was an invigorating, fun experience, both attending and speaking at the conference.

What follows is a brief summary of some of the talks I saw, as well as some insights/thoughts:

On Thursday:

“Managing PostgreSQL with Puppet” by Chris Everest. This talk covered experiences by CoverMyMeds.com staff in deploying PostgreSQL instances and integrating with custom Puppet recipes.

“A TARDIS for your ORM—​application level timetravel in PostgreSQL” by Magnus Hagander. Demonstrated how to construct a mirror schema of an existing database and manage (via triggers) a view of how data existed at some specific point in time. This system utilized range types with exclusion constraints, views, and session variables to generate a similar-structured schema to be consumed by an existing ORM application.

“Building a ‘Database of Things’ with Foreign Data Wrappers” by Rick Otten. This was a live demonstration of building a custom foreign data wrapper to control such attributes as hue, brightness, and on/off state of Philips Hue bulbs. Very interesting live demo, nice audience response to the control systems. Used a python framework to stub out the interface with the foreign data wrapper and integrate fully.

“Advanced use of pg_stat_statements: Filtering, Regression Testing & More” by Lukas Fittl. Covered how to use the pg_stat_statements extension to normalize queries and locate common performance statistics for the same query. This talk also covered the pg_query tool/library, a Ruby tool to parse/analyze queries offline and generate a JSON object representing the query. The talk also covered the example of using a test database and the pg_stat_statements views/data to perform query analysis to theorize about planning of specific queries without particular database indexes, etc.

On Friday:

“Webscale’s dead! Long live Postgres!” by Joshua Drake. This talk covered improvements that PostgreSQL has made over the years, specific technologies that they have incorporated such as JSON, and was a general cheerleading effort about just how awesome PostgreSQL is. (Which of course we all knew already.)  The highlight of the talk for me was when JD handed out “prizes” at the end for knowing various factoids; I ended up winning a bottle of Macallan 15 for knowing the name of the recent departing member of One Direction. (Hey, I have daughters, back off!)

“The Elephants In The Room: Limitations of the PostgreSQL Core Technology” by Robert Haas. This was probably the most popular talk that I attended. Robert is one of the major developers of the PostgreSQL team, and is heavily knowledgeable in the PostgreSQL internals, so his opinions of the existing weaknesses carry some weight. This was an interesting look forward at possible future improvements and directions the PostgreSQL project may take. In particular, Robert looked at the IO approach Postgres currently take and posits a Direct IO idea to give Postgres more direct control over its own IO scheduling, etc. He also mentioned the on-disk format being somewhat suboptimal, Logical Replication as an area needing improvement, infrastructure needed for Horizontal Scalability and Parallel Query, and integrating Connection Pooling into the core Postgres product.

“PostgreSQL Performance Presentation (9.5devel edition)” by Simon Riggs. This talked about some of the improvements in the 9.5 HEAD; in particular looking at the BRIN index type, an improvement in some cases over the standard btree index method. Additional metrics were shown and tested as well, which demonstrated Postgres 9.5’s additional performance improvements over the current version.

“Choosing a Logical Replication System” by David Christensen. As the presenter of this talk, I was also naturally required to attend as well. This talk covered some of the existing logical replication systems including Slony and Bucardo, and broke down situations where each has strengths.

“The future of PostgreSQL Multi-Master Replication” by Andres Freund. This talk primarily covered the upcoming BDR system, as well as the specific infrastructure changes in PostgreSQL needed to support these features, such as logical log streaming. It also looked at the performance characteristics of this system. The talk also wins for the most quote-able line of the conference:  “BDR is spooning Postgres, not forking”, referring to the BDR project’s commitment to maintaining the code in conjunction with core Postgres and gradually incorporating this into core.

As part of the closing ceremony, there were lightning talks as well; quick-paced talks (maximum of 5 minutes) which covered a variety of interesting, fun and sometimes silly topics. In particular some memorable ones were one about using Postgres/PostGIS to extract data about various ice cream-related check-ins on Foursquare, as well as one which proposed a generic (albeit impractical) way to search across all text fields in a database of unknown schema to find instances of key data.

As always, it was good to participate in the PostgreSQL community, and look forward to seeing participants again at future conferences.
