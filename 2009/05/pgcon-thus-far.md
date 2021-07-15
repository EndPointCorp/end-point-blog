---
author: Josh Tolley
title: PGCon thus far
github_issue_number: 151
tags:
- conference
- postgres
date: 2009-05-21
---



Though it might flood the End Point blog with PGCon content, I’m compelled to scribble something of my own to report on the last couple of days. Wednesday’s Developers’ Meeting was an interesting experience and I felt privileged to be invited. Although I could only stay for the first half, as my own presentation was scheduled for the afternoon, I enjoyed the opportunity to meet many PostgreSQL “luminaries”, and participate in some of the decisions behind the project.

Attendance at my “How to write a PostgreSQL Procedural Language” tutorial exceeded my expectations, no doubt in part, at least, because aside from the Developers’ Meeting it was the only thing going on. Many people seem interested in being able to write code for the PostgreSQL backend, and the lessons learned from PL/LOLCODE have broad application. It was suggested, even, that since PL/pgSQL converts most of its statements to SQL and passes the result to the SQL parser, PL/LOLCODE would have less parsing overhead than PL/pgSQL. Ensuing discussions of high performance LOLCODE were cancelled due to involuntary giggling.

Between talks I’ve had the opportunity to meet a wide variety of PostgreSQL users and contributors, and been interested to see various peoples’ ideas for future development. Perhaps it will result in a blog post one day, but suffice it to say there’s lots of activity under way. Most surprising to me has been the interest in my (still embryonic) work with multi-column statistics. On a number of different occasions people have unexpectedly asked me about it. Thanks to a hallway conversation with Tom Lane, another of the hard problems involved has a possible solution, the probable subject of yet another blog post.

Thanks to the organizers, sponsors, speakers, helpers, etc. who have made the conference possible so far; I’m looking forward to today.


