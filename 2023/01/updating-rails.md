---
author: "Couragyn Chretien"
title: "Updating Ruby on Rails"
date: 2023-01-12
github_issue_number: 1925
tags:
- rails
- ruby
- update
---

![A blue sky with sparse clouds, framed by the tops of two buildings viewed from below.](/blog/2023/01/updating-rails/blue-sky.webp)

<!-- Photo by Seth Jensen, 2023 -->

Updating your app to the latest versions of the framework it was built on, and dependencies it uses, is an important part of the development process. It may seem like a waste to invest time and money into it, but it can bring as much value as a new feature.

One good thing about using a framework like Ruby on Rails is that security features are baked in. This saves development time as the developer doesn't have to re-create the wheel for logins, permissions, authentication, etc. There are many users of the framework who work together to can catch and patch vulnerabilities. Unfortunately, this means if your app hasn't been updated its weaknesses become more obvious. A black hat attacker has easy access to a [list of past Rails vulnerabilities](https://www.cvedetails.com/vulnerability-list/vendor_id-12043/product_id-22569/Rubyonrails-Rails.html).

Have you ever been to a [website that hasn't been updated for a while](https://www.spacejam.com/) and found that everything moves slower than you're used to? As technology improves and functions are optimized application processing time can be reduced. Most releases come with a performance update that can help your application keep up with the best of them.

The gems your application uses also come out with updates to add new features and functionality. Usually these releases are made to work with the latest Rails versions. If you want to utilize them you'll have to meet the minimum Rails version requirements.

### Taking it step by step

When updating your Rails app, you can't just jump to the latest version. Updating to the next major release one at a time is recommended. This allows you to fix bugs as you go rather than trying to figure out what change broke what code.

> [The full list of Rails releases can be found here.](https://rubygems.org/gems/rails/versions)

Luckily you don't have to go through each one of these releases. Releases including `rc` or `beta` (`4.2.10.rc1`, `6.0.0.beta1`) can be skipped. Small releases can also be skipped, such as going from `6.0.0` to `6.0.1`.

If you wanted to update from `4.0.0` to `7.0.4`, I'd recommend this route:

`4.0.0` → `4.1.0` → `4.2.0` → `5.0.0` → `5.1.0` → `5.2.0` → `6.0.0` → `6.1.0` → `7.0.0` → `7.0.4`

Any of these updates can introduce bugs, but the biggest pain points will be the major version changes: 4 to 5, 5 to 6, etc.

### Fixing bundle errors

After changing the Rails and Ruby versions in the `Gemfile`, run `bundle update rails`.

```plain
source 'http://rubygems.org'
ruby '2.7.0'

gem 'rails', '~> 7.0.0'
```

Some gems won't be happy with the Rails update and will also need to be updated. Once this is done run `bundle update rails` again. If there are more errors, fix them. If it's successful `bundle install` can then be run. This will ensure all the gems are properly installed.

![A bundling error saying "Bundler could not find compatible versions for gem "nokigiri in Gemfile", followed by a list of several dependencies with incorrect resolutions.](/blog/2023/01/updating-rails/bundle-error.png)

Also make sure to start up your server and verify there's no problems there.

No more errors — that means we're done, right?

Well...

### Manual testing

Even if your app builds correctly that doesn't mean different parts of your app didn't explode. Functions that worked in a previous version might have been deprecated in the newest version.

For example, I came across this error in a recent update:

![Find all error. A red header reads "NoMethodError in HomeController#index". The body reads "undefined method `find_all_by_is_featured` for #<Class:0x000055f56c7efbf0>, followed by a code block showing the location of the error in the extracted source - in this case, line 5, reading `@featured_cds = CompactDisc.find_all_by_is_featured(true)`.](/blog/2023/01/updating-rails/find-all-by.png)

The `find_all_by_X` function was no longer working. Thankfully Stack Overflow is [there to help](https://stackoverflow.com/questions/59445783/undefined-method-find-all-by-x) us understand what changes were made and how to fix them. This function was deprecated in Rails 4, so `S.find_all_by_X_ID(x_ids)` functions need to change to `S.where(x_id: x_ids)`. Knowing this I was able to search the codebase for other `find_all_by_` functions and change all of them.

For large Rails updates (`5.2.0` → `6.0.0`), a full test of the app will need to be done. All functionality and pages should be verified and fixes applied.

For smaller Rails updates (`4.0.0` → `4.1.0`), you can get away with a smaller test suite. You can stick to testing the big, commonly used features of the application. Of course, if you want to be thorough, a full test can also be done.

Sometimes a gem will no longer be supported by the developer and no update has been made to allow it to work with the latest version of Rails. We have two options on how to proceed:

1. Find a replacement gem to accomplish the same functionality. Every reference to the original gem will need to be updated and fully tested.
2. Fork off of the gem and add the fixes yourself. Developers tend to stick with the gems they know across multiple applications. Owning the gem can be good as this updated version can be used on multiple apps by you and others. You'll need to update the Gemfile to point at this new repository.

    ```plain
    gem 'dead_gem', git: 'https://github.com/githubUser/dead_gem'
    ```

### Updating remaining gems

We're in the home stretch now. Rails is now on the most recent version and everything in the app is working correctly.

The last recommended task is to update all gems to their latest versions. This will open up the gems' latest features and make future Ruby on Rails updates easier.

Gems should be updated individually by running the command `bundle update #GemName`.
