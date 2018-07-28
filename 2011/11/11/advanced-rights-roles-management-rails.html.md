---
author: Steph Skardal
gh_issue_number: 512
tags: ruby, rails
title: Advanced Rights and Roles Management in Rails
---

I’ve been working with Phunk, Brian Buchalter, and Evan Tann on a large Rails 3.1 project that has included several unique challenges. One of these challenges is a complex rights, roles, and accessibility system, which I’ll discuss here.

Before I wrote any code, I researched existing authorization systems, and came across [this article](http://steffenbartsch.com/blog/2008/08/rails-authorization-plugins/) which lists a few of the popular authorization gems in Rails. After reading through the documentation on several more advanced current authorization gems, I found that no gem offered the level of complexity we needed, where rights are layered on top of roles and can be mapped out to specific actions. Because the client and my team were most familiar with [acl9](https://github.com/be9/acl9), we chose to work with it and layer rights on top of the existing access control subsystem. Here’s a look at the data model we were looking for:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2011/11/11/advanced-rights-roles-management-rails/image-0-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2011/11/11/advanced-rights-roles-management-rails/image-0.png" width="730"/></a></div>

The data model shows a has_and_belongs_to_many (or many-to-many) relationship between users and roles, and roles and rights. Things are an example model, which belong_to users. Rights map out to methods in the controller that can be performed on thing instances.

### Implementation

Starting from the admin interface, a set of rights can be assigned to a role, a standard has_and_belongs_to_many relationship:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2011/11/11/advanced-rights-roles-management-rails/image-1-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2011/11/11/advanced-rights-roles-management-rails/image-1.png"/></a></div>

The admin interface includes ability to assign roles to users, another has_and_belongs_to_many relationship:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2011/11/11/advanced-rights-roles-management-rails/image-2-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2011/11/11/advanced-rights-roles-management-rails/image-2.png"/></a></div>

And the user model has an instance method to determine if the user’s rights include the current method or right:

```ruby
class User < ActiveRecord::Base
  ...
  def can_do_method?(method)
    self.rights.detect { |r| r.name == method }
  end
  ...
end
```

At the controller level without abstraction, we use the access control system to determine if the user has the ability to do that particular action, by including a conditional on the rule. Note that in these examples, the user also must be logged in, which is connected to the application’s authentication system ([devise](https://github.com/plataformatec/devise)).

```ruby
class ThingsController < ApplicationController
  ...
  access_control do
    allow logged_in, :to => :example_right1, :if => :allow_example_right1?
    allow logged_in, :to => :example_right2, :if => :allow_example_right2?
    allow logged_in, :to => :example_right3, :if => :allow_example_right3?
  end

  def allow_example_right1?
    current_user.can_do_method?("example_right1")
  end
  def example_right1
    # actual method on Thing instance
  end
  def allow_example_right2?
    current_user.can_do_method?("example_right2")
  end
  def example_right2
    # actual method on Thing instance
  end
  def allow_example_right3?
    current_user.can_do_method?("example_right3")
  end
  def example_right3
    # actual method on Thing instance
  end
  ...
end
```

The controller is simplified with the following abstraction. The access control statements do not need to be modified for each new potential method/right, but the method itself must be defined.

```ruby
class ThingsController < ApplicationController
  ...
  access_control do
    allow logged_in, :to => :generic_method, :if => :allow_generic_method?
  end

  def allow_generic_method?
    current_user.can_do_method?(params[:method])
  end
  def generic_method
    self.send(params[:method])
  end

  def example_right1
    # actual method on Thing instance
  end
  def example_right2
    # actual method on Thing instance
  end
  def example_right3
    # actual method on Thing instance
  end
  ...
end
```

And don’t forget the handler for Acl9::AccessDenied exceptions, inside the ApplicationController, which handles both JSON and HTML responses:

```ruby
class ApplicationController < ActionController::Base
  ...
  # Rescuing from any Access denied messages, generic JSON response or redirect and flash message
  rescue_from Acl9::AccessDenied do |exception|
    respond_to do |format|
      format.json do
        render :json => { :success => false, :message => "You do not have access to do this action." }
      end
      format.html do
        flash[:error] = 'You do not have access to view this page.'
        redirect_to root_url
      end
    end
  end
end
```

### Conclusion

Note that in actuality, our application has additional complexities, such as:

- The relationship between rights and $subject is polymorphic, where $subject is a user or a role. This slightly complicates the has_and_belongs_to_many relationship between rights and users or roles. The can_do_method? predicate is updated to consider both user assigned rights and role assigned rights.
- Performance is a consideration in this application, so Rails low-level caching may be leveraged to minimize accessibility lookup.
- There is a notion of a global right and an ownership-level right, which means that a user with an ownership-level right may have the ability to do certain method only if they own the thing. A user with a global right has the ability to do the method regardless of ownership. This complicates our can_do_method? predicate further, to determine if the user has the global right or ownership-level right for that method on that thing.
- A few methods have more complex business logic which determine whether or not a user has the ability to do that method. In those cases, an additional access_control allow rule is created, and distinct conditional predicate is used to determine if the user can do that method (i.e. allow_generic_method? is not used for these actions).

Other than the additional complexities, leveraging acl9’s access control subsystem makes for a clean rights and roles management solution. Stay tuned for a follow-up article on leveraging this data model in combination with Rails’ attr_accessible functionality to create elegant server-side validation.
