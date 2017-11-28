---
author: Steph Skardal
gh_issue_number: 424
tags: ecommerce, rails, spree
title: A Ruby on Rails Tag Cloud Tutorial with Spree
---

<a href="/blog/2011/02/02/in-our-own-words"><img border="0" src="/blog/2011/03/07/rails-tag-cloud-tutorial-spree/image-0.png" width="754px"/></a>

A tag cloud from a recent End Point blog post.

Tag clouds have become a fairly popular way to present data on the web. One of our Spree clients recently asked End Point to develop a tag cloud reporting user-submitted search terms in his Spree application. The steps described in this article can be applied to a generic Rails application with a few adjustments.

### Step 1: Determine Organization

If you are running this as an extension on Spree pre-Rails 3.0 versions, you'll create an extension to house the custom code. If you are running this as part of a Rails 3.0 application or Spree Rails 3.0 versions, you'll want to consider creating a custom gem to house the custom code. In my case, I'm writing a Spree extension for an application running on Spree 0.11, so I create an extension with the command script/generate extension SearchTag.

### Step 2: Data Model & Migration

First, the desired data model for the tag cloud data should be defined. Here's what mine will look like in this tutorial:

<a href="/blog/2011/03/07/rails-tag-cloud-tutorial-spree/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5581403495920932162" src="/blog/2011/03/07/rails-tag-cloud-tutorial-spree/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 167px; height: 113px;"/></a>

Next, a model and migration must be created to introduce the class, table and it's fields. In Spree, I run script/generate extension_model SearchTag SearchRecord and update the migration file to contain the following:

```ruby
class CreateSearchRecords < ActiveRecord::Migration
  def self.up
    create_table :search_records do |t|
      t.string :term
      t.integer :count, :null => false, :default => 0
    end
  end

  def self.down
    drop_table :search_records
  end
end
```

I also add a filter method to my model to be used later:

```ruby
class SearchRecord < ActiveRecord::Base
  def self.filter(term)
    term.gsub(/\+/, ' ')
      .gsub(/\s+/, ' ')
      .gsub(/^\s+/, '')
      .gsub(/\s+$/, '')
      .downcase
      .gsub(/[^0-9a-z\s-]/, '')
  end
end
```

### Step 3: Populating the Data

After the migration has been applied, I'll need to update the code to populate the data. I'm going to add an after filter on every user search. In the case of using Spree, I update search_tag_extension.rb to contain the following:

```ruby
def activate
  Spree::ProductsController.send(:include, Spree::SearchTagCloud::ProductsController)
end
```

And my custom module contains the following:

```ruby
module Spree::SearchTagCloud::ProductsController
  def self.included(controller)
    controller.class_eval do
      controller.append_after_filter :record_search, :only => :index
    end
  end

  def record_search
    if params[:keywords]
      term = SearchRecord.filter(params[:keywords])
      return if term == ''
      record = SearchRecord.find_or_initialize_by_term(term)
      record.update_attribute(:count, record.count+1)
    end
  end
end
```

The module appends an after filter to the products#index action. The after filter method cleans the search term and creates a record or increments the existing record's count. If this is added directly into an existing Rails application, this bit of functionality may be added directly into one or more existing controller methods to record the search term.

### Step 4: Reporting the Data

To present the data, I create a controller with script/generate extension_controller SearchTag Admin::SearchTagClouds first. I update config/routes.rb with a new action to reference the new controller:

```ruby
map.namespace :admin do |admin|
  admin.resources :search_tag_clouds, :only => [:index]
end
```

And I update my controller to calculate the search tag cloud data, shown below. The index method method retrieves all of the search records, sorts, and grabs the the top x results, where x is some configuration defined by the administrator. The method determines the linear solution for scaling the search_record.count to font sizes ranging from 8 pixels to 25 pixels. This order of terms is randomized ([.shuffle](http://www.ruby-doc.org/core/classes/Array.html#M000284)) and linear equation applied. This linear shift can be applied to different types of data. For example, if a tag cloud is to show products with a certain tag, the totals per tag must be calculated and scaled linearly.

```ruby
class Admin::SearchTagCloudsController < Admin::BaseController
  def index
    search_records = SearchRecord.all
      .collect { |r| [r.count, r.term] }
      .sort
      .reverse[0..Spree::SearchTagCloud::Config[:count]]
    max = search_records.empty? ? 1 : search_records.first.first

    # solution is: a*x_factor - y_shift = font size
    # max font size is 25, min is 8
    x_factor = (Spree::SearchTagCloud::Config[:max] -
      Spree::SearchTagCloud::Config[:min]) / max.to_f
    y_shift = max.to_f*x_factor - Spree::SearchTagCloud::Config[:max]

    @results = search_records.shuffle.inject([]) do |a, b|
      a.push([b[0].to_f*x_factor - y_shift, b[1]])
      a
    end
  end
end
```

The data is presented to the user in the following view:

```nohighlight
<h3>Tag Cloud:</h3>
<div id="tag_cloud">
<% @results.each do |b| %>
<span style="font-size:<%= b[0] %>px;"><%= b[1] %></span>
<% end -%>
</div>
```

### Step 5: Adding Flexibility

In this project, I added configuration variables for the total number of terms displayed, and maximum and minimum font size using Spree's preference architecture. In a generic Rails application, this may be a nice bit of functionality to include with the preferred configuration architecture.

<a href="/blog/2011/03/07/rails-tag-cloud-tutorial-spree/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5581403499162521858" src="/blog/2011/03/07/rails-tag-cloud-tutorial-spree/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 327px; height: 132px;"/></a>

Example tag cloud from the extension.
Additional modifications can be applied to change the
overall styling or color of individual search terms.

### Conclusion

These steps are pretty common for introducing new functionality into an existing application: data migration and model, manipulation on existing controllers, and presentation of results with a new or existing controller and view. Following MVC convention in Rails keeps the code organized and methods simple. In the case of Spree 0.11, this functionality has been packaged into a single extension that is abstracted from the Spree core. The code can be reviewed [here](https://github.com/stephskardal/spree-search-tag-cloud), with a few minor differences.
