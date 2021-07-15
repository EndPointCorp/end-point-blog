---
author: Steph Skardal
title: Advanced Product Options (Variants) in Piggybak
github_issue_number: 737
tags:
- ecommerce
- piggybak
- rails
date: 2012-12-18
---

About a month ago, Tim Case and I developed and released a [Piggybak](https://github.com/piggybak/piggybak) extension [piggybak_variants](https://github.com/piggybak/piggybak_variants), which provides advanced product optioning (or variant) support in Piggybak. Piggybak is an open source Ruby on Rails ecommerce platform developed and maintained by End Point. Here, I discuss the background and basics of the extension.

### Motivation & Background

The motivation for this extension was the common ecommerce need for product options (e.g. size, color), where each variation shares high-level product information such as a title and description, but variants have different options, quantities available, and prices. Having been intimately familiar with Spree, another open source Ruby on Rails ecommerce framework, we decided to borrow similarities of Spree's product optioning data model after seeing its success in flexibility over many projects. The resulting model is similar to Spree's data model, but a bit different due to the varied nature in Piggybak's mountability design.

<img border="0" src="/blog/2012/12/advanced-product-options-variants-in/image-0.png"/>

Spree's data model for advanced product optioning. A product has many variants. Each variant has and belongs to many option values. A product also has many options, which define which option values can be assigned to it.

### Piggybak Variants Data Model

<img border="0" height="112" src="/blog/2012/12/advanced-product-options-variants-in/image-1.png" width="391"/>

Option configuration data model in Piggybak

The data model starts with option configurations, option configurations are created and specify which class they belong to. For example, a *Shirt* model may have options *Size* and *Color*, and this would be stored in the option configurations table. In this case, an option will have a name (e.g. *Size* and *Color*) and a position for sorting (e.g. 1 and 2). The option configuration will reference an option and assign a klass to that option (in this case *Shirt*). Another example of option configurations may be a Picture Frame, that has option configurations for *Dimensions* and *Finish*.

<img border="0" height="124" src="/blog/2012/12/advanced-product-options-variants-in/image-2.png" width="301"/>

Option value configuration in Piggybak

After option configurations are defined, one will define option values for each option configuration. For example, option values will include *Red*, *Blue*, and *Green* for the option *Color* with position 1, 2, and 3. And option values will include *Small*, *Medium*, and *Large* with positions 1, 2, and 3 for the option **Size**.

<img border="0" src="/blog/2012/12/advanced-product-options-variants-in/image-3.png" width="750"/>

After options, option configurations, and option values are defined, we are ready to create our variants. Per the above data model, a variant has and belongs to many option_values_variants (and must have one value per option). In our *Shirt* example, a variant must have one *Color* option value and one *Size* option value assigned to it through the option_values_variants table. A variant belongs to a specific sellable item (Shirt) through a polymorphic relationship, which is consistent with Piggybak's mountability design to allow different classes to be sellable items. Finally, a variant has_one piggybak_sellable and accepts piggybak_sellable attributes in a nested form, which means that a variant has one sellable which contains quantity, pricing, and cart description information. What this gives us is a sellable item (Shirt) with many variants where each variant has option values and each variant has sellable information such as quantity available, price, and description in cart. Below I'll provide a few screenshots of what this looks like in the admin and front-end interface.

### How to  Use the Plugin

To install the extension, the following steps must be applied:

1. Add the gem to the Gemfile and run bundle install
1. Install and run the extension rake piggybak_variants:install:migrations and rake db:migrate
1. Add acts_as_sellable_with_variants to any model that should have variants. You may need to add appropriate attr_accessible settings in your model as well, depending on your attribute accessibility settings.
1. In the admin, define option configurations and option values for each option, then create variants for your sellable instances.
1. Finally, add <%= variant_cart_form(@instance) %> to your sellable item's show page to render the cart form.

These steps are similar to Piggybak's core behavior for adding non-variant sellable items.

### Screenshots

The [Piggybak demo](https://github.com/piggybak/demo) uses this extension for selling several product options of photography frames. The images and captions below represent the variants extension for this use case.

<img border="0" src="/blog/2012/12/advanced-product-options-variants-in/image-4.png" style="border:5px solid #E6E6E6;margin-bottom:0px;" width="700"/>

The *Frame* class has two options assigned to it (Frame Size and Frame Finish). Since Frame Size has a position equal to one and Frame Finish has a position equal to two, Frame Size will show as the first option on the product page.

<img border="0" src="/blog/2012/12/advanced-product-options-variants-in/image-5.png" style="border:5px solid #E6E6E6;margin-bottom:0px;" width="700"/>

The *Frame Finish* option is assigned to the *Frame* class and it has four option values (Black, Cherry, Bronze, and Iron).

<img border="0" src="/blog/2012/12/advanced-product-options-variants-in/image-6.png" style="border:5px solid #E6E6E6;margin-bottom:0px;" width="700"/>

On the Frame edit page, 8 variants are created to represent the combinations of 2 Frame Sizes and 4 Frame Finishes.
Each variant has pricing, quantity, and cart description information, as well as additional sellable fields.

<img border="0" src="/blog/2012/12/advanced-product-options-variants-in/image-7.png" style="border:5px solid #E6E6E6;margin-bottom:0px;" width="700"/>

And the product page shows the options and option values for that item, displayed based on Position and Size data.
When each option value is triggered, appropriate pricing information is displayed.

### Conclusion

The goal of this extension was to provide variant functionality that is not necessarily required to be used with Piggybak. Piggybak can still be leveraged without this extension to provide simple single product option add to cart functionality. The Piggybak cart only examines what elements are in the cart based on the sellable_id and the quantity, which is the driving force of the core Piggybak architecture as well as this extension.

Stay tuned for additional updates to the [Piggybak Ruby on Rails Ecommerce](https://github.com/piggybak/piggybak) platform.
