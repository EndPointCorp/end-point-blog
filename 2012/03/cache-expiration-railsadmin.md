---
author: Steph Skardal
title: A Cache Expiration Strategy in RailsAdmin
github_issue_number: 570
tags:
- rails
date: 2012-03-16
---



I’ve been blogging about [RailsAdmin](https://github.com/sferik/rails_admin) a lot lately. You might think that I think it’s the best thing since sliced bread. It’s a great configurable administrative interface compatible with Ruby on Rails 3. It provides a configurable architecture for CRUD (create, update, delete, view) management of resources with many additional user-friendly features like search, pagination, and a flexible navigation. It integrates nicely with [CanCan](https://github.com/ryanb/cancan), an authorization library. RailsAdmin also allows you to introduce custom actions such as [import](/blog/2012/02/railsadmin-import-part-2), and [approving items](/blog/2012/03/railsadmin-custom-action-case-study).

Whenever you are working with a gem that introduces admin functionality (RailsAdmin, [ActiveAdmin](https://activeadmin.info/), etc.), the controllers that provide resource management do not live in your code base. In Rails, typically you will see cache expirations in the controller that provides the CRUD functionality. For example, in the code below, a PagesController will specify [caching and sweeping](https://apidock.com/rails/ActionController/Caching/Sweeping) of the page which expires when a page is updated or destroyed:

```ruby
class PagesController < AdminController
  caches_action :index, :show
  cache_sweeper :page_sweeper, :only => [ :update, :destroy ]

  ...
end
```

While working with RailsAdmin, I’ve come up with a different solution for expiring caches without extending the RailsAdmin functionality. Here are a couple of examples:

### Page Caching

On the front-end, I have standard full page caching on static pages. In this case, the config/routes.rb maps wildcard paths to the pages controller and show action.

```ruby
match '*path' => 'pages#show'
```

The controller calls the standard caches_page method:

```ruby
class PagesController < ApplicationController
  caches_page :show

  def show
    @page = Page.find_by_slug(params[:path])
    
    ...
  end
end
```

A simple ActiveRecord callback is added to clear the page cache:

```ruby
class Page < ActiveRecord::Base
  ...

  after_update :clear_cache

  def clear_cache
    ActionController::Base.expire_page("/#{self.slug}")
  end
end
```

### Fragment Caching

When a page can’t be fully cached, I might cache a view shared across the application. In the example below, the shared view is included in the layout—​it’s generated dynamically but the data does not change often, which makes it suitable for fragment caching.

```ruby
<% cache "navigation" do -%>
  <% Category.each do |category| -%>
    <%= link_to category.name, category_url(category) %>
  <% end -%>
<% end -%>
```

Inside the model, I add the following to clear the fragment cache when a category is created, updated, or destroyed:

```ruby
class Category < ActiveRecord::Base
  after_create :clear_cache
  after_update :clear_cache
  before_destroy :clear_cache

  def clear_cache
    ActionController::Base.new.expire_fragment("navigation")
  end
end
```

### Conclusion

One thing that’s noteworthy is that expire_page requires a class method on ActionController::Base while expire_fragment requires an instance method (see [here](https://github.com/rails/rails/blob/5284e650be321273a2bb68bf4baa8adeb6bc586b/actionpack/lib/action_controller/caching/pages.rb) versus [here](https://github.com/rails/rails/blob/5284e650be321273a2bb68bf4baa8adeb6bc586b/actionpack/lib/action_controller/caching/fragments.rb)). Action cache expiration with ActiveRecord callbacks should work similarly with action caching, as a class method ([reference](https://github.com/rails/rails/blob/5284e650be321273a2bb68bf4baa8adeb6bc586b/actionpack/lib/action_controller/caching/actions.rb)).

An alternative approach here would be to extend the [generic RailsAdmin admin controller](https://github.com/sferik/rails_admin/blob/master/app/controllers/rails_admin/main_controller.rb) to introduce a generic sweeper. However, the sweeper would have to determine what model was modified and what to expire it. This can be implemented and abstracted elegantly, but in my application I preferred to use simple ActiveRecord callbacks because the caching was limited to a small number of models.


