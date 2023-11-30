---
author: Josh Tolley
title: UTOSC, here I come
github_issue_number: 595
tags:
- conference
date: 2012-04-19
---

<div class="separator" style="clear: both; text-align: center;"><a href="https://www.eventbrite.com/e/utah-open-source-conference-2012-registration-3315016303" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" height="100" src="/blog/2012/04/utosc-here-i-come/utos-logo.png" width="257"/></a></div>

Recently the [Utah Open Source Foundation](https://web.archive.org/web/20120116090206/http://www.utos.org/) announced their schedule for this year’s [UTOSC](https://web.archive.org/web/20120525040559/http://conference.utos.org/), scheduled for May 3-5 at Utah Valley University. I’m not sure I’ve ever before felt sufficiently ambitious to submit two talk proposals for a conference, but I did this time, and both were accepted, so I’ll give one talk on database constraints, from simple to complex, and another on geospatial data visualization such as [we’ve been doing a whole lot of lately.](https://www.visionport.com/) [Jon Jensen](/team/jon-jensen/) will also be there with two talks of his own, one on website performance and the other a “screen vs. tmux faceoff”. We use screen pretty heavily company-wide, but I’ve wanted to learn tmux for quite a while, so this one is on my list to see.

**DATABASE CONSTRAINTS**

Database constraints are something I’ve always strongly encouraged, and my commitment to clearly constrained data has become more complete recently after a few experiences with various clients and inconsistent data. The idea of a database constraint is to ensure all stored data meets certain criteria, such as that a matching record exists in another table, or the “begin” date is prior to the “end date”, or even simply that a particular field is not empty. Applications and frameworks may claim to validate data for you, such that the database doesn’t need to worry about it, but in practice those claims often prove only marginally true. In recent years, PostgreSQL especially has become much more flexible and powerful in this regard, with the addition of exclusion constraints, but developers still frequently disregard database constraints, at their peril.

**GEOSPATIAL VISUALIZATION**

Geospatial data visualization—​that is, displaying data that has a location component—​is a huge field, and well-explored, but Google Earth and Liquid Galaxy are an impressive recent leap forward. End Point has done a great deal of work to make the Liquid Galaxy platform easily configurable and manageable, and has created powerful tools for development of these visualizations. My visualization presentation will cover the basics of Google Earth and Liquid Galaxy, and show how to begin turning data into visualizations.

UTOSC started a few years ago to cater to the large open source movement in Salt Lake City, Provo, and surrounding areas, and the conference has grown to something truly remarkable. Expect several hundred attendees for the three days full of talks and tutorials. The community is a vibrant one, and the attendees, as well as the sponsors, come from many different domains and with many different areas of expertise. End Point will be one of those sponsors this year: we’re going to man a booth with a scaled-down Liquid Galaxy, so come see what we’ve been talking about. We demonstrate several visualizations of the sort we’ve done recently, to include panoramic video, automatic visualization builders, and innovative systems for real-time control. [Registration is now open](https://www.eventbrite.com/e/utah-open-source-conference-2012-registration-3315016303), so sign up and come say hi.
