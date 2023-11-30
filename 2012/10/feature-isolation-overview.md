---
author: Mike Farmer
title: Feature Isolation, an Overview
github_issue_number: 704
tags:
- ruby
- rails
- testing
date: 2012-10-10
---

Yesterday, Brian Buchalter blogged about a recent [presentation I did for End Point Rails developers](/blog/2012/10/feature-isolation-with-mike-farmer/).

While the blog article did a great job of capturing some of the nitty gritty detail from the presentation, I'd like to just followup with a quick overview statement about Feature Isolation. I've also made [my slides](https://docs.google.com/presentation/d/1M4AV8ePgL7EKcZuEfjWdTJ4V1ULU79B4ffUixWuk0fs/edit) available for anyone who is interested.

Feature Isolation is what I'm calling a development strategy for adding new features to existing applications.  In Rails, I'm utilizing [cucumber](http://cukes.info/), a tool for transforming use-case language into ruby code, to specify the requirements and then execute them outside of the Rails environment and away from the complexity of the rest of the application.

Using stubbing and a minimal mock of ActiveRecord ([FastModel](https://github.com/mikefarmer/cucumber_tools)) I can then begin to design my feature from a more object oriented approach than is typical in Rails development. I can bring in any models, new or existing, that I will need and stub out the interface to the database. Likewise, I can design my classes and their public interface. Getting all my tests to pass from a high level without actually developing the behavior itself allows me to make design decisions quickly and ensure I'm capturing all the requirements in my design.

From there, it's just a matter of removing the stubs and mocks from the tests and then building them out in the application ensuring that I'm still passing from my outer cucumber tests as I go. Eventually, the cucumber tests will drive a browser (using a terminal headless browser called [capybara-webkit](https://github.com/thoughtbot/capybara-webkit)).

This approach has really disciplined me in how I approach a new feature and helped me to stay focused on building what is needed instead of trying to do too much. It's also centralized my business logic in objects within the application instead of Rails itself.

I'm hoping to get some feedback from the Rails community to improve the process and the tools some more, but having gone through the process several times, I believe it can really help -- especially when dealing with existing complex applications.
