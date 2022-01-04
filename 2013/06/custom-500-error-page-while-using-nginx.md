---
author: Richard Templet
title: Custom 500 error page while using nginx proxying
github_issue_number: 824
tags:
- nginx
- sysadmin
date: 2013-06-21
---



I was working with our customer [Paper Source](https://www.paper-source.com/) to setup a 500 error page that looked like the rest of the site when I ran into something interesting. I went through the nginx configuration and added this line to allow for a custom 500 error page just like I had done for the custom 404 error page.

```plain
error_page   500  =  /cgi-bin/paper/500.html;
```

What I noticed when I forced the site to create an Internal Server Error was that I was still getting the ugly normal Apache version of the 500 error page. It seemed like nginx was ignoring the error_page directive. I did some searching and found out that you have to use the [proxy_intercept_errors](https://wiki.nginx.org/HttpProxyModule#proxy_intercept_errors) directive.

```plain
proxy_intercept_errors on;
```

This directive allows nginx to recognize the 500 error code being returned from Apache and run its own directives to display the right page.


