---
author: Steph Skardal
gh_issue_number: 315
tags: conference, ecommerce, ruby, rails, spree
title: 'RailsConf 2010 Rate a Rails Application: Day One, Session One'
---

My first session at RailsConf 2010 was one that I found valuable: *12 hours to Rate a Rails Application* presented by Elise Huard. Elise discussed the process of picking up a Rails application and analyzing it, rather than being the developer who develops a Rails application from scratch. This is particularly valuable because I’ve had to dive into and comprehend Rails projects more in the last few months. I’d imagine this will become more common as Rails matures and legacy code piles up. Elise mentioned that her motivation for application review comes from either acquisition or for project maintenance. Below is the 12-hour timeline covered by Elise:

### 0:00: Team Overview

First, Elise suggests that speaking to a team will reveal much about the application you are about to jump into. In our case at End Point, we often make up part of or all of the development team. She briefly mentioned some essential personality traits to look for:

- control freak: someone who worries about details and makes other people pay attention to details
- innovator: someone who looks for the next exciting things and doesn’t hesitate to jump in
- automator: people who care about process, more sys admin side of things
- visionaries
- methodologizers (ok, i made this word up): someone who has long term planning ability, road mapping insight
- humility: important to be open to understanding code flaws and improve

Of course, there’s overlap of personality traits, but the point is that these traits are are reflected in the code base in some way or another. Elise briefly mentioned that having an issue tracker or version control is viewed positively in application review (of course).

### 2:00: Systemic Review

The next step in a Rails application evaluation is running the app, making sure it works, examining the maintainability, rails version, and license. She also discussed avoiding the [NIH syndrome](https://en.wikipedia.org/wiki/Not_invented_here) during a review, which I interpreted as reviewing the code and avoiding thinking about reinventing of the wheel and taking the code and functionality as is (not sure I interpreted her intentions correctly) rather than immediately deciding that you would rewrite everything. Additional systemic indications of a good application are applications that use open source gems or plugins that are maintained and used by others, and that the application has passing tests.

### 3:00: Start Digging Around

The next step in a 12-hour Rails application review should be an initial poke around of the code. Elise likes to look at config/routes.rb because it’s an interface application to the user and a good config/routes.rb file will be a representative inventory of the application. Another step in the review is to examine a model diagram, using a tool such as the railroad gem, or via rubymine. Another good overview is to examine how parts of the application are named, as the names should be understandable to someone in the business.

### 3:30: Metrics, Tools

Elise’s next step in application review is using several metrics to examine complexity and elegance of code, which covered several tools that I haven’t heard of besides the common and popular (already mentioned a few times at RailsConf) WTF-metric.

<a href="/blog/2010/06/08/railsconf-2010-review-rails-application/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5480491211053307922" src="/blog/2010/06/08/railsconf-2010-review-rails-application/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 377px;"/></a>

An overview of the tools:

- “rake stats”: lines of codes, methods, etc. per controllers, helpers, models
- [parsetree’s ruby_parser](https://web.archive.org/web/20100710141128/http://parsetree.rubyforge.org/ruby_parser/): code transformed into an abstract syntax tree
- flog: analysis of code complexity based on the ABC (Assignment Branch Condition) metric
- flay: analysis for similarity between classes
- [saikuro](https://github.com/metricfu/Saikuro): analysis of [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [roodi](https://github.com/roodi/roodi): detection of antipatterns using the visitor pattern
- reek: detection OO code smells
- rails_best_practices: smell for rails antipatterns
- churn: metrics on change of code run on version control history
- rcov: analysis of code coverage
- [metric_fu](https://github.com/metricfu/metric_fu): tool aggregate that includes many of above tools

Elise noted that although metrics are valuable, they don’t identify bugs, analyze code performance and don’t analyze the human readability of the code.

### 5:30: Check out the good stuff

Next up in an application review is looking at the good code. She likes to look at the database files: is everything in the migrations? is the database optimized sensibly? Occasionally, Rails developers can become a bit ignorant (sorry, true) to data modeling, so it’s important to note the current state of the database. She also looks at the views to analyze style, look for divitis, and identify too much JavaScript or logic.

### 7:30: Test Code Review

The next step in Elise’s review of a Rails application is checking out the test code. As implementation or requirements change, tests should change. The tests should express code responsibility and hide the implementation detail. Tests should reveal expressive code and don’t necessarily need to follow the development DRY standard.

### 9:30: Deployment Methodology Review

Another point of review is to understand the deployment methodology. Automated deployment such as deployment using capistrano, chef, etc. are viewed positively. Similar to software development tests, failures should be expressive. Deployment is also viewed positively if performance tests and/or bottleneck identification is built into deployment practices.

### 11:00: Brownie Points

In the final hour of application review, Elise looks for brownie-point-worthy coverage such as:

- continuous integration
- documentation and freshness of documentation
- monitoring (nagios, etc.), exception notification, log analyzers
- testing javascript

I found this talk to be informative on how one might approach understanding an existing rails application. As a consultant, we frequently have to pick up a project and **just go**, Rails or not, so I found the tools and approach presented by Elise insightful, even if I might rearrange some of the tasks if I am going to write code.

The talk might also be helpful in providing details to teach someone where to look in an application for information. For example, a couple of End Point developers are starting to get into Rails, and from this talk I think it’s a great recommendation to send someone to config/routes.rb to learn and understand the application routing as a starting point.
