---
author: Steph Skardal
gh_issue_number: 622
tags: rails
title: 'Devise on Rails: Prepopulating Form Data'
---



I recently had a unique (but reasonable) request from a client: after an anonymous/guest user had completed checkout, they requested that a "Create Account" link be shown on the receipt page which would prepopulate the user form data with the user's checkout billing address. Their application is running on Ruby on Rails 3.2 and uses [devise](https://github.com/plataformatec/devise). Devise is a user authentication gem that's popular in the Rails community.

<img border="0" height="216" src="/blog/2012/06/08/devise-on-rails-prepopulating-form-data/image-0.png" width="400"/>
A customer request was to include a link on the receipt page that would
 autopopulate the user create account form with checkout data.

Because devise is a Rails engine (self-contained Rails functionality), the source code is not included in the main application code repository. While using [bundler](http://gembundler.com/), the version information for devise is stored in the application's Gemfile.lock, and the engine source code is stored depending on bundler configuration. Because the source code does not live in the main application, modifying the behavior of the engine is not quite as simple as editing the source code. My goal here was to find an elegant solution to **hook** into the devise registration controller to set the user parameters.

### ActiveSupport::Concern

To start off, I set up a devise_registrations_controller_decorator.rb module in my application lib/ directory which extends [ActiveSupport::Concern](http://www.fakingfantastic.com/2010/09/20/concerning-yourself-with-active-support-concern/), shown below. ActiveSupport::Concern is a tool to elegantly extend or override core models and controllers. In this case, Devise::RegistrationsController was set up to be **decorated**.

```ruby
module DeviseRegistrationsControllerDecorator
  extend ActiveSupport::Concern
end

Devise::RegistrationsController.send(:include, DeviseRegistrationsControllerDecorator)
```

### Adding an InstanceMethods method

Next, I added a custom_new method that took into account a parameter that would be passed in the url (with_user=1). If this parameter exists and the user has a recent order stored in their session, the recent order is referenced to set the resource (User instance) values:

```ruby
module DeviseRegistrationsControllerDecorator
  extend ActiveSupport::Concern

  module InstanceMethods
    def custom_new
      resource = build_resource({})
      if params.has_key?(:with_user) &amp;&amp; session.has_key?(:last_order)
        last_order = Piggybak::Order.find(session[:last_order])
        resource.email = last_order.email
        resource.phone = last_order.phone
        [:firstname, :lastname, :address1, :address2, :institution, :city, :state_id, :zip, :country_id].each do |field|
          resource.send("#{field}=", last_order.billing_address.send("#{field}"))
        end
      end
      respond_with resource
    end
  end
end

Devise::RegistrationsController.send(:include, DeviseRegistrationsControllerDecorator)
```

### Alias and Redefinition

Finally, I updated the module so that when it was included, an alias for the core new method, and an override of the core new method with the custom_new method:

```ruby
module DeviseRegistrationsControllerDecorator
  extend ActiveSupport::Concern

  included do
    alias :devise_new :new
    def new; custom_new; end
  end

  module InstanceMethods
    def custom_new
      ...
    end
  end
end

Devise::RegistrationsController.send(:include, DeviseRegistrationsControllerDecorator)
```

### config/environments/development.rb

Because classes are not cached in development, and library modules are not automatically reloaded, I added the following call to config/environments/development.rb to force a reload of the module to ensure that the devise controller would always be extended:

```ruby
config.to_prepare do
  Devise::RegistrationsController.send(:include, DeviseRegistrationsControllerDecorator)
end
```

### Conclusion

In this case, ActiveSupport::Concern was used to easily override the core devise method without requiring hacking at the source code. One disadvantage to this implementation is that if significant changes are made to the core method, those changes also need to be applied to the custom controller if necessary.

<img border="0" src="/blog/2012/06/08/devise-on-rails-prepopulating-form-data/image-1.png" width="600"/>
Autopopulate success!


