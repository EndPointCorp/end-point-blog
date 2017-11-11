---
author: Jon Jensen
gh_issue_number: 379
tags: ecommerce, hosting, optimization, performance, rails, spree
title: Speeding up the Spree demo site
---

There's a lot that can be done to speed up Spree, and Rails apps in general. Here I'm not going to deal with most of that. Instead I want to show how easy it is to speed up page delivery using standard HTTP server tuning techniques, demonstrated on [demo.spreecommerce.com](http://demo.spreecommerce.com/).

First, let's get a baseline performance measure from the excellent webpagetest.org service using their remote Internet Explorer 7 tests:

- First page load time: **2.1 seconds**
- Repeat page load time: **1.5 seconds**

The repeat load is faster because the browser has images, JavaScript, and CSS cached, but it still has to check back with the server to make sure they haven't changed. Full details are [in this initial report](http://www.webpagetest.org/result/101102_ACDT/).

The demo.spreecommerce.com site is run on a Xen VPS with 512 MB RAM, CentOS 5 i386, Apache 2.2, and Passenger 2.2. There were several things to tune in the Apache httpd.conf configuration:

- mod_deflate was already enabled. Good. That's a big help.
- Enable HTTP keepalive: KeepAlive On and KeepAliveTimeout 3
- Limit Apache children to keep RAM available for Rails: StartServers 5, MinSpareServers 2, MaxSpareServers 5
- Limit Passenger pool size to 2 child processes (down from the default 6), to queue extra requests instead of using slow swap memory: PassengerMaxPoolSize 2
- Enable browser &amp; intermediate proxy caching of static files: ExpiresActive On and ExpiresByType image/jpeg "access plus 2 hours" etc. (see below for full example)
- Disable ETags which aren't necessary once Expires is enabled: FileETag None and Header unset ETag
- Disable unused Apache modules: free up memory by commenting out LoadModule proxy, proxy_http, info, logio, usertrack, speling, userdir, negotiation, vhost_alias, dav_fs, autoindex, most authn_* and authz_* modules
- Disable SSLv2 (for security and PCI compliance, not performance): SSLProtocol all -SSLv2 and SSLCipherSuite ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:-LOW:-SSLv2:-EXP

After making these changes, without tuning Rails, Spree, or the database at all, a new webpagetest.org run reports:

- First page load time: **1.2 seconds**
- Repeat page load time: **0.4 seconds**

That's an easy improvement, a reduction of 0.9 seconds for the initial load and 1.1 seconds for a repeat load! Complete details are in [this follow-on report](http://www.webpagetest.org/result/101102_ACF7/).

The biggest wins came from enabling HTTP keepalive, which allows serving multiple files from a single HTTP connection, and enabling static file caching which eliminates the majority of requests once the images, JavaScript, and CSS are cached in the browser.

Note that many of the resource-limiting changes I made above to Apache and Passenger would be too restrictive if more RAM or CPU were available, as is typical on a dedicated server with 2 GB RAM or more. But when running on a memory-constrained VPS, it's important to put such limits in place or you'll practically undo any other tuning efforts you make.

I wrote about these topics a year ago in a blog post about [Interchange ecommerce performance optimization](http://blog.endpoint.com/2009/10/performance-optimization-of.html). I've since expanded the list of MIME types I typically enable static asset caching for in Apache. Here's a sample configuration snippet to put in the <VirtualHost> container in httpd.conf:

```nohighlight
    ExpiresActive On
    ExpiresByType image/gif   "access plus 2 hours"
    ExpiresByType image/jpeg  "access plus 2 hours"
    ExpiresByType image/png   "access plus 2 hours"
    ExpiresByType image/tiff  "access plus 2 hours"
    ExpiresByType text/css    "access plus 2 hours"
    ExpiresByType image/bmp   "access plus 2 hours"
    ExpiresByType video/x-flv "access plus 2 hours"
    ExpiresByType video/mpeg  "access plus 2 hours"
    ExpiresByType video/quicktime "access plus 2 hours"
    ExpiresByType video/x-ms-asf  "access plus 2 hours"
    ExpiresByType video/x-ms-wm   "access plus 2 hours"
    ExpiresByType video/x-ms-wmv  "access plus 2 hours"
    ExpiresByType video/x-ms-wmx  "access plus 2 hours"
    ExpiresByType video/x-ms-wvx  "access plus 2 hours"
    ExpiresByType video/x-msvideo "access plus 2 hours"
    ExpiresByType application/postscript        "access plus 2 hours"
    ExpiresByType application/msword            "access plus 2 hours"
    ExpiresByType application/x-javascript      "access plus 2 hours"
    ExpiresByType application/x-shockwave-flash "access plus 2 hours"
    ExpiresByType image/vnd.microsoft.icon      "access plus 2 hours"
    ExpiresByType application/vnd.ms-powerpoint "access plus 2 hours"
    ExpiresByType text/x-component              "access plus 2 hours"
```

Of course you'll still need to tune your Spree application and database, but why not tune the web server to get the best performance you can there?
