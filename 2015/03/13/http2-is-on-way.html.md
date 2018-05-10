---
author: Jon Jensen
gh_issue_number: 1101
tags: networking, sysadmin
title: HTTP/2 is on the way!
---

### HTTPS and SPDY

Back in August 2014, we made our websites [www.endpoint.com](/) and [liquidgalaxy.endpoint.com](https://liquidgalaxy.endpoint.com/) HTTPS-only, which allowed us to turn on [HTTP Strict Transport Security](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security) and earn a grade of [A+ from Qualys’ SSL Labs](https://www.ssllabs.com/ssltest/analyze.html?d=endpoint.com&latest) server test.

Given the widely-publicized surveillance of Internet traffic and injection of advertisements and tracking beacons into plain HTTP traffic by some unscrupulous Internet providers, we felt it would be good to start using TLS encryption on even our non-confidential public websites.

This removed any problems switching between HTTP for most pages and HTTPS for the contact form and the POST of submitted data. Site delivery over HTTPS also [serves as a ranking signal](https://webmasters.googleblog.com/2014/08/https-as-ranking-signal.html) for Google, though presumably still a minor one.

Doesn’t SSL/TLS slow down a website? Simply put, not really these days. See [Is TLS Fast Yet?](https://istlsfastyet.com/) for lots of details. And:

Moving to HTTPS everywhere on our sites also allowed us to take advantage of nginx’s relatively new [SPDY](https://en.wikipedia.org/wiki/SPDY) (pronounced “speedy”) capability. SPDY is an enhancement to HTTPS created by Google to increase web page delivery time by compressing headers and multiplexing many requests in a single TCP connection. It is only available on HTTPS, so it also incentivizes sites to stop using unencrypted HTTP in order to get more speed, with security as a bonus. Whereas people once avoided HTTPS because SSL/TLS was slower, SPDY turned that idea around. We began offering SPDY for our sites in October 2014.

On the browser side, SPDY was initially only supported by Chrome and Firefox. Later support was added to Opera, Safari 8, and partially in IE 11. So most browsers can use it now.

There is only partial server support: In the open source world, nginx fully supports SPDY now, but Apache’s mod_spdy is incomplete and development on it has stalled.

Is SPDY here to stay? After all it was an experimental Google protocol. Instead of getting on track to become an Internet standard protocol as is, it was used as the starting point for the next version of HTTP, HTTP/2. That sounded like good news, except that the current version HTTP/1.1 was standardized in 1999 and hadn’t really changed since then. Many of us wondered if HTTP/2 would get mired in the standardization process and take years to see the light of day.

However, the skeptics were wrong! HTTP/2 was completed over about 3 years, and its official RFC form is now being finalized. Having it be the next version of HTTP will go a long way toward getting more implementation and adoption, since it is no longer a single company’s project. On the other hand, basing HTTP/2 on SPDY meant that there was a widely-used proof of concept out there already, so discussions didn’t get lost in the purely theoretical. The creators of SPDY at Google were heavily involved in the HTTP/2 standardization process, so their lessons were not lost, and it appears that HTTP/2 will be even better.

### What is different in HTTP/2?

- Request and response multiplexing in a single TCP connection (no need for 6+ connections to the same host!)
- Stream prioritization (prioritizing files that the client most needs first)
- Server push (of files the server expects the client to need, before the client knows it), and client stream cancellation (in case the server or the client is wrong and wants to abort a stream)
- Binary framing (no more hand-typing requests via telnet, sadly)
- Header compression (greatly reducing the bloat of large cookies)
- Backward-compatibility with HTTP/1.1 and autodiscovery of HTTP/2 support (transparent upgrading for users)
- When TLS is used, require TLS 1.2 and minimum acceptable cipher strength (to help retire weak TLS setups)

For front-end web developers, these back-end plumbing changes have some very nice consequences. As described in [HTTP2 for front-end web developers](https://mattwilcox.net/web-development/http2-for-front-end-web-developers), you will soon be able to stop using many of the annoying workarounds for HTTP/1.1’s weaknesses: no more sprites, combining CSS & JavaScript files, inlining images in CSS, sharding across many subdomains, etc.

This practically means that the web can largely go back to working the way it was designed, with different files for different things, independent caching of small files, serve assets from the same place.

### What is *not* changing?

Most of HTTP/1.1 basic semantics remain the same, with most of the changes being to the “wrapping” or transport of the data. All this stays the same:

- built on TCP
- stateless
- same request methods
- same request headers (including cookies)
- same response headers and body
- may be unencrypted or layered on TLS (although so far, Chrome and Firefox have stated that they will only support HTTP/2 over TLS, and IE so far only supports HTTP/2 over TLS as well)
- no changes in HTML, CSS, client-side scripting, same-origin security policy, etc.

### The real point: speed

Speed and efficiency are the main advantages of HTTP/2. It will use less data transfer for both requests and responses. It will use fewer TCP connections, lightening the load on clients, servers, firewalls, and routers.

As clients adapt more to HTTP/2, it will probably provide a faster perceived experience as servers push the most important CSS, images, and JavaScript proactively to the client before it has even parsed the HTML.

See these [simple benchmarks between HTTP/1.1, SPDY, and HTTP/2](https://blog.httpwatch.com/2015/01/16/a-simple-performance-comparison-of-https-spdy-and-http2/).

### When can we use it?

Refreshingly, Google has announced that they are happy to kill their own creation SPDY: [they will drop support for SPDY from Chrome in early 2016](https://blog.chromium.org/2016/02/transitioning-from-spdy-to-http2.html) in favor of HTTP/2.

[Firefox uses HTTP/2 by default](http://bitsup.blogspot.com/2015/02/http2-is-live-in-firefox.html) where possible, and Chrome has an option to enable HTTP/2. IE 11 for Windows 10 beta supports HTTP/2. You can see if your browser supports HTTP/2 now by using the [Go language HTTP/2 demo server](https://http2.golang.org/).

On the server side, Google and Twitter already have been opportunistically serving HTTP/2 for a while. [nginx plans to add support this year](https://nginx.com/blog/how-nginx-plans-to-support-http2/), and an experimental [Apache module mod_h2](https://icing.github.io/mod_h2/) is available now. The H2O open-source C-based web server [supports HTTP/2 now](http://blog.kazuhooku.com/2015/02/h2o-new-http-server-goes-version-100-as.html), as does Microsoft IIS for Windows beta 10.

So we probably have at least a year until the most popular open source web servers easily support HTTP/2, but by then most browsers will probably support it and it should be an easy transition, as SPDY was. As long as you’re ready to go HTTPS-only for your site, anyway. :)

I think HTTP/2 will be a good thing!

### Give me more details!

I highly recommend that system administrators and developers read the excellent [http2 explained](https://daniel.haxx.se/http2/) PDF book by Daniel Stenberg, Firefox developer at Mozilla, and author of curl. It explains everything simply and well.

Other reference materials:

- [HTTP/2 Approved](https://www.ietf.org/blog/2015/02/http2-approved/) on the IETF blog, by Mark Nottingham, chair the IETF HTTP Working Group
- [HTTP/2 home page](https://http2.github.io/) with specifications and FAQs
- [High Performance Browser Networking chapter 12 on HTTP/2](http://chimera.labs.oreilly.com/books/1230000000545/ch12.html) by Ilya Grigorik
- [HTTP/2 on Wikipedia](https://en.wikipedia.org/wiki/HTTP/2)
- [Nine Things to Expect from HTTP/2](https://www.mnot.net/blog/2014/01/30/http2_expectations) by Mark Nottingham
- [Making the Web Faster with HTTP 2.0: HTTP continues to evolve](http://queue.acm.org/detail.cfm?id=2555617) by Ilya Grigorik of Google
- [TLS in HTTP/2](https://daniel.haxx.se/blog/2015/03/06/tls-in-http2/): Daniel Stenberg on TLS in HTTP/2 being mandatory in effect if not in the specification, and discusses opportunistic encryption
- [HTTP/2 and the Internet of Things](http://robbysimpson.com/2015/01/26/http2-and-the-internet-of-things/) by Robby Simpson of GE Digital Energy
- [HTTP/2.0—​The IETF is Phoning It In: Bad protocol, bad politics](http://queue.acm.org/detail.cfm?id=2716278) by Poul-Henning Kamp, author of Varnish
