---
author: Steph Skardal
gh_issue_number: 715
tags: ecommerce, piggybak, ruby, rails
title: Association Extensions in Rails for Piggybak
---

I recently had a problem with Rails named scopes while working on minor refactoring in [Piggybak](http://www.piggybak.org/), an open source Ruby on Rails ecommerce platform that End Point created and maintains. The problem was that I found that [named scopes](http://guides.rubyonrails.org/active_record_querying.html#scopes) were not returning uncommitted or new records. Named scopes allow you to specify ActiveRecord query conditions and can be combined with joins and includes to query associated data. For example, based on recent [line item rearchitecture](/blog/2012/10/17/piggybak-update-line-item-rearchitecture), I wanted order.line_items.sellables, order.line_items.taxes, order.line_items.shipments to return all line items where line_item_type was sellable, tax, or shipment, respectively. With named scopes, this might look like:

```ruby
class Piggybak::LineItem < ActiveRecord::Base
    scope :sellables, where(:line_item_type => "sellable")
    scope :taxes, where(:line_item_type => "tax")
    scope :shipments, where(:line_item_type => "payment")
    scope :payments, where(:line_item_type => "payment")
  end
```

However, while processing an order, any uncommited or new records would not be returned when using these named scopes. To work around this, I added the [Enumerable select](http://ruby-doc.org/core-1.9.3/Enumerable.html#method-i-select) method to iterate over the line items, e.g.:

```ruby
# Reviewing shipments in an order
order.line_items.select { |li| li.line_item_type == "shipment" }.all? { |s| s.shipment.status == "shipped" }

# Get number of new payments
order.line_items.select { |li| li.new_record? && li.line_item_type == "payment" }.size
```

### Association Extensions

I felt that the above workaround was crufty and not very readable and sent out a request to my coworkers in hopes that there was a solution for improving the readability and clarity of the code. [Kamil](/team/kamil_ciemniewski) confirmed that named scopes do not return uncommitted records, and Tim Case offered an alternative solution by suggesting [association extensions](http://guides.rubyonrails.org/association_basics.html#association-extensions). An association extension allows you to add new finders, creators or methods that are only used as part of the association. After some investigation, I settled on the following code to extend the line_items association:

```ruby
class Piggybak::Order < ActiveRecord::Base
  has_many :line_items, do
    def sellables
      proxy_association.proxy.select { |li| li.ilne_item_type == "sellable" }
    end
    def taxes
      proxy_association.proxy.select { |li| li.ilne_item_type == "tax" }
    end
    def shipments
      proxy_association.proxy.select { |li| li.ilne_item_type == "shipment" }
    end
    def payments
      proxy_association.proxy.select { |li| li.ilne_item_type == "payment" }
    end
  end
end
```

The above code allows us to call order.line_items.sellables, order.line_items.taxes, order.line_items.shipments, and order.line_items.payments, which will return all new and existing line item records. These custom finder methods are used during order preprocessing which occurs during the ActiveRecord before_save callback before an order is finalized.

### Dynamic Creation

Of course, the Piggybak code takes this a step further because additional custom line item types can be added to the code via Piggybak extensions (e.g. coupons, gift certificates, adjustments). To address this, association extensions are created dynamically in the Piggybak engine instantiation:

```ruby
Piggybak::Order.class_eval do
  has_many :line_items, do
    Piggybak.config.line_item_types.each do |k, v|
      # k is sellable, tax, shipment, payment, etc.
      define_method "#{k.to_s.pluralize}" do
        proxy_association.proxy.select { |li| li.line_item_type == "#{k}" }
      end
    end
  end
end
```

### Conclusion

The disadvantage to association extensions versus named scopes are that association extensions are not chainable, which means you cannot add methods to the association extension. For example, a named scope may allow you to query order.line_items.sellables.price_greater_than_50 to return committed line items with a price greater than 50, but this functionality would not be possible with association extensions. This is not a limitation in the current code base, but it may become a limitation in the future.
