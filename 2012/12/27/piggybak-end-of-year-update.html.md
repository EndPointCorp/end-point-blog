---
author: Steph Skardal
gh_issue_number: 743
tags: ecommerce, piggybak, rails
title: 'Piggybak: End of Year Update'
---

Over the last few months, my coworkers and I have shared several updates on [Piggybak](https://github.com/piggybak/piggybak) progress ([October 2012 Piggybak Roadmap ](/blog/2012/10/08/piggybak-roadmap), [November 2012 Piggybak Roadmap Status Update](/blog/2012/11/06/piggybak-roadmap-status-update)).  Piggybak is an open source, mountable as a Rails Engine, Ruby on Rails ecommerce platform developed and maintained by End Point. Here's a brief background on Piggybak followed by an end of year update with some recent Piggybak news.

### A Brief Background

Over the many years that End Point has been around, we've amassed a large amount of experience in working with various ecommerce frameworks, open source and proprietary. A large portion of End Point's recent development work (we also offer database, hosting, and Liquid Galaxy support) has been with [Interchange](http://www.icdevgroup.org/), a Perl-based open source ecommerce framework, and [Spree](http://spreecommerce.com/), a Ruby on Rails based open sourced ecommerce framework. Things came together for Piggybak earlier this year when a new client project prompted the need for a more flexible and customizable Ruby on Rails ecommerce solution. Piggybak also leveraged earlier work that I did with light-weight Sinatra-based cart functionality.

Jump ahead a few months, and now Piggybak is a strong base for an ecommerce framework with several extensions to provide advanced ecommerce features. Some of the features built and already reported on were real-time shipping lookup (USPS, UPS, and FedEx support), improvement of the Piggybak installation process, gift certificate, discount, and bundle discount support.

### Recent Progress

Since the last general update, we've tackled a number of additional changes:

- SSL support: The Piggybak core now supports SSL for the checkout, which leverages the lightweight Rails gem [rack-ssl-enforcer](https://github.com/tobmatth/rack-ssl-enforcer). A Piggybak config variable specifying that checkout should be secure must be set to true in the main Rails application, which triggers that a specific set of pages should be secure. This configuration is not ideal to use if the main Rails application requires more complex management of secure pages.
- Minor bug fixes & cleanup: The updates below include minor refactoring and/or bug fixes to the Piggybak core:

        - Moved order confirmation outside of controller, to minimize failure of order processing if the email confirmation fails.
        - RailsAdmin DRY cleanup
        - Abilities (CanCan) cleanup to require less manual coding, which simplifies the code required in the CanCan model.
        - Breakdown of orders/submit.html.erb, which allows for easier override of checkout page elements.
        - Tax + coupons bug fixes.
        - RailsAdmin upgrade to updated recent versions.

- Heroku tutorial: Piggybak support in Piggybak was described [in this blog article](/blog/2012/11/12/piggybak-on-heroku).
- Advanced taxonomy or product organization: An extension for advanced product organization (e.g. categories, subcategories) was released, but we still plan to add more documentation regarding its functionality and use.
- Bundle discount support: Another extension for bundle discount support was released. Bundle discount offers the ability to give customer discounts when a bundle or set of products has been added to the cart. Barrett shared his experiences in creating this extension [in this article](/blog/2012/12/13/piggybak-extensions-basic-how-to-guide).
- **Fancy** jQuery tour: I wrote about [a new Piggybak demo tour](/blog/2012/12/06/interactive-piggybak-demo-tour) that I created for checking out the features of Piggybak.
- Advanced product optioning: Another extension for advanced product option support (e.g. size, color) was released a couple of months ago, but [this recent article](/blog/2012/12/18/advanced-product-options-variants-in) provides more documentation on its functionality and use.

### What's Next?

At this point, one of our big goals is to grow the Piggybak portfolio and see many of the extensions in action. We'd also like to improve the Piggybak core and extension documentation to help get folks up and running on Piggybak quickly. In addition to documentation and portfolio growth, additional features we may focus on are:

- Product reviews & ratings support
- Saved address/address book support
- Wishlist, saved cart functionality

A few large features that are on our wishlist that may need client sponsorship for build-out are:

- Multiple shipping addresses per order: This allows for users to select multiple shipping addresses per order. I implemented this functionality for [Paper Source](http://www.paper-source.com/) just over a year ago. This would likely be developed in the form of an extension that requires several non-trivial Piggybak core overrides.
- Subscription support: The [Piggybak Google Group](https://groups.google.com/forum/?fromgroups#!forum/piggybak) has expressed interest in subscription support, which also is not trivial.
- Point-based credit support
- Multi-store architecture: End Point is very familiar with multi-store architecture, which allows multiple stores to be support via one code base. I shared some of the options [in this blog article](/blog/2012/02/29/multi-store-architecture-ecommerce).
- One deal at a time support: This is another popular feature that End Point has been involved with for [Backcountry.com](http://www.backcountry.com/) sites [Steep and Cheap](http://www.steepandcheap.com/), [WhiskeyMilitia.com](http://www.whiskeymilitia.com/), and [Chainlove.com](http://www.chainlove.com/).

### Get Involved

If you are interested in helping develop Piggybak, don't hesitate to jump on the [Piggybak google group](https://groups.google.com/forum/?fromgroups#!forum/piggybak) or tackle one of the [Piggybak GitHub issues](https://github.com/piggybak/piggybak/issues).
