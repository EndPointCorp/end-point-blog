---
author: Greg Sabino Mullane
gh_issue_number: 282
tags: community, conference, database, postgres
title: PostgreSQL Conference East 2010 review
---



I just returned from the [PostgreSQL Conference East 2010](http://www.postgresqlconference.org/). This is one of the US “regional” Postgres conferences, which usually occur once a year on both the East and West coast. This is the second year the East conference has taken place in my home town of Philadelphia.

Overall, it was a great conference. In addition to the talks, of course, there are many other important benefits to such a conference, such as the “hallway tracks”, seeing old friends and clients, meeting new ones, and getting to argue about default postgresql.conf settings over lunch. I gave a 90 minute talk on “Postgres for non-Postgres people” and a lightning talk on the indispensable [tail_n_mail.pl program](https://bucardo.org/tail_n_mail).

This year saw the conference take place at a hotel for the first time, and this was a big improvement over the previous school campus-based conferences. Everything was in one building, there was plenty of space to hang out and chat between the talks, and everything just felt a little bit easier. The one drawback was that the rooms were not really designed to lecture to large numbers of people (e.g. no stadium seating), but this was not too much of an issue for most of the talks.

A few of the talks I attended included:

- Mine! Luckily, my talk was in the very first slot, so I was able to give it and then be done talking for the rest of the conference (with the exception of the lightning talk). My talk was “PostgreSQL for MySQL (and other database people)”. A quick show of hands showed that in addition to a good number of MySQL people, we had people coming from Oracle, Microsoft SQL Server, and even Informix. I walked through the steps to take when upgrading your application from using some other database to using Postgres, pointing out some of the pain points and particular Postgres gotchas, focusing on the SQL syntax. The second half of the talk focused on the Postgres project itself, explaining how it all worked, what the “community” and “core” consists of, how companies are involved, how development is done, and the philosophy of the project.
- “PostgreSQL at myYearbook.com” by Gavin M. Roy. I’ve heard earlier versions of this talk before, but it was neat to see how much myyearbook.com had grown in just one year and some of the new challenges they faced. Of course, Gavin is still upset about the primary key situation and they are still doing unique indexes instead of PKs so they can do in-place reindexing for bloat removal.
- Baron Schwartz spoke about “Query Analysis with mk-query-digest”. The “mk” is short for [maatkit](https://web.archive.org/web/20100616202319/http://www.maatkit.org/), a nice suite of tools for doing all sorts of database-related things. Granted, it’s very MySQL focused at the moment, but Baron has started to port things over to Postgres, and the demo he gave was pretty impressive. I’ll definitely be downloading that code and taking a look.
- Magnus Hagander gave a talk on “Secure PostgreSQL Deployment” which was a lot more interesting than I thought it would be (I knew it had Windows slides). My take-home lessons: never use the ssl mode of “prefer”, and always check your Debian systems as they like to switch SSL on everything for no good reason. It’s also quite fascinating to see the number of ways you can authenticate to a Postgres database.
- I attended a talk on “Inside the PostgreSQL Infrastructure” by Dave Page. A lot of it I already knew, as I’m a little involved in said infrastructure, but it was good to hear some of the future plans, including standardizing on Debian instead of FreeBSD in the future.
- Spencer Christensen’s talk on “PostgreSQL Administration for System Administrators” was very well done but mostly review for me :). It was nice to see a shout out in his talk (and some others) for [check_postgres.pl](https://bucardo.org/check_postgres/check_postgres.pl.html).
- Robert Haas gave a good talk on “The PostgreSQL Query Planner” that seemed to be very well received. The bit about the join removal tech was particularly interesting: the Postgres planner does some really, really clever things when trying to build the best possible plan for your query.

At the lunch on Saturday, Josh Drake asked if anyone else wanted to do a lightning talk, so I made a quick outline on the back of a nearby piece of paper and gave a no-slides, no-notes five minute talk on tail_n_mail.pl. It went pretty well, and I even had 30 seconds left over at the end for questions. To clarify my answer to one of those further now: tail_n_mail.pl can parse CSV logs (indeed, any text file), but it cannot consolidate similar entries yet or any of the other neat things it does until we can teach TNM about how to parse the CSV logs properly.

An excellent conference overall, but I’d be amiss if I didn’t offer a little 
constructive criticism for the next time (and other conferences):

- Scheduling. The rooms were sometimes hard to find, and the schedule did not list the room next to the talk. That color-coded thing just does not work. In addition, it seemed like similar talks were sometimes stacked up against each other rather than staggered. Thus, you could learn about londiste OR rubyrep, but not both. Similarly, there were two Python talks up against each other.
- Lightning talks. Always, always put the lightning talks at the *start* of the conference, not the end. Lightning talks are a great way to learn about what other people are doing. By having it at the start of the conference, you have the entire rest of the time to followup with people about their talks and foster more real-life discussions.
- Lightning talks. Okay, not done talking about these yet. Lightning talks are somewhat notorious for spending lots of time getting the video to work right, as people switch computers, fiddle with plugs, etc. If you can’t get it setup in 30 seconds, start the clock! You should be able to give your lightning talk without slides, if need be.


