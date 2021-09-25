---
author: Steph Skardal
title: 'Spree and Software Development: Git and Ruby techniques'
github_issue_number: 284
tags:
- rails
- spree
date: 2010-03-31
---

Having tackled a few interesting Spree projects lately, I thought I’d share some software evelopment tips I’ve picked up along the way.

### Gem or Source?

The first decision you may need to make is whether to run Spree from a gem or source. Directions for both are included at the [Spree Quickstart Guide](https://web.archive.org/web/20091231112834/http://spreecommerce.com/support/quick_start), but the guide doesn’t touch on motivation from running from a gem versus source. The [Spree documentation](https://web.archive.org/web/20101128005839/http://spreecommerce.com/documentation) does address the question, but I wanted to comment based on recent experience. I’ve preferred to build an application running from the gem for most client projects. The only times I’ve decided to work against Spree source code was when the Spree edge code had a major change that wasn’t available in a released gem, or if I wanted to troubleshoot the internals of Spree, such as the extension loader or localization functionality.

If you follow good code organization practices and develop modular and abstracted functionality, it should be quite easy to switch back and forth between gem and source. However, switching back and forth between Spree gem and source may not be cleanly managed from a version control perspective.

### git rebase

Git rebase is lovely. Ethan describes some examples of using git rebase [here](/blog/2009/05/git-rebase-just-workingness-baked-right). When working with several other developers and even when I’m the sole developer, I’ve included rebasing in my pull and push workflow.

### .gitmodules

Git submodules are lovely, also. An overview on git submodules with contributions from Brian Miller and [David Christensen](/blog/authors/david-christensen) can be read [here](/blog/2010/04/git-submodule-workflow). Below is an example of a .gitmodules from a recent project that includes several extensions written by folks in the Spree community:

```plain
[submodule "vendor/extensions/faq"]
        path = vendor/extensions/faq
        url = git://github.com/joshnuss/spree-faq.git
[submodule "vendor/extensions/multi_domain"]
        path = vendor/extensions/multi_domain
        url = git://github.com/railsdog/spree-multi-domain.git
[submodule "vendor/extensions/paypal_express"]
        path = vendor/extensions/paypal_express
        url = git://github.com/railsdog/spree-paypal-express.git
```

### .gitignore

This should apply to software development for other applications as well, but it’s important to setup .gitignore correctly at the beginning of the project. I typically ignore database, log, and tmp files. Occasionally, I ignore some public asset files (stylesheets, javascripts, images) if they are copied over from an extension upon server restart, which is standard in Spree.

### Overriding modules, controllers, and views

Now, the good stuff! So, let’s assume the Spree core is missing functionality that you need. Options for expanding from the Spree core include overriding or extending existing models, controllers, or views, or writing and including new models, controllers, or views. [Spree’s Extension Tutorial](https://web.archive.org/web/20091231113745/http://spreecommerce.com/documentation/extension_tutorial.html) covers adding new controllers, models, and views, so I’ll discuss extending and overriding existing models, views and controllers below.

#### Extend an Existing Controller

To extend an existing controller, I’ve typically included a module with the extended behavior in the *_extension.rb file. For all examples, let’s assume that my extension is named "Site", another standard in Spree. The code below shows the module include in site_extension.rb:

```ruby
...
def activate
  ProductsController.send(:include, Spree::Site::ProductsController)
end
...
```

My ProductsController module, inside the Spree::Site namespace, includes the following to define a before filter in the Spree core products controller:

```ruby
module Spree::Site::ProductsController
  def self.included(controller)
    controller.class_eval do
      controller.append_before_filter :do_stuff
    end
  end

  def do_stuff
    #doing stuff
  end
end
```

#### Override an Existing Controller Method

Next, to override a method in an existing controller, I’ve started the same way as before, by including a module in site_extension.rb:

```ruby
...
def activate
  CheckoutsController.send(:include, Spree::Site::CheckoutsController)
end
...
```

The Spree::Site::CheckoutsController module will contain:

```ruby
module Spree::Site::CheckoutsController
  def self.included(target)
    target.class_eval do
      alias :spree_rate_hash :rate_hash
      def rate_hash; site_rate_hash; end
    end
  end

  def site_rate_hash
    # compute new rate_hash
  end
end
```

In this example, the core rate_hash method is aliased for later use. And the rate_hash method is redefined inside the class_eval block. This example demonstrates how to override the core shipping rate computation during checkout.

#### Extend an Existing Model

Next, I’ll provide an example of extending an existing Spree model. site_extension.rb will include the following:

```ruby
...
def activate
  Product.send(:include, Spree::Site::Product)
end
...
```

And Spree::Site::Product module contains:

```ruby
module Spree::Site::Product
  def new_product_method
    # new product instance method
  end
end
```

In the situation where you may want to create a class object method rather than an instance object method, you may include the following in Spree::Site::Product:

```ruby
module Spree::Site::Product
  def self.included(target)
    def target.do_something_special
      'Something Special!'
    end
  end
end
```

The above example adds a method to the Product class object to be called from a view, for example <%= Product.do_something_special %> will return ‘Something Special!’.

#### Override an Existing Model Method

To override a method from an existing model, I start with a module include in site_extension.rb:

```ruby
...
def activate
  Product.send(:include, Spree::Site::Product)
end
...
```

And Spree::Site::Product contains the following:

```ruby
module Spree::Site::Product
  def self.included(model)
    model.class_eval do
      alias :spree_master_price :master_price
      def master_price; site_master_price; end
    end
  end
  def site_master_price
    '1 billion dollars'
  end
end
```

And from the view, the two methods can be called within the following block:

```plain
<% @products.each do |product| -%>
<%= product.master_price %> vs <%= product.spree_master_price.to_s %>
<% end -%>
```

#### Extend an Existing View

I previously discussed the introduction of hooks in depth [here](/blog/2010/01/rails-ecommerce-spree-hooks-tutorial) and [here](/blog/2010/01/rails-ecommerce-spree-hooks-comments). To extend an existing view that has a hook wrapped around the content you intend to modify, you may add something similar to the following to *_hooks.rb, where * is the extension name:

```ruby
insert_after :homepage_products, 'shared/promo'
```

The above code inserts the ‘shared/promo’ view to be rendered above the homepage_products hook in the Spree gem or Spree source ~/app/views/products.index.html.erb view. Other hook actions include insert_before, replace, or remove.

#### Override an Existing View

Before the introduction of hooks, the standard method of overriding or extending core views was to copy the core view into your extension view directory, and apply changes. In some cases, hooks are not always in the desired location. To override the footer view since there is no footer hook, I copy the Spree gem footer view to the extension view directory. The diff below compares the Spree gem view and my extension footer view:

```diff
- <div id="footer">
-  <div class="left">
-    <p>
-      <%= t("powered_by") %> <a href="http://spreecommerce.com/">Spree</a>
-    </p>
-  </div>
-  <div class="right">
-    <%= render 'shared/language_bar' if Spree::Config[:allow_locale_switching] %>
-  </div>
- </div>
  <%= render 'shared/google_analytics' %>
+ <p><a href="http://www.endpoint.com/">End Point</a></p>
```

### Sample data

A final tip that I’ve found helpful when developing with Spree is to create sample data files in the extension db directory to maintain data consistency between developers. In a recent project, I’ve created the following stores.yml data to initiate several stores for the multi domain extension:

```ruby
store_1:
  name: Store1
  code: store1
  domains: store1.mysite.com
  default: false
store_2:
  name: Store2
  code: store2
  domains: store2.mysite.com
  default: true
store_3:
  name: Store3
  code: store3
  domains: store3.mysite.com
  default: false
```

Many of these tips apply to general to software development. The tips specific to development in Spree (and possibly other Rails platforms) include the sample data syntax and the described Ruby techniques to extend and override class and model functionality.
