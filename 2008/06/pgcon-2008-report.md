---
author: Greg Sabino Mullane
title: PGCon 2008 Report
github_issue_number: 28
tags:
- conference
- database
- open-source
- postgres
- bucardo
- perl
date: 2008-06-13
---

End Point’s Greg Sabino Mullane recently returned from PGCon 2008, the annual conference for the PostgreSQL database project. The conference was held in Ottawa, Canada, and is a mix of Postgres developers, companies who are using Postgres, students, and everyone else involved in the vibrant Postgres community.

Greg presented a talk on Bucardo, the multi-master and master-slave replication system for Postgres. He explained the strengths and weaknesses of Bucardo, its typical use cases, and described in detail how it works. He detailed the innovative use of “hooks”, which allow custom code to be fired at any point throughout the replication process. The hooks are also the method of doing conflict resolution and exception handling, two important factors for multi-master replication. He also discussed the use of DBIx::Safe to pass restricted database handles to the custom code, as well as future directions for the Bucardo project. The talk even ended on time and left time for questions. The slides are [available on the PGCon 2008 site](http://www.pgcon.org/2008/schedule/events/93.en.html).

The other talk Greg gave was a “lightning talk” on DBIx::Cache, a query caching system for Postgres built on top of DBI and DBD::Pg. (Lightning talks are a collection of small five minute talks by different people, highlighting things they are currently working on.) There was a high level of interest in DBIx::Cache, which is still under development but should have its first released version within a few weeks.

There were many other interesting talks at the conference, many focusing on ways that companies and developers are pushing Postgres to new heights of performance and scalability. Yahoo! announced their new petabyte-sized database built on top of Postgres, and NTT presented an innovative way of doing synchronous log shipping for extremely fast failover capability. Andrew Dunstan described a replacement to the existing listen/notify system that he was working on, which will not only be faster and more reliable than the current system, but will allow the use of “payload” messages as well. Greg added support for payloads to DBD::Pg the next week, so we’re ready when you are, Andrew!

Pavel Deolasse of EnterpriseDB gave a great talk about Heap-Only Tuples (HOT), a clever new feature in Postgres 8.3 that significantly improves performance by only updating indexes when absolutely necessary, and many other optimizations. In other words, if you have a table with columns a and b, with an index on column a, updates that only affect column b will not change the index on a at all.

There were many other talks, covering a wide range of things, from PostGIS (geographical extensions) to upgrading Postgres on the fly, to satellite data processing by NASA. The full schedule can be seen [here](http://www.pgcon.org/2008/schedule/index.en.html). Just as valuable as the talks were the discussions among attendees over dinner and between sessions, about current problems, brainstorming future features, comparing war stories and victories, and catching up with people not seen for a year or more.
