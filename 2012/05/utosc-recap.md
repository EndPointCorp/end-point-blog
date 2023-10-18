---
author: Josh Tolley
title: UTOSC Recap
github_issue_number: 611
tags:
- community
- conference
- database
- visionport
- kamelopard
date: 2012-05-10
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/05/utosc-recap/utos-logo.png" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="100" src="/blog/2012/05/utosc-recap/utos-logo.png" width="257"/></a></div>

I spent three days last week attending the [Utah Open Source Conference](https://web.archive.org/web/20120525040559/http:/conference.utos.org/), in company with [Josh Ausborne](/team/josh-ausborne/) and [Jon Jensen](/team/jon-jensen/). Since End Point is a “distributed company”, I’d never met Josh Ausborne before, and was glad to spend a few days helping and learning from him as we demonstrated the Liquid Galaxy he has [already written about](/blog/2012/05/end-point-at-utah-open-source/).

This time around, the conference schedule struck me as being particularly oriented toward front-end web development. The talks were chosen based on a vote taken on the conference website, so apparently that’s what everyone wanted, but front-end stuff is not generally my cup of tea. That fact notwithstanding, I found plenty to appeal to my particular interests, and a number of talks I didn’t make it to but wished I had.

I delivered two talks during the conference, the first on database constraints, and the second on Google Earth and the Liquid Galaxy as they apply to geospatial visualization (slides [here](https://josh.endpointdev.com/dont-do-that.pdf) and [here](https://josh.endpointdev.com/mighty-maps.pdf), respectively). Though I couldn’t get past the feeling that my constraints talk dragged quite a bit, it was well received. Where possible I kept it as database-agnostic as possible, but no talk on the subject would be complete without mentioning PostgreSQL’s innovative [exclusion constraints](https://www.postgresql.org/docs/current/static/ddl-constraints.html#DDL-CONSTRAINTS-EXCLUSION). Their applicability to scheduling applications, by easily preventing things like overlapping time ranges, seemed particularly interesting to one attendee with recent experience writing such an application. Should I have opportunity to deliver the talk again, it will definitely include more examples of some of the more overlooked constraint types, as well as a more detailed description of the [surrogate vs. natural keys](https://en.wikipedia.org/wiki/Surrogate_key), which generated quite a bit of discussion after I mentioned it in passing.

My mapping talk was less enthusiastically attended, which may well be due to the topic or the speaker, but it was also scheduled at 6:00 PM, in the last slot of the day, and I expect many attendees had gone home. UTOSC features an unusually high number of attendees with young families, compared to most conferences I’ve attended, and clears out relatively rapidly toward evening. The last day’s tracks tend to be family-focused specifically because of all the parents who want to bring their children, and included hands-on labs, board game sessions, and child-friendly demonstrations.

Sparse attendance notwithstanding, I enjoyed introducing my audience to Google Earth’s KML language, the Kamelopard library I’ve been working on to facilitate making KML, and some of the applications of Google Earth for visualization. We moved the Liquid Galaxy from our display booth to the classroom for my presentation; I expect it was one of the more involved demonstrations in any talk, and certainly deserves honorable mention for being a live demo that actually worked.
