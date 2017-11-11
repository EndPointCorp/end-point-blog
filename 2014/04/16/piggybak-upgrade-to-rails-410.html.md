---
author: Steph Skardal
gh_issue_number: 965
tags: piggybak, rails, ecommerce
title: 'Piggybak: Upgrade to Rails 4.1.0'
---

[Piggybak](http://www.piggybak.org/) and gems available in the demo (piggybak_variants, piggybak_giftcerts, piggybak_coupons, piggybak_bundle_discounts, piggybak_taxonomy) have been updated to Rails 4.1.0, Ruby 2.1.1 via Piggybak version gem 0.7.1. Interested in the technical details of the upgrade? Here are some fine points:

- Dependencies were refactored so that the parent Rails app controls the Rails dependency only. There was a bit of redundancy in the various plugin gemspec dependencies. This has been cleaned up so the parent Rails app shall be the canonical reference to the Rails version used in the application.
- Modified use of assets which require "//= require piggybak/piggybak-application" to be added to the assets moving forward. There have been several observed issues with precompling and asset behavior, so I simplified this by requiring this require to be added to the main Rails application.js for now. The engine file is supposed to have a way around this, but it has not behaved as expected, specifically on unique deployment architectures (e.g. Heroku). Patches welcome to address this.
- Tables migrated to namespaced tables, e.g. "orders" migrated to "piggybak_orders". This is how namespaced engine tables are supposed to look, and this upgrade fixes the table names with a migration and related code.
- Handled strong parameters. This was one of the most significant jumps from Rails 3 to Rails 4. The main element of Piggybak that needed updating here was the orders controller, which receives the order parameters and must determine which parameters to handle. Any references to attr_accessible in the code were removed.
- ActiveRecord "find" method replaced with where &amp; chaining, where applicable. The jump to Rails 4.0 deprecated find methods, but did not remove support, but the jump to Rails 4.1 removed support of these finder methods. These were removed.
- Scope syntax update. Rails 4 handles scopes with new syntax, and all default scope and named scopes were updated to reflect this new syntax.
- Validates syntax updated. Rails 4 has new validates syntax which accepts arguments, e.g. presence: true, uniqueness: true. Piggybak was upgraded to use the new syntax, although the old syntax is still supported.
- Significant routes update. Rails 4 introduced a significant change in routing, and Piggybak was updated to reflect these changes.

The full commits of Piggybak are available for browsing [here](https://github.com/piggybak/piggybak/commit/ef4a33ba199c27e18e39434c7cd9aec659c2081f) and [here](https://github.com/piggybak/piggybak/commit/9174688a0f96cedb1b8707b54898a8b5fdbb9393).

### Wishlist

There are a few things that I'd love to see adopted in Piggybak, with the help of the community. These include:

- Consider move to [CoffeeScript](http://coffeescript.org/). I'm still on the fence about this, but I'm seeing more projects with node and CoffeeScript lately, so I wonder if it would be worth the overhead to move to CoffeeScript.
- Add test coverage. Perhaps [Travis CI](https://travis-ci.org/) integration would make sense since it hooks into github nicely?
- Build out more features. Things like reviews &amp; ratings, saved cart, wishlist support, and saved address support have been on the feature list for a while. It'd be nice to see movement here.
