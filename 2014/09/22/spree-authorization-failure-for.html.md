---
author: Matt Galvin
gh_issue_number: 1034
tags: ruby, rails, spree
title: Spree Authorization Failure for Customized Role
---



Hello again all. Recently I was working on another Spree site running Spree 2.1.1. The client wanted to create some custom roles. For example, the client wanted there to be a Sales Manager role. A Sales Manager could log in and have read and write access to all the orders. However, a sales manager should not have read/write access to products, configuration, promotions, users, etc. This was easily accomplished by following the steps in the [Spree documentation](https://guides.spreecommerce.org/developer/security.html). As I will describe, this documentation assumes that the custom role will have access to Orders#index.

The client wanted to create a second custom role that had create, read, update and delete access to the Training model and nothing more. The training model belongs to a taxon and has a unique event date and taxon id. An example would be a training instance with an event date of September 9th, 2014 that belongs to a taxon with the name “Fire Safety 101” and a description “Teaching fire safety in accordance with OSHA standards. 10 hours and lunch is provided”. So, I planned to create a training personnel role that should be able to log in and *only* have read/write access to Trainings. However, the Spree documentation did not provide an explanation on how to create a custom role that does not have read or write access to orders.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/09/22/spree-authorization-failure-for/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/09/22/spree-authorization-failure-for/image-0.png"/></a></div>

 

Following the pattern described in the [Spree documentation](https://guides.spreecommerce.org/developer/security.html) for creating custom roles and their respective authorization, I created an ability_decorator.rb with the contents:

```ruby
class AbilityDecorator
     include CanCan::Ability
     def initialize(user)
       if user.respond_to?(:has_spree_role?) && user.has_spree_role?('sales_manager')
         can [:admin, :index, :show], Spree::Order
       end
       if user.respond_to?(:has_spree_role?) && user.has_spree_role?('training')
         can [:admin, :manage], Spree::Training
       end
     end
   end
 
   Spree::Ability.register_ability(AbilityDecorator)
```

However, after creating a training user and attempting to log in, I got an unauthorized error. So, I checked the logs:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/09/22/spree-authorization-failure-for/image-1.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/09/22/spree-authorization-failure-for/image-1.png"/></a></div>

The log output above shows that while I was logged in as a user with the training role, the application was checking for authorization on Spree::Admin::OrdersController#index (the orders list page), because the base admin URL ("/admin") points to this controller action. I reviewed the [Devise documentation](http://rdoc.info/github/plataformatec/devise/master/Devise/Controllers/Helpers:after_sign_in_path_for) to modify where a user with the training role is redirected to upon login (via [Spree Auth Devise’s after_sign_in method](https://github.com/spree/spree_auth_devise)), as shown in the code shown below.

```ruby
def after_sign_in_path_for(resource)
    stored_location_for(resource) ||
      if resource.is_a?(Spree::User) && resource.has_spree_role?('training')
        admin_trainings_path
      else
        super
      end
  end
```

After making this change, I tried once again and was able to successfully log in as a training user and *only* have the desired access to Trainings. 

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/09/22/spree-authorization-failure-for/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/09/22/spree-authorization-failure-for/image-2.png"/></a></div>

 

To summarize, if you’d like to have a custom role and *not* give them access to Orders, you will need to make some adjustments outside the steps listed in Spree’s documentation for custom role authorization.


