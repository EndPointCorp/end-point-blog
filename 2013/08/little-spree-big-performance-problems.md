---
author: Marina Lohova
title: Little Spree Big Performance Problems
github_issue_number: 842
tags:
- heroku
- performance
- ruby
- rails
- spree
date: 2013-08-05
---

Recently I worked on an online food store serving an area with very little infrastructure. As a result, the orders tended to be really big with lots of products.

The website worked in the following environment:

- Ruby 1.9.2
- Spree 0.60
- Heroku, Bamboo stack
- PostgreSQL v9.2.4

### H12 timeout errors 

The performance problems started when we migrated Bamboo to Cedar on Heroku and replaced Thin webserver with Unicorn. We started getting a lot of [Heroku Request timeout errors - H12](https://devcenter.heroku.com/articles/request-timeout):

<a href="/blog/2013/08/little-spree-big-performance-problems/image-0.png" imageanchor="1"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-0.png"/></a>

The problems happened mostly when logging in to admin dashboard or during the checkout for the certain orders. H12 errors occur when a HTTP request takes longer than 30 seconds to complete. For example, if a Rails app takes 35 seconds to render the page, the HTTP router returns a 503 after 30 seconds and abandons the incomplete Rails request for good. The Rails request will keep working and logging the normal errorless execution. After completion, the request will indefinitely hang in the application dyno.

We started debugging H12: we set Unicorn timeout to 20 seconds to prevent the runaway requests and installed the rack-timeout gem with the timeout of 10 seconds to raise an error on a slow request. It all came down to a trivial database timeout!

<a href="/blog/2013/08/little-spree-big-performance-problems/image-1.png" imageanchor="1"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-1.png"/></a>

The application source has not changed during the transition from Bamboo to Cedar, but apparently Cedar/Unicorn is much more sensitive to the troubled code. Below is the list of performance bottlenecks and solutions in Spree. Some of them exist in version 0.60 only, but a lot of them are still present in Spree 1.x, which means that your application may have them too.  

### Issue #1: Real-time reports

Let’s take a closer look at the earlier database timeout code. It came from Admin Dashboard and admin/overview_controller.rb.

<a href="/blog/2013/08/little-spree-big-performance-problems/image-2.png" imageanchor="1"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-2.png"/></a>

The “Best Selling variants" report was being calculated real-time right in the web process:

```ruby
def best_selling_variants
  li = LineItem.includes(:order).
      where("orders.state = 'complete'").
      sum(:quantity, :group => :variant_id, :limit => 5)
  ...
end
```

Record counts in the database are large enough to crash the application on Heroku with the database timeout:

```ruby
irb(main):001:0> LineItem.count
=> 162279
irb(main):002:0> Order.count
=> 13027
irb(main):003:0> Variant.count
=> 14418
```
Other reports on the Dashboard experience the same problem. They would cause the timeout in turns when logging into Admin: 

- top_grossing_variants
- best_selling_taxons
- last_five_orders
- biggest_spenders

### Solution

Fortunately, in Spree 1.x the internal reporting system has been replaced with [Jirafe](https://web.archive.org/web/20130807090154/http://jirafe.com:80/):

<a href="/blog/2013/08/little-spree-big-performance-problems/image-3.png" imageanchor="1"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-3.png"/></a>

If switching to Spree 1.x is not an option, another way is to move the calculation into a background job, using, for example, delayed_job gem and Heroku Scheduler Addon:

```ruby
task :statistics => :environment do
  Delayed::Job.enqueue StatisticsJob.new
end
```

### Issue #2: Large numbers <div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-4.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-4.jpeg"/></a></div>

It is an established fact that humans eat a lot! Think about an order of a thousand Heineken 6-pack cans... 

Or even something like this:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-5.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-5.png"/></a></div>

or this:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-6.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-6.jpeg"/></a></div>

Spree, both 0.60 and 1.x, proved to have a huge problem if an order has a lot of line items and/or a large quantity of single line items. The potentially dangerous code can be found all over the place. Consider the following example:

```ruby
class InventoryUnit < ActiveRecord::Base
  def self.destroy_units(order, variant, quantity)
    variant_units = order.inventory_units.group_by(&:variant_id)[variant.id].sort_by(&:state)
    quantity.ceil.times do
      inventory_unit = variant_units.shift
      inventory_unit.destroy
    end
  end
```

Now imagine what will happen with the order from the first screenshot. We have 15100 inventory units for that one. They will be meticulously destroyed from the inventory one by one in a loop after the checkout. This method was born to crash the application!

### Solution

A simple mindful refactoring was enough to solve the problem for me. There is no need to call “destroy” in the loop for every single inventory unit because we can use the efficient “destroy_all” method. I’m sure this can be optimized further, but it was enough to get rid of the timeout:

```ruby
def self.destroy_units(order, variant, quantity)
  variant_units = order.inventory_units.
    group_by(&:variant_id)[variant.id].
    sort_by(&:state)
  variant_units = variant_units.shift(quantity.ceil)
InventoryUnit.
    where(:order_id => order.id,:variant_id => variant.id).
    order('state asc').limit(quantity.ceil).
    destroy_all
   end
```

### Issue #3: Real-time emails <div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-7-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-7.jpeg"/></a></div>

All emails in Spree are sent in real-time.

```ruby
class Order < ActiveRecord::Base
  def finalize!
    ...
    OrderMailer.confirm_email(self).deliver
    ...
  end
end
```

Why is it bad? Let’s look at the following example from my application:

```ruby
def confirm_email(order)
  attachments["invoice.pdf"] = {
    'Content-type' => 'application/pdf', 
    :content => OrderInvoice.new.to_pdf(order)}

  mail(:subject  => 'Order #' + order.number, 
       :from   =>    Spree::Config[:order_from],  
       :to => order.email)
end
```

In my application “confirm_email” was overridden and generated the pdf invoice. The invoice listed all the products in the order and had about 200 lines in it. Again, it lead to the H12 timeout error.

### Solution

All emails should be sent in the background rather than in the web request. First, because network operations can take a long time, and second, because generating an email can also be slow. For example, sending in the background can be accomplished using [delayed_job gem](https://github.com/collectiveidea/delayed_job):

```ruby
OrderMailer.delay.confirm_email(self)
```

### Issue #4: Lazy-loading <div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-7-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-7.jpeg"/></a></div>

Ecommerce objects are usually complicated with a lot of associations. This is totally fine as long as you eager-load the associations that will be used most with the loaded object later on. In most cases, Spree does not preload associations for its orders. For example, in spree/base_controller.rb:

```ruby
@order = Order.find_by_number! params[:order_id]
```

As the result, here is what I see in server console while loading the order display page on the frontend:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-9-big.png" imageanchor="1" style="clear: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-9.png"/></a></div>

...And five more screens like this! The associations of the order - line items, variants and products - generate an additional chain of queries to the database during lazy-loading.

### Solution: Eager-loading

If I modify the line from the controller like this...

```ruby
@order = Order.where(:number => params[:order_id])
         .includes(:line_items => {:product => :taxons, :variant => [:product, :option_values]})
         .includes(:adjustments).first
```

...SQL queries will shrink down to this:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-10-big.png" imageanchor="1" style="clear: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-10.png"/></a></div>

Eager-loading did the trick. Of course, not everything needs to be loaded eagerly, and the solution varies from case to case. It worked like charm in my case.

### Issue #5: Dangerous code all over the place <div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-7-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-7.jpeg"/></a></div>

There a lot of places in the Spree source code that are not optimized for performance. We don’t need to look far for an example, because there is another killer method right near the "destroy_units" one we inspected earlier!

```ruby
class InventoryUnit < ActiveRecord::Base
  def self.create_units(order, variant, sold, back_order)
    shipment = order.shipments.detect {|shipment| !shipment.shipped? }
    sold.ceil.times { 
order.inventory_units.create(:variant => variant, :state => “sold”, :shipment => shipment)
}
   back_order.ceil.times {     
order.inventory_units.create(:variant => variant, :state => “backordered”, :shipment => shipment)
}
  end
end
```

And then:

```ruby
order.line_items.each do |line_item|
  back_order = determine_backorder(order, variant, quantity)
  sold = quantity - back_order
  create_units(order, line_item.variant,  sold, back_order)
end
```

I received a timeout either in the “sold” or the “backorder” loop, but there wasn’t a time when I didn’t receive a timeout!

### Solution

```ruby
def self.create_units(order, variant, sold, back_order)
  shipment = order.shipments.detect {|shipment| !shipment.shipped? }
  values = sold.ceil.times.to_a.map { "(#{order.id},#{variant.id},'sold',#{shipment.id})" } +
    back_order.ceil.times.to_a.map { "(#{order.id},#{variant.id},'backordered',#{shipment.id})" }
  values.in_groups_of(500, false) do |group|
    InventoryUnit.connection.execute("INSERT INTO inventory_units(order_id, variant_id, state, shipment_id) VALUES #{group.join(',')}")
  end
end
```

Another example: every line item has the after_create and after_save callbacks. The callback invokes the  Order.update! method. Order.update! method calls update_totals method...twice throughout the method.

```ruby
def update_totals
    self.payment_total = payments.completed.map(&:amount).sum
    self.item_total = line_items.map(&:amount).sum
    self.adjustment_total = adjustments.map(&:amount).sum
    self.total = item_total + adjustment_total
  end
```

Now imagine the order from the second screenshot with a lot of line items. During the checkout “update_totals” will be called each time the line item is saved. Typically, this line would produce a timeout, because the  “line_items” association was, of course, not preloaded:

```ruby
line_items.map(&:amount).sum
```

I couldn’t list every circumstance like that, because it would require a lot of context to explain the catch, but I can still say many times: “No long-running tasks in the web request!”.

### No long-running tasks in the web request!

Be it Spree, Heroku or any other context, environment or platform, please, never do the following in the web process:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/08/little-spree-big-performance-problems/image-12-big.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/08/little-spree-big-performance-problems/image-12.png"/></a></div>

- (!!!) Heavy database usage (slow or numerous queries, N+1 queries)
- Sending an email
- Accessing a remote API (posting to Twitter, querying Flickr, etc.)
- Rendering an image or PDF
- Heavy computation (computing a fibonacci sequence, etc.)

### Say “No” to all these things to ensure a much happier life for your application!
