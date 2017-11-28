---
author: Steph Skardal
gh_issue_number: 318
tags: conference, ecommerce, ruby, rails, spree
title: 'Rails 3 at RailsConf 2010: Code Goodness'
---

At RailsConf 2010, popular technical topics this year are Rails 3 and NoSQL technologies. My first two articles on RailsConf 2010 so far ([here](/blog/2010/06/09/railsconf-2010-ecommerce-smackdown) and [here](/blog/2010/06/08/railsconf-2010-review-rails-application)) have been less technical, so I wanted to cover some technical aspects of Rails 3 and some tasty code goodness in standard ecommerce examples.

### Bundler

[Bundler](http://gembundler.com/), a gem management tool, is a hot topic at the conference, which comes with Rails 3. I went to a talk on Bundler and it was mentioned in several talks, but a quick run through on its use is:

```ruby
gem install bundler
gem update --system  # update Rubygems to 1.3.6+
```

Specify your gem requirements in the application root Gemfile directory.

```ruby
# excerpt from Spree Gemfile in the works
gem 'searchlogic',            '2.3.5'
gem 'will_paginate',          '2.3.11'
gem 'faker',                  '0.3.1'
gem 'paperclip',              '>=2.3.1.1'
```

```ruby
bundle install  # installs all required gems
git add Gemfile  # add Gemfile to repository
```

In Spree, the long-term plan is to break apart ecommerce functional components into gems and implement Bundler to aggregate the necessary ecommerce gems. The short-term plan is to use Bundler for management of all the Spree gem dependencies.

### ActiveRecord

ActiveRecord has some changes that affect the query interface. Some ecommerce examples on new querying techniques with the idea of chaining finder methods:

```ruby
recent_high_value_orders = Order
  .where("total > 1000")
  .where(["created_at >= :start_date", { :start_date => params[:start_date] }])
  .order("created_at DESC")
  .limit(50)
```

An example with the use of scope:

```ruby
class Order << ActiveRecord::Base
  scope :high_value_orders where("total > 1000")
    .where(["created_at >= :start_date", { :start_date => Time.now - 5.days )])
    .order("created_at DESC")
end
class SomeController << YourApplication::AdminController
  def index
    orders = Order.high_value_orders.limit(50)
  end

  def snapshot
    orders = Order.high_value_orders.limit(10)
  end

  def winner
    Order.high_value_orders.first
  end
end
```

The changes to ActiveRecord provide a more sensible and elegant way to build queries and moves away from the so-called drunkenness on hashes in Rails. ActiveRecord finder methods in Rails 3 include where, having, select, group, order, list, offset, joins, includes, lock, read only, and from. Because the relations are lazily loaded, you have the ability to chain query conditions with no performance effects as the query hasn't been executed yet, and fragment caching is more effective because the query is executed from a view call. Eager loading can be forced by using first, last, and all.

### Router Changes

Some new changes are introduced with Rails 3 in routing that move away from hash-itis, clarify flow ownership, and improve conceptual conciseness. A new route in a standard ecommerce site may be:

```ruby
resources :users do
  member do
    get :index, :show
  end
  resources :addresses
  resources :reviews
    post :create, :on => :member
  end
end
```

Another routing change on named routes allows:

```ruby
get 'login' => 'sessions#new'   # sessions is the controller, new is the action
```

### ActionMailer

Some significant changes were changed to the ActionMailer class after a reexamination of assumptions and the decision to model mailers after a Rails controller instead of a model/controller hybrid. An example of use with ActionMailer now:

```ruby
class OrderCompleteNotifier < ActionMailer::Base
  default :from => "customerservice@myecommercesite.com"

  def order_complete_notification(recipient)
    @recipient = recipient
    mail(:to => recipient.email_address_with_name,
         :subject => "Order information here")
  end
end
```

And some changes in sending messages, allowing the following:

```ruby
OrderCompleteNotifier.signup_notification(recipient1).deliver  # sends email
message = OrderCompleteNotifier.signup_notification(recipient2)
message.deliver
```

### RailTies

A few talks about Rails 3 mentioned the use of [RailTies](http://rubyforge.org/projects/railties/), which serves as the interface between the Rails framework and the rest of its components. It accepts configuration from application.rb, sets up initializers in extensions, tells Rails about generators and rake tasks in extensions, gems, plugins.

### Rails 3.1

[DHH](http://www.loudthinking.com/) briefly spoke about some Rails 3.1 things he's excited about, including reorganization of the public directory assets and implementing sprite functionality, which I am a big fan of.

### Rails 3 Resources

A few recommended Rails 3 learning resources were mentioned throughout the conference, including:

- [Rails 3 Screencasts](http://rubyonrails.org/screencasts/rails3) by Gregg Pollack
- [The Rails 3 Upgrade Handbook](http://www.railsupgradehandbook.com/) by Jeremy McAnally
- [The Rails Dispatch Blog](http://www.railsdispatch.com/)
- [The Great Decoupling](http://yehudakatz.com/2009/07/19/rails-3-the-great-decoupling/) by Yehuda Katz
- [Rails API Documentation](http://railsapi.com/)

There are tons of resources out there on these topics and more that I found as I was putting this article together. Go look and write code!
