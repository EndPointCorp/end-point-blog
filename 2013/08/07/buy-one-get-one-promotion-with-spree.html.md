---
author: Brian Buchalter
gh_issue_number: 843
tags: ecommerce, ruby, rails, spree
title: Buy One Get One Promotion with Spree
---



Implementing a "Buy One, Get One Free" promotion in
Spree requires implementation of a custom promotion action and
appropriate use of existing promotion rules. This article implements
the promotion by automatically adding and removing immutable "get one" line items whose
price is zero and whose quantity always mirrors its paid
"buy one" counterpart. Although written and tested with Spree's 1-3-stable branch, the core logic of this tutorial will work with any version of Spree.

## Promotion Eligibility

Begin by creating a new promotion using a meaningful name. Set the
"event name" field to be "Order contents changed"
so the promotion's actions are updated as the order is updated. Save
this new promotion, so we can then configure Rules and Actions. In
the Rules section, select the "Product(s)" rule and click
Add. Now choose the products you'd like to be eligible for your
promotion. If you'd like to include broader sets such as entire
taxonomies (and have implemented the custom promotion rules to do
so), feel free to use them. When we implement the promotion
action, you'll be able to make things work.

You should now have a product rule that selects some subset of
products eligible for your promotion.

## Adding a Custom Promotion Action

We'll now add a custom promotion action that will do the work of
creating the free line items for each eligible paid line item. Again, this implementation is specifically for the 1-3-stable branch, but the public interface for promotion actions has (amazingly) remained stable, and is supported from 0-7-0-stable all the way through 2-0-stable.

First,
we begin by doing [the
basic wiring for creating a new promotion action](http://guides.spreecommerce.com/developer/promotions.html#registering-a-new-action). As the guide
instructs, create a new promotion class in a file.

```ruby
# app/models/spree/promotion/buy_one_get_one.rb
class BuyOneGetOne < Spree::PromotionAction
  def perform(options={})
    # TODO
  end
end
```

Then register this new class with Spree using an initializer.

```ruby
# config/initializers/spree.rb

Rails.application.config.spree.promotions.actions << BuyOneGetOne
```

Then update your locales to provide translations for the promotion
action's name and description.

```ruby
# config/locales/en.yml

en:
  spree:
    promotion_action_types:
      buy_one_get_one:
        name: Buy One Get One
        description: Adds free line items of matching quantity of eligible paid line items.
```

And although the guide doesn't instruct you to, it seems required
that you add an empty partial to be rendered in the Spree admin when
you select the rule.

```ruby
# app/views/spree/admin/promotions/actions/_buy_one_get_one.html.erb

# Empty File. Spree automatically renders the name and description you provide,
# but you could expand here if you'd like.
```

### Pre-flight check

Before moving any farther, it's best to make sure the new
promotion action has been wired up correctly. Restart your
development server so the initializer registers your new promotion
action and refresh your browser. You should now see a "Buy One
Get One" promotion action.

## Buy One Get One Logic

Now that we've got the promotion action wired, we're ready to
implement the logic needed to create the new line items. Begin by
collecting the order from the options.

```ruby
# app/models/spree/promotion/buy_one_get_one.rb
class BuyOneGetOne < Spree::PromotionAction
  def perform(options={})
    return unless order = options[:order]
  end
end
```

Next we need to determine which line items in the order are eligible
for a corresponding free line item. Because line items are for
variants of products, we must collect the variant ids from the
product rule we setup. If you've used something other the default
Spree "Product(s)" rule, just make sure you end up with
equivalent output.

```ruby
# app/models/spree/promotion/buy_one_get_one.rb
class BuyOneGetOne < Spree::PromotionAction
  def perform(options={})
    return unless order = options[:order]

    eligible_variant_ids = get_eligible_variant_ids_from_promo_rule
    return unless eligible_variant_ids.present?
  end

  def get_eligible_variant_ids_from_promo_rule
    product_rule = promotion.promotion_rules.detect do |rule|
      # If not using the Product rule, update this line
      rule.is_a? Spree::Promotion::Rules::Product
    end 
    return unless product_rule.present?

    eligible_products = product_rule.products
    return unless eligible_products.present?

    eligible_products.collect { |p| p.variant_ids }.flatten.uniq
  end
end
```

Now that we've got the eligible variant ids from the promotion's
rule, we'll identify the line items which have those variants.

```ruby
# app/models/spree/promotion/buy_one_get_one.rb
class BuyOneGetOne < Spree::PromotionAction
  def perform(options={})
    return unless order = options[:order]

    eligible_variant_ids = get_eligible_variant_ids_from_promo_rule
    return unless eligible_variant_ids.present?

    order.line_items.where(variant_id: eligible_variant_ids).each do |li|
      #TODO
    end
  end
  ....
end
```

We're now ready to process eligible line items. There are several
cases we'll need to implement to have a working promotion:

- When we find an eligible, paid
 line item: 
 

 

        - If an existing corresponding free
  line item exists, update quantity to match the paid line item. 
  

          - Else, create corresponding free
  line item with appropriate quantity. 
  

 

 - When we find a Buy One Get One
 promotion line item: 
 

 

        - If the corresponding paid line
  item still exists, do nothing. 
  

          - Else, destroy the free line item. 
  

 

These cases handle the creation, updating, and removal of
promotional line items. Let's translate these cases into a skeleton
of code which can then be implemented incrementally.

```ruby
# app/models/spree/promotion/buy_one_get_one.rb
class BuyOneGetOne < Spree::PromotionAction
  def perform(options={})
    return unless order = options[:order]

    eligible_variant_ids = get_eligible_variant_ids_from_promo_rule
    return unless eligible_variant_ids.present?

    order.line_items.where(variant_id: eligible_variant_ids).each do |li|
      if li.price != 0
        # It's an eligible variant and it's price is not zero, so we
        # found a "buy one" line item.

        matching_get_one_line_item = find_matching_get_one_line_item(li)

        # Create or update matching promo line item.
        if matching_get_one_line_item
          matching_get_one_line_item.update_attribute(:quantity, li.quantity)
        else
          create_matching_get_one_line_item(li)
        end 

      else
        # It's an eligible variant and it's price is zero, so we
        # found a "get one" line item.

        # Verify "buy one" line item still exists, else destroy
        # the "get one" line item
        li.destroy unless find_matching_buy_one_line_item(li)
    end
  end

  def find_matching_buy_one_line_item(li)
  end
  def create_matching_get_one_line_item(li)
  end
  def find_matching_get_one_line_item(li)
  end
  ....
end
```

This well named and commented code reads nicely and clearly covers
the create, update, and destroy cases we need to be concerned with.
Now let's implement the helper methods.

```ruby
  ....
  def find_matching_buy_one_line_item(get_one_line_item)
    get_one_line_item.order.line_items.detect do |li|
      li.variant_id == get_one_line_item.variant_id and li.price != 0
    end 
  end

  def create_matching_get_one_line_item(buy_one_line_item)
    # You may need to update this with other custom attributes you've added.
    new_line_item = buy_one_line_item.order.line_items.build
    new_line_item.variant = buy_one_line_item.variant
    new_line_item.currency = buy_one_line_item.currency
    new_line_item.price = 0
    new_line_item.quantity = buy_one_line_item.quantity
    new_line_item.save
  end

  def find_matching_get_one_line_item(buy_one_line_item)
    buy_one_line_item.order.line_items.detect do |li|
      li.variant_id == buy_one_line_item.variant_id and li.price != 0
    end 
  end
  ....
end
```

We've now completed most of the implementation for the promotion
action. Every time the order is updated, all line items are scanned
for eligibility and the appropriate create/update/destroy actions are
taken. This however, isn't the end of our implementation. Unlike
other items in our cart, we need to prevent users from changing the
quantity of "get one" line items or removing them from the
cart. We also need some way of indicating that these zero price line
items are complements of the Buy One Get One promotion.

## Locked Line Items with Additional Text

While the concept of locked or immutable line items might rightly
deserve its own, separate Spree plugin, we'll roll a quick one here
to complete the implementation of our promotion. We'll need to add a
few attributes to the spree_line_items database table, and tweak our
implementation of create_matching_get_one_line_item.

```ruby
# db/migration/add_immutable_and_additional_text_to_spree_line_items.rb
class AddImmutableAndAdditionalTextToSpreeLineItems < ActiveRecord::Migration
  def change
    add_column :spree_line_items, :immutable, :boolean
    add_column :spree_line_items, :additional_text, :string
  end
end

# app/models/spree/promotion/buy_one_get_one.rb
  def create_matching_get_one_line_item(buy_one_line_item)
    # You may need to update this with other custom attributes you've added.
    new_line_item = buy_one_line_item.order.line_items.build
    new_line_item.variant = buy_one_line_item.variant
    new_line_item.currency = buy_one_line_item.currency
    new_line_item.price = 0
    new_line_item.quantity = buy_one_line_item.quantity

    new_line_item.immutable = true
    new_line_item.additional_text = "Buy One Get One"

    new_line_item.save
  end
```

Now that we know which line items aren't meant to be edited by users,
we can update our UI to not render the options to remove immutable
line items or update their quantity. We can also display the
additional text in the line line item when it's available.

Missing from this implementation is a way to secure the immutable
line items from manipulation of the immutable line items POSTed
parameters. While this might be required in other cases using
immutable line items, because our promotion action sets the "get
one" line items quantity with every order update, we don't need
to worry about this issue in this case.

## Test Driving

At this point, you can begin manual testing of your
implementation, but of course automated testing is best. Ideally, we
would have TDDed this against a failing integration test, but the
testing infrastructural setup required to do this is beyond the scope
of the article. What's worth sharing though, is the syntax of the
assertions I've developed to inspect line items, so that you can
implement something similar for your specific needs. Here's a snippet
from an integration test to give you a sense of the DSL we've built
up.

```ruby
# spec/requests/buy_one_get_one_spec.rb

context "add eligible item to cart" do
  before do
    # setup cart
    visit_product_and_add_to_cart eligible_product
    visit "/cart"
  end   
      
  it "should add an identical, immutable, free item" do
    assert_line_item_count(2)
    assert_line_item_present(eligible_product.name, unit_price: undershirt_amount, unit_price: eligible_product.price, immutable: false)
    assert_line_item_present(eligible_product.name + " - (Buy One Get One)", unit_price: 0.00, immutable: true)
    assert_order_total(eligible_product.price)
  end
end
```

Of course you'd want to test all the cases we've implemented, but
what's worth focusing on is the ability to assert specific attributes
across many different line items. This is an extremely reusable tool
to have in your testing suite. Good luck implementing!


