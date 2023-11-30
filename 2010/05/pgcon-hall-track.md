---
author: Josh Tolley
title: The PGCon “Hall Track”
github_issue_number: 312
tags:
- community
- conference
- database
- open-source
- postgres
date: 2010-05-25
---

<a href="/blog/2010/05/pgcon-hall-track/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5475232667283865314" src="/blog/2010/05/pgcon-hall-track/image-0.png" style="float:left; margin:0 10px 10px 0;cursor:pointer; cursor:hand;width: 128px; height: 128px;"/></a>

One of my favorite parts of PGCon is always the “hall track”, a general term for the sideline discussions and brainstorming sessions that happen over dinner, between sessions (or sometimes during sessions), and pretty much everywhere else during the conference. This year’s hall track topics seemed to be set by the developers’ meeting; everywhere I went, someone was talking about hooks for external security modules, MERGE, predicate locking, extension packaging and distribution, or exposing transaction order for replication. Other developers’ pet projects that didn’t appear in the meeting showed up occasionally, including unlogged tables and range types. Even more than, for instance, the [wiki pages describing the things people plan to work on](https://wiki.postgresql.org/wiki/PgCon_2010_Developer_Meeting), these interstitial discussions demonstrate the vibrancy of the community and give a good idea just how active our development really is.

This year I shared rooms with Robert Haas, so I got a good overview of his plans for [global temporary and unlogged tables](http://rhaas.blogspot.com/2010/05/global-temporary-and-unlogged-tables.html). I spent a while with [Jeff Davis](https://web.archive.org/web/20100512170404/http://thoughts.j-davis.com/) looking through the code for exclusion constraints and deciding whether it was realistically possible to cause a starvation problem with many concurrent insertions into a table with an exclusion constraint. I didn’t spend the time I should have talking with [Dimitri Fontaine](https://twitter.com/tapoueh) about his PostgreSQL extensions project, but if time permits I’d like to see if I could help out with it. Nor did I find the time I’d have liked to work on [PL/Parrot](http://parrot.org/), but I was glad to meet Jonathan Leto, who has done most of the coding work thus far on that project.

In contrast to other conferences, I didn’t have a particular itch of my own to scratch between sessions. During past conferences I’ve been eager to discuss ideas for multi-column statistics; though that work continues, slowly, time hasn’t permitted enough recent development even for the topic to be fresh in my mind, much less worthy of in-depth discussion. This lack of one overriding subject turned out to be a refreshing change, however, as it left the other hall track subjects less filtered.

Finally, it was nice to spend time with co-workers, and in fact to meet (finally) in person the [one of the “Greg”s](/blog/authors/greg-sabino-mullane/) I’d talked to on the phone many times, but never actually met in person. Various engagements in my family or his have gotten in the way in the past. One of the quirks of working for a distributed organization...

Update: Fixed link to developers’ meeting wiki page, thanks to comment from roppert
