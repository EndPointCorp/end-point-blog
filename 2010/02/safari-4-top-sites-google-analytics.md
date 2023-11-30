---
author: Jon Jensen
title: Safari 4 Top Sites feature skews analytics
github_issue_number: 267
tags:
- analytics
- browsers
- django
- ecommerce
- interchange
- php
- rails
date: 2010-02-13
---

[Safari](https://www.apple.com/safari/) version 4 has a new “Top Sites” feature that shows thumbnail images of the sites the user most frequently visits (or, until enough history is collected, just generally popular sites).

Martin Sutherland describes this feature in details and shows [how to detect these requests](https://web.archive.org/web/20100316231239/http://www.sunpig.com/martin/archives/2010/01/08/how-to-detect-a-page-request-from-safari-4s-top-sites-feature.html), which set the X-Purpose HTTP header to “preview”.

The reason this matters is that Safari uses its normal browsing engine to fetch not just the HTML, but all embedded JavaScript and images, and runs in-page client JavaScript code. And these preview thumbnails are refreshed fairly frequently—​possibly several times per day per user.

Thus every preview request looks just like a regular user visit, and this skews analytics which see a much higher than average number of views from Safari 4 users, with lower time-on-site averages and higher bounce rates since no subsequent visits are registered (at least as part of the preview function).

The solution is to simply not output any analytics code when the X-Purpose header is set to “preview”. In [Interchange](/expertise/perl-interchange/) this is easily done if you have an include file for your analytics code, by wrapping the file with an [if] block such as this:

```plain
[tmp x_purpose][env HTTP_X_PURPOSE][/tmp]
[if scratch x_purpose eq 'preview']
<!-- skip analytics for browser previews -->
[else]
(normal Google Analytics, Omniture SiteCatalyst, or other analytics code)
[/else]
[/if]
```

In [Ruby on Rails](/expertise/ruby-on-rails/) you’d check request.env["HTTP_X_PURPOSE"].

In PHP you’d check $_SERVER["HTTP_X_PURPOSE"].

In [Django](/expertise/django-python/) you’d check request.META["HTTP_X_PURPOSE"] or the equivalent request.META.get("HTTP_X_PURPOSE") (from the [HttpRequest](https://docs.djangoproject.com/en/dev/ref/request-response/) class).

And so on.

I confirmed the analytics tracking code was omitted by waiting for Safari to make its preview request and inspecting the response with the [Fiddler proxy](https://www.telerik.com/download/fiddler), on Windows. The same can be done for Safari on Mac OS X with a suitable Mac OS X HTTP proxy.
