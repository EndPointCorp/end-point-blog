---
author: Steph Skardal
title: The rails_admin gem in Ecommerce
github_issue_number: 484
tags:
- ecommerce
- ruby
- rails
- sinatra
date: 2011-08-09
---

Update: Since writing this article, this gem has had several updates. All rails_admin configuration now must be pulled out of ActiveRecord models and into the initializer. The look and feel has also been updated. Read about it more [here](https://github.com/sferik/rails_admin). Additionally, End Point has released a [Ruby on Rails Ecommerce Engine](/blog/2012/01/piggybak-mountable-ecommerce-ruby-on/) with a sleek admin interface driven by rails_admin. Read more about it [here](https://github.com/piggybak/piggybak).

I recently installed the [rails_admin](https://github.com/sferik/rails_admin) gem into a new Rails project. This particular site is currently running on [Interchange](http://www.icdevgroup.org/i/dev), but it is not an ecommerce business, so Interchange is overkill for the site. The client has recently decided to make the switch to Rails (and [DevCamps](http://www.devcamps.org/)) with our help, and they have a moderate budget to do so. For the first increment, we considered installing [phpMyAdmin](https://www.phpmyadmin.net/) for them to work directly with the data until a nice admin interface was built, but instead I spent a bit of time installing the rails_admin gem which has been on my mind for the last 6 months. The result: I’m **extremely** impressed with what rails_admin has to offer.

To show some examples of rails_admin in action, I’ll use the data model from a Sinatra ecommerce setup I [recently wrote about](/blog/2011/03/ecommerce-sinatra-shopping-cart/), because it has a basic ecommerce data model that should be universally understood by my coworkers and clients.

To create a new site, I went through the standard Rails 3.0 installation steps:

- **gem install rails -v=3.0.9** to install Rails
- **rails new mystore** to create a new Rails application
- In my gemfile, I added:

```ruby
gem 'devise'
gem 'rails_admin', :path => 'vendor/gems/rails_admin'
gem 'ckeditor' # for WYSIWYG editing
gem 'paperclip' # and installed imagemagick, for image attachments
```

- **sudo bundle install** to install the project gems
- **rake rails_admin:install** to install rails_admin, which also runs devise setup and migrations
- **rails generate ckeditor:install** to install ckeditor
- Copied my Sinatra data migrations and models over to my Rails application (except for the User, which is now replaced with devise’s User)
- **rake db:migrate** to apply all migrations
- **rails s** to start my server
- Also, I created a user from the **rails console**

Note that I also tried to use Rails 3.1 and the master branch of rails_admin, but I was experiencing a few bugs, so I decided to stick with Rails 3.0.9 for this article. Coincidentally, the rails_admin master branch just jumped to Rails 3.1 very recently. There are a few Rails 3.1 things to be aware of with the Rails 3.1 [Asset Pipeline](https://weblog.rubyonrails.org/2011/5/22/rails-3-1-release-candidate/).

### Out of the Box

After I got everything up and running, my first look at /admin looks nice. It shows the number of records per model, recent history, and a list of models for navigation on the right side:

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-0.png" style="display:block; margin:0px auto 30px; text-align:center;cursor:pointer; cursor:hand;width: 745px;"/>

rails_admin has a nice DSL to modify the admin interface. I applied a few updates to my application, described below.

### Remove Model / Tab

First, I wanted to hide Users from the /admin, which required the change below. Note that you can also pass a block to determine the visibility of a model, which may be valuable if you want to limit the visibility of models to specific roles or users.

```ruby
class User < ActiveRecord::Base
  ...

  rails_admin do
    visible false # or visible { some block }
  end
end
```

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-1.png" style="display:block; margin:0px auto 0px; text-align:center;cursor:pointer; cursor:hand;width:745px;"/>

Users Tab removed from navigation

### List Views

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-2.png" style="display:block; margin:0px auto; text-align:center;cursor:pointer; cursor:hand;width:745px;"/>

Product List View, rails_admin Out of the Box

Next, I updated my products list view with the following changes, to limit the list view to the name and price field, sort by the name, and format the price:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<td style="border-right:1px solid #999;">Limit listing of fields.</td>
<td style="border-right:1px solid #999;">Add default sort by :name field.</td>
<td>Add formatting to price field.</td>
</tr>
<tr>
<td align="left" style="border-right:1px solid #999;" valign="top"><pre class="brush:ruby" style="margin:0px;">
class Product < ActiveRecord::Base
  rails_admin do
    list do
      field :name
      field :price
    end
  end
end
</pre></td>
<td align="left" style="border-right:1px solid #999;" valign="top"><pre class="brush:ruby" style="margin:0px;">
class Product < ActiveRecord::Base
  rails_admin do
    list do
      sort_by :name
      field :name
      field :price
    end
  end
end
</pre></td>
<td align="left" valign="top"><pre class="brush:ruby" style="margin:0px;">
class Product < ActiveRecord::Base
  rails_admin do
    list do
      sort_by :name
      field :name
      field :price do
        formatted_value do
          sprintf "$%.2f",
        end
      end
    end
  end
end
</pre></td>
</tr>
</tbody></table>

Here’s a screenshot of the Products list view after these updates:

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-3.png" style="display:block; margin:0px auto 30px; text-align:center;cursor:pointer; cursor:hand;width:745px;"/>

### WYSIWIG-ing It

Next, I want to add a WYSIWYG editor for one of my fields, which can be accomplished with the following change:

```ruby
class Page < ActiveRecord::Base
  rails_admin do
    edit do
      include_all_fields
      field :content, :text do
        ckeditor true
      end
    end
  end
end
```

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-4.png" style="display:block; margin:0px auto; text-align:center;cursor:pointer; cursor:hand;width:745px;"/>

ckeditor used for content field.

### Paperclip Image Attachments

rails_admin also works nicely with [Paperclip](https://github.com/thoughtbot/paperclip), a very popular image attachment Rails gem. Paperclip requires that imagemagick be installed on the server. I add the following code to my product model, which already had the Paperclip reference to an attached image, and the migration to introduce the Paperclip required attachment fields.

```ruby
class Product < ActiveRecord::Base
  rails_admin do
    edit do
      include_all_fields
      field :image do
        thumb_method :thumb
      end
    end
  end
end
```

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-5.png" style="display:block; margin:0px auto; text-align:center;cursor:pointer; cursor:hand;width:745px;"/>

The products edit view is now a multitype form to allow for image upload.

And to update the show view, I made this change:

```ruby
class Product < ActiveRecord::Base
  ...
  rails_admin do
    show do
      include_all_fields
      field :image do
        thumb_method :thumb
      end
    end
  end
end
```

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-6.png" style="display:block; margin:0px auto; text-align:center;cursor:pointer; cursor:hand;width:745px;"/>

Thumb image added to product show view.

### Overriding Views

Another common update in rails_admin might be the need to override views to change the look of the backend interface. I accomplished this by copying the rails_admin partial views into my Rails application and updating them to include “My Store” branding:

```ruby
# app/views/rails_admin/main/_title.html.haml
%h1.title
  = link_to rails_admin_dashboard_path do
    %span.red My
    %span.white Store
```

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-7.png" style="display:block; margin:0px auto; text-align:center; cursor:pointer; cursor:hand;width:745px;"/>

After overriding the header view, “My Store” now appears in the header.

<img alt="" border="0" src="/blog/2011/08/railsadmin-gem-ecommerce/image-8.png" style="display:block; margin:0px auto; text-align:center; cursor:pointer; cursor:hand;width:745px;"/>

And an override of app/views/layouts/rails_admin/main.html.haml removes “Rails Admin | 2011” from the bottom of the page.

### Conclusion

There’s tons(!) more you can do with the gem, and it’s documented thoroughly [here](https://github.com/sferik/rails_admin). rails_admin comes out of the box with export to CSV, JSON, and XML logic, which makes it a nice base for building simple APIs. It recognizes the Rails associations has_many, belongs_to, has_and_belongs_to_many, etc. It also includes user history and filtering of items and does authentication with [devise](https://github.com/plataformatec/devise), which has become a very popular user authentication choice in Rails. I found a few potential disadvantages:

- Some type of import functionality is missing (needed for my client)
- ActiveRecord is the only ORM supported, but that’s fine with me.
- It’s right on the bleeding edge of Rails, which makes it ideal for new Rails applications and can’t always be used for older apps.
- I am curious to see if performance suffers on applications with a large number of records.

Despite the potential disadvantages, I’ve been extremely impressed with it’s functionality and how much development time can be saved here to allow more time for custom business-centric functionality for a client.

Note that a couple of popular alternatives to rails_admin are [ActiveAdmin](https://activeadmin.info/) and [Typus](https://github.com/typus/typus/wiki)

### What next?

Since I’ve already built a Sinatra front-end ecommerce application, I might try to get my Rails admin running with a Sinatra frontend by following tips [in this article](https://web.archive.org/web/20110830052603/http://m.onkey.org/rails-meets-sinatra). It’ll be a little more complex here since I need to map user and admin and user routes to Rails and other routes to Sinatra, but the article covers the general idea for dispatching the routes. Why do it this way? Because you get the best of both worlds: a nice Rails backend for the CRUD interface and API management, and a speedy Sinatra driven frontend with simple paths to define product navigation, product pages, content pages, the cart and checkout process (which is not standard RESTful behavior). You can also leverage Ruby gem functionality in both Sinatra and Rails.
