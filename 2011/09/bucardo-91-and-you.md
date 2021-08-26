---
author: Josh Williams
title: Bucardo, 9.1, and you!
github_issue_number: 497
tags:
- conference
- postgres
date: 2011-09-13
---



A little bit of bad news for Bucardo fans, Greg Sabino Mullane won’t be making Postgres Open due to scheduling conflicts. But not to worry, I’ll be giving the [“Postgres masters, other slaves”](https://web.archive.org/web/20111129045834/http://postgresopen.org/2011/schedule/presentations/55/) talk in the meantime in his place.

In looking over the slides, one thing that catches my eye is how quickly Bucardo is adopting PostgreSQL 9.1 features. Specifically, Unlogged Tables will be very useful in boosting performance where Bucardo stages information about changed rows for multi-database updates. I also wonder if the enhanced Serializable Snapshot Isolation would be helpful in some situations. Innovation encouraging more innovation, gotta love open source!

If I hadn’t said it before, thanks to everyone that made Postgres 9.1 possible. Some of the other enhancements are just as exciting. For instance, I’m eager to see some creative uses for Writable CTE’s. And it’ll be very interesting to see what additional Foreign Data Wrappers pop up over time.

Now, back to packing...


