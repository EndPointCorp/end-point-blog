---
author: Brian Gadoury
gh_issue_number: 950
tags: camps, nginx, rails
title: Proxy Nginx ports using a regular expression
---

I’m working on a big Rails project for Phenoms Fantasy Sports that uses the [ActiveMerchant gem](https://rubygems.org/gems/activemerchant) to handle [Dwolla](https://www.dwolla.com/developers) payments. One of the developers, [Patrick](/team/patrick_lewis), ran into an issue where his code wasn’t receiving the expected postback from the Dwolla gateway. His code looked right, the Dwolla account UI showed the sandbox transactions, but we never saw any evidence of the postback hitting our development server.

Patrick’s theory was that Dwolla was stripping the port number off the postback URL he was sending with the request. We tested that theory by using the [RequestBin.com service](https://requestbin.com/) for the postback URL, and it showed Dwolla making the postback successfully. Next, we needed to verify that Dwolla could hit our development server on port 80.

I started Nginx on port 80 of our dev server and Patrick fired his Dwolla transaction test again. The expected POST requests hit the Nginx logfile. Suspicions confirmed. It looked like we would just have to work around the Dwolla weirdness by proxying port 80 to the port that Patrick’s development instance was running on. Then we’d need a way to make that work for the other developers’ instances on the dev. server, as well.

Proxying a single port to another port with Nginx is easy, but that second requirement is a little more complicated. We did get a little lucky with this bit, however. We are using [DevCamps.org “camps”](http://www.devcamps.org/) for this project. DevCamps’ naming convention for a given development instance (AKA a “camp”) number uses a two digit camp number as the hostname and as part of the port number. For example, camp 42 would run on 42.camp.example.com:9042. (I bet you can already see where I’m going with this.)

I tweaked the Nginx config for the port 80 instance to use a regex to capture the hostname (“42” in this case) from the server_name portion of the HTTP request. It then appends that to the full hostname/IP address and the first two digits of that camp’s port number. That made the proxy work for everyone’s camp. Finally, I updated the config to work with any URI under the /dwolla directory.

We now have the following tidbit in our Nginx config:

```nohighlight
server {
    # [SNIP unrelated config stuff]

    server_name ~^(?<portname>\d\d)\.camp\.;

    location /dwolla {
        proxy_pass        http://169.29.89.157:90${portname}$uri;
        proxy_set_header  X-Real-IP  $remote_addr;
    }
}
```

As root, I ran `service nginx reload` to pick up the new config changes. Now Nginx automagically proxies connections to specific ports based on the server’s hostname.
