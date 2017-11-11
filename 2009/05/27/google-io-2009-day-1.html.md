---
author: Jon Jensen
gh_issue_number: 153
tags: conference
title: Google I/O 2009 day 1
---

I'm at [Google I/O](http://code.google.com/events/io/) at the Moscone Center in downtown San Francisco, and today was the first day. Everything was bustling:

<a href="http://picasaweb.google.com/lh/photo/FoyB9K0LL6YIfh94lTYpKg?feat=embedwebsite"><img src="/blog/2009/05/27/google-io-2009-day-1/image-0.jpeg"/></a>

<a href="http://picasaweb.google.com/lh/photo/l3xOILBBNBpHL6ZlCKxkLw?feat=embedwebsite"><img src="/blog/2009/05/27/google-io-2009-day-1/image-0.jpeg"/></a>

<a href="http://picasaweb.google.com/lh/photo/fMULbclxEUCXrw5irTuekw?feat=embedwebsite"><img src="/blog/2009/05/27/google-io-2009-day-1/image-0.jpeg"/></a>

The opening keynote started with Google CEO Eric Schmidt, and I was worried wondering how he would make over an hour be interesting. He only took a few minutes, then Vic Gundotra, VP of Engineering, led the rest of the keynote which had many presenters showing off various projects, starting with 5 major HTML 5 features already supported in Chrome, Firefox, Safari, and Opera:

Matt Waddell talked about Canvas, the very nice drawing & animation API with pixel-level control. Brendan Gibson of Backcountry.com used this at [SteepandCheap.com](http://www.steepandcheap.com/) and sister sites for the cool People on Site graphs (with a workaround for Internet Explorer which doesn't support Canvas yet). Also a quick demo of [Bespin](https://bespin.mozilla.com/), an IDE in the browser.

Matt Papakipos showed off [o3d](http://code.google.com/apis/o3d), 3-D in the browser with just HTML 5, JavaScript, and CSS. Also the new <video> tag that makes video as easy as <img> is. Geolocation has come a long way with cell tower and wi-fi ID coverage over much of the globe.

Jay Sullivan, VP of Mozilla, showed off Firefox 3.5's upcoming features. Basically all of the above plus app cache & database (using SQLite) and web workers (background JavaScript that won't freeze the browser).

Michael Abbott, SVP of Palm, showed off their webOS 1.0 which uses HTML 5.

A good summary of the 5 big features of HTML 5 is in [Tim O'Reilly's blog post](http://radar.oreilly.com/2009/05/google-bets-big-on-html-5.html) about it.

Kevin Gibbs & Andrew Bowers of Google gave some numbers about [Google App Engine](http://code.google.com/appengine/): 200K+ developers, 80K+ apps. Coming in App Engine: background processing, large object storage, database export, XMPP, incoming email. He also showed off Google Web Toolkit a bit, with code written in Java that compiles down to JavaScript with per-browser tweaks automatically handled.

DeWitt Clinton, Tech Lead at Google, showed [Google Web Elements](http://www.google.com/webelements), embeddable Google apps similar to the way YouTube & AdSense have always worked. Currently conversations, maps, search. A [blog post by Tim O'Reilly](http://radar.oreilly.com/2009/05/google-web-elements-and-google.html) gives more details about Web Elements.

Romain Guy, Software Engineer at Google, showed off Android's coming text to speech functionality. Then all attendees were told we'll be receiving a new Google Ion (aka HTC Magic) phone, the unlocked developer edition, with a SIM card for T-Mobile giving 30 days of unlimited 3G data & domestic voice so we can play with it. That was enthusiastically received. Certain attendees such as myself were hoping there'd be a discounted way to buy one at the conference, so this surprise worked out nicely. :) [Various](http://www.androidandme.com/2009/05/news/unboxing-the-google-ion-free-htc-magic-phone-from-google-io/) [people](http://www.techcrunch.com/2009/05/27/googles-oprah-moment-an-android-phone-for-everyone-at-google-io/#comment-2769145) wrote this up in more detail. Here's mine getting unpacked:

<a href="http://picasaweb.google.com/lh/photo/cSUkooe3aHAgLInAQq6n-w?feat=embedwebsite"><img src="/blog/2009/05/27/google-io-2009-day-1/image-0.jpeg"/></a>

The rest of the conference was split into various tracks, and I stuck mostly with Google App Engine talks which were good. Most useful was Brett Slatkin's on using Datastore's list properties with separate entities just for lists that can be used just for their indexes in queries without serializing/deserializing the lists which avoids a lot of CPU overhead but is a little tricky to set up.

The after-hours party (dinner, music, silly video games, etc.) is now winding up, and a semi-drunk guy is walking around with a garbage can asking for laptops we want to throw away. I still need this one for a while longer, so I declined his helpful offer.
