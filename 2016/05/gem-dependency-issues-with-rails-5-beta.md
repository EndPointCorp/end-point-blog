---
author: Patrick Lewis
title: Gem Dependency Issues with Rails 5 Beta
github_issue_number: 1226
tags:
- rails
- ruby
date: 2016-05-02
---

The third-party gem ecosystem is one of the biggest selling points of Rails development, but the addition of a single line to your project’s Gemfile can introduce literally dozens of new dependencies. A compatibility issue in any one of those gems can bring your development to a halt, and the transition to a new major version of Rails requires even more caution when managing your gem dependencies.

In this post I’ll illustrate this issue by showing the steps required to get rails_admin (one of the two most popular admin interface gems for Rails) up and running even partially on a freshly-generated Rails 5 project. I’ll also identify some techniques for getting unreleased and forked versions of gems installed as stopgap measures to unblock your development while the gem ecosystem catches up to the new version of Rails.

After installing the current beta3 version of Rails 5 with gem install rails --pre and creating a Rails 5 project with rails new I decided to address the first requirement of my application, admin interface, by installing the popular Rails Admin gem. The [rubygems page for rails_admin](https://rubygems.org/gems/rails_admin) shows that its most recent release 0.8.1 from mid-November 2015 lists Rails 4 as a requirement. And indeed, trying to install rails_admin 0.8.1 in a Rails 5 app via bundler fails with a dependency error:

```nohighlight
Resolving dependencies...
Bundler could not find compatible versions for gem "rails":
In snapshot (Gemfile.lock):
rails (= 5.0.0.beta3)

In Gemfile:
rails (< 5.1, >= 5.0.0.beta3)

rails_admin (~> 0.8.1) was resolved to 0.8.1, which depends on
rails (~> 4.0)
```

I took a look at the [GitHub page for rails_admin](https://github.com/sferik/rails_admin) and noticed that recent commits make reference to Rails 5, which is an encouraging sign that its developers are working on adding compatibility with Rails 5. Looking at the [gemspec in the master branch](https://github.com/sferik/rails_admin/blob/master/rails_admin.gemspec) on GitHub shows that the rails_admin gem dependency has been broadened to include both Rails 4 and 5, so I updated my app’s Gemfile to install rails_admin directly from the master branch on GitHub:

```ruby
gem 'rails_admin', github: 'sferik/rails_admin'
```

This solved the above dependency of rails_admin on Rails 4 but revealed some new issues with gems that rails_admin itself depends on:

```nohighlight
Resolving dependencies...
Bundler could not find compatible versions for gem "rack":
In snapshot (Gemfile.lock):
rack (= 2.0.0.alpha)

In Gemfile:
rails (< 5.1, >= 5.0.0.beta3) was resolved to 5.0.0.beta3, which depends on
actionmailer (= 5.0.0.beta3) was resolved to 5.0.0.beta3, which depends on
actionpack (= 5.0.0.beta3) was resolved to 5.0.0.beta3, which depends on
rack (~> 2.x)

rails_admin was resolved to 0.8.1, which depends on
rack-pjax (~> 0.7) was resolved to 0.7.0, which depends on
rack (~> 1.3)

rails (< 5.1, >= 5.0.0.beta3) was resolved to 5.0.0.beta3, which depends on
actionmailer (= 5.0.0.beta3) was resolved to 5.0.0.beta3, which depends on
actionpack (= 5.0.0.beta3) was resolved to 5.0.0.beta3, which depends on
rack-test (~> 0.6.3) was resolved to 0.6.3, which depends on
rack (>= 1.0)

rails_admin was resolved to 0.8.1, which depends on
sass-rails (< 6, >= 4.0) was resolved to 5.0.4, which depends on
sprockets (< 4.0, >= 2.8) was resolved to 3.6.0, which depends on
rack (< 3, > 1)
```

This bundler output shows a conflict where Rails 5 depends on rack 2.x while rails_admin’s rack-pjax dependency depends on rack 1.x. I ended up resorting to a Google search which led me to the following issue in the rails_admin repo: [https://github.com/sferik/rails_admin/issues/2532](https://github.com/sferik/rails_admin/issues/2532)

Installing rack-pjax from GitHub:

```ruby
gem 'rack-pjax', github: 'afcapel/rack-pjax', branch: 'master'
```

resolves the rack dependency conflict, and bundle install now completes without error. Things are looking up! At least until you try to run the Rake task to rails g rails_admin:install and you’re presented with this mess:

```nohighlight
/Users/patrick/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/actionpack-5.0.0.beta3/lib/action_dispatch/middleware/stack.rb:108:in `assert_index': No such middleware to insert after: ActionDispatch::ParamsParser (RuntimeError)
from /Users/patrick/.rbenv/versions/2.3.0/lib/ruby/gems/2.3.0/gems/actionpack-5.0.0.beta3/lib/action_dispatch/middleware/stack.rb:80:in `insert_after'
```

This error is more difficult to understand, especially given the fact that the culprit (the remotipart gem) is not actually mentioned anywhere in the error. Thankfully, commenters on the above-mentioned rails_admin issue #2532 were able to identify the remotipart gem as the source of this error and provide a link to a forked version of that gem which allows rails_admin:install to complete successfully (albeit with some functionality still not working).

In the end, my Gemfile looked something like this:

```ruby
gem 'rails_admin', github: 'sferik/rails_admin'
# Use github rack-pjax to fix dependency versioning issue with Rails 5
# https://github.com/sferik/rails_admin/issues/2532
gem 'rack-pjax', github: 'afcapel/rack-pjax'
# Use forked remotipart until following issues are resolved
# https://github.com/JangoSteve/remotipart/issues/139
# https://github.com/sferik/rails_admin/issues/2532
gem 'remotipart', github: 'mshibuya/remotipart', ref: '3a6acb3'
```

A total of three unreleased versions of gems, including the forked remotipart gem that breaks some functionality, just to get rails_admin installed and up and running enough to start working with. And some technical debt in the form of comments about follow-up tasks to revisit the various gems as they have new versions released for Rails 5 compatibility.

This process has been a reminder that when working in a Rails 4 app it’s easy to take for granted the ability to install gems and have them “just work” in your application. When dealing with pre-release versions of Rails, don’t be surprised when you have to do some investigative work to figure out why gems are failing to install or work as expected.

My experience has also underscored the importance of understanding all of your application’s gem dependencies and having some awareness of their developers’ intentions when it comes to keeping their gems current with new versions of Rails. As a developer it’s in your best interest to minimize the amount of dependencies in your application, because adding just one gem (which turns out to have a dozen of its own dependencies) can greatly increase the potential for encountering incompatibilities.
