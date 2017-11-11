---
author: Brian Buchalter
gh_issue_number: 703
tags: rails, testing
title: Feature Isolation with Mike Farmer
---

My brilliant co-worker Mike Farmer gave a presentation today talking about a development strategy he calls "Feature Isolation." It involves developing new features on the fringe of your application, isolating it from the complexity of existing code. This allows greater focus on ensuring that your feature is well designed from an object-oriented perspective and that you don't build more than you need.

In order to truly isolate the feature, Mike put together some [cucumber tools](https://github.com/mikefarmer/cucumber_tools) to allow you to run cucumber without Rails and to create what he calls a "FastModel". The models are fast for two reasons. First, you don't need to load ActiveRecord to get functionality like [specifying field names](https://github.com/mikefarmer/cucumber_tools/blob/master/fast_model.rb#L20), [specifying relationships](https://github.com/mikefarmer/cucumber_tools/blob/master/fast_model.rb#L10), or [emulating saving records](https://github.com/mikefarmer/cucumber_tools/blob/master/fast_model.rb#L128). Second, it let's you to sketch out a design for your class while the cost of change is very very low.

### An Example: Product Variants

Here's an example of a tight little feature and step set for showing shoppers a comparison of product variants.

```
Feature: As a shopper, I want to compare the variants of a product

  Background:
    Given there is a product named "Product A"
    And it has some variants with various options
    And I am on the comparison page for "Product A"

  Scenario: The shopper sees a comparison chart of Variant A
    When "Variant A" has options "a,b,c"
    Then the comparison chart header should have options "a,b,c"
    And the comparison grid should have 3 checkboxes
```

When a feature request comes in you write out your cucumber scenarios and do the usual sign-off from the product manager. Nothing new or exciting here. Next, implement **failing** step files; yes of course they should fail first, this is TDD right? Mike has a strong opinion about what your features and steps should look like: short and specific. He's found that if you're writing too much setup, your feature is not well isolated or that perhaps this feature needs to be broken into several smaller ones.

Now that we have the feature in place, we can create the steps.

```ruby
Given /^there is a product named "([^"]*)"$/ do |product_name|
    @product = Product.create(:name => product_name)
  end

  Given /^it has some variants with various options$/ do
    @variant_a = Variant.create(:sku => 'Variant A', product => @product)
    VariantOption.create(:name => "Option A", :variant => @variant_a)
    #... same thing for B, C, D
  end

  Given /^I am on the comparison page for "([^"]*)"$/ do |product|
    # UI Action
    # visit product_path(@product.permalink)
    @current_product = Product.find product
  end

  When /^"([^"]*)" has options "([^"]*)"$/ do |variant, options|
    @current_variant = Variant.find variant
    opts = options.split(",")
    #... find the options
    @options = [@option_a, @option_b, @option_c, @option_d]
  end

  #... more steps
```

Keep in mind that at first, that these steps are going to be powered by FastModel and not Rails. Let's see how we use cucumber_tools to do this.

### Magic Sauce: Rapid Class Design

After compeleting a RED TDD cycle, Mike's strategy really takes center stage. Instead of creating classes, he uses FastModel to define the models, including existing models, fields and relationships needed for his feature. He goes even farther and stubs out the interface which is needed to satisify the cucumber test. Let's look at a specific example.

```ruby
class Product < FastModel
    fields :name
    has_many :variants
  end

  class Variant < FastModel
    fields :name
    has_many :variant_options
    belongs_to :product
  end

  class VariantOption < FastModel
    fields :name
    belongs_to :variant
  end

  class VariantCompareChart; end
```

### FastModel

Without writing migrations, or even loading Rails, you can use FastModel to think about some of the basics of your ActiveRecord models. This let's you focus on the design of your classes, by iterarting and testing quickly. These FastModels can actually go in the step file making it easier to stay focused on what matters: class design.

### Why stub in a cucumber feature?

It might seem strange to start stubbing out your class interface inside a cucumber feature. Mike understands this and just like the FastModels above, he isn't expecting these stubs to stay. He's using it as a tool to drive very quick class interface modeling. It's a great way to stay inside one test file and keep the cost of iterating through the class design low. This is a central part of the magic of his strategy. By keeping the design of class' interface directly linked to the design of the feature's steps, we ensure we only design and test our public interface. Let's see it in action:

```ruby
Then /^the comparison chart header should have options "([^"]*)"$/ do |options|
    opts = options.split(",")
    header = stub(:header) { opts }
    chart = stub(:chart, :header => header)
    VariantComparisonChart.stub(:build_for) { chart }

    chart = VariantComparisonChart.build_for(@current_product)
    opts.each do |option|
      chart.header.should include option
    end
  end
```

### Outside: Green. Time to move inside!

With passing cucumber tests backed by FastModels and stubs, our class design is complete. It's time to actually start building out the real, but still isolated classes, outside Rails. Using your FastModels and stubs as guides you can TDD up a well unit tested class that does the job. Then swap out the stubs and the FastModels with your real classes and confirm the cucumber cycle is still green.

### How do I use it?

FastModel and the stubbing library are included as part of cucumber_tool's [no_rails.rb](https://github.com/mikefarmer/cucumber_tools/blob/master/no_rails.rb) which can be called when executing your cucumber spec:

```
cucumber -r no_rails.rb path/to/feature.feature
```

Mike recommends avoiding the standard env.rb usage of cucumber to avoid loading Rails until you need it later. Mike says these tools were thrown together very quickly to capture the concept of "Feature Isolation" so any pull requests would be greatly appreciated. For more details, please visit Mike's [follow up article](http://blog.endpoint.com/2012/10/feature-isolation-overview.html).
