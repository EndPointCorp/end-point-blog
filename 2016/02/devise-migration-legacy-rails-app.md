---
author: Brian Gadoury
title: Migrating to Devise in a Legacy Rails App
github_issue_number: 1205
tags:
- rails
- ruby
- testing
date: 2016-02-22
---

I’ve recently started working in a Rails 4 application that has accrued a lot of technical debt since it began life on Rails 1. To avoid spending the next few months tip-toeing around the code base, scared to bump something or step on a boobie-trapped brick, I pitched the client for a slice of budget to pay down some of that debt and write some tests. I got the thumbs up.

<img border="0" src="/blog/2016/02/devise-migration-legacy-rails-app/image-0.jpeg"/>

I decided to tackle the app’s home-grown user authentication. The encryption it was using wasn’t up to industry standards any more, and there were a few bugs with the flash messages it set. I went with the obvious choice of using [the Devise gem](https://rubygems.org/gems/devise) and backed the whole thing with some simple integration tests using [the Cucumber gem](https://rubygems.org/gems/cucumber). I didn’t want to annoy the users by making them reset their password when we deployed, so I came up with a way to migrate users’ passwords with no manual intervention or interruption to their workflow.

I ran the Devise generator and trimmed down the generated migration to set up only the database_authenticatable module.

```ruby
[phunk@work ]$ rails generate devise:install

# db/migrate/20160121005233_add_devise_to_users.rb
class AddDeviseToUsers < ActiveRecord::Migration
  def self.up
    change_table(:users) do |t|
      ## Database authenticatable
      ## null: true because we are transitioning from legacy passwords to devise
      t.string :encrypted_password, null: true, default: ""
    end
  end
end
```

Next, I commented out all the legacy authentication code sprinkled throughout the application. (I deleted it afterwards, but I kept it around for reference during this work.) I powered through setting the Devise routes, tweaking the Devise views for sign in and password changes, and aliasing helper methods to call the new Devise versions. Lastly, I created Cucumber tests for the common scenarios. Each test expectation verified that the page contained the expected string as they're defined in config/locales/devise.en.yml.

```nohighlight
Feature: User authentication

Background:
  Given User bob has an account with a password of pizza1

  Scenario: User signs in with correct credentials
    When he signs in login bob and password of pizza1
    Then he should be see Signed in successfully

  Scenario: User signs in with incorrect credentials
    When he signs in login bob and password of wrongpass
    Then he should be see Invalid login or password
```

My first stab at keeping existing user passwords involved implementing [a Devise custom encryptor](https://github.com/plataformatec/devise/wiki/How-To:-Create-a-custom-encryptor). I ended up bailing on that approach. I didn’t like adding that amount of complexity in exchange for a solution that was slightly less cryptographically secure than Devise’s bcrypt default. I needed to find a better way.

This is where Devise’s valid_password? method comes in. I created my own version of that method and mixed it into the User model via a new ActiveSupport::Concern. Here are the relevant parts of that module:

```ruby
# app/concerns/user_authentication.rb
require 'active_support/concern'

module UserAuthentication
  extend ActiveSupport::Concern

  included do

  def valid_password?(password)
    if !has_devise_password? && valid_transitional_password?(password)
      convert_password_to_devise(password)
      return true
    end

    super
  end

  def has_devise_password?
    encrypted_password.present?
  end

  def valid_transitional_password?(password)
    # secret legacy magic happens here
  end

  def convert_password_to_devise(password)
    update!(password: password)
  end
end
```

The valid_transitional_password? method calls the legacy auth check. If it’s a match, it updates the user’s password attribute, which is supplied by Devise and saves the Devise-encrypted version of the password param. Note that it’s a one way street - Once they have a Devise-encrypted password in the database, that’s what they get authenticated against via that call to super.

Our User model mixes in the new module:

```ruby
# app/models/user.rb
require 'user_authentication'

class User < ActiveRecord::Base
  include UserAuthentication

  devise :database_authenticatable

end
```

Once this has been running in production for a while and all the users have signed in and auto-migrated their passwords, clean-up will be easy: I’ll delete this mixin module, the two lines in the User class that reference it, and drop the legacy encrypted password column from the users table. All traces of this migration code will be gone, and this will look and run just like a vanilla Devise setup.

A side note about the arguably gratuitous one-liner methods in that mix-in module: Those help maintain a consistent level of abstraction in the main method and support the use case where a developer needs to quickly answer the question, “What’s special about how this app handles passwords?” (There are also some subtleties that these one-liners help hide, such as the legacy and Devise attribute names differing by only two characters.)

By adding integration tests to the sign in use cases, switching to Devise behind the scenes and coming up with a way to securely migrate passwords without interrupting users’ work, I was able to reduce technical debt, familiarize myself with some of the surrounding code, and make it easier and safer for us to work in this app. I also got to delete a ton of crufty code, which might be my favorite part.

PS. If you’re working with Devise, you want to be spending your time in [the extensive Devise Wiki on GitHub](https://github.com/plataformatec/devise/wiki).
