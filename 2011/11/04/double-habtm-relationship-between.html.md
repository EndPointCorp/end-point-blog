---
author: Steph Skardal
gh_issue_number: 510
tags: ruby, rails
title: Double habtm Relationship Between Models
---

Oh, man! It's been a month since my last blog article. End Pointers Brian Buchalter, Evan Tann, Phunk, and I have been working on a sizable Ruby on Rails project for a client. We've been excited to work with Rails 3.1 and work on a project that presents many unique and interesting web application challenges.

Today I wanted to write about the fairly simple task of defining two has and belongs to many (or many to many) associations between the same models, which is something I haven't seen often in Rails applications.

### Data Model

<img border="0" height="162" src="/blog/2011/11/04/double-habtm-relationship-between/image-0.png" width="400"/>

First, let's look at the data model and discuss the business case for the data model. As shown above, the data model excerpt contains four tables. Users is the standard users table, which uses [devise](https://github.com/plataformatec/devise) for user authentication. Groups are intended to be a group of users that will be allowed to *do some combination of controller#action* in our application. In our case, groups have many members (or users), but they also have many owners, who are allowed to manage the group. And obviously on the user side, users can exist as a member or an owner in many groups.

### The Code

The groups_users relationship is a standard has and belongs to many relationship. The User class defines its relationship to groups:

```ruby
class User < ActiveRecord::Base
  ....
  has_and_belongs_to_many :groups
  ...
end
```

And the Group class defines it's relationship to users:

```ruby
class Group < ActiveRecord::Base
  ...
  has_and_belongs_to_many :users
  ...
end
```

Rails makes it fairly easy to define has_and_belongs_to_many associations and override the join table, class name, and foreign key, which is applicable to the groups_owners relationship. Here, the User class defines it's relationship to owned_groups, and specifies the join_table, class name, and foreign key:

```ruby
class User < ActiveRecord::Base
  ....
  has_and_belongs_to_many :owned_groups, :class_name => "Group", :join_table => "groups_owners", :foreign_key => "owner_id"
  ...
end
```

And the Group model has similar overrides (except in this case, we override the association foreign key):

```ruby
class Group < ActiveRecord::Base
  ..
  has_and_belongs_to_many :owners, :association_foreign_key => "owner_id", :join_table => "groups_owners", :class_name => "User"
  ..
end
```

And that's how to define the has and belong to many relationship between two of the same models! Obviously in our case, we can easily call and modify these associations, by calling some_user.groups, some_user.owned_groups, some_group.owners, and some_group.users.

### Extras

Here I've also created a couple of instance methods on the Group and User model to make it easy to pull the aggregate of owners and users (Group) and owned_groups and groups (User):

```ruby
class User < ActiveRecord::Base
  ...
  def all_groups
    (self.groups + self.owned_groups).uniq
  end
  ...
end
```

And:

```ruby
class Group < ActiveRecord::Base
  ...
  def all_members
    (self.owners + self.users).uniq
  end
  ...
end
```

Performance techniques such as calling raw SQL or with Rails low-level caching can potentially be applied to these methods, since I would not expect them to be highly performing as they are shown above. Examples of raw SQL and Rails low-level caching are described [here](http://blog.endpoint.com/2011/09/ruby-on-rails-performance-overview.html)!
