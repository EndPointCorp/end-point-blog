---
author: Bianca Rodrigues
title: Enhancing the labelsontime.com Spree application
github_issue_number: 1029
tags:
- ecommerce
- ruby
- rails
- spree
date: 2014-09-09
---

[Labels on Time](http://www.labelsontime.com) is an online retailer that delivers top-quality thermal roll and direct thermal labels—​and all on time, of course. They came to us last year to upgrade their Spree site, resolve bugs, and develop cutting-edge features, utilizing our expertise with the ecommerce platform. Spree Commerce is an open-source ecommerce solution built on Ruby on Rails, and manages all aspects of the fulfillment process, from checkout to shipping to discounts, and much more.

### UPGRADING THE SPREE PLATFORM

There were quite a few challenges associated with the upgrade, since Labels on Time was still running on Spree’s version 2.0, which was not yet stable. To keep some stability, we initially worked off a fork of Spree, and selectively brought in changes from 2.0 when we were sure they were stable and reliable enough.

### USING SPREE GEMS

To date, some of the Spree gems we have used on the site include:

[Active Shipping](https://github.com/spree-contrib/spree_active_shipping): This is a Spree plugin that can interface with USPS, UPS and FedEx. Label on Time’s active_shipping gem interacts with the UPS API, which is a big task to tackle since it requires a lot of configuration, especially every time Spree is updated.

Another important gem we use for Labels on Time is [Volume Pricing](https://github.com/spree/spree_volume_pricing). Volume Pricing is an extension to Spree that uses predefined ranges of quantities to determine the price for a particular product variant. When we first added this gem on the labelsontime.com checkout page, we kept finding that if a user increased the number of items in their cart sufficiently to activate the volume pricing and receive a discount per item, the standard Spree view did not show the new (discounted) price that was currently in effect (although it was correctly calculating the totals). To resolve this, our developer [Matt Galvin](/blog/authors/matt-galvin) created some custom JavaScript and Ruby code. Thanks to Matt’s ingenuity, the application can now return every price for every possible size and sort it accordingly.

### WHAT WE’RE WORKING ON NEXT

Matt recently upgraded the application to 2.0.10, which was needed for security reasons. You can read more about the security fix [here](https://spreecommerce.org/pages/blog/security-update-spree-2).

We are also working on implementing a neat SEO gem called [Canonical Rails](https://github.com/jumph4x/canonical-rails), which helps search engines understand that any duplicate content URLs it can access all refer to the canonical URL.

Next up, we’re going to implement inventory management, where, according to a customer’s location, we can suggest the available inventory in the closest warehouse to that location.
