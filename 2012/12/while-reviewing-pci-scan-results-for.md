---
author: Ron Phipps
title: Redirect from HTTP to HTTPS before basic auth
github_issue_number: 741
tags:
- apache
- audit
- hosting
- security
date: 2012-12-22
---



While reviewing PCI scan results for a client I found an issue where the scanner had an issue with a private admin URL requesting basic http auth over HTTP.  The admin portion of the site has its own authentication method and it is served completely over HTTPS.  We have a second layer of protection with basic auth, but the issue is the username and password could be snooped on since it can be accessed via HTTP.

The initial research and attempts at fixing the problem did not work out as intended.  Until I found [this blog post on the subject](http://misof.blog.matfyz.sk/p10659-redirection-to-https-done-the-right-way).  The blog laid out all of the ways that I had already tried and then a new solution was presented.

I followed the recommended hack which is to use SSLRequireSSL in a location matching the admin and a custom 403 ErrorDocument.  This 403 ErrorDocument does a bit of munging of the URL and redirects from HTTP to HTTPS.  The instructions in the blog did have one issue, in our environment I could not serve the 403 document from the admin, I had to have it in an area that could be accessed by HTTP and by the public.  I'm not sure how it could work being served from a URL that requires ssl and is protected by basic auth.  The reason that this hack does work is because SSLRequireSSL is processed before any auth requirements and ErrorDocument 403 is presented when SSL is not being used.

Now hopefully the scanner will be happy (as happy as a scanner can be) by always requiring HTTPS when /admin appears in the URL and presenting an error when that is not the case, before the basic auth is requested.


