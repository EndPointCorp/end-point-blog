---
author: Steph Skardal
title: 'Piggybak: The Roadmap'
github_issue_number: 702
tags:
- ecommerce
- piggybak
- ruby
- rails
date: 2012-10-08
---

Over the last couple of weeks, a few of us at End Point have had some discussion about the future direction of [Piggybak](https://github.com/piggybak/piggybak). Piggybak is an open source mountable ecommerce framework written in Ruby on Rails supported and developed by End Point. It introduces core ecommerce functionality into a Rails application, but is intended to allow the mounted Rails application to maintain control over some architecture elements.

### Pros of Piggybak

Until now, the advantage of Piggybak is that it's a fairly lightweight approach. It leverages the power of [RailsAdmin](https://github.com/sferik/rails_admin) rather than creating it's own admin. It allows the mounted Rails application to make decisions on what types of items are sellable and how these items are found (i.e. product finding methods, SSL configuration). Piggybak also has streamlined integration of [ActiveMerchant](http://activemerchant.org/), which immediately provides support of over 40 popular payment gateways. Piggybak has a cookie-based cart and an AJAX-driven one-page checkout.

### Cons of Piggybak Approach

Because Piggybak has a lightweight approach, the major disadvantage is that it cannot compete with existing ecommerce frameworks as an out of the box solution with a full ecommerce feature set. When compared with more feature-rich ecommerce platforms like [Spree](http://spreecommerce.com/) and [Magento](http://www.magentocommerce.com/) these other ecommerce platforms may have more features out of the box. This is a disadvantage because the abstraction, code cleanliness and maintainability provided by Piggybak is not necessarily as strong of a selling point to the feature list to a potential website owner.

### The Roadmap

In looking towards the future of Piggybak, we've decided to build out some features of Piggybak, but will try to maintain a balance between having a good feature set while still maintaining the lightweightedness of Piggybak. Some of our goals in the future include:

- [Realtime Shipping with USPS, UPS, and Fedex support](https://github.com/piggybak/piggybak_realtime_shipping) [as extension]
- Improvement of Piggybak installation process [core]
- Advanced Product Optioning Support [as extension]
- Line Item Rearchitecture to support future work on Gift Certificates, Discounts [core]
- Gift Certificate, Discount Support [core]
- Advanced Taxonomy [as extension]
- Reviews & Ratings [as extension]

Follow the Piggybak GitHub user [here](https://github.com/piggybak), check out the website and demo [here](https://github.com/piggybak/piggybak) and keep an eye out for future blog posts on the progress of Piggybak.
