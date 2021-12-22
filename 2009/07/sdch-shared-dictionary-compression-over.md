---
author: Jon Jensen
title: 'SDCH: Shared Dictionary Compression over HTTP'
github_issue_number: 177
tags:
- browsers
- hosting
- networking
- security
- compression
date: 2009-07-27
---

Here’s something new in HTTP land to play with: Shared Dictionary Compression over HTTP (SDCH, apparently pronounced “sandwich”) is a new HTTP 1.1 extension announced by Wei-Hsin Lee of Google last September. Lee explains that with it “a user agent obtains a site-specific dictionary that then allows pages on the site that have many common elements to be transmitted much more quickly.” SDCH is applied before gzip or deflate compression, and Lee notes 40% better compression than gzip alone in their tests. Access to the dictionaries stored in the client is scoped by site and path just as cookies are.

The first client support was in the Google Toolbar for Internet Explorer, but it is now going to be much more widely used because it is supported in the Google Chrome browser for Windows. (It’s still not in the latest Chrome developer build for Linux, or at any rate not enabled by default if the code is there.)

Only Google’s web servers support it to date, as far as I know. Someone intended to start a mod_sdch project for Apache, but there’s no code at all yet and no activity since September 2008.

It is interesting to consider the challenge this will have on HTTP proxies that filter content, since the entire content would not be available to the proxy to scan during a single HTTP conversation. Sneakily-split malicious payloads would then be reassembled by the browser or other client, not requiring JavaScript or other active reassembly methods. [This forum thread](http://prxbx.com/forums/showthread.php?tid=1379&pid=12519) discusses this threat and gives an example of stripping the Accept-encoding: sdch request headers to prevent SDCH from being used at all. Though the threat is real, it’s hard to escape the obvious analogy with TCP filtering, which had to grow from stateless to more difficult stateful TCP packet inspection. New features mean not just new benefits but also new complexity, but that’s not reason to reflexively reject them.

SDCH references:

- [SDCH Google Group](https://groups.google.com/forum/#!forum/SDCH) which includes the specification PDF and ongoing discussion
- [Wei-Hsin Lee’s presentation slides on SDCH](http://assets.en.oreilly.com/1/event/7/Shared%20Dictionary%20Compression%20Over%20HTTP%20Presentation.ppt)
- [IETF mailing list announcement of SDCH](https://lists.w3.org/Archives/Public/ietf-http-wg/2008JulSep/0441.html) and ensuing discussion thread
- [Velocity 2008 conference notes](http://www.webadminblog.com/index.php/2008/06/24/the-velocity-2008-conference-experience-part-vi/) where the pronunciation of SDCH is given as “sandwich”
- Vaporware [Apache mod_sdch project](https://code.google.com/archive/p/mod-sdch/)
