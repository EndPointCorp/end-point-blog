---
author: Steph Skardal
gh_issue_number: 745
tags: interchange, nginx, performance
title: 'Paper Source: The Road to nginx Full Page Caching in Interchange'
---

### Background & Motivation

During the recent holiday season, it became apparent that some efforts were needed to improve performance for [Paper Source](http://www.paper-source.com/) to minimize down-time and server sluggishness. Paper Source runs on Interchange and sells paper and stationery products, craft products, personalized invitations, and some great gifts! They also have over 40 physical stores which in addition to selling products, offer on-site workshops.

<a href="http://www.paper-source.com/"><img border="0" height="46" src="/blog/2013/01/03/paper-source-nginx-full-page-caching/image-0.gif" width="362"/></a>

Over the holiday season, the website experienced a couple of instances where server load spiked causing extreme sluggishness for customers. Various parts of the site leverage Interchange's [timed-build](http://www.icdevgroup.org/doc/frames/ictags_112.html) tag, which creates static caches of parts of a page (equivalent to Rails' and Django's fragment caching). However, in all cases, Interchange is still being hit for the page request and often the pages perform repeated logic and database hits that opens an opportunity for optimization.

### The Plan

The long-term plan for Paper Source is to move towards full page [nginx](http://nginx.org/) caching, which will yield speedily served pages that do not require Interchange to be touched. However, there are several code and configuration hurdles that we have to get over first, described below.

### Step 1: Identify Commonly Visited Pages

First, it's important to recognize which pages are visited the most frequently and to tackle optimization on those pages first, essentially profiling the site to determine where we will gain the most from performance optimization. In the case of Paper Source, popular pages include:

- Thumbnail page, or the template where multiple products are shown in list format
- Product detail page, or the template that serves the basic product page
- Swatching page, or the template that serves a special product page with special product options
- Personalization detail page, or a template that serves the special product page for personalizeable products (e.g. wedding invitatations, birth announcements, etc.)

### Step 2: Remove Dynamic User Elements on pages of interest

The next step in the process is to remove dynamic elements on the page, by having cookies or AJAX render these dynamic elements. Below are a couple of examples of these dynamic elements on two primary page templates.

<img border="0" src="/blog/2013/01/03/paper-source-nginx-full-page-caching/image-0.png" width="740"/>

The thumbnail page contains two dynamic elements: the mini-cart template, which shows how many items are in the user's cart, and the log in information, which shows "my account" and "log out" links if the user is logged in, and shows a "log in" link if the user is not logged in.

<img border="0" src="/blog/2013/01/03/paper-source-nginx-full-page-caching/image-1.png" width="740"/>

In addition to the mini-cart and logged in elements, the product page contains additional dynamic elements which signify if a user has added an item to their cart, and presentation of the user's previously viewed items.

In the examples above, the following changes were applied to replace these dynamic elements:

- Mini-cart Component: This section utilizes cookies with the [jQuery.cookie](https://github.com/carhartl/jquery-cookie) plugin. A cookie stored in the browser identifies the number of cart items and the cart subtotal. After the DOM loads, the mini-cart is rendered and displayed if the user has a non-empty cart. These cookies are manipulated whenever the cart contents are modified.
- Login Component: This section also reads a browser-stored cookie. If the cookie indicates the user is logged in, the navigation elements are updated to reflect that.
- Added to cart Component: On the product detail page, this code was invasively modified to allow items to be added to cart via AJAX. The AJAX call results in an update of the cart cookies specified above. The feedback of the AJAX call is presented to the user to indicate that the item has been successfully added.
- Previously Viewed Component: Finally, the product page also contains previously viewed items. This is generated via a cookie that stores recent skus visited by the user, and each sku has an associated cookie that includes information such as the image source, link, description, and price. Because a maximum of three previously viewed items is shown, cookies here of older previously viewed items are deleted to minimize cookie build-up.

### Step 3: Implement fully timed-build caching pages

During this incremental process to reach the end goal of full nginx caching, the next step is to implement fully timed-build pages, or use Interchange's caching mechanism to fully cache these pages and reduce repetitive database hits and backend logic. In this step, the entire page is wrapped in a timed-build tag, which results in writing and serving a static cached file for that page. While this step is not a necessity, it does allow for us to deploy and test our changes in preparation for nginx caching. In adddition to giving us an opportunity to work out kinks, this step also gives us an added bump in performance because several of these page templates have no caching at all.

### Step 4: Reproduce redirect logic outside of Interchange

Next up, we plan to move logic that handles page redirects outside of Interchange to nginx. At the moment, Interchange is responsible for handling 301 redirects on old product and navigation pages. This will need to be moved to nginx redirects to minimize the hits on Interchange here.

### Step 5: Implement nginx architecture on camps

Another non-trivial step in this process will be to implement nginx architecture on DevCamps (or camps). [DevCamps](http://www.devcamps.org/) is an open source tool developed by End Point for developing on multiple instances of copies of the production server. Camps are heavily used for Paper Source because several End Point and internal Paper Source employees simultaneously work on different projects on their development instances or camps. Nginx caching will need to be set up to also work with the camp system in place.

### Step 6: Turn nginx caching on!

Finally, we can turn on nginx caching for specific pages of interest. Nginx will then serve these fully cached pages and will avoid Interchange entirely. Cookies and AJAX will still be used to render the dynamic elements on the fully cached pages. While we'd ideally like to cache every page on the site except for the cart, checkout and my account pages, it makes more sense to find the bottlenecks and tackle them incrementally.

### Where are we now?

At the moment, I've made progress on steps 1-3 for several subsets of pages, including the thumbnail and product detail pages. I plan to continue these steps for additional bottleneck pages. I have worked out out a couple of minor kinks throughout the recent progress, but things have been progressing well. [Richard](/team/richard_templet) plans to make progress on the nginx related tasks in preparation for reaching the end goal.
