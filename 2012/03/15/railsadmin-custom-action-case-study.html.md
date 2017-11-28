---
author: Marina Lohova
gh_issue_number: 569
tags: rails
title: 'RailsAdmin: A Custom Action Case Study'
---



[RailsAdmin](https://github.com/sferik/rails_admin) is an awesome tool that can be efficiently used right out of box. It provides a handy admin interface, automatically scanning through all the models in the project and enhancing them with List, Create, Edit and  Delete actions. However, sometimes we need to create a custom action for a more specific feature.

### Creating The Custom Action

Here we will create an "Approve Review" action, that the admin will use to moderate user reviews. First, we need to create an action class rails_admin_approve_review.rb in Rails::Config::Actions namespace and place it in the "#{Rails.root}/lib" folder. Here is the template for it:

```ruby
require 'rails_admin/config/actions'
require 'rails_admin/config/actions/base'

module RailsAdminApproveReview
end

module RailsAdmin
  module Config
    module Actions
      class ApproveReview < RailsAdmin::Config::Actions::Base
      end
    end
  end
end
```

By default, all actions are present for all models. We will only show the "Approve" action for the models that actually support it and are yet unapproved. It means that they have *approved* attribute defined and set to *false*:
```ruby
register_instance_option :visible? do
  authorized? && !bindings[:object].approved
end
```
RailsAdmin has a lot of configuration options. We will use one of them to specify that the action acts on the object (member) scope:
```ruby
register_instance_option :member? do
  true
end
```
We will also specify a css class for the action (from a grid of icons), so the link will display a little checkmark icon:
```ruby
register_instance_option :link_icon do
  'icon-check'
end
```
Now, this is what I call "customized"!

The last step is, perhaps, the most important, because it actually processes the action. In this case, the action sets the *approved* attribute to *true* for the object. The code needs to be placed into the controller context. To do so we wrap it in the following block:

```ruby
register_instance_option :controller do
  Proc.new do
    @object.update_attribute(:approved, true)
    flash[:notice] = "You have approved the review titled: #{@object.title}."

    redirect_to back_or_index
  end
end
```

### Integrating the Custom Action Into RailsAdmin

The action is ready, now it is time to plug it in RailsAdmin. This includes two steps.

First, it should be registered with RailsAdmin::Config::Actions like this:

```ruby
module RailsAdmin
  module Config
    module Actions
      class ApproveReview < RailsAdmin::Config::Actions::Base
        RailsAdmin::Config::Actions.register(self)
      end
    end
  end
end
```

This code was placed into config/initializers/rails_admin.rb to avoid the loading issue, that occurred because RailsAdmin config was loaded first and custom action class was not present yet. Next, the custom action needs to be listed in the actions config in config/initializers/rails_admin.rb:

```ruby
RailsAdmin.config do |config|
  config.actions do
    dashboard
    index
    new

    approve_review

    show
    edit
    delete
  end
end
```

If your application is using [CanCan](https://github.com/ryanb/cancan) with RailsAdmin, you also need to authorize the approve_review action:

```ruby
class Ability
  include CanCan::Ability
  def initialize(user)
    if user && user.is_admin?
      ...
      cannot :approve_review, :all
      can :approve_review, [UserReview]
    end
  end
end
```

Full custom action can be viewed [here](https://gist.github.com/2039001)

### Additional Notes

[RailsAdmin has a nice script](https://github.com/sferik/rails_admin/wiki/Custom-action) that can be used for generating custom actions as external gems (engines). In the case of this blog article, the approve_review was integrated directly into the Rails application. RailsAdmin action configuration options can be found [here](https://github.com/sferik/rails_admin/blob/master/lib/rails_admin/config/actions/base.rb).

End Point has been using RailsAdmin for an ecommerce project that uses [Piggybak](http://www.piggybak.org/). Here are a few related articles:

- [RailsAdmin and Import functionality](/blog/2012/02/01/railsadmin-import-part-2)
- [Piggybak: A Mountable Ruby on Rails Ecommerce Engine](/blog/2012/01/06/piggybak-mountable-ecommerce-ruby-on)
- [RailsAdmin in ecommerce](/blog/2011/08/09/railsadmin-gem-ecommerce)


