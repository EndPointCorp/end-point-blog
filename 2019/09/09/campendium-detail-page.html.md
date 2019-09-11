---
title: "Campendium: A Responsive, Fancy Detail Page"
author: Steph Skardal
tags: rails, solr, sunspot, react, maps, javascript, user-interface, ruby, clients
gh_issue_number: 1554
---

![](/blog/2019/09/09/campendium-detail-page/banner.jpg)

This week, I was very excited to deploy a project for [Campendium](https://www.campendium.com/), one of our long-time clients. As noted in [my recent post on Campendium updates for the year](https://www.endpoint.com/blog/2019/08/05/campendium-updates), Campendium has thousands of listings of places to camp and provides a great infrastructure for the development of a rich community of travelers around North America.

For the past few months, I’ve been working on a significant update to Campendium’s campground detail page, the page template where in-depth information is provided for each of Campendium’s locations. This is equivalent to a product detail page on an ecommerce site.

The “guts” of the update included a new detail page design with expanded responsiveness, the introduction of 360° videos, and expanded user driven content in the form of Question & Answer (Q&A or QnA), reviews, notes, nightly rates, etc. Read on to find out more and see video examples of several of the features!

### User Interface & Responsiveness Updates

One of the things the Campendium team and I are most proud of here is the responsiveness of the new design. In the case of traveling and camping, responsiveness is important since a large amount of traffic comes from mobile devices, relative to what you might see in other industries.

User images are shown as “hero images” and the user interface updates depending on the browser device and width, as shown in the following videos for [Gilbert Ray Campground](https://www.campendium.com/gilbert-ray-campground) and [Cayuga Lake State Park](https://www.campendium.com/cayuga-lake-state-park).

<p style="text-align:center;font-weight:bold;"><iframe src="https://drive.google.com/file/d/1FFF8GcztnV-KGaJ4pjDYixCbkxw6kduu/preview" width="770" height="450"></iframe>A preview of responsive behavior on the campground detail page with user submitted photos.</p>

<p style="text-align:center;font-weight:bold;"><iframe src="https://drive.google.com/file/d/1caQZT9ogh_piuTX2UDIvWGEBZse0zwnx/preview" width="770" height="450"></iframe>A second preview of responsive behavior on the campground detail page with embedded maps.</p>

Another updated design usability tweak was a sticky navigation bar to navigation throughout the page, which can get especially long with user submitted content. See how the “Overview”, “Video”, etc. links become sticky as you scroll down on the page, and the current region coming into view of the page is underlined:

<p style="text-align:center;font-weight:bold;"><iframe src="https://drive.google.com/file/d/1w_MjP_HUXntYXHTG6FeREtMWwhKv4KgG/preview" width="770" height="450"></iframe>Navigation becomes fixed to the top of the browser as a user scrolls through the content.</p>

Campendium uses Ruby on Rails as a backend, a bit of [Bootstrap](https://getbootstrap.com/), and [Sass](https://sass-lang.com/) and best practice responsive design is used throughout this updated user interface.

### 360° Videos

The Campendium team has been hard at work creating 360 degree videos of the various locations to provide significant value to their users. These videos are now embedded into the campground detail page. Video hosting is provided by YouTube and dropped into the Campendium campground HTML template.

<p style="text-align:center;font-weight:bold;"><iframe src="https://drive.google.com/file/d/12XEu-95diRRMjlqb28jD0xdj9qIWXSb7/preview" width="770" height="450"></iframe>A video in a video—a 360 degree video example.</p>

I personally think these 360° videos are awesome, especially to those visual learners out there! You can learn so much from a video that can be hard to capture in user reviews.

### Community Q&A

Another new feature with this deploy is the introduction of community driven Question & Answer. Users can submit questions about a campground, and users who have contributed to this campground are invited to respond (or they can opt-out site-wide to responding to questions). In addition to Q&A itself, user content can be “upvoted” (marked as Helpful) or flagged for an improved user content browsing experience.

![Campendium community in Question & Answer](/blog/2019/09/09/campendium-detail-page/community.png)

All Q&A functionality is driven by JavaScript coupled with the Ruby on Rails backend.

### Expansion of User Contributed Content and Features

Finally, this update includes expansion of user contributed content in addition to Q&A. This includes the ability for users to contribute notes, cell signal reports, and nightly rates. Reviews can now be filtered by user profile information and sorted by date or specific ranking. Reviews can also be searched by keywords and those keywords highlighted in the results. The following video demonstrates sorting and searching of reviews with highlighted keyword match:

<p style="text-align:center;font-weight:bold;"><iframe src="https://drive.google.com/file/d/1G2KGfxCkOmuJm-AJE8BPXUC-OWdw1iQS/preview" width="770" height="450"></iframe>Review searchability with highlighting and filterability.</p>

All search functionality driven by JavaScript on the frontend, and a Ruby on Rails backend coupled with [Sunspot](https://github.com/sunspot/sunspot) and [Solr](https://lucene.apache.org/solr/). 

### Who Doesn’t Love Stats?

Just for the sake of sharing stats, from GitHub, this update included:

* 215 changed files
* 6,284 additions
* 3,924 deletions (removal / cleanup of unneeded JavaScript files)
