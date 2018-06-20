---
author: "David Christensen"
title: "Instant TLS Upgrades Through Proxy Magic!"
tags: ecommerce, nginx, proxies, rails, security, sysadmin, hosting, tls
gh_issue_number: 1434
---

<img alt="cards" src="/blog/2018/06/14/tls-proxy-magic/cards.jpg" />

### TLS shutdowns are real

The payment gateways have been warning for years about the impending and required TLS
updates. Authorize.net and PayPal—to name a few—have stopped accepting transaction requests from
servers using TLS 1.0. Despite the many warnings about this (and many delays in the final
enforcement date), some projects are affected by this and payments are coming to a stop, customers
cannot checkout, and e-commerce is at a standstill.

Ideally, getting to security compliance would include a larger migration to update your underlying
operating system and your application. But a migration and software update can be an expensive
project and in some cases, the business can’t wait weeks while this is done.

End Point has worked with several clients recently to try to remedy the situation by using a reverse
proxy to fix this and we’ve had good success on getting payments flowing again.

### What is a proxy?

A proxy is a mid-point, essentially a digital middleman, moving your data from one place to another.
In two recent client instances, we ended up using nginx (the stack’s webserver) as
the reverse proxy, basically running a separate server for just shuttling requests to/​from the
payment gateway. Since we want to be able to run the gateway in both live and test modes, we use
two separate server definitions in our nginx include, one for each.

Since the proxy is talking to the gateway in TLS 1.2 the payment gateway is happy. Since the
application can talk http to the proxy running on the same machine, your application is happy.
Since payments are now flowing, the business is happy.

### Why use a proxy?

While we always impress on clients the importance of staying up-to-date with their entire stack (operating system,
language, application frameworks), this is not always practical for some sites, whether for cost
reasons or some technical limitations which keep them on a specific library or framework version.
In our case, these clients had been migrated to CentOS 7 already (which supports TLS 1.2), but the
versions of Ruby and Ruby on Rails they were on were too old to be able to use the TLS 1.2 libraries
built-in.

This can then be a fast way to get payments flowing again, ideally the first step on updating the
site to work with a modern stack. This can also minimize development costs compared to doing a full
migration or complete stack upgrade.

### Steps

- Run on an operating system version that supports TLS 1.2 natively. In practice for us, this is CentOS 7, but modern Debian, Ubuntu, and other Linux distributions would work.

- Locate the existing payment gateway URLs for live and test modes. For Authorize.net, this differs depending on if you are connecting to their legacy systems or their modern systems.

- Set up and configure the proxy. We used nginx for this; a later section covers the sample configs with explanations. We created a config file that we can just drop in an `/etc/nginx/sites/` directory to be able to quickly set up and deploy the reverse proxies.

- Adjust the configuration of the software to point to alternate payment gateway URLs. If you are using Rails’ ActiveMerchant, this can be accomplished via an application-level configuration override. We provide an example of the overriding of the live/test mode URLs for a Rails application later.

### nginx sample config

```
# apitest.authorize.net

server {
    listen 127.0.0.1:1337 default_server;

    resolver 8.8.8.8;

    access_log /var/log/nginx/sites/authnet-proxies/access_log;
    error_log /var/log/nginx/sites/authnet-proxies/error_log warn;

    location / {
        proxy_pass_header Authorization;
        proxy_pass https://apitest.authorize.net$request_uri;
        proxy_set_header Host apitest.authorize.net;
        proxy_redirect off;
    }
}

# api.authorize.net

server {
    listen 127.0.0.1:1338 default_server;

    resolver 8.8.8.8;

    access_log /var/log/nginx/sites/authnet-proxies/access_log;
    error_log /var/log/nginx/sites/authnet-proxies/error_log warn;

    location / {
        proxy_pass_header Authorization;
        proxy_pass https://api.authorize.net$request_uri;
        proxy_set_header Host api.authorize.net;
        proxy_redirect off;
    }
}
```

In this file, we are defining a separate server block for each service (test mode and production),
choosing an arbitrarily defined TCP port. Because nginx is speaking TLS 1.2 to the upstream gateway
and we are speaking plain HTTP only to `localhost` and not storing any information regarding the request, we
are able to fulfill the PCI DSS requirements.

A few notes about this:

- We needed the `resolver` line for this to work given our configuration/​setup because we are
  referring to the upstream servers by domain name instead of IP addresses; we just used the
  easily-memorable Google public DNS resolver servers for this purpose.

- We need the `Authorization` header passed through the proxy, as this is what contains the site
  credentials when making a request from ActiveMerchant.

- We need the `Host` header defined explicitly in the server block, as we want to override the
  `localhost` value that will be sent by the application due to application configuration.
  Authorize.net was (understandably) very picky about this being provided and correct.

- The port numbers here are arbitrary and just need to match what we configure the application to
  connect to; one for the test server and one for production.

- This setup will work for multiple development environments running on the same server as long as
  they are configured to point to the correct test/​live server. There is nothing inherently
  insecure about doing this, as no authorization is shared, it just bounces the connection.

### Rails sample application config

A configuration file for the Authorize.net CIM gateway, for clients using ActiveMerchant as the base for payment gateway integration:

```rb
require File.expand_path('../boot', __FILE__)
require 'rails/all'

module MyApp
  class Application < Rails::Application
    ActiveMerchant::Billing::AuthorizeNetCimGateway.test_url = 'http://localhost:1337/xml/v1/request.api'
    ActiveMerchant::Billing::AuthorizeNetCimGateway.live_url = 'http://localhost:1338/xml/v1/request.api'
  end
end
```

And another one for the legacy Authorize.net gateway:

```rb
require File.expand_path('../boot', __FILE__)
require 'rails/all'

module MyApp
  class Application < Rails::Application
    ActiveMerchant::Billing::AuthorizeNetGateway.test_url = 'http://localhost:1337/gateway/transaction.dll'
    ActiveMerchant::Billing::AuthorizeNetGateway.live_url = 'http://localhost:1338/gateway/transaction.dll'
  end
end
```

Ensure that you override the URLs depending on the gateway setup that your merchant account is set up for. Also make sure that your `localhost` URLs are using the ports corresponding to the `server` blocks set up in nginx to make sure these are proxying to the correct server.

While this example is using Authorize.net, you could use a similar setup for any payment gateway which allows you to set the URLs.

### Summary

Hopefully this gives you some ideas about how you can use reverse proxies to upgrade the outgoing
connection strength. If you need assistance getting something like this set up, feel free to [contact us](/contact) for help.

<hr>

(Co-authored by [Elizabeth Garrett Christensen](/team/elizabeth_garrett_christensen).)
