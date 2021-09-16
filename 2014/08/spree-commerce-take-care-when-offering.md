---
author: Matt Galvin
title: Spree Commerce, Take Care When Offering Free Shipping Promotion
github_issue_number: 1024
tags:
- ruby
- spree
date: 2014-08-20
---



Hello again all. I was working on another [Spree Commerce Site](https://guides.spreecommerce.org/), a Ruby on Rails based e-commerce platform. As many of you know, Spree Commerce comes with [Promotions](https://guides.spreecommerce.org/developer/promotions.html). According to Spree Commerce documentation, Spree Commerce Promotions are:

“... used to provide discounts to orders, as well as to add potential additional items at no extra cost. Promotions are one of the most complex areas within Spree, as there are a large number of moving parts to consider.”

The promotions feature can be used to offer discounts like free shipping, buy one get one free etc.. The client on this particular project had asked for the ability to provide a coupon for free shipping. Presumably this would be a quick and easy addition since these types of promotions are included in Spree.

The site in question makes use of [Spree’s Active Shipping Gem](https://github.com/spree/spree_active_shipping), and plugs in the [UPS Shipping API](https://www.ups.com/content/us/en/bussol/browse/online_tools_shipping.html) to return accurate and timely shipping prices with the UPS carrier.

The client offers a variety of shipping methods including Flat Rate Ground, Second Day Air, 3 Day Select, and Next Day Air. Often, Next Day Air shipping costs several times more than Ground. E.g.: If something costs $20 to ship Ground, it could easily cost around $130 to ship Next Day Air.

When creating a free shipping Promotion in Spree it’s important to understand that by default it will be applied to all shipping methods. In this case, the customer could place a small order, apply the coupon and receive free Next Day Air shipping! To take care of this you need to use [Promotion Rules](https://guides.spreecommerce.org/developer/promotions.html#rules). Spree comes with several built-in rules:

- First Order: The user’s order is their first.
- ItemTotal: The order’s total is greater than (or equal to) a given value.
- Product: An order contains a specific product.
- User: The order is by a specific user.
- UserLoggedIn: The user is logged in.

As you can see there is no built in Promotion Rule to limit the free shipping to certain shipping methods. But fear not, it’s possible to [create a custom rule](https://guides.spreecommerce.org/developer/promotions.html#registering-a-new-rule).

```ruby
module Spree
     class Promotion
       module Rules
         class RestrictFreeShipping < PromotionRule
           MATCH_POLICIES = %w(all)
 
           def eligible?(order, options={})
             e = false
             if order.shipment.shipping_method.admin_name == "UPS Flat Rate Ground"
               e = true
             else
               e = false
             end
            return e
           end
        end
      end
    end
  end
```

Note that you have to create a partial for the rule, as per the [documentation](http://guides.spreecommerce.com/developer/promotions.html#rules).

Then, in config/locales/en.yml I added a name and description for the rule.

```ruby
en:
     spree:
       promotion_rule_types:
         restrict_free_shipping:
           name: Restrict Free Shipping To Ground
           description: If somebody uses a free shipping coupon it should only apply to ground shipping
```

The last step was to restart the app and configure the promotion in the Spree Admin interface.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/08/spree-commerce-take-care-when-offering/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/08/spree-commerce-take-care-when-offering/image-0.png"/></a></div>

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/08/spree-commerce-take-care-when-offering/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/08/spree-commerce-take-care-when-offering/image-1.png"/></a></div>


