---
author: Matt Galvin
gh_issue_number: 926
tags: ecommerce, rails, shipping, spree
title: Spree Active Shipping Gem “We are unable to calculate shipping rates for the selected items.” Error
---

I was recently working on a [Spree](http://spreecommerce.org/) site and setting up the [Spree Active Shipping Gem](https://github.com/spree/spree_active_shipping) along with the UPS API. For those not familiar, the Spree Active Shipping Gem interacts with various shipping APIs like UPS, USPS, and FedEx. Due to the nature of Spree—where it does so much for you, and the interaction between the Active Shipping Gem and a shipping API also being “auto-magic”, it is often difficult to debug. As I was recently undertaking the task of setting this up I found a few “gotchas” that I hope, through this blog post, may be able to save others a lot of time.

I have found that there wasn’t a lot of instruction for setting up the Active Shipping Gem and a shipping carrier API like the UPS Shipping API. Ostensibly, there isn’t much to it—the Active Shipping Gem handles much of the interaction between the shipping API of choice and Spree.

First, you’re going to go the [Spree Active Shipping Gem](https://github.com/spree/spree_active_shipping) GitHub repo and follow the instructions for installing the Active Shipping Gem. It is very straightforward, but do proceed in the order mentioned in the Spree Active Shipping Gem documentation as some steps depend on the successful completion of others.

Second, you’re going to go to the shipper of your choice, in this case UPS, and follow their directions for using their [API](http://www.ups.com/content/us/en/bussol/browse/cat/developer_kit.html). I do recommend actually reading, or at least skimming, the pages and pages of documentation. Why? Because there are some important agreements explaining how the API is to be used (basically legal requirements for the UPS logo).

The Active Shipping Gem makes a call to the API, the API returns a hash of various shipping methods and prices based on the parameters you’ve sent it (such as shipment origin and destination), and then it automatically displays in the UI as an adjustment. How great is that?!

Well, it would be great if it all worked out exactly as planned. However, if you are running Spree 2-0-stable you may find yourself battling an unusual circumstance. Namely, Spree 2-0-stable will create your core/app/views/spree/checkout/edit.html.erb as

```ruby
<% content_for :head do %>
     <%= javascript_include_tag '/states' %>
   <% end %>
```

This will provide the incorrect path. It is intended to hit the StatesController, so update it like so:

```ruby
<% content_for :head do %>
     <%= javascript_include_tag states_url %>
   <% end %>
```

Now, once this correction has been made you may find that you are still having an error, “We are unable to calculate shipping rates for the selected items.”

<a href="/blog/2014/02/12/spree-active-shipping-gem-we-are-unable/image-0.png" imageanchor="1"><img border="0" src="/blog/2014/02/12/spree-active-shipping-gem-we-are-unable/image-0.png"/></a>

At this point Chrome Dev Tools will not show any errors. When I had this error, a number of Google searches returned results of the kind "make sure you have set up your shipping zones correctly and added shipping methods to these zones". I verified this again and again in the console, as did many others who were equally perplexed by this message on [StackOverflow](http://stackoverflow.com/questions/18277367/spree-commerce-error-on-checkout-we-are-unable-to-ship-the-selected-items-to-y) as well as in Google Groups, like [here](https://groups.google.com/forum/#!msg/spree-user/aCJz5iNemfo/3v4uJ8hPBVsJ) and [here](https://groups.google.com/forum/#!topic/spree-user/aCJz5iNemfo). Some got this error when they added an item to the cart that had a count_on_hand of 0 and backorderable equal to false, like you can see here at [Spree GitHub issues](https://github.com/spree/spree/issues/3521). If a 0 count_on_hand is what is giving you this error, but you want a product to be backorderable, make sure to also check the “Propagate All Variants” in the Spree admin as seen below. This will loop through all of the product’s variants with a count_on_hand of 0, and allow them to be backorderable.

<a href="/blog/2014/02/12/spree-active-shipping-gem-we-are-unable/image-1-big.png" imageanchor="1"><img border="0" src="/blog/2014/02/12/spree-active-shipping-gem-we-are-unable/image-1.png"/></a>

After a long while of searching and wondering, is it the API? Is it the Active Shipping Gem? Is it a blacklisted zip code? I went through and changed one setting at a time in the Spree admin until finally arriving at the source of this error for me. Missing product weight. Because UPS needs the product weight in order to calculate shipping charges, make sure this is set.

The “We are unable to calculate shipping rates for the selected items” error message is misleading. If you encounter this error after correcting the javascript_include_tag, the cause is most likely a setting in the admin. Check for how insufficient inventory is handled, missing product weights, or incorrectly setup up or non-existent shipping zones & associated methods. I hope if this error message is what brought you here that this post has saved you some time.
