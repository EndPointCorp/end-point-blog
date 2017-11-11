---
author: Jeff Boes
gh_issue_number: 764
tags: chrome, html, interchange, javascript
title: Crossed siting; or How to Debug iOS Flash issues with Chrome
---



This situation had all the elements of a programming war story: unfamiliar code, an absent author, a failure that only happens in production, and a platform inaccessible to the person in charge of fixing this: namely, me.

Some time ago, an engineer wrote some Javascript code to replace a Flash element on a page with an HTML5 snippet, for browsers that don't support Flash (looking at you, iOS). For various reasons, said code didn't make it to production. Fast forward many months, and that engineer has left for another position, so I'm asked to test it, and get it into production.

Of course, it works fine. My only test platform is an iPod, but it looks great here. Roll it out, and ker-thunk: it doesn't work. Of course, debugging Javascript on an iPod is less than optimal, so I enlisted others with Apple devices and found that it mostly failed, but maybe worked a few times, depending on [SOMETHING].

To make matters a bit worse, the Apache configurations for the test and production environments differed, just enough to raise my suspicions and convince me that was worth investigating. Once I went down that path, it was tough to jar myself loose from that suspicion.

I tried disabling Flash in Firefox to trigger the substitution, but that didn't seem to have the desired effect (as the replacement didn't happen, which was a different error than the replacement *failing*). I tried a browser emulation site (which shall remain nameless for this post, as I don't think they are bad at what they do, but they don't emulate iOS browsers in *this* capacity).

Eventually we disabled flash in Chrome (by visiting the chrome://plugins page). That unveiled the hidden error:

```
XMLHttpRequest cannot load http://www.somewhere.com/ajax/newstuff.html. Origin http://somewhere.com is not allowed by Access-Control-Allow-Origin.
```

There's the crux of it: the browser was sitting on an address which appeared different than that of the AJAX target.

The site involved is an Interchange site, and page constructed a URL using the [area] tag, which makes a fully-qualified URL from a fragment like "ajax/newstuff". That URL was being seen by the iOS browsers as a cross-site scripting attempt, as it didn't *precisely* match where the browser found the page. The error was not visible in the Safari browser on my iPod, and browsers I had access to which *could* have displayed the error, weren't suffering it.

I replaced the [area] tag with a plain relative URL and the problem disappeared.

TL;DR:

```
               $.ajax({
-                  url: "[area href=|ajax/newstuff|]",
+                  url: "ajax/newstuff.html",
                   type: 'html',
```

The original code caused a cross-site scripting failure.


