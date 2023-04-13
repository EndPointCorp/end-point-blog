---
author: Selena Deckelmann
title: 'Talk slides are available! Bucardo: Replication for PostgreSQL'
github_issue_number: 209
tags:
- postgres
- bucardo
date: 2009-10-17
---

I'm in Seattle for the PostgreSQL Conference West today! I just finished giving a talk on [Bucardo](http://bucardo.org), a master-slave and multi-master replication system for Postgres.

<iframe src="//www.slideshare.net/slideshow/embed_code/key/h00gDzwUEz4JNl" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/selenamarie/bucardo" title="Bucardo" target="_blank">Bucardo</a> </strong> from <strong><a href="//www.slideshare.net/selenamarie" target="_blank">Selena Deckelmann</a></strong> </div>

The talk was full, and had lots of people who've used Slony in the past, so I got lots of great questions. I realized we should publish some "recommended architectures" for setting up the Bucardo control database, and provide more detailed diagrams for how replication events actually occur. I also talked to someone interested in using Bucardo to show DDL differences between development databases and suggested he post to the mailing list. Greg has created scripts to do similar things in the past, and it would be really cool to have Bucardo output runnable SQL for applying changes.

I also made a hard pitch for people to start a SEAPUG, and it sounds like some folks from the [Fred Hutchinson Cancer Research Center](http://www.fhcrc.org/) are interested. (I'm naming names, hoping that we can actually do it this time. :D) If you are from the Seattle area, go ahead and subscribe to the [seapug@postgresql.org mailing list](http://www.postgresql.org/community/lists/subscribe) (pick 'seapug' from the list dropdown menu)!

Thanks everyone who attended, and I'm looking forward to having lunch with a bunch of PostgreSQL users here in Seattle!
