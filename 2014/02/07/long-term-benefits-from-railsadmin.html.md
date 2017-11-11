---
author: Steph Skardal
gh_issue_number: 923
tags: rails
title: Long-term Benefits from RailsAdmin
---



Sometimes setting up an admin tool with user authorization at the onset of a new Rails project can take a bit of work, and it's not until later that long-term benefits of this framework can be realized. This came up recently when I was asked to write an export method to allow website admins to export customer and order data (for a specific date range) on a platform that was already using [RailsAdmin](https://github.com/sferik/rails_admin) in combination with [CanCan](https://github.com/ryanb/cancan) for user authorization.

A normal Rails development process for this (from scratch) might look like this:

1. Create controller.
1. Create route to map to controller. 
1. Create method in controller to render initial view and send data.
1. Create view which allows user to select date range.
1. Add user authorization to allow specific users to access functionality.

This isn't that much work, but here's how the same functionality was built using RailsAdmin:

### RailsAdmin Action

First, I create Rails Admin action, which inherits from RailsAdmin::Config::Actions. Inheriting from RailsAdmin::Config::Actions includes many class methods such as defining the actions http_methods (get, post, etc.), defining if the action is applicable to a single instance or a set of instances (which influences whether the action shows as a tab or individual item listings), and defining the icon that a user will see in the admin for this action. This bit of code also contains the controller method. In my case, this includes this method checks if the request is a get or post to determine whether to render the view or send the exported data. Here's what the code looks like:

```ruby
module RailsAdmin
  module Config
    module Actions
      class SpecialExport < RailsAdmin::Config::Actions::Base
        register_instance_option :collection do
          true
        end

        register_instance_option :http_methods do
          [:get, :post]
        end

        register_instance_option :controller do
          Proc.new do
            if request.post?
              # generate CSV data
              send_data csv_data, :filename => "export.csv", :type => "application/csv"
            end
            # renders view otherwise
          end
        end
        register_instance_option :link_icon do
          'icon-share'
        end
      end
    end
  end
end
```

### Register Action

Next, I register and activate the action in the RailsAdmin configuration. Here's what this looks like:

```ruby
module RailsAdmin
  module Config
    module Actions
      class SpecialExport < RailsAdmin::Config::Actions::Base
        RailsAdmin::Config::Actions.register(self)
      end
    end
  end
end
RailsAdmin.config do |config|
  config.actions do
    # existing actions
    special_export
  end
end
```

### CanCan Modifications

Next up, I modify [CanCan's abilities](https://github.com/ryanb/cancan#1-define-abilities) to specify that the action can be performed on a specific class, and not others. Here's what my code looks like for this:

```ruby
class Ability
  include CanCan::Ability
  def initialize(user)
    if user && user.is_admin?
      #existing user authentication
      
      cannot :special_export, :all
      can :special_export, Order
    end
  end
end
```

### Create view

After the above steps, I create a view to allow the user to select a date range. This is fairly simple, and uses the already included jQuery UI date select functionality for the calendar UI.

### Conclusion

Although line for line, the amount of code in the latter code infrastructure with RailsAdmin may be about the same to the former option, the API for hooking custom functionality into RailsAdmin is a win in terms of inherited functionality and maintenance. My "Special Export" method shows as a tab that can be performed on Orders only in the admin, and I wrote very little code for that specific behavior. Another maintenance gain here is that my custom methods are all consistent, which makes it easier for another developer to jump in and make changes, especially someone who is already familiar with RailsAdmin.

<img border="0" src="/blog/2014/02/07/long-term-benefits-from-railsadmin/image-0.png"/>
Example "Special Export" tab in RailsAdmin interface.

I'm not married to RailsAdmin in particular, but it happens to be a tool I've become familiar with and it integrates well with existing user authorization and user authentication tools. But I do always make a suggestion to use an existing Admin interface in new Rails applications, whether it's RailsAdmin, ActiveAdmin, or another. These tools have a great foundation and have settled on a consistent API that encourage efficient customization and maintenance.


