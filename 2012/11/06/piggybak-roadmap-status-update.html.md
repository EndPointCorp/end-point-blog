---
author: Steph Skardal
gh_issue_number: 718
tags: ecommerce, open-source, piggybak, ruby, rails
title: 'Piggybak: Roadmap Status Update'
---

About a month ago, I shared an outline of the current [Piggybak Roadmap](http://blog.endpoint.com/2012/10/piggybak-roadmap.html). Piggybak is an open-source Ruby on Rails ecommerce platform created and maintained by End Point. It is developed as a Rails Engine and is intended to be mounted on an existing Rails application. Over the last month, Tim and I have been busy at work building out features in Piggybak, and completing refactoring that opens the door for better extension and feature development. Here's a summary of the changes that we've finished up.

### Real-time Shipping Lookup

One of our Piggybak clients already had integrated USPS and UPS shipping, but we decided to extract this and combine it with FedEx, to offer [real-time shipping lookup shipping in Piggybak](https://github.com/piggybak/piggybak_realtime_shipping). This extension leverages [Shopify's open-source ActiveShipping](https://github.com/Shopify/active_shipping) Ruby gem. When you are ready to get your Piggybak store up and running, you can include this new extension and configure USPS, UPS, and FedEx real-time shipping lookup immediately.

### Installer process

Tim Case updated the installation process to be more streamlined. The previous installation process was a bit crufty and required changes to your Gemfile, routes, layouts, and precompiled assets. Tim described the installation work [in this article](http://blog.endpoint.com/2012/11/how-to-build-command-line-executable.html).

### Rename Variant to Sellable

A minor but notable change that happened in the last month was the change of "variant" to "sellable". Any model in a Rails application, now can be extended with the class method acts_as_sellable, which will allow that item to be managed as a sellable item and be a purchaseable item.

### Variants Extension

Tied directly to the variant to sellable change, we developed a new extension to provide [advanced variant support in Piggybak](https://github.com/piggybak/piggybak_variants). The advanced variant data model has similarities to [Spree](http://spreecommerce.com/)'s data model, one that we have observed as a successful feature of Spree. The basic principles are that you assign specific options to sellable items (e.g. size and color), and then you assign option values to those options (e.g. red and blue for size, large and small for color). Then, for each sellable item, you can define many variants each with a different combination of options, each with a unique sku, quantity on hand, cart description, and price. The user sees these options on the product detail page, and selects option values to add items to the cart.

<img border="0" src="/blog/2012/11/06/piggybak-roadmap-status-update/image-0.png" width="600"/>

Advanced production optioning support in Piggybak: In this screenshot, options for frame size and frame finish are provided.

Each variant has individual pricing, quantity on hand, and a description in the cart.

### Line Item Rearchitecture

I also spent a good amount of time rearchitecting line item associations to orders, where a line item now represents all monetary items in an order (sellable, payment, tax item, shipment, etc.). This results in a more simplified order total and balance due calculation, as well as allows for extensions to introduce custom line items that are included in order calculations without order processing code changes. This significant change is described [in this article](http://blog.endpoint.com/2012/10/piggybak-update-line-item-rearchitecture.html).

### Piggybak Coupons

The line item rearchitecture work was done in tandem with development of a [Piggybak coupon extension](https://github.com/piggybak/piggybak_coupons). The extension includes support for defining discount type (percent, dollar, or free shipping), discount amount (for percent and dollar), minimum cart total, expiration date, allowed number of uses.

<img border="0" src="/blog/2012/11/06/piggybak-roadmap-status-update/image-1.png" width="600"/>

Coupon support in Piggybak: Coupon application on the checkout happens via AJAX and

is displayed in the order totals calculations shown in the screenshot.

### Gift Certificate Support

Finally, one of the recent extensions completed was development of a [gift certificate extension](https://github.com/piggybak/piggybak_giftcerts). A gift certificate can be purchased at various increments and applied on the checkout page to an order via an AJAX call. Gift certificates may also be purchased and redeemed in the Piggybak admin.

<img border="0" src="/blog/2012/11/06/piggybak-roadmap-status-update/image-2.png" width="600"/>

Gift Certificate support in Piggybak: Gift certificate application on the checkout happens via AJAX and is displayed in the order totals calculations shown in the screenshot. In this case, the gift certificate covers the entire order.

### Minor Bug Fixes, Refactoring and Feature Development

Several bug fixes and minor refactoring was applied during development of these features, including but not limited to:

- attr_accessible updates to support Rails 3 mass assignment attributes
- Improved inventory management on the admin side
- Minor refactoring to introduce [Proxy Association extensions](http://blog.endpoint.com/2012/10/association-extensions-in-rails-for.html)
- Removal of [jeweler](https://github.com/technicalpickles/jeweler), and move to standard Rails engine architecture
- Added functionality to support copying a billing address to shipping address in admin.
- Added logic to enforce one payment method be added at a time via admin.
- JavaScript-based validation on the checkout.
- [Stripe payment gateway support](https://github.com/piggybak/piggybak_stripe) via an extension.

### What's Next?

If we take a look the roadmap list a month ago, we can cross several items off from the list:

- Realtime Shipping with USPS, UPS, and Fedex support
- Improvement of Piggybak installation process
- Advanced Product Optioning Support
- Line Item Rearchitecture to support future work on Gift Certificates, Discounts
- Gift Certificate, Discount Support
- Advanced Taxonomy
- Reviews &amp; Ratings

A few new things have recently been added to the list:

- Add SSL support in core
- Create Heroku deployment tutorial
- Saved cart, Wishlist support
- Saved address support

Our goal for the immediate future is to focus on development of the most common ecommerce features.

All of the features described in this article are active on the Piggybak demo. [Check it out now!](http://www.piggybak.org/demo_details.html)
