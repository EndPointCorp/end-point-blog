---
author: Steph Skardal
gh_issue_number: 1033
tags: piggybak, ruby, rails
title: 'Piggybak: Recent Updates and Upgrades'
---



[Piggybak](http://www.piggybak.org/), an open source Ruby on Rails ecommerce gem, implemented as a mountable solution, has continued to be upgraded and maintained over the last several months to keep up to date with Rails security releases and Ruby releases. Here are some quick notes on recent work:

- Piggybak (version 0.7.5) is now compatible with Rails 4.1.6, which is the most up to date release of Rails. See [the Rails release notes](http://weblog.rubyonrails.org/2014/9/12/Rails-4-1-6-and-4-0-10-has-been-released/) for more details on this recent release. The [Piggybak Demo](http://www.piggybak.org/demo/) is now running on Rails 4.1.6.
- Piggybak is compatible with Ruby 2.1.2, and the demo is running on Ruby 2.1.2
- Recent updates in [Piggybak](https://github.com/piggybak/piggybak) include migration fixes to handle table namespace issues, and updates to remove methods that are no longer present in Rails (that were previously deprecated).
- Recent updates to [the demo](https://github.com/piggybak/demo) include updates to the integration testing suite to allow testing to be compatible with Rails 4.1.6, as well as modifications to how the demo handles exceptions.

Make sure to check out [Piggybak on github](https://github.com/piggybak/piggybak) repository for more details on these recent updates.


