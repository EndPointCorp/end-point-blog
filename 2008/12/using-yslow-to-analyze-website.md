---
author: Ron Phipps
title: Using YSlow to analyze website performance
github_issue_number: 84
tags:
- browsers
- performance
date: 2008-12-19
---

While attending OSCON ’08 I listened to [Steve Souders](http://stevesouders.com/) discuss some topics from his O’Reilly book, High Performance Web Site, and a new book that should drop in early 2009. Steve made the comment that 80%-90% of the performance of a site is in the delivery and rendering of the front end content. Many engineers tend to immediately look at the back end when optimizing and forget about the rendering of the page and how performance there effects the user’s experience.

During the talk he demonstrated the Firebug plugin, [YSlow](http://developer.yahoo.com/yslow/), which he built to illustrate 13 of the 14 rules from his book. The tool shows where performance might be an issue and gives suggestions on which resources can be changed to improve performance. Some of the suggestions may not apply to all sites, but they can be used as a guide for the engineer to make an informed decision.

On a related note, Jon Jensen brought this [blog posting](https://adwords.googleblog.com/2008/03/landing-page-load-time-will-soon-be.html) to our attention that Google is planning to incorporate landing page time into its quality score for Adword landing pages. With that being known, front-end website performance will become even more important and there may be a point one day where load times come into play when determining natural rank in addition to landing page scores.
