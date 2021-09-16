---
author: Selena Deckelmann
title: 'Talk slides are available! Bucardo: Replication for PostgreSQL'
github_issue_number: 209
tags:
- postgres
date: 2009-10-17
---



I'm in Seattle for the PostgreSQL Conference West today!  I just finished giving a talk on [Bucardo](http://bucardo.org), a master-slave and multi-master replication system for Postgres.  

[Bucardo](http://www.slideshare.net/selenamarie/bucardo)

<object height="355" style="margin:0px" width="425"><param name="movie" value="http://static.slidesharecdn.com/swf/ssplayer2.swf?doc=bucardo-091017075408-phpapp02&stripped_title=bucardo"/><param name="allowFullScreen" value="true"/><param name="allowScriptAccess" value="always"/><embed allowfullscreen="true" allowscriptaccess="always" height="355" src="http://static.slidesharecdn.com/swf/ssplayer2.swf?doc=bucardo-091017075408-phpapp02&stripped_title=bucardo" type="application/x-shockwave-flash" width="425"/></object>

View more [documents](http://www.slideshare.net/) from [Selena Deckelmann](http://www.slideshare.net/selenamarie).

The talk was full, and had lots of people who've used Slony in the past, so I got lots of great questions. I realized we should publish some "recommended architectures" for setting up the Bucardo control database, and provide more detailed diagrams for how replication events actually occur. I also talked to someone interested in using Bucardo to show DDL differences between development databases and suggested he post to the mailing list. Greg has created scripts to do similar things in the past, and it would be really cool to have Bucardo output runnable SQL for applying changes.

I also made a hard pitch for people to start a SEAPUG, and it sounds like some folks from the [Fred Hutchinson Cancer Research Center](http://www.fhcrc.org/) are interested. (I'm naming names, hoping that we can actually do it this time :D).  If you are from the Seattle area, go ahead and subscribe to the [seapug@postgresql.org mailing list](http://www.postgresql.org/community/lists/subscribe) (pick 'seapug' from the list dropdown menu)!

Thanks everyone who attended, and I'm looking forward to having lunch with a bunch of PostgreSQL users here in Seattle!


