---
author: Mike Farmer
gh_issue_number: 654
tags: ruby
title: Guard Cucumber Command Prefix
---



[Guard](https://github.com/guard/guard) is an incredibly useful ruby gem that allows you to monitor changes to files and then execute commands when files change. Some of the common uses of guard are to watch code changes and then automatically execute your test suite. Guard comes with a plugin framework that allows developers to write specific watches. Some common plugins are [guard-rspec](https://github.com/guard/guard-rspec) and [guard-cucumber](https://github.com/guard/guard-cucumber). You can see a list of over 120 plugins on the [rubygems website](https://rubygems.org/search?query=guard-).

Yesterday I was working on some cucumber tests and wanted to use guard to automatically run my tests. I currently run [all of my cucumber tests using capybara-webkit](/blog/2011/12/08/running-integration-tests-in-webkit) to allow me to run my tests in the terminal. To do so, I need to run xvfb-run bundle exec cucumber. The xvfb-run command allows the test to run in a headless X11 window. The problem is that the guard-cucumber plugin didn’t allow for a command prefix so my tests wouldn’t run correctly.

Thankfully, the [guard-cucumber](https://github.com/guard/guard-cucumber) plugin is available on github and I was able to fork the project and [add an option to allow a prefix](https://github.com/mikefarmer/guard-cucumber/commit/935d3f09c2e8397c54b5159b34d47f52c9838587). When it was completed, I added some documentation and a test and then made sure the tests all passed. I thought others may want this functionality as well so I sent a [pull request](https://github.com/guard/guard-cucumber/pull/3) to the project owner and was happy to see that within an hour it was accepted and merged into the project.

Github really rocks for this kind of development and I was glad to add to the project in a positive way. I get the functionality I need and the community at large does as well. Open source rocks!


