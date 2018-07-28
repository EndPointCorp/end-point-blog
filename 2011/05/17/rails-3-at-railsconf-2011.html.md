---
author: Steph Skardal
gh_issue_number: 452
tags: conference, ruby, rails
title: Rails 3 at RailsConf 2011
---

A keynote by [DHH](http://david.heinemeierhansson.com/) kicked off Day 2 of RailsConf, where much of his talk was spent discussing new asset behavior in Rails 3.1. Here’s a run down of a few topics I found worth noting:

### Asset Pipeline

DHH started by explaining how although a Rails application has lovely organization in terms of Ruby files, the assets (stylesheets, images, and JavaScripts) have become a junk drawer where junk continues to pile in. Once there’s more than a handful of files, the [broken window theory](https://en.wikipedia.org/wiki/Broken_windows_theory) applies and no one tries to maintain organization of those assets. This gets nasty, [ like a honey badger](https://www.youtube.com/watch?v=4r7wHMg5Yjg).

With Rails 3.1, the asset pipeline addresses the junk drawer. Assets directories (images, stylesheets, and JavaScripts) are now created in the app, lib, and vendor assets directories as they pertain to the main app, plugin dependencies, or introduce new library dependencies like a jquery calendar date select plugin. There’s also the introducton of appending to config.assets.paths, which allows you to add new directories that store these assets in arbitrary directories. The new asset pipeline allows you to store these assets in different organization, which encourages JavaScript files to be stored based on their level of abstraction, and the asset pipeline combined with Bundler enables you to track the jquery version with a jquery-rails gem yielding better maintenance.

### New Defaults

Rails 3.1 now assumes the default of CoffeeScript and scss (Sass). [Jason discussed](/blog/2011/05/16/railsconf-2011-day-one) a Sass talk he attended yesterday at [BohConf](http://bohconf.com/) which includes things like nesting to reduce duplicate code and variables to improve maintainability. I haven’t worked with CoffeeScript much, so I’ll just link to the [CoffeeScript documentation](https://coffeescript.org/) and possibly attend a CoffeeScript talk tomorrow. The argument between setting defaults and setting no defaults was revisited, and defaults won. The new defaults use Bundler to include Sass and coffee-script in the Gemfile:

```ruby
gem 'sass'
gem 'coffee-script'
```

And these can simply be commented out of the dependency list if desired. In my case, if I were developing a Rails app tomorrow with a limited budget, I might choose to use Sass since I’ve worked with it before, but pass on CoffeeScript until I learned more and felt confident working with it.

### Scalability and Compiling

Another question that comes up with these new defaults is the scalability and compilability. A new rake task is introduced:

```ruby
rake assets:precompile
```

The rake task goes through the load path to precompile application JavaScript and CSS into application-*md5_hash*.js or application-*md5_hash*.css and copy over the images to the application public directory. This new file based method ensures that users will request the correct application file in addition to keeping the older compiled files around. Finally, compression tools are built straight into Rails, uglifier for JavaScript compression and scss for CSS compression. There is no penalty to writing comments or white-space rich code with these compression tools built in.

<img src="/blog/2011/05/17/rails-3-at-railsconf-2011/image-0.jpeg"/>

We need a photo break. [A Honey Badger.](https://en.wikipedia.org/wiki/Honey_badger)

The second talk I attended was [“SOLID Design Principles Behind the Rails 3 Refactoring”](https://conferences.oreilly.com/rails2011/public/schedule/detail/19579) by José Valim, a member of the Rails core team.

### Single Responsibility Principle

Jose spent the most time talking about the [single responsibility principle](https://en.wikipedia.org/wiki/Single_responsibility_principle), or that a class should have one and only one purpose. José discussed the evolution of the ActionView::Base that was responsible for tracking details, finding templates, compling templates, and rendering to gradually be divided into the following components and responsibilities in Rails 3:

- View Path: holds resolvers
- Resolver: finds template. The resolvers abstraction no longer restricts templates to the filesystem (can be anywhere in the app,
web service, or even database) which simplifies testing and therefore improves maintainability.
- Lookup Context: tracks details, lookup context object is passed to the view.
- AV::Renderer: renders templates
- ActionView::Base: renders context

By applying the single responsibility principle to the view rendering functionality in Rails, modularization now allows us to extend or override individual points of the process (such as grabbing a template from a CMS-driven database, or passing a different lookup context object to the view) and ensure maintainability by enabling more testable code.

José talked about the other principles, but some pertain to static languages more so than Ruby as the book was originally written with static languages in mind. These included:

- [Open/closed principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle): José discussed extending ActiveRecord::Base for one modular bit of application but not another.
- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
- [Liskov Substitution Principle:](https://en.wikipedia.org/wiki/Liskov_substitution_principle) José’s example here in substitution can be applied to the argument between DataMapper versus ActiveRecord and Rails 3.0 took steps to define an API working with an ORM to make it more substitutable.
- [Interface Segregation Principle](https://en.wikipedia.org/wiki/Interface_segregation_principle)

Since I missed a few points here and there, feel free to check out the conference keynote videos [here](https://conferences.oreilly.com/rails2011/public/content/video) and I’ll add a link to José’s talk when it becomes available. Undoubtedly, Rails 3.0 and related Rails 3.0 topics will continue to be a highlight of the conference and I look forward to sharing more!
