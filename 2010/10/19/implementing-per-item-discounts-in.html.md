---
author: Sonny Cook
gh_issue_number: 370
tags: ecommerce, ruby, rails, spree
title: Implementing Per Item Discounts in Spree
---



## Discounts in Spree

For a good overview of discounts in Spree, the documentation is a good place to start.  The section on [Adjustments](http://spreecommerce.com/documentation/coupons_and_discounts.html) is particularly apropos.

In general, the way to implement a discount in Spree is to subclass the Credit class and attach or allow for attaching of one or more Calculators to your new discount class.  The Adjustment class file has some good information on how this is supposed to work, and the CouponCredit class can be used as a template of how to do such an implementation.

## What we Needed

For my purposes, I needed to apply discounts on a per Item basis and not to the entire order.

The issue with using adjustments as-is is that they are applied to the entire order and not to particular line items, so creating per line item discounts using this mechanism is not obviously straight forward. The good news it that there is nothing actually keeping us from using adjustments in this manner.  We just need to modify a few assumptions.

## Implementation Details

This is going to be a high-level description of what I did with (hopefully) enough hints about what are probably the important parts to point someone who wants to do something similar in the same direction.

Analogous to the Coupon class in Spree, I create a Discount class. It holds the meta-data information about the discount.  Specifically, the product that the discount applies to and the business logic for determining under what circumstances to apply the discount and how much to apply.

There is also a DiscountCredit class which subclasses the Credit class.  In this class I re-define two methods:

- **applicable?** returns true when the discount applies to the line_item

- **calculate_adjustment** calculates the amount of the discount based on the business rules.

I also add a couple of convenience methods:

- **line_item** returns self.adjustment_source

- **discount** returns self.line_item.variant.product.discount

The trick (as an astute reader might infer from the convenience methods) is to set the line_item which the discount is getting applied to to the adjustment_source attribute in the discount object.

The adjustment generally expects that you will be setting this to something like an instance of the Discount class, but as long as we ensure that LineItems implement any interface constraints required by Adjustments, we should be okay.

To that end, I monkey patch the LineItem class in my extension to add a method called add_discount.  This method creates a new instance of a DiscountCredit object and passes in iteslf as the adjustment_source. I then add this credit object to the adjustments on the order.

I also add a method to iterate through all of the discounts to look for one that might already be applied to this line_item instance.  I use this method in the add_discount method to ensure that I don't add more than one credit per line item.

To bring this together, I monkey patch the Order class to add a method that iterates through all of the line items in the order and calls add_discount on each one.  I add a after_save callback which calls this method to ensure that discounts are applied to all line items
each time the order is updated.

That takes care of the mechanics of applying the discounts.  From this point several things will be taken care of by Spree.  Any discounts that are not applicable will get removed.  The cart totals will get added up properly and discounts will be applied as adjustments.

## Other things you might want to do

You may not want Spree to only display applied discounts at checkout as a (potentially) long list of credits tacked on to the end of the order. 

For example, I found it useful to create some helpers to peek into the order adjustments and pull out the discount for a particular line item when displaying the cart.  I also wanted to consolidate all of the discounts as a total amount under discount, rather than display them independently, so, I modified the views that handled displaying the credits.

In my implementation, I found it more straight-forward to forgo the use of calculators when implementing the business logic.  But, they would work just fine as part of the Discount class and the DiscountCredit#calculate_adjustment method can call the calculator#calculate method to determine the amount to discount.

## Problems

This approach works because Spree automatically consolidates products/variants into the same line_item in the cart.  In my approach, I assigned discounts at the product level, but applied them at the variant level.  This worked for me because I didn't have any variants in my data set.

A general solution would probably assign discounts at the product level (it's too annoying to track them on a per-variant basis) and further track enough information to ensure that a discount was properly applied to any valid line_items that contained variants of that product.

## Conclusion

All in all, I found that most of the heavy lifting was already done by the Adjustments code.  All it really took was looking at the assumptions behind how the credits were working from a slightly different angle to see how I could modify things to allow per line item discounts to be implemented.


