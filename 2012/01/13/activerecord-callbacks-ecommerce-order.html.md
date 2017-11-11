---
author: Steph Skardal
gh_issue_number: 541
tags: ecommerce, open-source, piggybak, rails
title: ActiveRecord Callbacks for Order Processing in Ecommerce Applications
---



As I recently blogged about, I introduced a new [Ruby on Rails Ecommerce Engine](http://piggybak.org). The gem relies on [RailsAdmin](https://github.com/sferik/rails_admin), a Ruby on Rails engine that provides a nice interface for managing data. Because the RailsAdmin gem drives order creation on the backend in the context of a standard but configurable CRUD interface, and because I didn't want to hack at the RailsAdmin controllers, much of the order processing logic leverages ActiveRecord callbacks for processing. In this blog article, I'll cover the process that happens when an order is saved.

### Order Data Model

The first thing to note is the data model and the use of nested attributes. Here's how the order model relates to its associated models:

```ruby
class Order &lt; ActiveRecord::Base
  has_many :line_items, :inverse_of =&gt; :order
  has_many :payments, :inverse_of =&gt; :order
  has_many :shipments, :inverse_of =&gt; :order
  has_many :credits, :inverse_of =&gt; :order

  belongs_to :billing_address, :class_name =&gt; "Piggybak::Address"
  belongs_to :shipping_address, :class_name =&gt; "Piggybak::Address"
  belongs_to :user
  
  accepts_nested_attributes_for :billing_address, :allow_destroy =&gt; true
  accepts_nested_attributes_for :shipping_address, :allow_destroy =&gt; true
  accepts_nested_attributes_for :shipments, :allow_destroy =&gt; true
  accepts_nested_attributes_for :line_items, :allow_destroy =&gt; true
  accepts_nested_attributes_for :payments
end
```

An order has many line items, payments, shipments and credits. It belongs to [one] billing and [one] shipping address. It can accept nested attributes for the billing address, shipping address, multiple shipments, line items, and payments. It cannot destroy payments (they can only be marked as refunded). In terms of using ActiveRecord callbacks for an order save, this means that all the nested attributes will also be validated during the save. Validation fails if any nested model data is not valid.

### Step #1: user enters data, and clicks submit

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/01/13/activerecord-callbacks-ecommerce-order/image-0-big.jpeg" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2012/01/13/activerecord-callbacks-ecommerce-order/image-0.jpeg" width="750"/></a></div>

### Step #2: before_validation

Using a before_validation ActiveRecord callback, a few things happen on the order:

- Some order defaults are set
- The order total is reset
- The order total due is reset

### Step #3: validation

This happens without a callback. This method will execute validation on both order attributes (email, phone) and nested element attributes (address fields, shipment information, payment information, line_item information).

Payments have a special validation step here. A custom validation method on the payment attributes is performed to confirm validity of the credit card:

```ruby
validates_each :payment_method_id do |record, attr, value|
  if record.new_record?
    credit_card = ActiveMerchant::Billing::CreditCard.new(record.credit_card)
    
    if !credit_card.valid?
      credit_card.errors.each do |key, value|
        if value.any? &amp;&amp; !["first_name", "last_name", "type"].include?(key)
          record.errors.add key, value
        end
      end
    end
  end
end
```

This bit of code uses ActiveMerchant's functionality to avoid reproducing business logic for credit card validation. The errors are added on the payment attributes (e.g. card_number, verification_code, expiration date) and presented to the user.

### Step #4: after_validation

Next, the after_validation callback is used to update totals. It does a few things here:

- Calculates shipping costs for new shipments only.
- Calculates tax charge on the order.
- Subtracts credits on the order, if they exist.
- Calculates total_due, to be used by payment

While these calculations could be performed before_validation, after_validation is a bit more performance-friendly since tax and shipping calculations could in theory be expensive (e.g. shipping calculations could require calling an external API for real-time shipping lookup). These calculations are saved until after the order is confirmed to be valid.

### Step #5: before_save part 1

Next, a before_save callback handles payment (credit card) processing. This must happen after validation has passed, and it can not happen after the order has saved because the user must be notified if it fails. If any before_save method returns false, the entire transaction fails. So in this case, after all validation has passed, and before the order saves, the payment must process successfully.

Examples of failures here include:

- Credit card transaction denied for a number of reasons
- Payment gateway down
- Payment gateway API information incorrect

### Step #6: before_save part 2

After the payment processes, another before_save method is called to update the status of the order based on the totals paid. I initially tried placing this in an after_save method, but you tend to experience infinite loops if you try to save inside and after_save callback :)

### Step #7: Save

Finally, if everything's gone through, the order is saved.

### Summary

As I mentioned above, the RailsAdmin controllers were not extended or overridden to handle backroom order processing. All of the order processing is represented in the Order model in these active record callbacks. This also allows for the frontend order processing controller to be fairly lightweight, which is a standard practice for writing clean MVC code.

Check out the full list of ActiveRecord callbacks [here](http://guides.rubyonrails.org/active_record_validations_callbacks.html#available-callbacks). And check out the Order model for Piggybak [here](https://github.com/stephskardal/piggybak/blob/master/app/models/piggybak/order.rb).


