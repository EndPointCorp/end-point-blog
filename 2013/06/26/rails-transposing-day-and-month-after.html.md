---
author: Brian Buchalter
gh_issue_number: 825
tags: rails
title: Rails transposing day and month after upgrading Ruby 1.8.7
---



If you’re wondering why your month and day are being transposed when saved in your database, you’re likely:

- Using a text field input for dates (likely with some JavaScript date picker)
- Using American style date formatting (mm/dd/YYYY)
- Upgrading from Ruby 1.8.7

If you meet these criteria you’ll find that American style dates get parsed incorrectly in Ruby 1.9+ because of [Ruby 1.9.x’s new date parsing](https://bugs.ruby-lang.org/issues/634#note-10) strategy. Unbelievably, this change effectively does away with American style date parsing in Ruby 1.9.x and Rails has happily followed suit!

### american_date to the rescue!

After trying and failing to restore American style date parsing using timeliness, delocalize, and i18n_alchemy, I found [american_date](https://github.com/jeremyevans/ruby-american_date). If you look at [the implementation](https://github.com/jeremyevans/ruby-american_date/blob/master/lib/american_date.rb), it is straight forward and restores backwards compatibility by simply adding a line to your Gemfile. Enjoy the return to sanity!

With [Ruby 1.8.7 going EOL this month](http://www.ruby-lang.org/en/news/2011/10/06/plans-for-1-8-7/), and [Rails 2.3.x and older losing support for even sevre security issues](https://weblog.rubyonrails.org/2013/2/24/maintenance-policy-for-ruby-on-rails/), it’s time to bust out your upgrade-foo for those old Rails apps. Of course, this is a tried and true topic, with many resources, most notibly [Railscast #225](http://railscasts.com/episodes/225-upgrading-to-rails-3-part-1). Good luck with your upgrades!


