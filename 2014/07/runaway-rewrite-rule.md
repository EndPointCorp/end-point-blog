---
author: Jeff Boes
title: Runaway Rewrite Rule
github_issue_number: 1013
tags:
- apache
date: 2014-07-16
---



I am *not* an expert in Apache configuration. When I have to delve into a *.conf file for more than five minutes, I come out needing an aspirin, or at least a nerve-soothing cupcake. But necessity is the mother of contention, or something like that.

My application recently had added some new URLs, which were being parsed by your typical [MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) route handler (although in Perl, because that’s how I roll, and not in [Dancer](http://perldancer.org/), because … well, I don’t think it had been invented yet when this application first drew breath). 99.9% of the URLs worked just fine:

```plain
/browse/:brand/:category (the pattern)
/browse/acme/widget
/browse/ben-n-jerry/ice-cream
```

and so on. Suddenly a report reached me that one particular brand was failing:

```plain
/browse/unseen-images/stuff
```

(“unseen-images” has been changed to protect the innocent. The key here is the word “images”; put a pin in that and hang on.)

```plain
/browse/unseen-images
```

worked just fine. What’s worse, instrumenting the route handler code proved that it wasn’t even being called for /browse/unseen-images/foo or any of its siblings, whether :category was valid or not.

Making sure my bottle of aspirin was at hand, I dove into the Apache configuration. I added –

```plain
RewriteLog /path-to-logs/logs/rewrite_log
RewriteLogLevel 9
```

and while its output was fascinating, it wasn’t very enlightening. However, I did stumble upon this gem:

```plain
RewriteRule  ^/.*images/.*   -       [NE,PT,L]
```

Aha! Oho! A runaway regular expression is our culprit. I’m pretty sure this was added innocently, hoping to catch things like

```plain
/css/images/foo.jpg
/images/foo.png
```

and so on, but it misfired and gathered up my application URL. I replaced this temporarily with:

```plain
RewriteRule  ^/(.+/)*images/.*   -       [NE,PT,L]
```

“Temporarily” because I’m still trying to find someone who knows why that particular kind of rewrite was deemed necessary, so I don’t know whether my replacement rule will have the same effect in the cases where it is supposed to be doing a job.

Is there a moral to this story? I don’t know just yet, but it’s probably something like “Regular expressions are powerful, use them with care”, or maybe “When rewrite rules are good, they are very, very good, but when they are bad they are horrid.”


