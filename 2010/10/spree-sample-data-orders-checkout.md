---
author: Steph Skardal
title: 'Spree Sample Data: Orders and Checkout'
github_issue_number: 363
tags:
- ecommerce
- rails
- spree
date: 2010-10-11
---



A couple of months ago, I wrote about [setting up Spree sample data in your Spree project with fixtures](/blog/2010/07/spree-sample-product-data) to encourage consistent feature development and efficient testing. I discussed how to create sample product data and provided examples of creating products, option types, variants, taxonomies, and adding product images. In this article, I’ll review the sample order structure more and give an example of data required for a sample order.

The first step for understanding how to set up Spree order sample data might require you to revisit a simplified data model to examine the elements that relate to a single order. See below for the interaction between the tables orders, checkouts, addresses, users, line items, variants, and products. Note that the data model shown here applies to Spree version 0.11 and there are significant changes with Spree 0.30.

<a href="/blog/2010/10/spree-sample-data-orders-checkout/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5526773457021042002" src="/blog/2010/10/spree-sample-data-orders-checkout/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 118px;"/></a>

Basic diagram for Spree order data model.

The data model shown above represents the data required to build a single sample order. An order must have a corresponding checkout and user. The checkout must have a billing and shipping address. To be valid, an order must also have line items that have variants and products. Here’s an example of a set of fixtures to create this bare minumum sample data:

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:ruby">
#orders.yml
order_1:
  id: 1
  user_id: 1
  number: "R00000001"
  state: new
  item_total: 20.00
  created_at: <%= Time.now %>
  completed_at: <%= Time.now %>
  total: 20.00
  adjustment_total: 0.00
</pre>
</td>
<td valign="top">
<pre class="brush:ruby">
#checkouts.yml
checkout_1:
  bill_address: address_1
  ship_address: address_1
  email: 'spree@example.com'
  order_id: 1
  ip_address: 127.0.0.1
  state: complete
  shipping_method: canada_post
</pre>
</td>
</tr>
<tr>
<td valign="top">
<pre class="brush:ruby">
#addresses.yml
address_1:
  firstname: Steph
  lastname: Powell
  address1: 12360 West Carolina Drive
  city: Lakewood
  state_id: 889445952
  zipcode: 80228
  country_id: 214
  phone: 000-000-0000
</pre>
</td>
<td valign="top">
<pre class="brush:ruby">
#line_items.yml
li_1:
  order_id: 1
  variant: test_variant
  quantity: 2
  price: 10.00
</pre>
</td>
</tr><tr>
<td valign="top">
<pre class="brush:ruby">
#variants.yml
test_variant:
  product: test_product
  price: 10.00
  cost_price: 5.00
  count_on_hand: 10
  is_master: true
  sku: 1-master
</pre>
</td>
<td valign="top">
<pre class="brush:ruby">
#products.yml
test_product:
  name: Test Product 1
  description: Lorem ipsum...
  available_on: <%= Time.zone.now.to_s(:db) %>
  count_on_hand: 10
  permalink: test-product
</pre>
</td>
</tr>
<tr>
<td valign="top">
<pre class="brush:ruby">
#users.rb
#copy Spree core to create a user with id=1
</pre>
</td>
<td>
</td>
</tr>
</tbody></table>

After adding fixtures for the minimal order data required, you might be interested in adding peripheral data to test custom work or test new feature development. This peripheral data might include:

- shipping methods: A checkout belongs to a shipping method, and has many shipping rates and shipments.
- shipments: An order has many shipments. Shipments are also tied to the shipping method.
- inventory units: An order has many inventory units, corresponding to each item in the order.
- payments: Orders and checkouts have many payments that must cover the cost of an order. Multiple payments can be assigned to each order.
- adjustments: Shipping charges and tax charges are tracked by adjustments, which belong to orders.
- return authorizations: Return authorizations belong to orders and track returns on orders, tied to inventory_units in the order that are returned.

In my experience, I’ve worked with a few Spree projects where we created fixtures for setting peripheral sample data to test custom shipping and inventory management. Again, note that the data models described in this article are in place in Spree <= 0.11.0. Spree 0.30 will introduce data model changes to be discussed at a later date.


