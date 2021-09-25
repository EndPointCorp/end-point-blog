---
author: Jon Jensen
title: Performance optimization of icdevgroup.org
github_issue_number: 211
tags:
- performance
- interchange
- seo
date: 2009-10-23
---

Some years ago Davor Ocelić redesigned [icdevgroup.org](http://www.icdevgroup.org/), Interchange's home on the web. Since then, most of the attention paid to it has been on content such as news, documentation, release information, and so on. We haven't looked much at implementation or optimization details. Recently I decided to do just that.

**Interchange optimizations**

There is currently no separate logged-in user area of icdevgroup.org, so Interchange is primarily used here as a templating system and database interface. The automatic read/write of a server-side user session is thus unneeded overhead, as is periodic culling of the old sessions. So I turned off permanent sessions by making all visitors appear to be search bots. Adding to interchange.cfg:

```plain
RobotUA *
```

That would not work for most Interchange sites, which need a server-side session for storing mv_click action code, scratch variables, logged-in state, shopping cart, etc. But for a read-only content site, it works well.

By default, Interchange writes user page requests to a special tracking log as part of its UserTrack facility. It also outputs an X-Track HTTP response header with some information about the visit which can be used by a (to my knowledge) long defunct analytics package. Since we don't need either of those features, we can save a tiny bit of overhead. Adding to catalog.cfg:

```plain
UserTrack No
```

Very few Interchange sites have any need for UserTrack anymore, so this is commonly a safe optimization to make.

**HTTP optimizations**

Today I ran the excellent webpagetest.org test, and this was the [icdevgroup.org test result](http://www.webpagetest.org/result/091023_2M8V/). Even though icdevgroup.org is a fairly simple site without much bloat, two obvious areas for improvement stood out.

First, gzip/deflate compression of textual content should be enabled. That cuts down on bandwidth used and page delivery time by a significant amount, and with modern CPUs adds no appreciable extra CPU load on either the client or the server.

We're hosting icdevgroup.org on Debian GNU/Linux with Apache 2.2, which has a reasonable default configuration of mod_deflate that does this, so it's easy to enable:

```plain
a2enmod deflate
```

That sets up symbolic links in /etc/apache2/mods-enabled for deflate.load and deflate.conf to enable mod_deflate. (Use a2dismod to remove them if needed.)

I added two content types for CSS & JavaScript to the default in deflate.conf:

```plain
AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css application/x-javascript
```

That used to be riskier when very old browsers such as Netscape 3 and 4 claimed to support compressed CSS & JavaScript but actually didn't. But those browsers are long gone.

The next easy optimization is to enable proxy and browser caching of static content: images, CSS, and JavaScript files. By doing this we eliminate all HTTP requests for these files; the browser won't even check with the server to see if it has the current version of these files once it has loaded them into its cache, making subsequent use of those files blazingly fast.

There is, of course, a tradeoff to this. Once the browser has the file cached, you can't make it fetch a newer version unless you change the filename. So we'll set a cache lifetime of only one hour. That's long enough to easily cover most users' browsing sessions at a site like this, but short enough that if we need to publish a new version of one of these files, it will still propagate fairly quickly.

So I added to the Apache configuration file for this virtual host:

```plain
ExpiresActive On
ExpiresByType image/gif  "access plus 1 hour"
ExpiresByType image/jpeg "access plus 1 hour"
ExpiresByType image/png  "access plus 1 hour"
ExpiresByType text/css   "access plus 1 hour"
ExpiresByType application/x-javascript "access plus 1 hour"
FileETag None
Header unset ETag
```

This adds the HTTP response header "Cache-Control: max-age=3600" for those static files. I also have Apache remove the ETag header which is not needed given this caching and the Last-modified header.

There are cases where the above configuration would be too broad, for example, if you have:

- images that differ with the same filename, such as CAPTCHAs
- static files that vary based on logged-in state
- dynamically-generated CSS or JavaScript files with the same name

If the website is completely static, including the HTML, or identical for all users at the same time even though dynamically generated, we could also enable caching the HTML pages themselves. But in the case of icdevgroup.org, that would probably cause trouble with the Gitweb repository browser, live documentation searches, etc.

After those changes, we can see the [results of a new webpagetest.org run](http://www.webpagetest.org/result/091023_2M91/) and see that we reduced the bytes transferred, and the delivery time. It's especially dramatic to see how much faster subsequent page views of the Hall of Fame are, since it has many screenshot thumbnail images.

Optimizing a simple non-commerce site such as icdevgroup.org is easy and even fun. With caution and practicing on a non-production system, complex ecommerce sites can be  optimized using the same techniques, with even more dramatic benefits.
