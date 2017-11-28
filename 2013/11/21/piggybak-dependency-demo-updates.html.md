---
author: Steph Skardal
gh_issue_number: 889
tags: ecommerce, piggybak, ruby, rails
title: Piggybak Dependency & Demo Updates
---

Things have been quiet on the Piggybak front lately, but we recently upgraded the demo to Ruby 2.0.0 via rbenv, Rails 3.2.15, and Postgres 9.3. The [Piggybak demo](http://www.piggybak.org/demo_details.html) runs on Debian 7 with nginx and Unicorn. The upgrade went fairly smoothly, with the exception of jQuery related issues, described below.

As of jQuery 1.7, the [live()](http://api.jquery.com/live/) method is deprecated, replaced with the [on()](http://api.jquery.com/on/) method. As of jQuery 1.10.*, the live() method no longer exists. The previous version of Rails that was used on the demo, Rails 3.2.12, required the jquery-rails gem version which included an older version of jQuery. Upon upgrading to Rails 3.2.15, the attached jquery-rails gem now includes jQuery 1.10.*, resulting in the live() method no longer existing. As a result, several of the dependencies needed to be updated to accomodate this change ([Rails_admin](https://github.com/sferik/rails_admin), the Piggybak Coupon gem, and the Piggybak Gift Cert gem, [jQuery Nivo Slider](http://dev7studios.com/plugins/nivo-slider/)).

What's next for Piggybak? Our future plans include an upgrade to support Rails 4.0. Additional features described on our last [Roadmap Update](/blog/2012/11/06/piggybak-roadmap-status-update) include advanced taxonomy, reviews & ratings, saved cart, wishlist functionality, and saved address support. Piggybak continues to be a great [mountable ecommerce solution](http://www.piggybak.org/features.html#mountability) for Ruby on Rails, but End Point has a great deal of experience with other popular Ruby on Rails ecommerce platforms as well.
