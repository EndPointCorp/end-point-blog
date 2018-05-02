---
author: Steph Skardal
gh_issue_number: 550
tags: ecommerce, piggybak, ruby, rails
title: Download Functionality for Rails Ecommerce
---

I recently had to build out downloadable product support for a client project running on [Piggybak (a Ruby on Rails Ecommerce engine)](https://github.com/piggybak/piggybak) with extensive use of [RailsAdmin](https://github.com/sferik/rails_admin). Piggybak's core functionality does not support downloadable products, but it was not difficult to extend. Here are some steps I went through to add this functionality. While the code examples apply specifically to a Ruby on Rails application using [paperclip](https://github.com/thoughtbot/paperclip) for managing attachments, the general steps here would apply across languages and frameworks.

### Data Migration

Piggybak is a pluggable ecommerce engine. To make any models inside your application "sellable", the class method acts_as_variant must be called for any class. This provides a nice flexibility in defining various sellable models throughout the application. Given that I will sell tracks in this example, my first step to supporting downloadable content is adding an is_downloadable boolean and attached file fields to the migration for a sellable item. The migration looks like this:

```ruby
class CreateTracks < ActiveRecord::Migration
  def change
    create_table :tracks do |t|
      # a bunch of fields specific to tracks

      t.boolean :is_downloadable, :nil => false, :default => false

      t.string :downloadable_file_name
      t.string :downloadable_content_type
      t.string :downloadable_file_size
      t.string :downloadable_updated_at
    end
  end
end
```

### Class Definitions

Next, I update my class definition to make tracks sellable and hook in paperclip functionality:

```ruby
class Track < ActiveRecord::Base
  acts_as_variant

  has_attached_file :downloadable,
                    :path => ":rails_root/downloads/:id/:basename.:extension",
                    :url => "downloads/:id/:basename.:extension"
end
```

The important thing to note here is that the attached downloadable files **must not** be stored in the public root. Why? Because we don't want users to access the files via a URL through the public root. Downloadable files will be served via the send_file call, discussed below.

### Shipping

Piggybak's order model has_many shipments. In the case of an order that contains only downloadables, shipments can be empty. To accomplish this, I extend the Piggybak::Cart model using [ActiveSupport::Concern](http://www.fakingfantastic.com/2010/09/20/concerning-yourself-with-active-support-concern/) to check whether or not an order is downloadable, with the following instance method:

```ruby
module CartDecorator
  extend ActiveSupport::Concern

  module InstanceMethods
    def is_downloadable?
      items = self.items.collect { |li| li[:variant].item }
      items.all? { |i| i.is_downloadable }
    end
  end
end

Piggybak::Cart.send(:include, CartDecorator)
```

If all of the cart items are downloadable, the order is considered downloadable and no shipment is generated for this order. With this cart method, I show the FREE! value on the checkout page under shipping methods.

<img border="0" height="213" src="/blog/2012/02/08/download-functionality-rails-ecommerce/image-0.png" width="400"/>

### Forcing Log In

The next step for adding downloadable support is to add code to enforce user log in. In this particular project, I assume that downloads are not included as attachments in files since the files may be extremely large. I add a has_downloadable method used to enforce log in:

```ruby
module CartDecorator
  extend ActiveSupport::Concern

  module InstanceMethods
    ...

    def has_downloadable?
      items = self.items.collect { |li| li[:variant].item }
      items.any? { |i| i.is_downloadable }
    end
  end
end

Piggybak::Cart.send(:include, CartDecorator)
```

On the checkout page, a user is forced to log in if cart.has_downloadable?. After log in, the user bounces back to the checkout page.

<div class="separator" style="clear: both; text-align: center;">
<img border="0" height="177" src="/blog/2012/02/08/download-functionality-rails-ecommerce/image-1.png" width="400"/></div>

### Download List Page

After a user has purchased downloadable products, they'll need a way to access these files. Next, I create a downloads page which lists orders and their downloads:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/02/08/download-functionality-rails-ecommerce/image-2-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" height="380" src="/blog/2012/02/08/download-functionality-rails-ecommerce/image-2.png" width="400"/></a></div>

With a user instance method (current_user.downloads_by_order), the download index page iterates through orders with downloads to display orders and their downloads. The user method for generating orders and downloads shown here:

```ruby
class User < ActiveRecord::Base
  ...
  def downloads_by_order
    self.piggybak_orders.inject([]) do |arr, order|
      downloads = []
      order.line_items.each do |line_item|
        downloads << line_item.variant.item if line_item.variant.item.is_downloadable?
      end

      arr << {
          :order => order,
          :downloads => downloads
      } if downloads.any?
      arr
    end
  end
end
```

The above method would be a good candidate for Rails low-level caching or alternative caching which should be cleared after user purchases to minimize download lookup.

### Sending Files

As I mentioned above, download files should not be stored in the public directory for public accessibility. From the download list page, the "Download Now" link maps to the following method in the downloads controller:

```ruby
class DownloadsController < ApplicationController
  def show
    item = ProductType.find(params[:id])

    if current_user.downloads.include?(item)
      send_file "#{Rails.root}/#{item.downloadable.url(:default, false)}"
    else
      redirect_to(root_url, :notice => "You do not have access to this content.")
    end
  end
end
```

Note that there is additional verification here to check if the current user's downloads includes the download requested. The .url(:default, false) bit hides paperclip's cache buster (e.g. "?123456789") from the url in order to send the file.

### Conclusion

This straightforward code accomplished the  major updates required for download support: storing and sending the file, enforcing login, and handling shipping. In some cases, download support functionality may be more advanced, but the elements described here make up the most basic building blocks.

If you are interested in this project, check out these related articles:

- [Introducing Piggybak: A Mountable Ruby on Rails Ecommerce Engine](/blog/2012/01/06/piggybak-mountable-ecommerce-ruby-on)
- [ActiveRecord Callbacks for Order Processing in Ecommerce Applications](/blog/2012/01/13/activerecord-callbacks-ecommerce-order)
- [Importing into RailsAdmin: Part 1](/blog/2012/01/19/import-railsadmin)
- [Importing into RailsAdmin: Part 2](/blog/2012/02/01/railsadmin-import-part-2)
