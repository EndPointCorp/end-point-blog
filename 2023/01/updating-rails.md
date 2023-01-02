---
author: "Couragyn Chretien"
title: "Updating Rails"
date: 2023-01-01
tags:
- rails
- ruby
- update
- gem
---

## Updating Rails
Updating your app to the latest version is an important part of the development process. It may seem like a waste to invest time and money into it, but it can bring as much value as a new feature.

One good thing about using a framework like Rails is that security features are baked in. This saves development time as the devloper doesn't have to re-create the wheel for logins, permissions, authentication, etc. There are many users of the framework who work together to can catch and patch vulnerabilities. Unfortunately this means if your app hasn't been updated in becomes more obvious what its weaknesses are. A black hat developer even has access to a [list of previous Rails version vulnerabilities.](https://www.cvedetails.com/vulnerability-list/vendor_id-12043/product_id-22569/Rubyonrails-Rails.html)

Have you ever been to a [website that hasn't been updated for a while](https://www.spacejam.com/) and found that everything moves slower than your used to? As technology improves and functions are optimized application processing time can be reduces. Most releases come with a performance update that can keep help your application keep up with the best of them.

The Gems of your application also come out with releases to add new features and functionality. Usually these releases are made to work with the latest Rails versions. If you want to utilize them you'll have to meet the minimum Rails version requirements.

### Taking it Step by Step

When updating your Rails app, you can't just jump to the latest version. Updating to the next major release one at a time is recommended. This allows you to fix bugs as you go rather than trying to figure out what broke what. 

[The Full List of Releases can be found here.](https://rubygems.org/gems/rails/versions)

Luckily you don't have to go through each one of these releases. Releases that have rc or beta (`4.2.10.rc1`, `6.0.0.beta1`) can be skipped. Small releases can also be skipped (going from `6.0.0` to `6.0.1`). 

If you wanted to update from `4.0.0` to `7.0.4`, I'd recommend this route:

`4.0.0` -> `4.1.0` -> `4.2.0` -> `5.0.0` -> `5.1.0` -> `5.2.0` -> `6.0.0` -> `6.1.0` -> `7.0.0` -> `7.0.4`

Any of these updates can introduce bugs, but the biggest pain points will be the big version changes (4 to 5, 5 to 6, etc.)

### Fixing Bundle Errors
![Gemfile](/blog/2022/12/updating-rails/upgraded-gemfile.png)

After changing the Rails and Ruby version in the `Gemfile`, run `bundle update rails`.

![Bundle Error](/blog/2022/12/updating-rails/bundle-error.png)

Some Gems won't be happy with the Rails update and will also need to be updated. Once this is done run `bundle update rails` again. If there are more errors, fix them. If it's successful `bundle install` can then be run. This will ensure all the gems are properly installed.

Also make sure to start up your server and verify there's no problems there.

No more errors, that means we're done, right?

Well...

### Manual Testing
Even if your app builds correctly that doesn't mean different parts of your app didn't explode. Functions that worked in a previous version might have been deprecated in the newest version

For example, I came across this error in a recent update.
![Find All Error](/blog/2022/12/updating-rails/find-all-by.png)

The `find_all_by_X` function was no longer working. Thankfully [stackoverflow](https://stackoverflow.com/questions/59445783/undefined-method-find-all-by-x) is there to help us understand what changes were made and how to fix them. This function was deprecated in Rails 4, so `S.find_all_by_X_ID(x_ids)` functions need to change to `S.where(x_id: x_ids)`. Knowing this I was able to search the codebase for other `find_all_by_` functions and change all of them.

For large Rails updates (`5.2.0` -> `6.0.0`), a full test of the app will need to be done. All functionality and pages should be verified and fixes applied.

For smaller Rails updates (`4.0.0` -> `4.1.0`), you can get away with a smaller test suite. You can stick to testing the big commonly used features of the application. Of course if you want to be thorough, a full test can also be done.

Sometimes a gem will no longer be supported by the developer and no update has been made to allow it to work with the latest version of Rails. We have two options on how to proceed:

1. Find a replacment gem to accomplish the same functionality. Every reference to the original gem will need to be updated and fully tested.

2. Fork off of the gem and add the fixes yourself. Developers tend to stick with the gems they know across multiple applications. Owning the gem can be good as this updated version can be used on multiple apps by you and others. You'll need to update the Gemfile to point as this new repository.

![Dead Gem](/blog/2022/12/updating-rails/dead-gem.png)

### Updating Remaining Gems
We're in the home stetch now. Rails is now on the most recent version and everything in the app is working correctly.

The last recommended task is to update all gems to their latest versions. This will open up the gems latest features and make future Rails updates easier.

Gems should be updated individually and can be envoked by running the command `bundle update #GemName`.