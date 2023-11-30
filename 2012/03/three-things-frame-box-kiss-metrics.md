---
author: Steph Skardal
title: 'Three Things: frame box, Kiss Metrics, DUMP_VHOSTS'
github_issue_number: 580
tags:
- tips
date: 2012-03-30
---

Here’s my latest installment of sharing content that doesn’t necessarily merit entire blog posts, but I still want to write it down somewhere so I’ll remember!

### 1. Kiss Metrics on Design and Conversion

First up is an article sent over by [Jon](/team/jon-jensen/). [This](https://web.archive.org/web/20120424141314/https://blog.kissmetrics.com/shocking-truth-about-graphics/) is a great article from The Kiss Metrics Blog. Several of us at End Point have been a part of redesigning the End Point website and this is an interesting article that discusses how design decisions affect conversion, and how it’s important to justify design decisions with metrics and testing.

### 2. Apache DUMP_VHOSTS

Next up is a quick system admin command line that I came across while troubleshooting something with [Richard](/team/richard-templet/):

```plain
apache2ctl -t -D DUMP_VHOSTS
```

We have a team of hosting experts here at End Point, and I am not often involved in that aspect of the web application deployment. But I was recently trying to figure out why the default Apache site was being served when a recent domain had been updated to point to my IP address. I worked with Richard on a [screen session](https://www.gnu.org/software/screen/) and he pointed out how the above command was helpful in examining how all the virtual hosts are handled by Apache. We identified that the default host was being served for an incoming request that didn’t have a matched definition.

### 3. frame box

I was recenty reunited with a great tool that I lost track of: [frame box](http://www.framebox.org). It’s an free online quick mockup tool, great for building a quick mockup to visually communicate an idea to a client, or great for suggesting to clients to put together a quick mockup to visually communicate to a developer. Check it out!

<a href="http://www.framebox.org/" target="_blank"><img border="0" src="/blog/2012/03/three-things-frame-box-kiss-metrics/image-0.png" width="750"/></a>
