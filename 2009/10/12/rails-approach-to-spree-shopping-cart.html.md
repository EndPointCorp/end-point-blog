---
author: Steph Skardal
gh_issue_number: 208
tags: ecommerce, open-source, rails, spree
title: Rails Approach for Spree Shopping Cart Customization
---

Recently, I was assigned a project to develop [Survival International's](http://shop.survivalinternational.org/) ecommerce component using Spree. [Survival International](http://www.survivalinternational.org/) is a non-profit organization that supports tribal groups worldwide in education, advocacy and campaigns. Spree is an open source Ruby on Rails ecommerce platform that was sponsored by End Point from its creation in early 2008 until May 2009, and that we continue to support. End Point also offers a [hosting solution for Spree (SpreeCamps)](http://www.spreecamps.com/), that was used for this project.

Spree contains ecommerce essentials and is intended to be extended by developers. The project required customization including significant cart customization such as adding a buy 4 get 1 free promo discount, adding free giftwrap to the order if the order total exceeded a specific preset amount, adding a 10% discount, and adding a donation to the order. Some code snippets and examples of the cart customization in rails are shown below.

An important design decision that came up was how to store the four potential cart customizations (buy 4 get 1 free promo, free giftwrap, 10% discount, and donation). The first two items (4 get 1 free and free gift wrap) are dependent on the cart contents, while the latter two items (10% discount and donation) are dependent on user input. Early on in the project, I tried using session variables to track the 10% discount application and donation amount, and I applied an after_filter to calculate the buy 4 get 1 free promo and free giftwrap for every order edit, update, or creation. However, this proved somewhat cumbersome and required that most Rails views be edited (frontend and backend) to show the correct cart contents. After discussing the requirements with a coworker, we came up with the idea of using a single product with four variants to track each of the customization components.

I created a migration file to introduce the following variants similar to the code shown below. A single product by the name of 'Special Product' contained four variants with SKUs to denote which customization component they belonged to ('supporter', 'donation', 'giftwrap', or '5cards').

```ruby
p = Product.create(:name =&gt; 'Special Product', :description =&gt; "Discounts, Donations, Promotions", :master_price =&gt; 1.00)
v = Variant.create(:product =&gt; p, :price =&gt; 1.00, :sku =&gt; 'supporter') # 10% discount
v = Variant.create(:product =&gt; p, :price =&gt; 1.00, :sku =&gt; 'donation')  # donation
v = Variant.create(:product =&gt; p, :price =&gt; 1.00, :sku =&gt; 'giftwrap')  # free giftwrap
v = Variant.create(:product =&gt; p, :price =&gt; 1.00, :sku =&gt; '5cards')    # buy 4 get 1 free discount
```

Next, I added accessor elements to retrieve the variants shown below. Each of these accessor methods would be used throughout the code and so this would be the only location requiring an update if the variant SKU was modified.

```ruby
module VariantExtend
  ...
  def get_supporter_variant
    Variant.find_by_sku('supporter')
  end
  def get_donation_variant
    Variant.find_by_sku('donation')
  end
  def get_giftwrap_variant
    Variant.find_by_sku('giftwrap')
  end
  def get_cards_promo_variant
   Variant.find_by_sku('5cards')
  end
  ...
end
```

The design to use variants makes the display of cart contents on the backend and frontend much easier, in addition to calculating cart totals. In Spree, the line item price is not necessarily equal to the variant price or product master price, so the prices stored in the product and variant objects introduced above are meaningless to individual orders. An after_filter was added to the Spree orders controller to add, remove, or recalculate the price for each special product variant. The order of the after_filters was important. The cards (buy 4 get 1 free) discount was added first, followed by a subtotal check for adding free giftwrap, followed by adding the supporter discount which reduces the total price by 10%, and finally a donation would be added on top of the order total:

```ruby
OrdersController.class_eval do
  after_filter [:set_cards_discount, :set_free_giftwrap, :set_supporter_discount, :set_donation], :only =&gt; [:create, :edit, :update]
end
```

Each after filter contained specific business logic. The cards discount logic adds or removes the variant from the cart and adjusts the line item price:

```ruby
def set_cards_discount
  v = Variant.new.get_cards_promo_variant  # get variant
  # calculate buy 4 get 1 free discount (cards_discount)
  # remove variant if order contains variant and cards_discount is 0
  # add variant if order does not contain variant and cards_discount is not 0
  # adjust price of discount line item to cards_discount
  # save order
end
```

The free giftwrap logic adds or removes the variant from the cart and sets the price equal to 0:

```ruby
def set_free_giftwrap
  v = Variant.new.get_giftwrap_variant  # get variant
  # remove variant if cart contains variant and order subtotal &lt; 40
  # add variant if cart does not contain variant and order subtotal &gt;= 40
  # adjust price of giftwrap line item to 0.00
  # save order
end
```

The supporter discount logic adds or removes the discount variant depending on user input. Then, the line item price is adjusted to give a 10% discount if the cart contains the discount variant:

```ruby
def set_supporter_discount
  v = Variant.new.get_supporter_variant  # get variant
  # remove variant if cart contains variant and user input to receive discount is 'No'
  # add variant if cart does not contain variant and user input to receive discount is 'Yes'
  # adjust price of discount line item to equal 10% of the subtotal (minus existing donation)
  # save order
end
```

Finally, the donation logic adds or removes the donation variant depending on user input:

```ruby
def set_donation
  v = Variant.new.get_donation_variant  # get variant
  # remove variant if cart contains variant and user donation is 0
  # add variant if cart does not contain variant and user donation is not 0
  # adjust price of donation line item
  # save order
end
```

This logic results in a simple process for all four variants to be adjusted for every recalculation or creation of the cart. Also, the code examples above used existing Spree methods where applicable (add_variant) and created a few new methods that were used throughout the examples above (Order.remove_variant(variant), Order.adjust_price(variant, price)). A few changes were made to the frontend cart view.

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/StOpfpZx4bI/AAAAAAAACPo/7bxY192QOz8/s1600-h/survival1.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5391839540047634866" src="/blog/2009/10/12/rails-approach-to-spree-shopping-cart/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 307px;"/></a>

To render the desired view, line items belonging to the "Special Product" were not displayed in the default order line display. The buy 4 get 1 free promo and free giftwrap were added below the default line order items. Donations and discounts were shown below the line items in order of how they are applied to the order. The backend views were not modified and as a result the site administrators would see all special variants in an order:

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/StOpf3YE6vI/AAAAAAAACPw/IMjVC7LWGbI/s1600-h/survival2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5391839543798590194" src="/blog/2009/10/12/rails-approach-to-spree-shopping-cart/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 245px;"/></a>

An additional method was created to define the total number of line items in the order, shown at the top right of every page except for the cart and checkout page.

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/StOpgbiGEQI/AAAAAAAACP4/F_ebUth-jFM/s1600-h/survival3.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5391839553504284930" src="/blog/2009/10/12/rails-approach-to-spree-shopping-cart/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 85px;"/></a>

```ruby
module OrderExtend
  ...
  def mod_num_items
    item_count = line_items.inject(0) { |kount, line_item| kount + line_item.quantity } +
      (contains?(Variant.new.get_supporter_variant) ? -1 : 0) +
      (contains?(Variant.new.get_donation_variant) ? -1 : 0) +
      (contains?(Variant.new.get_giftwrap_variant) ? -1 : 0) +
      (contains?(Variant.new.get_cards_promo_variant) ? -1 : 0)
    item_count.to_s + (item_count != 1 ? ' items' : ' item')
  end
  ...
end
```

The solution developed for this project was simple and extended the Spree core ecommerce code elegantly. The complex business logic required was easily integrated in the variant accessor methods and after_filters to re add, remove, and recalculate the price of the custom variants where necessary. The project required additional customizations, such as view modifications, navigation modifications, and complex product optioning, which may be discussed in future blog posts :).
