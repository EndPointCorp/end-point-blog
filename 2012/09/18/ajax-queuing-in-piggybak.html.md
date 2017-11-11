---
author: Steph Skardal
gh_issue_number: 693
tags: ajax, ecommerce, jquery, piggybak, rails
title: AJAX Queuing in Piggybak
---



AJAX is inherently asynchronous; for the most part, this works fine in web development, but sometimes it can cause problem if you have multiple related AJAX calls that are asynchronous to eachother, such as the use case described in this article.

In [Piggybak](http://www.piggybak.org/), a Ruby on Rails open source shopping cart module developed and maintained by End Point, the one page checkout uses AJAX to generate shipping options. Whenever state and zip options change, the shipping address information is sent via AJAX and valid shipping methods are returned and rendered in a select dropdown.

<img border="0" src="/blog/2012/09/18/ajax-queuing-in-piggybak/image-0.png" width="750"/>

Event listeners on the state and zip code inputs trigger to generate shipping options via AJAX.

While working on development for a client using Piggybak, I came across a scenario where AJAX asynchronous-ity was problematic. Here's how the problematic behavior looked on a timeline, picking up as the user enters their shipping address:

- 0 seconds: User changes state, triggers AJAX shipping lookup with state value, but no zip code entered (Let's refer to this as AJAX REQUEST 1).
- 1 second: User changes zip code, triggers AJAX shipping lookup with state and zip value present (Let's refer to this as AJAX REQUEST 2).
- 2 seconds: AJAX REQUEST 2 returns valid shipping options.
- 3 seconds: AJAX REQUEST 1 returns invalid shipping options, because no zip code provided in this data set, and overwrites shipping options returned by AJAX REQUEST 2.

The result is that the user has finished entering a valid shipping address, but sees that no valid shipping options can be chosen:<img border="0" src="/blog/2012/09/18/ajax-queuing-in-piggybak/image-1.png" width="750"/>

To address this issue, I researched AJAX queuing, with the requirement that AJAX requests should be performed synchronously and existing AJAX requests could be aborted if needed. After experimenting with a few different plugins, I found the most success with the [jQuery-ajaxq](http://code.google.com/p/jquery-ajaxq/) plugin. It's simple to use:

- To append a new AJAX call on to a queue, you call $.ajaxq(queue_name, options), where options includes the standard AJAX arguments.
- To cancel or abort AJAX calls currently running in a queue, you call $.ajaxq(queue_name).

The event listener on state and zip changes now looks like the code shown below, in simplified form. The piggybak.update_shipping_options cancels AJAX requests on the shipping_options queue and then adds a new request to the queue which will execute immediately. This does not affect other asynchronous AJAX requests on the page.

```javascript
var piggybak = {
    update_shipping_options: function() {
        $.ajaxq("shipping_options");
        $.ajaxq("shipping_options", {
            url: ...,
            cached: false,
            data: ...,
            dataType: "JSON",
            beforeSend: function() {
                 ...
            },
            success: function(data) {
                ...
            }
        });
    }
}
```

Here's how this looks on a timeline:

- 0 seconds: User changes state, triggers AJAX shipping lookup with state value, but no zip code entered (Let's refer to this as AJAX REQUEST 1).
- 1 second: User changes zip code, triggers AJAX shipping lookup with state and zip value present (Let's refer to this as AJAX REQUEST 2). This signals to abort all current AJAX requeusts on the shipping_options queue.
- 2 seconds: AJAX REQUEST 2 returns valid shipping options.

This was an interesting technical problem to solve, but the needs were not surprising. The [jQuery-ajaxq plugin](http://code.google.com/p/jquery-ajaxq/) offers a simple, elegant solution for handling AJAX queing in jQuery.


