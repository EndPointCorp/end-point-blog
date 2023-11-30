---
author: Josh Williams
title: Another Post-Postgres Open Post
github_issue_number: 500
tags:
- conference
- postgres
- bucardo
date: 2011-09-22
---

Well, that was fun! I’ve always found attending conferences to be an invigorating experience. The talks are generally very informative, it’s always nice to put a face to names seen online in the community, and between the “hall track”, lunches, and after-session social activities it’s difficult to not find engaging discussions.

My favorite presentations:

- [Scaling servers with Skytools](https://web.archive.org/web/20111001091321/http://postgresopen.org/2011/schedule/presentations/90/) — seeing what it takes to balance several high-velocity nodes was intriguing.
- [Mission Impossible](https://web.archive.org/web/20111001091308/http://postgresopen.org/2011/schedule/presentations/22/) — lots of good arguments for why Postgres can be an equivalent, nay, better replacement for an enterprise database.
- [The PostgreSQL replication protocol](https://web.archive.org/web/20111001174349/http://postgresopen.org/2011/schedule/presentations/65/) — even if I never intend to write something that’ll interact with it directly, knowing how something like the new streaming replication works under the hood goes a long way to keeping it running at a higher level.
- [True Serializable Transactions Are Here!](https://web.archive.org/web/20111001091313/http://postgresopen.org/2011/schedule/presentations/61/) — I’ll admit I haven’t had a chance to fully check out the changes to Serializable, so getting to hear some of the reasoning and stepping through some of the use cases was quite helpful.

But what of my talks? [Monitoring](http://joshwilliams.name/talks/monitoring/) went well—​it seemed to get the message out. There was a lot of “gee, I have Postgres, and Nagios, but they’re not talkin’. Now they can!” So hopefully, with a little more visibility into how the database is standing, the tools can boost confidence within business environments that aren’t as sure about Postgres and help keep existing installations in place. I think the [Bucardo presentation](https://bucardo.org/slides/b5_multi_master/) had me a bit more animated for some reason. That one also led to some interesting questions from the audience, and a couple challenges for the Bucardo project.

All in all, great work everyone!
