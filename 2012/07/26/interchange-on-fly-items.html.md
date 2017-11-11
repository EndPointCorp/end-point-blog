---
author: Jeff Boes
gh_issue_number: 674
tags: ecommerce, interchange, json
title: Interchange "on-the-fly" items
---



Interchange has a handy feature (which, in my almost-seven-years of involvement, I'd not seen or suspected) allowing you to create an item "on-the-fly", without requiring any updates to your products table. Here's a recipe for making this work.

First, you need to tell Interchange that you're going to make use of this feature (in catalog.cfg).

```nohighlight
OnFly onfly
```

Simple, no? The "OnFly" directive names a subroutine that is called to pre-process the custom item before it's added to the cart. The default "onfly" routine can be found in the system tag "onfly": code/SystemTag/onfly.coretag in the standard Interchange installation. (If you need more that what it provides, that's beyond the scope of my post, so good luck, bon voyage, and please write back to let us know what you learned!)

Then, you need to submit some special form parameters to set up the cart:

- mv_order_item: the item number identifying this line
- mv_order_fly: a structured string with | (vertical bar) delimiters. Each sub-field specifies something about the custom item, thus: ~~~nohighlight
description=My custom item|price=12.34
```

Now, in my particular case, I was encapsulating an XML feed of products from another site (a parts supplier) so that the client (a retail seller) could offer replacement parts, but not have to incorporate thousands of additional lines in the "products" table. So after drilling down to the appropriate model and showing the available parts, each item got the following bit of JavaScript (AJAX) code associated with its add-to-cart button:

```perl
var $row = $(this).parents('tr');
    $.ajax({
        url: '/cgi-bin/mycat/process',
        data: {
            mv_todo: 'refresh',
            mv_order_quantity: 1,
            mv_order_item: $row.find('td.item_number').html(),
            mv_order_fly: 'description='
                + $row.find('td.description').html().replace('|','')
                + '|'
                + 'price='
                + $row.find('td.price').html().replace('$','').replace(',','')
        },
        method: 'POST',
        success: function(data, status) {
            $('#msg_div').html('Added to cart.')
        }
    });
```

And that's all it took. With Interchange, you don't even need a special "landing page" for your AJAX submission; Interchange handles all the cart-updating out of sight.

I still need to add some post-processing to handle errors, and update the current page so I can see the new cart line count, but the basics are done.


