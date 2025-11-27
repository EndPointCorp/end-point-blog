---
title: "Quick and Dirty Admin Pages with Rails scaffold_controller"
author: Couragyn Chretien
date: 2025-12-01
description: Build admin interfaces fast with Rails' scaffold_controller generator. Skip heavy gems and create full CRUD controllers/views for existing models in minutes. Perfect for internal tools and prototypes.
tags: 
- rails
- admin
- scaffold_controller
- quick and dirty
---

## Quick and Dirty Admin Pages with Rails scaffold_controller
You're building a Rails application, and you've reached that point where you or your team needs a simple way to manage data. You need an admin interface. You've heard of heavy-weight solutions like ActiveAdmin or Rails Admin, but they feel like overkill for adding a few new categories or moderating user posts. You don't want to spend an afternoon configuring a gem. You need something now.

Luckily Rails has a built-in lightning-fast way to generate a fully functional admin CRUD interface for any existing model. Meet the often-overlooked scaffold_controller generator. It's the secret weapon for building "quick and dirty" internal tools.

### What is scaffold_controller and why Use It?
When you run `rails generate scaffold Post`, it creates everything: the model, migration, controller, and views. The scaffold_controller generator does only half of that, it creates just the controller and views (as long as the model already exists).

This is perfect for creating a separate admin namespace because:
- **It's Non-Destructive:** Your existing, user-facing PostsController remains untouched.
- **It's Fast:** One command gives you a complete set of CRUD actions and ERB views.
- **It's Simple:** No new gems, dependencies, or complex configurations to learn.

### Let's Build an Admin Interface for a Product Model
Imagine you have a Product model in your application. You have a ProductsController for your main site, but now you need an admin area to create, edit, and delete products.

#### Step 1: Create the Admin Namespace and Route

First, we'll set up a routing namespace to keep our admin logic separate. This will put our URLs in this format: `/admin/products`

Open your `config/routes.rb` file and add:

ruby
# config/routes.rb
Rails.application.routes.draw do
  # ... existing routes ...

  namespace :admin do
    resources :products
  end
end
Running `rails routes` will now show new routes like `admin_products_path`, `edit_admin_product_path`, etc.

#### Step 2: Generate the Scaffold Controller

Now for the magic. In your terminal, run `rails generate scaffold_controller Admin::Product`

Important Notes:
- The namespace (Admin::) must match the one you used in your routes.
- The model name (Product) must be singular, just like with a regular scaffold.

This one command generates several files:
- **Controller:** `app/controllers/admin/products_controller.rb`
- **Views:** A full set of ERB templates in `app/views/admin/products/` (`index.html.erb`, `show.html.erb`, `new.html.erb`, `edit.html.erb`, `_form.html.erb`)

#### Step 3: Update the generated Controller

The generated controller is a great start but it needs one crucial tweak. It doesn't know about our namespace, so it will look for the Product model in the wrong place. The key change is ensuring every reference to the model is to Product, not Admin::Product.

Open the products_controller.r and change the class definition and any model references. Here's a simplified example of what it should look like:

```ruby
# app/controllers/admin/products_controller.rb
module Admin
  class ProductsController < ApplicationController
    before_action :set_product, only: [:show, :edit, :update, :destroy]

    # GET /admin/products
    def index
      @products = Product.all
    end

    # ... other actions ...

    private
      def set_product
        @product = Product.find(params[:id])
      end

      def product_params
        params.require(:product).permit(:name, :description, :price, :stock)
      end
  end
end
```

#### Step 4: Add a Link and Access Control

Your admin interface is now live at `http://localhost:3000/admin/products`. Before you deploy you must add some form of access control. This can be as simple as a basic HTTP authentication check in your Admin::ProductsController.

```ruby
# app/controllers/admin/products_controller.rb
module Admin
  class ProductsController < ApplicationController
    http_basic_authenticate_with name: ENV['ADMIN_USER'], password: ENV['ADMIN_PASSWORD']

    # ... rest of the controller code ...
  end
end
```

It would also be good to add a link in your navigation for easy access:
`<%= link_to "Admin Products", admin_products_path if Rails.env.development? %>`

### When Should You Use This Method?
**Ideal for:**
- Internal tools, administrative, and support functions.
- Rapid prototyping.
- Simple CRUD needs where a full-blown admin gem is overkill.

**Not ideal for:**
- Customer-facing admin panels that need complex filtering, dashboards, or custom forms.
- Applications where you need fine-grained, role-based permissions.

### Conclusion
The scaffold_controller generator is a fantastic piece of Rails tooling that is often overlooked. It embodies the Rails philosophy of providing quick solutions for common problems. In just a few minutes you can have a functional, separate admin area for any model without the overhead of a new gem or the risk of breaking your public-facing code. So next time you need a simple data management interface, skip the gem research and let scaffold_controller do the heavy lifting for you.