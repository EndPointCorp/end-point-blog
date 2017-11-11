---
author: Steph Skardal
gh_issue_number: 334
tags: ecommerce, rails, spree
title: 'Spree: Gift Certificates and Coupons'
---

In a recent Spree project, I've been working with Bill Bennett to add gift certificate functionality. According to the [Spree documentation](http://spreecommerce.com/documentation/coupons_and_discounts.html#gift-certificates), gift certificate functionality is trivial to implement using the existing coupon architecture. Here are some of the changes we went through as we tried to use the coupon architecture for gift certificate implementation - we found that it wasn't so simple after all.

<a href="/blog/2010/07/29/spree-gift-certificates-and-coupons/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5501245338028413938" src="/blog/2010/07/29/spree-gift-certificates-and-coupons/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 155px;"/></a>

Here is a very simplified visualization of the coupon and adjustment data model in Spree. Coupons use polymorphic calculators to compute the applicable discount.

First, Bill and I brainstormed to come up with an initial set of changes required for implementing gift certificates as coupons after we reviewed the data model shown above:

1. Add logic to create a coupon during checkout finalization, which was done with the following:
```ruby
# coupon object class method
def self.generate_coupon_code
  # some method to generate an unused random coupon code beginning in 'giftcert-'
end
```

```ruby
# inside order model during checkout finalization
line_items.select { |li| li.variant.product.is_gift_cert? }.each do |line_item|
  line_item.quantity.times do
    coupon = Coupon.create(:code =&gt; Coupon.generate_coupon_code,
                           :description =&gt; "Gift Certificate",
                           :usage_limit =&gt; 1,
                           :combine =&gt; false,
                           :calculator =&gt; Calculator::FlatRate.new)
    coupon.calculator.update_attribute(:preferred_amount, line_item.variant.price)
  end
end
```

1. Add logic to decrease a coupon amount during checkout finalization if used:
```ruby
# order model during checkout finalization
coupon_credits.select{ |cc| cc.adjustment_source.code.include?('giftcert-') }.each do |coupon_credit|
  coupon = coupon_credit.adjustment_source
  amount = coupon.calculator.preferred_amount - item_total
  coupon.calculator.update_attribute(:preferred_amount, amount &lt; 0 ? 0 : amount)
end
```

1. Add relationship between line item and coupon because we'd want to have a way to associate coupons with line items. The intention here was to limit a gift certificate line item to a quantity of 1 since the gift certificate line item might include personal information like an email in the future.
```ruby
LineItem.class_eval do
  has_one :line_item_coupon
  has_one :coupon, :through =&gt; :line_item_coupon
end
```

```ruby
class LineItemCoupon &lt; ActiveRecord::Base
  belongs_to :line_item
  belongs_to :coupon

  validates_presence_of :line_item_id
  validates_presence_of :coupon_id
end
```

1. Create the sample data for a gift certificate (coupon) - the implementation offers a master variant for a fixed cost of $25.00. In addition to the code below, Bill created sample data to assign a product property is_gift_cert to the product.
```ruby
# products.yml
gift_certificate:
  name:          Gift Certificate
  description:   Gift Certificate
  available_on:  &lt;%= Time.zone.now.to_s(:db) %&gt;
  permalink:     gift-certificate
  count_on_hand: 100000
```

```ruby
# variants.yml
gift_cert_variant:
  product:       gift_certificate
  sku:           giftcert
  price:         25.00
  is_master:     true
  count_on_hand: 10000
  cost_price:    25.00
  is_extension:  false
```

1. Finally, Bill edited the order mailer view to include gift certificate information

After the above changes were implemented, additional changes were required for our particular Spree application.

1. Adjust the shipping API so it doesn't include gift certificates in the shipping request, because gift certificates aren't shippable. Below is an excerpt of the XML builder code that generates the XML request made to the shipping API:
```diff
# shipping calculator
-order.line_items.each do |li|
+order.line_items.select { |li| !li.variant.product.is_gift_cert? }
   x.item {
     x.quantity(li.quantity)
     x.weight(li.variant.weight != 0.0 ? li.variant.weight : Spree::MyShipping::Config[:default_weight])
     x.length(li.variant.depth ? li.variant.depth : Spree::MyShipping::Config[:default_depth])
     x.width(li.variant.width ? li.variant.width : Spree::MyShipping::Config[:default_width])
     x.height(li.variant.height ? li.variant.height : Spree::MyShipping::Config[:default_height])
     x.description(li.variant.product.name)
   }
```

1. Create a new calculator for free shipping applicable to orders with gift certificate line items only, using the is_gift_cert product property:

```ruby
# registering the calculator inside Spree site_extension.rb (required for all calculators to be used in Spree)
[
  Calculator::GiftCertificateShipping,
].each{ |c_model|
  begin
    c_model.register if c_model.table_exists?
  rescue Exception =&gt; e
    $stderr.puts "Error registering calculator #{c_model}"
  end
}
```

```ruby
# shipping method and calculator creation in sample data
s = ShippingMethod.new(:zone_id =&gt; 16, :name =&gt; 'Gift Certificate Shipping')
s.save
c = Calculator.new
c.calculable = s
c.type = 'Calculator::GiftCertificateShipping'
c.save
```

```ruby
# calculator for free gift cert shipping
class Calculator::GiftCertificateShipping &lt; Calculator
  ...
  def available?(order)
    order.line_items.inject(0) { |sum, li| sum += li.quantity if !li.variant.product.is_gift_cert?; sum } == 0
  end

  def compute(line_items)
    0
  end
end
```

After Bill implemented these changes, I contemplated the following code more:

```ruby
coupon_credits.select{ |coupon_credit| coupon_credit.adjustment_source.code =~ /^giftcert-/}.each do |coupon_credit|
  coupon = coupon_credit.adjustment_source
  amount = coupon.calculator.preferred_amount - item_total
  coupon.calculator.update_attribute(:preferred_amount, amount &lt; 0 ? 0 : amount)
end
```

I wondered why the coupon amount being decremented by the item_total and not the order total. What about shipping and sales tax? I verified by looking at the the Spree Coupon class that a coupon's amount will only take into account the item total and not shipping or tax, which would present a problem since gift certificates traditionally apply to tax and shipping costs.

<a href="/blog/2010/07/29/spree-gift-certificates-and-coupons/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5499726539401259346" src="/blog/2010/07/29/spree-gift-certificates-and-coupons/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 289px; height: 291px;"/></a>

In the Spree core, coupons are never applied to shipping or tax costs.

I investigated the following change to separate coupon and gift certificate credit calculation:

```ruby
def site_calculate_coupon_credit
  return 0 if order.line_items.empty?
  amount = adjustment_source.calculator.compute(order.line_items).abs
  order_total = adjustment_source.code.include?('giftcert-') ? order.item_total + order.charges.total : order.item_total
  amount = order_total if amount &gt; order_total
  -1 * amount
end
```

After this change, I found that when arriving on the payment page where the gift certificate has covered the entire order including tax and shipping, the payment logic isn't set up handle orders with a total cost of 0. Additional customization on payment implementation, validation and checkout flow would be required to handle orders where gift certificates cover the entire cost. However, rather than implementing these additional customizations, our client was satisfied with the implementation where gift certs don't cover tax and shipping, so I did not pursue this further.

In the future, I'd recommend creating a new model for gift certificate and gift certificate credit management rather than combining the business logic with coupons, because:

1. The coupon implementation in Spree doesn't have a whole lot to it. It uses several custom Spree calculators, has a backend CRUD interface, and credits are applied to orders. Grabbing the coupon implementation and copying and modifying it for gift certificates shouldn't be daunting.
1. It will likely be more elegant to separate coupon logic from gift certificate logic. Coupons and gift certificates share a few business rules, but not all. Gift certificates traditionally apply to tax and shipping and multiple gift certificates can be used on one order (but this part can be configurable). Coupons may have more complex logic to apply to items and do not traditionally get applied to tax and shipping (however, in some cases a free shipping coupon may be needed that covers the cost of shipping only). Additionally, a big difference in business logic is that gift certificates should probably be treated as a payment, where checkout accepts gift certificates as a form of payment, and the backend provides reporting on the gift certificate driven payments. Rather than dirtying-up the the coupon logic with checks for gift certificates versus coupon behavior, it'll be more elegant to separate the logic into classes that address the individual business needs.

Besides "hindsight is 20/20", the takeaway for me here is that you have to understand business rules and requirements for coupon and gift certificate implementation in ecommerce, which can get tricky quickly. We were lucky because the client was satisfied with the resulting behavior of using the coupon architecture for gift certificates. Hopefully, the takeaway for someone not familiar with Spree is that gift certificate implementation might require things like functionality for creating gift certificates after checkout completion, decrementing the gift certificate after it's used, backend reporting to show gift certificates purchase and use and coding for the impact of gift certificate purchase on shipping.

Note that all of the changes described here apply to the latest stable version of Spree (0.11.0). After taking a look at the Spree edge code, I'll mention that there is a bit of an overhaul on coupons (to be called promotions). However, it looks many of the customizations described here would be needed for gift certificate implementation as the edge promotions still apply to item totals only and do not include any core modifications in accepting a credit as a payment.
