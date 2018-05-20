---
author: Brian Buchalter
gh_issue_number: 668
tags: hosting, rails
title: Changing Passenger Nginx Timeouts
---



It may frighten you to know that there are applications which take longer than Passenger’s default timeout of 10 minutes. Well, it’s true. And yes, those application owners know they have bigger fish to fry. But when a customer needs that report run *today* being able to lengthen a timeout is a welcomed stopgap.

### Tracing the timeout

There are many different layers at which a timeout can occur, although these may not be immediately obvious to your users. Typically they receive a 504 and an ugly “Gateway Time-out” message from Nginx. Review the Nginx error logs both at the reverse proxy and application server, you might see a message like this:

```
upstream timed out (110: Connection timed out) while reading response header from upstream
```

If you’re seeing this message on the reverse proxy, the solution is fairly straight forward. Update the [proxy_read_timeout](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_read_timeout) setting in your nginx.conf and restart. However, it’s more likely you’ve already tried that and found it ineffective. If you expand your reading of the Nginx error you might notice another clue.

```
upstream timed out (110: Connection timed out) while reading response header from upstream, 
upstream: "passenger://unix:/tmp/passenger.3940/master/helper_server.sock:"
```

This is the kind of error message you’d see on the Nginx application server when a Passenger process takes longer than the default timeout of 10 minutes. If you’re seeing this message, it’d be wise to review the Rails logs to get a sense for how long this process actually takes to complete so you can make a sane adjustment to the timeout. Additionally, it’s good to see what task is actually taking so long so you can offload the job into the background eventually.

### Changing nginx-passenger module’s timeout

If you’re unable to address the slow Rails process problem and must extend the length of the time out, you’ll need to modify the Passenger gem’s Nginx configuration. Start by locating the Passenger gem’s Nginx config with locate nginx/Configuration.c and edit the following lines:

```
ngx_conf_merge_msec_value(conf->upstream.read_timeout,
                              prev->upstream.read_timeout, 60000);
```
Replace the 60000 value with your desired timeout in milliseconds. Then run sudo passenger-install-nginx-module to recompile nginx and restart.

### Improving Error Pages

Another lesson worth addressing here is that Nginx error pages are ugly and unhelpful. Even if you have a Rails plugin like [exception_notification](https://github.com/rails/exception_notification/) installed, these kind of Nginx errors will be missed, unless you use the [error_page](https://nginx.org/en/docs/http/ngx_http_core_module.html#error_page) directive. In other applications I’ve setup explicit routes to test exception_notification properly sends an email by creating a controller action that simple raises an error. Using Nginx’s error_page directive, you can call an exception controller action and pass useful information along to yourself as well as present the user with a consistent error experience.


