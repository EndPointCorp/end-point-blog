---
author: Brian Dillon
gh_issue_number: 635
tags: ecommerce, piggybak, rails
title: Why Piggybak exists
---

<a href="/blog/2012/06/13/why-piggybak-exists/image-0-big.png" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="320" src="/blog/2012/06/13/why-piggybak-exists/image-0.png" width="205"/></a>

There are some clients debating between using Spree, an e-commerce platform, and a homegrown Rails solution for an e-commerce application.

E-commerce platforms are monolithic -- they try to solve a lot of different problems at once. Also, many of these e-commerce platforms frequently make premature decisions before getting active users on it. One way of making the features of a platform match up better to a user's requirements is to get a minimal viable product out quick and grow features incrementally.

Piggybak was created by first trying to identify the most stable and consistent features of a shopping cart. Here are the various pieces of a cart to consider.

- Shipping
- Tax
- CMS Features
- Product Search
- Cart / Checkout
- Product Features
- Product Taxonomy
- Discount Sales
- Rights and Roles

What doesn't vary? **Cart &amp; Checkout.**

Shipping, tax, product catalog design, sales promotions, and rights and roles all vary across different e-commerce sites. The only strict commonality is the cart and the checkout.

Piggybak is just the cart and checkout.

You mount Piggybak as a gem into any Rails app, and can assign any object as a purchasable product using a the tag "acts_as_variant" and you're good to go. To learn more, and to see it in action 'checkout' [Piggybak.org](http://www.piggybak.org/).
