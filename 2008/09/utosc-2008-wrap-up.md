---
author: Jon Jensen
title: UTOSC 2008 wrap-up
github_issue_number: 62
tags:
- conference
date: 2008-09-15
---



### Using Vyatta to Replace Cisco Gear

At the [2008 Utah Open Source Conference](https://web.archive.org/web/20080725072722/http://2008.utosc.com/) I attended an interesting presentation by [Tristan Rhodes](http://useopensource.blogspot.com/) about the [Vyatta](https://web.archive.org/web/20080920035541/http://www.vyatta.com/) open source networking software. Vyatta’s software is designed to replace Cisco appliances of many sorts: WAN routers, firewalls, IDSes, VPNs, and load balancers. It runs on Debian GNU/Linux, on commodity hardware or virtualized.

A key selling point is the price/performance benefit vs. Cisco (prominently noted in Vyatta’s marketing materials), and the IOS-style command-line management interface for experienced Cisco network administrators. Regular Linux interfaces are available too, though Tristan wasn’t positive that writes would stick in all cases, as he’s mostly used the native Linux tools for monitoring and reading, not writing.

Pretty cool stuff, and Vyatta sells pre-built appliances and support too. The Vyatta reps were handing out live CDs, but I haven’t had a chance to try it out yet. [Presentation details are here](https://web.archive.org/web/20080912055238/http://2008.utosc.com/presentation/111/).

### Google App Engine 101

[Jonathan Ellis](http://spyced.blogspot.com/) did a presentation and then hands-on workshop on Google App Engine, which I found especially useful because he’s a longtime Python and Postgres user. His talk on SQLAlchemy last year made me think he wouldn’t gloss over the huge differences in the runtime environment of GAE vs. regular Django, for example having GQL and BigTable instead of SQL and a relational database. And he didn’t. They’re quite different, and one is very primitive to use. I’ll let you guess which one. :)

In fact, the day of the conference he wrote a blog post, [App Engine Conclusions](http://spyced.blogspot.com/2008/08/app-engine-conclusions.html), where he says: “I’ve reluctantly concluded that I don’t like it.” His reasoning makes sense to me, and maybe it *will* improve enough later to be really nice. We’ll see. Of course that’s all ignoring the hosting lock-in too.

His [presentation details are here](https://web.archive.org/web/20080912055217/http://2008.utosc.com/presentation/106/).

### Writing Documentation with Open Source Tools

Paul Frields (of the Fedora Project) and Jared Smith (of Asterisk fame) showed how to use DocBook XML to write documentation. It was a practical talk, we asked questions, they tag-teamed the answers and live demonstrations, showed us the Red Hat tool “Publican” and Gnome’s yelp documentation viewer that can present DocBook XML natively. Good stuff, though XML sure hasn’t gotten any less verbose.

The [presentation details](https://web.archive.org/web/20080912055335/http://2008.utosc.com/presentation/131/) include a link to the slides.

### Automated System Management with Puppet

[Andrew Shafer](https://stochasticresonance.wordpress.com/) did a [presentation](https://web.archive.org/web/20080912055445/http://2008.utosc.com/presentation/60/) on [Puppet](https://puppet.com/), and I was sad to miss the beginning of it. But what I heard was quite enjoyable.

The message I took away is this: Without some overlap of the traditionally separate domains or disciplines of system administrator and programmer, no software tool is going to be able to magically manage all your systems for you. Puppet provides a domain-specific language for specifying what resources should be available. (Resources are comprised of packages, files, and services.) You still have to say what you want, but there’s a nice way to do that in a cross-platform way, once. Paraphrasing Einstein, it’s a simple as it can be, but not simpler.

The questions were good, but I had the feeling from a few of them that people wanted things to be simpler than possible. :)

### LOLCATS

A nice bonus was the UTOSC crew giving out fortune cookies with LOLCATS fortunes. Mine read:

> i’m in ur cookie
> 
> given ur fortune

That was a delight. And I happened to meet up right about then with Josh Tolley, author of [PL/LOLCODE](http://pgfoundry.org/projects/pllolcode/).


