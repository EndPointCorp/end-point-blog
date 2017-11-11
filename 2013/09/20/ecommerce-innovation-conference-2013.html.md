---
author: Richard Templet
gh_issue_number: 856
tags: camps, community, conference, dancer, ecommerce, interchange, perl
title: eCommerce Innovation Conference 2013
---

The [eCommerce Innovation Conference 2013](http://www.ecommerce-innovation.com/) is a new conference being held in Hancock, New York, between October 8th and 11th. The conference aims to discuss everything ecommerce with a focus on [Perl](http://www.perl.org/)-based solutions including [Dancer](http://perldancer.org/) and [Interchange](http://www.icdevgroup.org/). It isn't geared directly to any one specific type of person unlike most conferences. The current speakers list include in-house ecommerce software developers, consultants, sales managers, project managers, and marketing experts. The talk topics range from customer relationship management to template engines for Perl.

[Mark Johnson](/team/mark_johnson) and I are both going to be speaking at the conference. Also there will be Mike Heins, creator of Interchange, and Stefan Hornburg, longtime Interchange development group "team captain".

Mark is going to be discussing [full page caching in Interchange 5](http://act.ecommerce-innovation.com/eic2013/talk/5107). This is becoming a more frequent request from our larger customers. They want to be able to do full page caching to allow the web browser and a caching proxy server alone to handle most requests leaving Interchange and the database open to handle more shopping-based requests like add to cart or checkout. This is a commonly-used architecture in many application servers, and my colleague David Christensen has several new features already in use by customers to make full-page caching easier, which are expected to go into Interchange 5.8.1 soon.

I will be doing a talk on [multi-site setup in Interchange 5](http://act.ecommerce-innovation.com/eic2013/talk/5111). This is a request we have received frequently over the years. Companies may either already have some kind of wholesale website or just want to have multiple websites use the same database and programming but allow for different website designs. They normally need to control what website a product will show up on and possibly adjust the price accordingly. I'll discuss the different methods we have used to accomplish this at End Point.

I see on the schedule that Sam Batschelet will be [speaking about the camps system](http://act.ecommerce-innovation.com/eic2013/talk/5109) and some new capabilities he's added for [perlbrew](http://perlbrew.pl/) and [Carton](https://github.com/miyagawa/carton), among other things. We are also using camps some places with perlbrew and [plenv](https://github.com/tokuhirom/plenv), so it will be interesting to compare notes. I hope we'll see some discussion and/or contribution to the [open source DevCamps](http://www.devcamps.org/) project soon!

It promises to be a very nice conference with lots of diverse information!
