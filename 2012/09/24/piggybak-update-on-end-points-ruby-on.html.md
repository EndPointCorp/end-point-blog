---
author: Steph Skardal
gh_issue_number: 696
tags: ecommerce, piggybak, rails
title: 'Piggybak: An Update on End Point''s Ruby on Rails Ecommerce Engine'
---



With the recent release of one of our client sites running on [Piggybak](http://www.piggybak.org/), Piggybak saw quite a few iterations, both for bug fixes and new feature development. Here are a few updates to Piggybak since its announcement [earlier this year](http://blog.endpoint.com/2012/01/piggybak-mountable-ecommerce-ruby-on.html).

### Admin: Continues to Leverage RailsAdmin

Piggybak continues to leverage [RailsAdmin](https://github.com/sferik/rails_admin). RailsAdmin is a customizable admin interface that automagically hooks into your application models. In the case of the recent project completion, the admin was customized to add new features and customize the appearance, which can be done in RailsAdmin with ease.

As much as I enjoy working with RailsAdmin, I think it would be great in the future to expand the admin support to include other popular Rails admin tools such as [ActiveAdmin](http://activeadmin.info/), which has also gained popularity in the Rails space.

### Refund Adjustments

When Piggybak first came out, there was little in the way to allow orders to be monetarily adjusted in the admin after an order was placed. One requirement that came out of client-driven development was the need for recording refund adjustments. A new model for "Adjustments" is now included in Piggybak. An arbitrary adjustment can be entered in the admin, which is tied to a specific user, an amount, and a recorded note. This functionality allows for site administrators to record adjustments given against orders.

<img border="0" height="188" src="/blog/2012/09/24/piggybak-update-on-end-points-ruby-on/image-0.png" width="400"/>

At the moment, the creation of an adjustment is **not** tied to a payment gateway to refund against the original transaction, because ActiveMerchant payment gateways have varied refund support.

### AJAX Queueing for Shipping Requests on One-Page Checkout

Discussed [in this article](http://blog.endpoint.com/2012/09/ajax-queuing-in-piggybak.html), AJAX queuing was added for shipping method generation on the one-page AJAX-driven checkout.

### Order Notes

Another feature that originated from client needs was the need to record order changes over time. Now included in Piggybak are "Order Notes". Order notes are automatically created when attributes or nested attributes are changed on the order:

<img border="0" height="161" src="/blog/2012/09/24/piggybak-update-on-end-points-ruby-on/image-1.png" width="400"/>

And arbitrary order notes can be added to record data not represented in attribute changes:

<img border="0" height="176" src="/blog/2012/09/24/piggybak-update-on-end-points-ruby-on/image-2.png" width="400"/>

All order notes have a created_at attribute and belong to a user, which is tied to the administrator who made the change to the order.

### Masked CC Number Storage

While we don't want to store unencrypted credit card numbers in the database per [PCI compliance](https://www.pcisecuritystandards.org/), Piggybak now includes storage of the masked credit card number to the payments table. This allows the site administrators to examine the credit card type and reference a particular card if needed. This was accomplished using the following method added to the String class:

```ruby
class String
  def mask_cc_number
    masked = ''

    if self.gsub(/\D+/i, '').match(/^(\d\d)(.+)(\d\d\d\d)$/)
      masked = $1 + $2.length.times.inject('') { |s, i| "#{s}*" } + $3
    end

    masked
  end
end
```

### Upgrade to Rails 3.2.8

The [Piggybak demo](http://www.piggybak.org/demo_details.html) has recently been updated to Rails 3.2.8. No changes were required, as this was considered a minor Rails update.

### Conclusion

It's exciting to see the progress of Piggybak over the last several months, as well as to see Piggybak launch for a site with complex custom needs. I believe it accomplishes the vision I had in mind for it ([summarized in this presentation](http://blog.endpoint.com/2012/09/company-presentation-ecommerce-as-engine.html)), without requiring fighting against assumptions that traditional monolithic ecommerce platforms make. Granted, Piggybak still makes specific ecommerce assumptions, but they are limited to cart, checkout, and order functionality rather than systematic application-level behavior.

The future likely holds incremental improvements to Piggybak, but there are no plans to change Engine-like structure or principles of Piggybak.


