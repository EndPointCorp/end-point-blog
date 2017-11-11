---
author: Barrett Griffith
gh_issue_number: 733
tags: piggybak, rails
title: 'Piggybak Extensions: A Basic How-To Guide'
---

This article outlines the steps to build an extension for [Piggybak](http://www.piggybak.org/). Piggybak is an open-source Ruby on Rails ecommerce platform created and maintained by End Point. It is developed as a Rails Engine and is intended to be mounted on an existing Rails application. If you are interested in developing an extension for Piggybak, this article will help you identify the steps you need to take to have your extension leveraging the Piggybak gem, and integrating smoothly into your app.

### Introduction

The Piggybak platform is lightweight and relies on Rails meta-programming practices to integrate new extensions. The best references to use alongside your development should be the previously developed extensions found here:

- [Bundle Discounts](https://github.com/piggybak/piggybak_bundle_discounts)
- [Coupons](https://github.com/piggybak/piggybak_coupons)
- [Variants](https://github.com/piggybak/piggybak_variants)
- [Taxonomy](https://github.com/piggybak/piggybak_taxonomy)
- [Real-time Shipping](https://github.com/piggybak/piggybak_realtime_shipping)

It is likely that your extension will tie into the admin interface. Piggybak utilizes the [RailsAdmin gem](https://github.com/sferik/rails_admin) for its admin interface.

### Setting up the Development Environment

A convenient way to start building out your extension is to develop against the demo app found [here](https://github.com/piggybak/demo). The demo app utilizes the Piggybak gem and comes with sample data to populate the e-commerce store.

The Piggybak demo app [sample data](https://github.com/piggybak/demo/blob/master/sample.psql) is exported for a PostgreSQL database. To use this data (suggested) you should be prepared to do one of the following:

- be using PostgreSQL and understand how to work with the existing data dump
- transform this data dump to another database format that fits your database flavor of choice
- ignore the sample data and create your own

### Creating the Extension (Gem, Engine)

In a folder outside of the project utilizing the Piggybak gem, create a mountable rails engine:

```bash
$ rails plugin new [extension_name] --mountable
```

The "mountable" option makes you engine namespace-isolated.

Next, update your app's Gemfile to include the extension under development

```ruby
gem "piggybak_new_extension", :path => "/the/path/to/the/extension"
```

Run bundle install to install the extension in your application and restart your application.

### Special Engine Configuration

Your extension will rely on the engine.rb file to integrate with Piggybak. A sample engine.rb for the piggybak_bundle_discount can be found [here](https://github.com/piggybak/piggybak_bundle_discounts/blob/master/lib/piggybak_bundle_discounts/engine.rb). Let's go over this file to get a clue of how bundle discounts are served as an extension in Piggybak.

Make sure you are requiring any of your classes at the top of your engine.rb file, e.g.:

```ruby
require 'piggybak_bundle_discounts/order_decorator'
```

The code below is decorating the Piggybak::Order class, which is a helpful pattern to use when you wish to enhance class capabilities across engines. In the bundle discount case, the decorator adds several active record callbacks.

```ruby
config.to_prepare do
  Piggybak::Order.send(:include, ::PiggybakBundleDiscounts::OrderDecorator)
end
```

An order is comprised of many line items, which are used to calculate the balance due. More information on the line item architecture is described [here](http://blog.endpoint.com/2012/10/piggybak-update-line-item-rearchitecture.html). If your extension needs to register new line item types to the order, you may use something similar to the following code to set up the information regarding this new line item type.

```ruby
config.before_initialize do
  Piggybak.config do |config|
    config.extra_secure_paths << "/apply_bundle_discount"
    config.line_item_types[:bundle_discount] = {
      :visible => true,
      :allow_destroy => true,
      :fields => ["bundle_discount"],
      :class_name => "::PiggybakBundleDiscounts::BundleDiscount",
      :display_in_cart => "Bundle Discount",
      :sort => config.line_item_types[:payment][:sort]
    }
    config.line_item_types[:payment][:sort] += 1
  end
end
```

Does your extension need client side support? Piggybak utilizes the asset pipeline so you will need to register your assets here to have them pre-compiled.

```ruby
initializer "piggybak_bundle_discounts.precompile_hook" do |app|
  app.config.assets.precompile += ['piggybak_bundle_discounts/piggybak_bundle_discounts.js']
end
```

Finally, since Piggybak utilizes RailsAdmin for its admin system, we need to register the models as following the [RailsAdmin documentation]().

```ruby
initializer "piggybak_bundle_discounts.rails_admin_config" do |app|
  RailsAdmin.config do |config|
    config.model PiggybakBundleDiscounts::BundleDiscount do
      navigation_label "Extensions"
      label "Bundle Discounts"

      edit do
        field :name
        field :multiply do
          help "Optional"
        end
        field :discount
        field :active_until
        field :bundle_discount_sellables do
          active true
          label "Sellables"
          help "Required"
        end
      end
    end

    config.model PiggybakBundleDiscounts::BundleDiscountSellable do
      visible false
      edit do
        field :sellable do
          label "Sellable"
          help "Required"
        end
      end
    end
  end
end
```

### What else?

From here, extension development can follow standard Rails engine development, which allows for support of its own models, controllers, views, and additional configuration. Any database migrations inside an extension must be copied to the main Rails application to be applied.

You may also need to be aware of how Piggybak integrates with CanCan to ensure that CanCan permissions on your extension models are set correctly.

End Point created and maintains Piggybak project. Much of the inspiration for Piggybak comes from our expert engineers who have ecommerce experience working and contributing to platforms such as Spree, RoR-e, and Interchange. If you are interested in talking with us about your next ecommerce project, or have an ecommerce project that needs support, let us know.
