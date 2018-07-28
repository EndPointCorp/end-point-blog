---
author: Josh Williams
gh_issue_number: 464
tags: ipv6, networking, sysadmin
title: 'June 8, 2011: World IPv6 Day'
---

<img alt="This post has 6 a lot" border="0" src="http://joshwilliams.name/ipv6/hev6certshirt.jpg"/>

I’m a little surprised they didn’t do it today. 06-06, what better day for IPv6? Oh well, at least Hurricane Electric was awesome enough to send a Sage certification shirt just in time!

June 8th, 2011 is the day! In just a couple days time [World IPv6 Day](https://web.archive.org/web/20110606225039/http://www.worldipv6day.org/) begins. Several of the largest and most popular sites on the Internet, [and many others](https://web.archive.org/web/20110613121940/http://www.worldipv6day.org/participants/), turn on IPv6 addresses for a 24-hour interval. Many of them already have it, but you have to seek it out on a separate address. Odds are if you’re seeking that out specifically you’re configured well enough to not have any problems. But with IPv6 configured on the primary addresses of some of the largest Internet sites, people that don’t specifically know they’re testing something become part of the test. That’s important to track down exactly what composes those [1-problem-in-2,000 configurations](https://www.facebook.com/notes/facebook-engineering/world-ipv6-day-solving-the-ip-address-chicken-and-egg-challenge/484445583919), and assess if that’s even an accurate number these days.

Not sure about your own connection? [https://test-ipv6.com/](https://test-ipv6.com/) is an excellent location to run a number of tests and see how v6-enabled you are. Odds are you’ll end up at one end of the spectrum or the other. But if there’s a configuration glitch that could help you track it down.

At End Point we decided to get a bit of a head start. For the last 24 hours or so www.endpoint.com has been running with an IPv6 AAAA record. And it was pleasantly surprising, the first IPv6 hits started showing up nearly instantaneously! Our visitors are in general likely to be more on the technical side of the scale, but so far the results have been promising. By all accounts everything works as it should. Soon, we’ll likely begin offering to enable it for some of our customer sites.

A part of me wants to express some disappointment that an event like this is even necessary. My favorite database project got IPv6 support way back in the [PostgreSQL 7.4 release](https://www.postgresql.org/docs/9.0/static/release-7-4.html), now long under EOL. But at the same time I know what a huge undertaking the IPv6 migration is on a number of levels. Encouragement by providers and end user awareness go a long way to help things along. So I applaud those sites taking part in World IPv6 Day, helping pave the way for the next generation protocol.

I kinda feel for the tunnel providers, now that I think about it. I’ve had a [Hurricane Electric](https://tunnelbroker.net/) tunnel that’s been carrying my home traffic for quite a while now. So far, that’s primarily been things like IRC over to Freenode, ssh traffic to the servers that have IPv6 addresses, a few random hits to sites that have it, etc. But with high bandwidth sites like YouTube and frequently hit CDN providers on board for World IPv6 Day I’d bet that those tunnels will see traffic spike dramatically.

Granted a number of the tunnel providers are running portions of the Internet backbone anyway, but there’s only a handful of tunnel endpoints for that traffic to go through. It’s also forcing it to travel over sections of the provider’s network before it can find its way out to a peer. Both of these are pretty substantial barriers to route optimization, at least compared to native traffic. Don’t get me wrong, even as it is the performance of the tunnel has been great. I just hope providing an arguably necessary (and free!) service isn’t too painful to these providers while end-user deployments are still occurring.
