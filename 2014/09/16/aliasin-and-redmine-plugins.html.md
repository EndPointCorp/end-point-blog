---
author: Miguel Alatorre
gh_issue_number: 1032
tags: extensions, ruby, rails
title: Aliasin' and Redmine plugins
---

Recently I was tasked with creating a plugin to customize End Point's Redmine instance.
In working through this I was exposed for the first time to alias_method_chain.
What follows is my journey down the rabbit hole as I wrap my head around new (to me) Ruby/Rails magic.

The Rails core method alias_method_chain encapsulates a common pattern of using alias_method twice: first to rename an original method to a method "without" a feature, and second to rename a new method "with" a feature to the original method. Whaaaa? Let's start by taking a look at Ruby core methods alias and alias_method before further discussing alias_method_chain.

### alias and alias_method

At first glance, they achieve the same goal with slightly different syntax:

```ruby
class Person
  def hello
    "Hello"
  end

  alias say_hello hello
end

Person.new.hello
=> "Hello"
Person.new.say_hello
=> "Hello"
```

```ruby
class Person
  def hello
    "Hello"
  end

  alias_method :say_hello, :hello
end

Person.new.hello
=> "Hello"
Person.new.say_hello
=> "Hello"
```

Let's see what happens when we have a class inherit from Person in each of the cases above.

```ruby
class Person
  def hello
    "Hello"
  end

  # Wrapped in a class function to examine scope
  def self.apply_alias
    alias say_hello hello
  end
  apply_alias
end

class FunnyPerson < Person
  def hello
    "Hello, I'm funny!"
  end
  apply_alias
end

FunnyPerson.new.hello
=> "Hello, I'm funny!"
FunnyPerson.new.say_hello
=> "Hello"
```

```ruby
class Person
  def hello
    "Hello"
  end

  # Wrapped in a class function to examine scope
  def self.apply_alias
    alias_method :say_hello, :hello
  end
  apply_alias
end

class FunnyPerson < Person
  def hello
    "Hello, I'm funny!"
  end
  apply_alias
end

FunnyPerson. new.hello
=> "Hello, I'm funny!"
FunnyPerson.new.say_hello
=> "Hello, I'm funny!"
```

Because alias is a Ruby keyword it is executed when the source code gets parsed which in our case is in
the scope of the Person class. Hence, say_hello will always be aliased to the hello method defined in Person.
Since alias_method is a method, it is executed at runtime which in our case is in the scope of the FunnyPerson
class.

### alias_method_chain

Suppose we want a child class to extend the hello method. We could do so with a couple of alias_method calls:

```ruby
class Person
  def hello
    "Hello"
  end
end

class PolitePerson < Person
  def hello_with_majesty
    "#{hello_without_majesty}, your majesty!"
  end

  alias_method :hello_without_majesty, :hello
  alias_method :hello, :hello_with_majesty
end

PolitePerson.new.hello
=> "Hello, your majesty!"
PolitePerson.new.hello_with_majesty
=> "Hello, your majesty!"
PolitePerson.new.hello_without_majesty
=> "Hello"
```

What we did above in PolitePerson can be simplified by replacing the two alias_method calls with just one call to alias_method_chain:

```ruby
class Person
  def hello
    "Hello"
  end
end

class PolitePerson < Person
  def hello_with_majesty
    "#{hello_without_majesty}, your majesty!"
  end

  alias_method_chain :hello, :majesty
end

class OverlyPolitePerson < Person
  def hello_with_honor
    "#{hello_without_humbling} I am honored by your presence!"
  end

  alias_method_chain :hello, :honor
end

PolitePerson.new.hello
=> "Hello, your majesty!"
OverlyPolitePerson.new.hello
=> "Hello, your majesty! I am honored by your presence!"
```

Neat! How does this play into Redmine plugins, you ask? Before we get into that there is one more thing to go over: a module's **included** method.

### The **included** callback

When a module is included into another class or module, Ruby invokes the **included** method if defined. You can think of it as a sort of module initializer:

```ruby
module Polite
  def self.included(base)
    puts "Polite has been included in class #{base}"
  end
end

class Person
  include Polite

  def hello
    "Hello"
  end
end
Polite has been included in class Person
=> Person
```

Now, what if you can't modify the Person class directly with the **include** line? No biggie. Let's just send Person a message to include our module:

```ruby
class Person
  def hello
    "Hello"
  end
end

module Polite
  def self.include(base)
    puts "Polite has been included in class #{base}"
  end

  def polite_hello
    "Hello, your majesty!"
  end
end

Person.send(:include, Polite)
Polite has been included in class Person
=> Person
```

What if we now want to extend Person's hello method? Easy peasy:

```ruby
class Person
  def hello
    "Hello"
  end
end

module Polite
  def self.included(base)
    base.send :include, InstanceMethods

    base.class_eval do
      alias_method_chain :hello, :politeness
    end
  end

  module InstanceMethods
    def hello_with_politeness
      "#{hello_without_politeness}, your majesty!"
    end
  end
end

Person.new.hello
=> "Hello"
Person.send :include, Polite
=> Person
Person.new.hello
=> "Hello, your majesty!"
```

How polite! Let's talk about what's going on in the Polite module. We defined our hello_with_politeness method inside an InstanceMethods module in order to not convolute the self.include method. In self.include we send an include call to the base class so that InstanceMethods is included.
This will allow our base class instances access to any method defined in InstanceMethods. Next, class_eval is used on the base class so that the alias_method_chain method is called within the context of the class.

### How this applies to Redmine

If you take a look at the Redmine plugin documentation, specifically [Extending the Redmine Core](http://www.redmine.org/projects/redmine/wiki/Plugin_Internals#Extending-the-Redmine-Core), you'll see the above pattern as the recommended method to overwrite/extend Redmine core functionality.
I'll include the RateUsersHelperPatch example from the documentation here so that you can see it compared with the above code blocks:

```ruby
module RateUsersHelperPatch
  def self.included(base) # :nodoc:
    base.send(:include, InstanceMethods)

    base.class_eval do
      unloadable # Send unloadable so it will not be unloaded in development

      alias_method_chain :user_settings_tabs, :rate_tab
    end
  end

  module InstanceMethods
    # Adds a rates tab to the user administration page
    def user_settings_tabs_with_rate_tab
      tabs = user_settings_tabs_without_rate_tab
      tabs << { :name => 'rates', :partial => 'users/rates', :label => :rate_label_rate_history}
      return tabs
    end
  end
end
```

Sending an include to RateUsersHelper can be done in the plugin's init.rb file:

```ruby
Rails.configuration.to_prepare do
  require 'rate_users_helper_patch'
  RateUsersHelper.send :include, RateUsersHelperPatch
end
```

So, the tabs variable is set using user_settings_tabs_without_rate_tab, which is aliased to the Redmine core user_settings_tabs method:

```ruby
# https://github.com/redmine/redmine/blob/2.5.2/app/helpers/users_helper.rb#L45-L53
def user_settings_tabs
  tabs = [{:name => 'general', :partial => 'users/general', :label => :label_general},
          {:name => 'memberships', :partial => 'users/memberships', :label => :label_project_plural}
          ]
  if Group.all.any?
    tabs.insert 1, {:name => 'groups', :partial => 'users/groups', :label => :label_group_plural}
  end
  tabs
end
```

Then, a new hash is added to tabs. Because method user_settings_tabs is now aliased to user_settings_tabs_with_rate_tab, the users/groups partial will be included when the call to render user_settings_tabs is executed:

```ruby
#https://github.com/redmine/redmine/blob/2.5.2/app/views/users/edit.html.erb#L9
<div class="contextual">
<%= link_to l(:label_profile), user_path(@user), :class => 'icon icon-user' %>
<%= change_status_link(@user) %>
<%= delete_link user_path(@user) if User.current != @user %>
</div>

<%= title [l(:label_user_plural), users_path], @user.login %>

<%= render_tabs user_settings_tabs %>
```

Although alias_method_chain is a pretty cool and very useful method, it's not without its shortcomings. There's a great, recent blog article about that [here](http://www.justinweiss.com/blog/2014/09/08/rails-5-module-number-prepend-and-the-end-of-alias-method-chain/) in which Ruby 2's Module#prepend as a better alternative to alias_method_chain is discussed as well.
