---
author: Josh Williams
gh_issue_number: 1054
tags: ssl, sysadmin
title: Can we Server Name Indicate yet?
---



The encryption times, they are a-changin'.

Every once in a  while I'll take a look at the state of SNI, in the hopes that we're  finally ready for putting it to wide-scale use.

It started a few years back when [IPv6 got a lot of attention](http://www.worldipv6day.org/),  though in reality very few end user ISP's had IPv6 connectivity at that  time.  (And very few still do!  But that's another angry blog.)  So,  essentially, IPv4 was still the only option, and thus SNI was still  important.

Then earlier this year when Microsoft dropped [public]  support for Windows XP.  Normally this is one of those things that would  be pretty far off my radar, but Internet Explorer on XP is one of the  few clients* that doesn't support SNI.  So at that time, with hope in my  heart, I ran a search through the logs on a few of our more active  servers, only to find that roughly 5% of the hits are MSIE on Windows  XP.  So much for that.

(* Android < 3.0 has the same problem,  incidentally. But it in contrast constituted 0.2% of the hits.  So I'm  not as worried about the lack of support in that case.)

Now in  fairly quick succession a couple other things have happened: SSLv3 is  out, and SSL certificates with SHA-1 signatures are out.  This has me  excited.  I'll tell you why in a moment.

First, now that I've written "SNI" four times at this point I should probably tell you that it stands for [Server Name Indication](http://en.wikipedia.org/wiki/Server_Name_Indication),  and basically means the client sends the intended server name very  early in the connection process.  That gives the server the opportunity  to select the correct certificate for the given name, and present it to  the client.

If at this point you're yelling "of course!" at the screen, press Ctrl-F and search for "SSLv3" below.

For the rest, pull up a chair, it's time for a history lesson.

Back  in the day, when a web browser wanted to connect to a site it performed  a series of steps: it looks up the given name in DNS and gets an IP  address, connects to that IP address, and then requests the path in the  form of "GET /index.html".  Quite elegant, fairly straightforward.  And  notice the name only matters to the client, as it uses it for the DNS  look-up.  To the server it matters not at all.  The server accepts a  connection on an IP address and responds to the request for a specific path.

A need arose for secure communication.  Secure Socket Layer  (SSL) establishes an encrypted channel over which private information  can be shared.  In order to fight man-in-the-middle attacks, a  certificate exchange takes place. When the connection is made the server  offers up the certificate and the client (among other things I'm  glossing over) confirms the name on the certificate matches the name it  thinks it tried to connect to.  Note that the situation is much the same  as above, in that the client cares about the name, but the server just  serves up what it has associated with the IP address.

Around the  same time, the Host header appears.   Finally the browser has a way to  send the name of the site it's trying to access over to the server; it  just makes it part of the request.  What a simple thing it is, and what a  world that opens up on the server side.  Instead of associating a  single site per IP address, a single web server listening on one address  can examine the Host header and serve up a virtually unlimited number  of completely distinct sites.

However there's a problem.  At the  time, both were great advances.  But, unfortunately, were mutually  exclusive.  SSL is established first, immediately upon connection, and  after which the HTTP communication happens over the secure channel.  But  the Host header is part of the HTTP request.  Spot the problem yet?   The server has to serve up a certificate before the client has an  opportunity to tell the server what site it wants.  If the server has  multiple and it serves up the wrong one, the name doesn't match what the  client expects, and at best it displays a big, scary warning to the end  user, or at worst refuses to continue with communication.

There's  a few work-arounds, but this is already getting long and boring.  If  you're really curious, search for "Subject Alternate Name" and try to  imagine why it's an inordinately expensive solution when the list of  sites a server needs to support changes.

So for a long time, that  was the state of things.  And by a long time, I mean almost 20 years,  from when these standards were released.  In computing, that's a long  time.  Thus I'd hoped that by now, SNI would be an option as the real  solution.

Fast forward to the last few months.  We've had the news that [SSLv3 isn't to be trusted](https://isc.sans.edu/diary/SSLv3+POODLE+Vulnerability+Official+Release/18827), and the news that [SHA-1 signatures on SSL certificates are pretty un-cool](http://googleonlinesecurity.blogspot.com/2014/09/gradually-sunsetting-sha-1.html).   SHA-256 is in, and major CA's are now using that signature by default.   Why does this have me excited?  In the case of the former, Windows XP  pre-SP3 only supports up to SSLv3, so any site that's mitigated the  POODLE vulnerability is already excluding these clients.  Similarly  pre-IE8 clients are excluded by sites that have implemented SHA-2  certificates in the case of the latter.

Strictly speaking we're  not 100% there, as a fully up-to-date Internet Explorer on Windows XP is  still compatible with these recent SSL ecosystem changes.  But the sun  is setting on this platform, and maybe soon we'll be able to start  putting this IPv4-saving technology into use.

Soon.


