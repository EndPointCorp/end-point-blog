---
author: Steph Skardal
title: 'Piggybak Update: Line Item Rearchitecture'
github_issue_number: 708
tags:
- ecommerce
- piggybak
- ruby
- rails
date: 2012-10-17
---

Over the last couple of weeks, I’ve been involved in doing significant rearchitecture of [Piggybak](https://github.com/piggybak/piggybak)’s line items data model. Piggybak is an open-source mountable Ruby on Rails ecommerce solution created and maintained by End Point. A few months ago after observing a few complications with Piggybak’s order model and it’s interaction with various nested elements (product line items, shipments, payments, adjustments) and calculations, and after reviewing and discussing these complications with a couple of my expert coworkers, we decided to go in the direction of a uniform line item data model based on our success with this model for other ecommerce clients over the years (whoa, that was a long sentence!). Here, I’ll discuss some of the motiivations and an overview of the technical aspects of this rearchitecture.

### Motivation

The biggest drivers of this change were a) to enable more simplified order total calculations based on uniform line items representing products, shipments, payments, etc. and b) to enable easier extensibility or hookability into the order architecture without requiring invasive overrides. For example, the code before for order totals may looked something like this:

```
order.subtotal = sum of items + sum of adjustments + sum of credits + sum of shipments
order.total_due = sum of items + sum of adjustments + sum of payments + sum of credits + sum of shipments
```

And after the order calculation, a more simplified version of order total calculation looks like this:

```
self.subtotal = sum of line item prices that aren't payments
self.total_due = sum of all line items
```

A related motivation that helped drive this change was to develop several credit-based features for Piggybak such as gift certificates, coupons and bundle discounts to grow the feature set of Piggybak. Rather than requiring complex overrides to incorporate these custom credits to orders, a consistent line item interface supports integration of additional custom line item types.

### Data Model Changes

Prior to the rearchitecture, the data model looked like this:

<img border="0" src="/blog/2012/10/piggybak-update-line-item-rearchitecture/image-0.png"/>

Piggybak data model prior to line item rearchitecture.

Some important notes on this are:

- Line items, payments, shipments and adjustments belong to the order. An order can have many of these elements.
- During order processing, all of these elements had to be processed independently without uniform consistency. An order balance due represented the sum of various charge related elements (items, shipments, tax) minus any payments or adjustments.
- In the case of adjustments, this was a bit tricky because an adjustment could be in the form of a negative or positive amount. This introduced complications in the order calculation process.
- Line items represented products only.

With the rearchitecture, the data model now looks like this:

<img border="0" src="/blog/2012/10/piggybak-update-line-item-rearchitecture/image-1.png"/>

Piggybak data model after line item rearchitecture.

Important notes on this are:

- In the core Piggybak data model, line item types represent sellable (product), payment, shipment, adjustment, and tax entries.
- Line items can still be related to other elements, such as payment and shipment, but the line item has uniform information such as price and description.
- Line item types are controlled by a Piggybak configuration variable, which allows for Piggybak extensions and the main Rails application to incorporate additional custom line item types.
- Because various calculation methods are applied on each line item type (e.g. payments are charged against credit card, shipping is recalculated with a shipping calculator) the line item order model is amenable to custom preprocessing and processing per line item type. This takes advantage Ruby’s respond_to? method to determine if specific preprocessing or postprocessing methods exist.
- The new architecture also takes advantage of metaprogramming by defining methods dynamically against the line item types. For example, order instance methods "shipping_charge" and "tax_charge" are dynamically created which return the sum of line item prices where the line item type is shipping or tax, respectively.

### Coupon Support in Piggybak

Much of the line item rearchitecture work was done in tandem with development of a Piggybak coupon extension, so I’m excited to announce that with this change, we now have another Piggybak extension [piggybak_coupons](https://github.com/piggybak/piggybak_coupons) available for use with Piggybak. The piggybak_coupon extensions includes support for defining discount type (percent, dollar, or free shipping), discount amoount (for percent and dollar), minimum cart total, expiration date, allowed number of uses. A coupon may be applied on the checkout page via an AJAX lookup. The piggybak_coupons extension is similar to piggybak in that it must be installed as a gem into the application. It includes it's own migration, model, controller, view, and decorator files.

### What's Next?

Introducing this new architecture gives us the abiliity to incorporate new and custom line item processing functionality. Popular line item types that correspond to popular ecommerce features include:

- refunds
- gift certificates
- coupons
- bundle discounts

Less common, but still possible with this new architecture might include:

- custom discounts (e.g. buy one get one free)
- payment via purchase order
- payment via check
- donations

The future for the Piggybak team includes further development of extensions to support some of the common line item type features.

Naturally, there may be a few follow-up incremental improvements since this was a significant change. All of this work is included in the Piggybak gem release version 0.6.2. Read more about Piggybak and check out the demo [here](https://github.com/piggybak/piggybak).
