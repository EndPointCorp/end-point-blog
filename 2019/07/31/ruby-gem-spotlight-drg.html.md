---
author: "Patrick Lewis"
title: "Ruby Gem Spotlight: DRG"
tags: ruby
gh_issue_number: 1544
---

<img src="/blog/2019/07/31/ruby-gem-spotlight-drg/banner.jpg" alt="Pins" /> [Photo](https://flic.kr/p/ewr4C) by [Ioan Sameli](https://www.flickr.com/people/biwook/), used under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/), cropped from original.

The [DRG gem](https://github.com/ridiculous/drg) is “a Ruby utility to help automate dependency management using Bundler.” I use DRG to manage gem versions in all of my Rails projects and have found it to have several useful features for managing project dependencies in Gemfiles.

### Pinning with 'drg:pin'

DRG works by adding a variety of Rake tasks for updating your Gemfile. I like to start with `rake drg:pin:minor` to pin a project’s Gemfile to the approximate minor version of the gems currently installed in a project’s `Gemfile.lock`. This fills in missing version information where needed, and updates the Gemfile to better reflect the state of the currently-installed gems.

Here’s an example of a Gemfile from a freshly generated Rails project before and after running `rake drg:pin:minor`:

Before:

```ruby
gem 'bootsnap', '>= 1.1.0', require: false
gem 'drg'
gem 'puma', '~> 3.11'
gem 'rails', '~> 5.2.3'
gem 'sass-rails', '~> 5.0'
gem 'sqlite3'
gem 'uglifier', '>= 1.3.0'

group :development, :test do
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
end
```

After:

```ruby
gem 'bootsnap', '~> 1.4', require: false
gem 'drg', '~> 1.5'
gem 'puma', '~> 3.12'
gem 'rails', '~> 5.2'
gem 'sass-rails', '~> 5.0'
gem 'sqlite3', '~> 1.4'
gem 'uglifier', '~> 4.1'

group :development, :test do
  gem 'byebug', '~> 11.0', platforms: [:mri, :mingw, :x64_mingw]
end
```

### Unpinning with 'drg:unpin'

My preferred method for upgrading all of my project’s gems in bulk is to first unpin the entire Gemfile with `bin/rails drg:unpin`, run `bundle update`, and then re-pin the Gemfile with `bin/rails drg:pin:minor`.

After `drg:unpin`:

```ruby
gem 'bootsnap', require: false
gem 'drg'
gem 'puma'
gem 'rails'
gem 'sass-rails'
gem 'sqlite3'
gem 'uglifier'

group :development, :test do
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
end
```

After `bundle update` and `drg:pin:minor`:

```ruby
gem 'bootsnap', '~> 1.4', require: false
gem 'drg', '~> 1.5'
gem 'puma', '~> 4.0'
gem 'rails', '~> 5.2'
gem 'sass-rails', '~> 5.0'
gem 'sqlite3', '~> 1.4'
gem 'uglifier', '~> 4.1'

group :development, :test do
  gem 'byebug', '~> 11.0', platforms: [:mri, :mingw, :x64_mingw]
end
```

There are some tasks provided by DRG like `drg:pin:latest` but they seem to be inconsistent with how they pin the upgraded gem versions, using hard-coded versions instead of the approximate values you get from `drg:pin:minor`, so I have tended to stick with the process listed above.

### Excluding gems from DRG

Sometimes there are external factors that make it difficult or undesirable to upgrade a gem to its latest version; I have had times when a project was limited to an older, specific version of Ruby that was not compatible with the most recent version of certain gems. In those situations, it is easy to have DRG ignore the gem and not attempt to upgrade it when performing any bulk operations. Simply add a comment to the end of the gem’s definition in your Gemfile, like:

```ruby
  gem 'web-console', '~> 3.7' # @drg skip
```

DRG will ignore any lines with the `@drg skip` comment in them.

### Summary

I have found the DRG gem to be a convenient time-saver for all of my Rails projects over the past few years. My only current concern with it is that the GitHub project has not been updated since January 2017; the most recent 1.5.2 release still works well for the current versions of Ruby/Rails/Bundler but it is possible that some future update might break DRG’s functionality. Fortunately, it is open source and should be easy to update for future compatibility when needed.
