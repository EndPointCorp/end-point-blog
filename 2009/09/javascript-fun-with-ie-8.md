---
author: Max Cohan
title: JavaScript fun with IE 8
github_issue_number: 193
tags:
- browsers
- javascript
date: 2009-09-01
---

I ran into, and found solutions for, two major gotchas targeting IE 8 with a jQuery-based (and rather JavaScript-heavy) web application.

First is to specify the ‘IE 8 Standard’ rendering mode by adding the following meta tag:
<meta equiv="X-UA-Compatible" content="IE=8">

The default rendering mode is rather glitchy and tends to produce all sorts of garbage from ‘clean’ HTML and JavaScript. The result renders slightly different sizes, reports incorrect values from common jQuery calls, etc.

The default rendering also caused various layout issues (CSS handling looked more like IE 6 than IE 7). Also, minor errors (an extra '' tag on one panel) caused the entire panel to not render.

Another issue is the browser is overly lazy about invalidating the cache for AJAX pulled content, especially (X)HTML. This means that though you think you’re pulling current data, in reality it keeps feeding you the same old data. This also means that if you use the same exact URL for HTML & JSON data, you must add a parameter to avoid running into cache collisions. IE 8 only seemed to honor ‘Cache-control: no-cache’ in the header to cause it to behave properly.

On the other side, I’ve got a big thumbs up for jQuery. I was able to produce a skinned fairly ‘heavy’ client-side application that works equally well (and looks almost the same) on Firefox, Chrome, Safar, and now IE 8.
