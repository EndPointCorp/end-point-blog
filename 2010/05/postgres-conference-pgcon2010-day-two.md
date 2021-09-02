---
author: Greg Sabino Mullane
title: Postgres Conference — PGCon2010 — Day Two
github_issue_number: 310
tags:
- community
- conference
- database
- open-source
- postgres
date: 2010-05-24
---

<a href="/blog/2010/05/postgres-conference-pgcon2010-day-two/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5473789666231795170" src="/blog/2010/05/postgres-conference-pgcon2010-day-two/image-0.png" style="margin: 0pt 10px 10px 0pt; float: left; cursor: pointer; width: 128px; height: 128px;"/>
</a>

[Day two of](postgres-conference-pgcon2010-day-two/image-0-big.png) [the PostgreSQL Conference](http://www.pgcon.org/2010/) started a little later than the previous day in obvious recognition of the fact that many people were up very, very late the night before. (Technically, this is day four, as the first two days consisted of tutorials; this was the second day of “talks”).

The first talk I went to was [PgMQ: Embedding messaging in PostgreSQL](http://www.pgcon.org/2010/schedule/events/251.en.html) by Chris Bohn. It was well attended, although there were definitely a lot of late-comers and bleary eyes. A tough slot to fill! Chris is from Etsy.com and I’ve worked with him there, although I had no interaction with the PgMQ project, which looks pretty cool. From the talk description:

> PgMQ (PostgreSQL Message Queueing) is an add-on that embeds a messaging client inside PostgreSQL. It supports the AMQP, STOMP and OpenWire messaging protocols, meaning that it can work with all of the major messaging systems such as ActiveMQ and RabbitMQ. PgMQ enables two replication capabilities: “Eventually Consistent” Replication and sharding.

As near as I can tell, “eventually consistent” is the same as “asynchronous replication”: the slave won’t be the same as the master right away, but will be eventually. As with Bucardo and Slony, the actual lag is very small in practice: a handful of seconds at the most. I like the fact that it supports all those common messaging protocols. Chris mentioned in the talk that it should be possible for other systems like Bucardo to support something similar. I’ll have to play around with PgMQ a bit and see about doing just that. :)

<img alt="The typical post-talk gatherings" border="0" id="BLOGGER_PHOTO_ID_5474936538302599138" src="/blog/2010/05/postgres-conference-pgcon2010-day-two/image-1.jpeg" style="cursor: pointer; width: 320px; height: 240px;"/>
*The typical post-talk gatherings*

The next “talk” was the enigmatically labeled [Replication Panel](http://www.pgcon.org/2010/schedule/events/268.en.html). Enigmatic in this case as it had no description whatsoever. It’s a good thing I had decided to check it out anyway (I’m a sucker for any talk related to replication, in case it wasn’t obvious yet). I was apparently nominated to be on the panel, representing Bucardo! So much for getting all my speaking done and over with the first day. The panel represented a pretty wide swatch of Postgres replication technologies, and by the people who are very deep in the development of each one. From left to right on a cluster of stools at the front of the room was:

- [Londiste](https://web.archive.org/web/20100529094424/http://skytools.projects.postgresql.org/doc/londiste.cmdline.html) (Marko Kreen)

- [Slony](http://slony.info/) (Jan Wieck)

- [pgpool-II](https://wiki.postgresql.org/wiki/Pgpool-II) ([Tatsuo Ishii](http://www.pgcon.org/2008/schedule/speakers/95.en.html))

- [Hot standby](https://wiki.postgresql.org/wiki/Hot_Standby) and [Streaming replication](https://wiki.postgresql.org/wiki/Streaming_Replication) (Heikki Linnakangas)

- [Bucardo](https://bucardo.org/) (Greg Sabino Mullane)

- [Golconde](https://code.google.com/archive/p/golconde/) (Gavin M. Roy)

After a quick one-minute each intro describing who we were and what our replication system was, we took questions from the audience. Rather, Dan Langille played the part of the moderator and gathered written questions from the audience which he read to us, and we each took turns answering. We managed to get through 16 questions. All were interesting, even if some did not apply to all the solutions. Some of the more relevant ones I remember:

*“If your replication solution was not available, which of the other replication solutions would you recommend?”* This was my favorite question. My answer was: if using Bucardo in multi-master mode, switch to pgpool. If using in master-slave mode, use Slony.

*“How will PG 9.0 affect your solution? Will your solution still remain relevant?”* This most heavily affects Bucardo, Slony, and Londiste, and we all agreed that we’re happy to lose users who simply need a read-only copy of their database. Their remains plenty of use cases that 9.0 will not solve however.

*“For multi-master solutions: How are database collisions resolved? Do you recommend your solution for geographically remote locations?”* This one is pretty much for me alone. :) I gave a quick overview of Bucardo’s built-in conflict resolution systems, and how custom ones built on business logic works. Since Bucardo was originally built to support servers over a non-optimal network, the second part was an easy Yes.

*“Is there a way to standardize and reduce the number of replication systems and focus on making the subset more robust, efficient, and versatile?”* The general answer was no, as the use cases for all of them are so wildly different. I thought the only possible reduction was to combine Slony and Londiste, as they are very close technically and have pretty much identical use cases.

*“How easy is it to switch masters? Are you planning on improving the tools to do so?”* With Bucardo, switching is as easy as pointing to a different database if using master-master. However, Bucardo master-slave has no built in support at all for failover (like Slony does). So the answer is “not easy at all” and yes, we want to provide tools to do so.

*“What is your biggest bug, problem, or limitation you are fixing now?”* All three of the async trigger solutions (Bucardo, Slony, and Londiste) answered “DDL triggers”. Which is hopefully coming for 9.1 (stop reading this blog and get to work on that, Jan).

All in all, I really liked the panel, and I think the audience did as well. Hopefully we’ll see more things like at future conferences. Since we did not know the questions before hand, and took everything from the audience, it was the polar opposite of someone giving a talk with prepared slides.

I had some people come up to me afterwards to ask for more details about Bucardo, because (as they pointed out), it’s the only multi-master replication system for Postgres (not technically true, as pg-pool and rubyrep provide multi-master use cases as well, but the former is synchronous and fairly complex, while the latter is very new and lacking some features). Maybe next year I should give a whole talk on Bucardo rather than just blabbing about it here on the blog. :)

After that, I popped into the [Check Please! What Your Postgres Databases Wishes You Would Monitor](http://www.pgcon.org/2010/schedule/events/257.en.html) talk by Robert Treat (who I also used to work with). It was a good talk, but pretty much review for me, as watching over and monitoring databases is what I spend a lot of my time doing. :) Here’s the description:

> Compared to many proprietary systems, Postgres tends to be pretty straight forward to run. However, if you want to get the most from your database, you shouldn’t just set it and forget it, you need to monitor a few key pieces of information to keep performance going. This talk will review several key metrics you should be aware of, and explain under which scenarios you may need additional monitoring.

The final talk I went to was [Deploying and testing triggers and functions in multiple databases](http://www.pgcon.org/2010/schedule/events/244.en.html) by Norman Yamada. This was an interesting talk for me because he was using a lot of the code from the same_schema action in the check_postgres program to do the actual comparison. Indeed, I made some patches while at the conference to allow for better index comparison’s at Norman’s request. I also managed to get some work done on tail_n_mail and Bucardo while there—​something about being surrounded by all that Postgres energy made me productive despite having very little free time.

I had to catch an early flight, and was not able to catch the final talk slot of the day, nor the closing session or the BOFs that night. Hopefully someone who did catch those will blog about it and let me know how it went. I hear the t-shirt we signed at the developer’s meeting went for a sweet ransom.

If you went to PgCon, I have two requests for you.

<a href="/blog/2010/05/postgres-conference-pgcon2010-day-two/image-2-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5474935485723884514" src="/blog/2010/05/postgres-conference-pgcon2010-day-two/image-2.jpeg" style="margin: 0pt 10px 10px 0pt; float: left; cursor: pointer; width: 228px; height: 266px;"/></a>

 First, please fill out the feedback for each talk you went to. It takes less than a minute per talk, and is invaluable for both the speakers and the conference organizers. Second, please blog about PgCon. It’s helpful for people who did not get to go to see the conference through other people’s eyes. And do it now, while things are still fresh.

If you did not go to PgCon, I have one request for you: go next year! Perhaps next year at PgCon 2011 we’ll break the 200 person mark. Thanks to Dan Langille as always for creating PgCon and keeping it running smooth year after year.
