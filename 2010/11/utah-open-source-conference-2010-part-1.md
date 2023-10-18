---
author: Jon Jensen
title: Utah Open Source Conference 2010 part 1
github_issue_number: 381
tags:
- conference
- database
- ecommerce
- javascript
- open-source
- perl
- python
- ruby
- security
- magento
date: 2010-11-12
---

It’s been about a little over a month since the 2010 Utah Open Source Conference, and I decided to take a few minutes to review talks I enjoyed and link to my own talk slides.

**Magento:** Mac Newbold of Code Greene spoke on the Magento ecommerce framework for PHP. I’ve somewhat familiar with Magento, but a few things stood out:

- He finds the Magento Enterprise edition kind of problematic because Varien won’t support you if you have any unsupported extensions. Some of his customers had problems with Varien support and went back to the community edition.

- Magento is now up to around 30 MB of PHP files!

- As I’ve heard elsewhere, serious customization has a steep learning curve.

- The Magento data model is an EAV (Entity-Attribute-Value) model. To get 50 columns of output requires 50+ joins between 8 tables (one EAV table for each value datatype).

- There are 120 tables total in default install—​many core features don’t use the EAV tables for performance reasons.

- Another observation I’ve heard in pretty much every conversation about Magento: It is very resource intensive. Shared hosting is not recommended. Virtual servers should have a minimum of 1/2 to 1 GB RAM. Fast disk & database help most. APC cache recommended with at least 128 MB.

- A lot of front-end things are highly adjustable from simple back-end admin options.

- Saved credit cards are stored in the database, and the key is on the server. I didn’t get a chance to ask for more details about this. I hope it’s only the public part of a public/secret keypair!

It was a good overview for someone wanting to go beyond marketing feature lists.

**[Node.js](https://nodejs.org/):** Shane Hansen of Backcountry.com spoke on Node, comparing it to Tornado and Twisted in Python. He calls JavaScript “Lisp in C’s clothing”, and says its culture of asynchronous, callback-driven code patterns makes Node a natural fit.

Performance and parallel processing are clearly strong incentives to look into Node. The echo server does 20K requests/sec. There are 2000+ Node projects on GitHub and 500+ packages in npm (Node Package Manager), including database drivers, web frameworks, parsers, testing frameworks, payment gateway integrations, and web analytics.

A few packages worth looking into further:

- express — web microframework like Sinatra
- Socket-IO — Web Sockets now; falls back to other things if no Web Sockets available
- hummingbird — web analytics, used by Gilt.com
- bespin — “cloud JavaScript editor”
- yui3 — build HTML via DOM, eventbus, etc.
- connect — like Ruby’s Rack

I haven’t played with Node at all yet, and this got me much more interested.

**[Metasploit](https://www.metasploit.com/):** Jason Wood spoke on Metasploit, a penetration testing (or just plain penetrating!) tool. It was originally in Perl, and now is in Ruby. It comes with 590 exploits and has a text-based interactive control console.

Metasploit uses several external apps: nmap, Maltego (proprietary reconnaissance tool), Nessus (no longer open source, but GPL version and OpenVAS fork still available), Nexpose, Ratproxy, Karma.

The reconnaissance modules include DNS enumeration, and an email address collector that uses the big search engines.

It can backdoor PuTTY, PDFs, audio, and more.

This is clearly something you’ve got to experiment with to appreciate. Jason posted [his Metasploit talk slides](https://web.archive.org/web/*/http://www.jwnetworkconsulting.com/downloads/utos-msf-2010.pdf) which have more detail.

**So Many Choices: Web App Deployment with Perl, Python, and Ruby**: This was my talk, and it was a lot of fun to prepare for, as I got to take time to see some new happenings I’d missed in these three languages communities’ web server and framework space over the past several years.

The [slides give pointers](https://jon.endpoint.com/utosc-2010-slides/) to a lot of interesting projects and topics to check out.

My summary was this. We have an embarrassment of riches in the open source web application world. Perl, Python, and Ruby all have very nice modern frameworks for developing web applications. They also have several equivalent solid options for deploying web applications. If you haven’t tried the following, check them out:

- Perl: [Dancer](http://perldancer.org/), [Starman](https://metacpan.org/release/Starman)
- Python: [Flask](http://flask.pocoo.org/)
- Ruby: [Sinatra](http://sinatrarb.com/), [Unicorn](https://unicorn.bogomips.org/)

That’s about half of my notes on talks, but all I have time for now. I’ll cover more in a later post.
