---
author: Steph Skardal
title: Rails 4 Highlights
github_issue_number: 695
tags:
- ruby
- rails
date: 2012-09-20
---



I watched this recent video [What to Expect in Rails 4.0](http://bostonrb.org/presentations/what-to-expect-in-rails-40) presented by Prem Sichanugrist to the [Boston Ruby Group](http://bostonrb.org/). Here are a few high-level topics he covered in the talk:

- **StrongParameters**: replaces attr_accessor, attr_protected, moves param filtering concern to the controller rather than the model. Moving param filtering concern to the controller allows you to more easily modify user attribute change-ability in controllers (e.g. customer-facing vs admin).
- **ActiveSupport::Queue**: Discussed at RailsConf, add queueing support to Rails, e.g.:

```ruby
# Add to queue
Rails.queue.push UserRegistrationMailerJob(@user.id)

# Control queue configuration (asynchronous, synchronous or resque, e.g.
config.queue = [:asynchronous, :synchronous, :resque]
```

- **Cache Digests**: Rails 4.0 introduces cache key generation based on an item and its dependencies, so nested cache elements properly expire when an item is updated.
- **PATCH verb support**: Support of [HTTP PATCH](http://tools.ietf.org/html/rfc5789) method (_method equals "patch"), which will map to your update action is introduced in Rails 4.0.
- **Routing Concern**: Rails 4.0 introduces some methods to help clean up your duplicate routes.
- **Improvements to [ActiveRecord::Relation](http://api.rubyonrails.org/classes/ActiveRecord/Relation.html)**

    - Relation.all: returns ActiveRecord::relation object. User.all => User.to_a
    - Relation.none: Returns ActiveRecord::NullRelation, still chainable
    - Relation.___!: mutates current relation, e.g. @users.where!, @users.include!

- **Deprecations**

    - AR::Base.scoped
    - Dynamic Finder Methods: e.g. find_all_by_*
    - Hash-based Finders: e.g. User.find(:first)
    - Eager Evaluated Scope: scope will require a lambda
    - ActiveRecord::SessionStore
    - ActiveResource
    - Rails::Plugin

- **New Deprecation Policy**: Many of the above deprecations will still work in Rails 4.0 and included as gem dependencies, but will be removed in the jump to Rails 4.1. This means that the upgrade to Rails 4.1 may be more painful than the upgrade to Rails 4.0.

Check out [the video](http://bostonrb.org/presentations/what-to-expect-in-rails-40) or read the official current Rails 4.0 release notes [here](http://edgeguides.rubyonrails.org/4_0_release_notes.html). Also, check out [this post](http://reefpoints.dockyard.com/ruby/2012/09/18/rails-4-sneak-peek-postgresql-array-support.html) I came across about PostgreSQL array support in Rails 4, which may be pretty interesting to our PostgreSQL experts.


