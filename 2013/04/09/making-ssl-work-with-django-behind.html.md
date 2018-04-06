---
author: Greg Davidson
gh_issue_number: 786
tags: sysadmin, django, python, tls
title: Making SSL Work with Django Behind an Apache Reverse Proxy
---

### Bouncing Admin Logins

We have a [Django](https://www.djangoproject.com/) application that runs on [Gunicorn](http://gunicorn.org/) behind an [Apache](https://httpd.apache.org/) reverse proxy server. I was asked to look into a strange issue with it: After a successful login to the admin interface, the browser was re-directed to the http (non-SSL) version of the interface.

After some googling and investigation I determined the issue was likely due to our specific server arrangement. Although the login requests were made over https, the requests proxied by Apache to Gunicorn used http (securely on the same host). Checking the Apache SSL error logs quickly affirmed this suspicion. I described the issue in the #django channel on [freenode IRC](http://freenode.net/) and received some assistance from Django core developer [Carl Meyer](https://github.com/carljm). As of Django 1.4 there was a new setting Carl had [developed](https://code.djangoproject.com/ticket/14597#comment:16) to handle this particular scenario.

### Enter SECURE_PROXY_SSL_HEADER

The documentation for the [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header) variable describes how to configure it for your project. I added the following to the settings.py config file:

```
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Because this setting tells Django to trust the X-Forwarded-Proto header coming from the proxy (Apache) there are security concerns which must be addressed. The details are described in the Django documentation and this is the Apache configuration I ended up with:

```
# strip the X-Forwarded-Proto header from incoming requests
RequestHeader unset X-Forwarded-Proto

# set the header for requests using HTTPS
RequestHeader set X-Forwarded-Proto https env=HTTPS
```

With SECURITY_PROXY_SSL_HEADER in place and the Apache configuration updated, logins to the admin site began to work correctly.

This is standard practice for web applications that reside behind an HTTP reverse proxy, but if the application was initially set up using only plain HTTP, when HTTPS is later added, it can be easy to be confused and overlook this part of the setup.
