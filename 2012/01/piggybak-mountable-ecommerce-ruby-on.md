---
author: Steph Skardal
title: 'Introducing Piggybak: A Mountable Ruby on Rails Ecommerce Engine'
github_issue_number: 539
tags:
- ecommerce
- piggybak
- rails
date: 2012-01-06
---

Here at End Point, we work with a variety of open source solutions, both full-fledged ecommerce applications and smaller modular tools. In our work with open source ecommerce applications, we spend a significant amount of time building out custom features, whether that means developing custom shipping calculations, product personalization, accounting integration or custom inventory management.

There are advantages to working with a full-featured ecommerce platform. If you are starting from scratch, a full-featured platform can be a tool to quickly get product out the door and money in your pocket. But to do this, you must accept the assumptions that the application makes. And most generic, monolithic ecommerce platforms are created to satisfy many users.

Working with a large monolithic ecommerce platform has disadvantages, too:

- Sometimes over-generic-izing a platform to satisfy the needs of many comes at the cost of code complexity, performance, or difficulty in customization.
- Occasionally, the marketing of an ecommerce solution overpromises and underdelivers, leaving users with unrealistic expectations on what they get out of the box.
- Customization on any of these platforms is not always simple, elegant, or cheap. And it may prevent easy maintenance or upgrades in the future. For example, building out customization A, B, and C on the platform *today* may make it difficult to upgrade *later* to use the added features X, Y, and Z.
- Users of a platform rely heavily on the maintainers of the project. This can mean that users may not be able to keep up with a fast-moving platform, or even that a slow-moving platform doesn’t stay up to date with ecommerce trends.

Full-featured ecommerce platforms do make sense for a some clients. Hosted ecommerce solutions ([Shopify](http://www.shopify.com/), [Volusion](http://www.volusion.com/)) even make sense for a lot of people too. Here at End Point, we try to be realistic about the pros and cons of building off of an ecommerce platform, but balance that with available tools to develop something for our clients efficiently and pragmatically.

 

### Enter Rails

I like Ruby, and Ruby on Rails a lot. With [bundler](http://gembundler.com/), Rails has gotten particularly smart regarding managing dependencies. The Rails community also has a lot of great tools (gems) that can supplement an application. And a great MVC foundation plus include an improved way to manage assets (CSS, JavaScript, images) to help with performance and code organization. A few really great gems I’ve worked with are:

- [ActiveMerchant](http://activemerchant.org/): a Ruby library for handling payments
- [RailsAdmin](https://github.com/sferik/rails_admin): admin interface for managing data
- [ActsAsTaggableOn](https://github.com/mbleigh/acts-as-taggable-on): tagging functionality
- [Prawn](http://prawnpdf.org/api-docs/2.0/): a Ruby pdf generator
- [Paperclip](https://github.com/thoughtbot/paperclip), file attachment management functionality

The other thing that’s really cool about Ruby on Rails is [Rails Engines](http://edgeapi.rubyonrails.org/classes/Rails/Engine.html). Engines allow you to wrap Rails applications into modular elements that can be and easily shared across applications. And the parent application has control over the mount point of an Engine, meaning that a parent application can mount another engine at "/blog", "/shop", "/foo", "/bar" without affecting the Engine’s behavior.

I’m not trying to be a Rails fangirl here (I use WordPress for my personal website and still sometimes think Perl is the best tool for a job) :) But the ability to include and manage modular elements (gems, gems that are Engines) is great for building applications based on a few core modular elements.

### My Story

Several weeks ago, I started putting together a prototype for a client for a Ruby on Rails ecommerce site. Their site has fairly custom needs with a complex data relationships (data model), complex search requirements, but relatively simple cart and checkout needs. I was certain that existing open source Ruby on Rails ecommerce platforms would require a significant amount of customization and would be a hassle to maintain. I also recently spent a good deal of time working with RailsAdmin on a non-ecommerce Rails project ([blogged here](/blog/2011/08/railsadmin-gem-ecommerce)).

Rather than try to fight against an existing framework, I developed a prototype website using RailsAdmin. My prototype quickly developed into an ecommerce Ruby on Rails Engine, which offers basic shopping cart functionality, but it doesn’t try to solve every problem for everyone. Below are some details about this gem as a Rails Engine, called [Piggybak](https://github.com/piggybak/piggybak):

### Non-Tech Details

The Piggybak gem includes the following features:

- Basic shopping cart functionality for adding, updating, or removing items in a cart
- One page checkout, with AJAX for shipping and tax calculation
- Checkout for registered users or guests
- Configurable payment methods (via ActiveMerchant)
- Configurable shipping and tax calculators
- Admin interface for entering and managing orders

Here are a few screenshots:

<a href="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-0-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-0.png" /></a>

Demo homepage. The primary Rails application includes all the code for defining product navigation. In this case, it displays featured products and product categories.

<a href="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-1-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-1.png"/></a>

One page checkout

<a href="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-2-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-2.png" /></a>

Admin dashboard: Note that distinction between the primary application and the Piggybak gem regarding left navigation.

<a href="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-3-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" height="350" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-3.png"/></a>

Any item in the application can become sellable. This nested form displays in the admin for the sellable items.

<a href="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-4-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-4.png" /></a>
The cart form added to the image page is driven by the Piggybak gem, but the rest of the page content is driven by the primary application. The gem doesn’t make any decisions about what will be displayed on a standard product page. It only helps with generating the form to add something to the shopping cart.

<a href="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-5.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-5.png" /></a>

The admin interface for editing an order. An order has one billing and shipping address. It can have many line items, shipments, and payments. All of these nested elements are controlled directly on the order edit page.

### Tech Details

The Piggybak gem has the following dependencies:

- Ruby on Rails 3.1+
- RailsAdmin
- Devise (which is a dependency of RailsAdmin)
- CanCan (the parent application takes responsibility for defining authorization rules

This is certainly not a short list of dependencies, but if you are developing a new application on Rails, you are likely already using a couple of these tools. And I highly recommend using RailsAdmin :)

To get an idea of how the mountable solution works, these are the installation steps:

- Add to Gemfile and install with bundler
- Rake task for copying migrations and run migrations
- Mount engine in the parent’s appplication config/routes.rb

And then the following integration points are:

- **acts_as_variant** is added inside any model in your application to become sellable. This affectively assigns a relationship between your model(s) and the variants table. A variant belongs_to an item through a polymorphic relationship, and a model has_one variant. The variants table has information for its sku, price, quantity on hand, and shopping cart display name.
- **acts_as_orderer** is added inside inside the user model in your application that owns orders (probably User).
- <%= cart_form(@item) %> is a helper method that displays an add to cart form
- <%= cart_link %> is a helper method that displays a link to the cart with the current number of items and total
- <%= orders_link("Order History") %> is a helper method which links to a users orders page

### Summary

Here at End Point, we’ve had a few internal discussions about building ecommerce solutions based on more modular components to address the disadvantages we’ve seen in working with large monolithic ecommerce platforms. Rails provides a strong base for stitching modular components together easily.

<div style="margin: 0 25px 0 0; float:left;"><img style="margin: 0;" border="0" src="/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/image-6.jpeg" width="290"/><br/><small>© Steph Skardal</small></div>

My goal with this tool was to write a modular cart and checkout component that takes advantage of RailsAdmin’s DSL to provide a nice Admin interface for nested forms for models that already existing in your application. It wasn’t created to solve every ecommerce problem, or world peace. As its name indicates, this gem <b>piggybak</b>’s off of an existing Rails application.

It leaves the decision of all product finding methods and product navigation up to the developer, which means it might be great for:

- A deal of the day site that controls items offered daily. Deal of the day sites often don’t fit the standard mold of ecommerce so ecommerce platforms don’t always suit them well. And they may need significant performance customization, which is not always a feature included in a generic ecommerce platform.
- An ecommerce site with complex demands for search, where existing ecommerce solutions aren’t easily integrated with those search solutions. A developer may build their own custom search solution and mount piggybak for handling cart and checkout only.
- An ecommerce site with a complex data model, where multiple types of items with varied navigation. This gem gives the functionality to turn any item on a site into a sellable item (or variant).

Demo and more documentation is forthcoming. View the repository [here](https://github.com/piggybak/piggybak). Contributions (see TODO) appreciated. As I work through this project for the client in the next few weeks, I’m sure that there’ll be a few minor bugs to work out.
