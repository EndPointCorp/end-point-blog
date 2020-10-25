---
author: Tim Case
gh_issue_number: 830
tags: ruby
title: Use Rubygems.org To Find GitHub Source For Gems
---

If you want to look at source for a gem on GitHub, make sure to go to [Rubygems.org](https://rubygems.org/) first and find the gem’s GitHub project through rubygems’ page for that particular gem. The reason for this is that there are lot of forks on GitHub and you may end up finding the source to a fork that is dead. Rubygems.org is guaranteed to have the right path to the gem you are installing via “gem install mynewgem”.

Most of the profile pages for a gem on Rubygems.org have a link for the “home page” and “source code” of a gem and these usually link to the GitHub page of the gem’s source. This trick isn’t a 100% as not every gem’s source is located on GitHub but it works about 90% of the time. In the case where you can’t find a gem’s source through Rubygems.org, try “gem unpack <mynewgem>” which will give you the source locally.
