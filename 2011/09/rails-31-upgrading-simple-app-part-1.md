---
author: Steph Skardal
title: 'Rails 3.1: Upgrading a Simple App — Part 1'
github_issue_number: 499
tags:
- javascript
- jquery
- rails
date: 2011-09-21
---

Here at End Point, I’ve worked with a few Rails 3 applications in production and a couple of Rails 3.1 apps in development, so I’ve become familiar with the new features and functionality including the [Rails 3.1 Asset Pipeline](http://guides.rubyonrails.org/asset_pipeline.html) that [I mentioned](/blog/2011/05/rails-3-at-railsconf-2011/) earlier this year. I thought it was a good time to upgrade [our website](/) to Rails 3.1 and share the experience.

To start, here’s a quick summary of our website:

- Simple Rails application running on Rails 2.1.2 with no database
- Static pages throughout the site, fully cached
- Rake tasks to generate partials throughout the site to display dynamic blog content
- Site uses a moderate amount of jQuery and jQuery plugins.
- Site is optimized in terms of asset serving (ETags, Expires headers, CSS sprites, etc.)

While I’ve worked with a few Rails 3 apps, I haven’t been involved in the actual upgrade process myself. There are plenty of resources out there with upgrade advice, including a few RailsCasts ([one](http://railscasts.com/episodes/225-upgrading-to-rails-3-part-1), [two](http://railscasts.com/episodes/226-upgrading-to-rails-3-part-2), and [three](http://railscasts.com/episodes/227-upgrading-to-rails-3-part-3)). My favorite resource was the [rails_upgrade gem](https://github.com/rails/rails_upgrade), a gem that is now officially supported by Rails to help with the upgrade process. I followed the instructions to install the gem (**script/plugin install git://github.com/rails/rails_upgrade.git**) to install it as a plugin in our site’s application in a fresh git branch (on [a camp](http://www.devcamps.org/), of course!).

The rails_upgrade provides a few new rake tasks for checking compatibility, upgrading the routes, creating a Gemfile, and upgrading configuration. For me, the most valuable task was the **rake rails:upgrade:check** task. Here’s what the output looked like for this app:

### Deprecated session secret setting

Previously, session secret was set directly on ActionController::Base; it's now config.secret_token. More information: http://lindsaar.net/2010/4/7/rails_3_session_secret_and_session_store

The culprits:

- config/initializers/session_store.rb

### Old router API

The router API has totally changed. More information: http://yehudakatz.com/2009/12/26/the-rails-3-router-rack-it-up/

The culprits:

- config/routes.rb

### New file needed: config/application.rb

You need to add a config/application.rb. More information: http://omgbloglol.com/post/353978923/the-path-to-rails-3-approaching-the-upgrade

The culprits:

- config/application.rb

### Deprecated constant(s)

Constants like RAILS_ENV, RAILS_ROOT, and RAILS_DEFAULT_LOGGER are now deprecated. More information: http://litanyagainstfear.com/blog/2010/02/03/the-rails-module/

The culprits:

- app/views/layouts/application.rhtml
- ...

### Soon-to-be-deprecated ActiveRecord calls

Methods such as find(:all), find(:first), finds with conditions, and the :joins option will soon be deprecated. More information: http://m.onkey.org/2010/1/22/active-record-query-interface

The culprits:

- app/views/blog_archive/_ruby_on_rails.html.erb
- ...

### Deprecated AJAX helper calls

AJAX javascript helpers have been switched to be unobtrusive and use :remote => true instead of having a seperate function to handle remote requests. More information: http://www.themodestrubyist.com/2010/02/24/rails-3-ujs-and-csrf-meta-tags/

The culprits:

- app/views/blog_archive/_company.html.erb
- ...

### Deprecated ActionMailer API

You're using the old ActionMailer API to send e-mails in a controller, model, or observer. More information: http://lindsaar.net/2010/1/26/new-actionmailer-api-in-rails-3

The culprits:

- app/controllers/contact_controller.rb

### Old ActionMailer class API

You're using the old API in a mailer class. More information: http://lindsaar.net/2010/1/26/new-actionmailer-api-in-rails-3

The culprits:
- app/models/contact_form.rb

As you can see, the upgrade check spits out a list of necessary and recommended upgrades and the corresponding *culprits*. It’s also nice that the task provides documentation in the form of a link for each message. Studying the source of the plugin, I found additional examples of upgrade messages: named_scope updates, validate_on_* syntax, test_help path updates, gem bundling configuration, Rails generator API syntax updates, messaging on known broken plugins (e.g. searchlogic, cucumber, nifty-generators), and depracation on ERb helper and AJAX calls.

I went through and applied my updates, according to the checklist. Notable updates were:

**Routing updates**

*Before*

```ruby
ActionController::Routing::Routes.draw do |map|
  map.root :controller => 'home', :action => 'index'
  map.connect 'contact/submit', :controller => 'contact', :action => 'submit'
  map.connect ':controller/:id'
  map.connect '*path', :controller => 'redirect'
end
```

*After*

```ruby
Endpoint::Application.routes.draw do
  root :to => 'home#index'
  match 'contact/submit' => 'contact#submit'
  match ':controller(/:id)', :action => :index
  match '*path' => 'redirect#index'
end
```

**Introduction of a Gemfile**

```ruby
source 'http://rubygems.org'

gem 'rails', '3.1.0'
gem 'json'

# Gems used only for assets and not required
# in production environments by default.
group :assets do
  gem 'sass-rails', "  ~> 3.1.0"
  gem 'coffee-rails', "~> 3.1.0"
  gem 'uglifier'
end

gem 'jquery-rails'
gem 'fastercsv'
gem 'execjs'
gem 'therubyracer'
gem 'rake', '0.8.7'
```

**Renaming rhtml files**

Something that didn’t come up in the rails upgrade check that is required to have a working app is renaming all rhtml files to html.erb, briefly described [here](http://www.railstips.org/blog/archives/2007/03/04/renaming-rhtml-to-erb/).

**Basic Asset Management**

To get the basic app working, I moved the public/stylesheets and public/javascripts to the new app/assets directories to start. I did not move the images out of the public/ directory because several of the images in the application are referenced by blog articles.

**Database-less Application**

I followed the directions [here](https://stackoverflow.com/questions/3954307/rails-3-how-do-i-avoid-database-altogether) combined with a bit of troubleshooting to configure a Rails 3.1 app that does not require a database.

**Conclusion**

The upgrade was a relatively painless process, although it still took a few hours for even the most basic application with only a handful of controllers, routes, and one mailer. My experience suggests that with a more complex application, the upgrade will take at least a few hours, if not much more. This simple app doesn’t do much with [remote forms and links](https://www.alfajango.com/blog/rails-3-remote-links-and-forms/), so I didn’t spend any time upgrading the app to work with the [jquery-ujs gem](https://github.com/rails/jquery-ujs). Also, I obviously didn’t mess around with [Rails 3.1 ActiveRecord](http://guides.rubyonrails.org/3_1_release_notes.html#active-record) issues since the application is database-less. Both of these items may add significant overhead to the upgrade process.

I spent a significant amount of time working with the new asset pipeline and restructuring the assets, which I plan to describe in **Part 2** of the upgrade. Stay tuned!
