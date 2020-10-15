---
author: Steph Skardal
gh_issue_number: 537
tags: rails
title: 'Ruby on Rails: Attributes Management through Rights'
---

I’ve written a couple times about a large Rails project that a few End Pointers have been working on. The system has a fairly robust system for managing rights and access. The basic data model for rights, users, groups, and roles is this:

<img border="0" height="337" src="/blog/2012/01/05/ruby-on-rails-rights-attributes/image-0.png" width="737"/>

In this data model, right_assignments belong to a single right, and belong to a subject, through a polymorphic relationship. The subject can be a Role, Group, or User. A User can have a role or belong to a group. This allows for the ability to assign a right to a user directly or through a group or role.

In our code, there is a simple method for grabbing a user’s set of rights:

```ruby
  class User < ActiveRecord::Base
    ...
    def all_rights
      rights = [self.rights +
                self.groups.collect { |g| g.allowed_rights } +
                self.roles.collect { |r| r.rights }]
      rights = rights.flatten.uniq.collect { |r| r.action }

      rights
    end
    ...
  end
```

In the case of this data model, groups also have a boolean which specifies whether or not rights can be assigned to them. The allowed_rights method looks like this:

```ruby
  class Group < ActiveRecord::Base
    ...
    def allowed_rights
      self.assignable_rights ? self.rights : []
    end
    ...
  end
```

This additional layer of protection on the group rights is because groups represent a collection of users that have implied behavior attached to them (different from roles). A group may or may not have rights assigned only through a user with the ability to assign rights to groups.

The interesting part of this application is how the rights are used. In Rails, you can define the accessible attributes for an object on the fly. In our code, rights may translate to attributes that can be updated. For example, the following [extremely simplified] example demonstrates this:

```ruby
  # controller
  def update # or create
    if @item.custom_save(params)
      # saved
    else
      # handle errors
    end
  end

  # Given an item, with attributes title, description, tags, origin
  class Item < ActiveRecord::Base
    ...
    def custom_save(parameters)
      self.accessible = self.attr_accessible_for(current_user)

      item.update_attributes(parameters)
    end

    def attr_accessible_for(user)
      attrs = [:title, :description]  # Defaults

      [:tags, :origin].each do |field|
        # check for if user can_set_(tags || origin)
        if current_user.all_rights.include?("can_set_#{field.to_s}")
          attrs << field
        end
      end

      attrs
    end
    ...
  end
```

The above block updates an existing item. The default accessible attributes are title and description, which means that anyone can set those values. Tags and origin can only be set if the user has the right that correspond to that attribute. Tags and origin will not be saved for a user without those rights, even if they are passed in the parameters. The obvious disadvantage with this method is that there’s no exception handling when a user tries to submit parameters that they cannot set.

The method above is reused to define which fields are editable to the current user, with the code shown below. So in theory, a user submitting parameters that they can’t edit would only be doing it through a [malicious] post not based on the view below.



```ruby
  # controller
  def new
    @item = Item.new

    @accessible = attr_accessible_for(current_user)
  end

  # view
  <%= form_for @item do |f| %>
    <% [:title, :description, :tag, :origin].each do |field| %>
      <%= f.label field %>

      <% if @accessible.include?(field) %>
        <%= f.text_field %>
      <% else -%>
        <%= @item.send(field) %>
      <% end -%>

    <% end -%>
  <% end -%>
```

The data model and rights management described in this article isn’t novel, but applying it in this fashion is elegant and produces modular and reusable methods. The code shown here has been simplified for this blog post. In reality, there are a few additional complexities:

- The application utilizes [acl9](https://github.com/be9/acl9) for access control, which is an additional layer of security that will prevent non-registered users from creating items, and will prohibit specific users from updating existing items.
- The user’s all_rights method utilizes Rails low-level caching, with appropriate cache invalidation when the user’s rights, groups, or roles change. I’ve given a simple example of Rails low-level caching [in this blog article](/blog/2011/09/06/ruby-on-rails-performance-overview).
- The logic in attr_accessible_for is more complex and can be based on the object’s values or parameters. For example, an item may have a boolean that indicates anyone can tag it. The attr_accessible_for method will incorporate additional logic to determine if the :tags field is editable.
- The view handles different field types (checkbox, textarea, etc) and allows for overriding the field label.

Here are several articles related to the same large Ruby on Rails project, for your reading pleasure:

- [Working with Solr Results in Rails](/blog/2011/12/12/sunspot-solr-rails-working-with-results)
- [Performing Bulk Edits in Rails: Part 1](/blog/2011/11/14/performing-bulk-edits-in-rails-part-1)
- [Performing Bulk Edits in Rails: Part 2](/blog/2011/12/03/performing-bulk-edits-in-rails-part-2)
- [Advanced Rights and Role Management in Rails](/blog/2011/11/11/advanced-rights-roles-management-rails)
- [Double Has and Belongs to Many Relationship in Rails](/blog/2011/11/04/double-habtm-relationship-between)
