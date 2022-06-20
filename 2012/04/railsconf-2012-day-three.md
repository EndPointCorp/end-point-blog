---
author: Steph Skardal
title: 'RailsConf 2012: Day Three'
github_issue_number: 601
tags:
- conference
- ruby
- rails
date: 2012-04-25
---



It’s Day 3 of RailsConf 2012 here in Austin Texas. Check out my posts from [Day 1](/blog/2012/04/railsconf-2012-day-one/) and [Day 2](/blog/2012/04/railsconf-2012-day-two/).

### RailsConf 5k

To kick off the day, I ran the low-key RailsConf 5k along the lake here in Austin. I’m glad that this event was organized —
I think it’s good to take a mental break from all the conference activities.

### RubyRogues

This morning kicked off with a [RubyRogues](https://devchat.tv/ruby-rogues) live session. The topic for today’s podcast was a discussion about what Rails developers care about and/or should care about. I thought that the answers apply to developers in general. Below are some of the topics covered in the talk.


- [James Edward Gray II](http://graysoftinc.com/)

        - James focused on the point that experimentation is important and to perceive all code as experimental.

- [Avdi Grimm](https://twitter.com/avdi)

        - Avdi’s main argument was a suggestion to practice deliberate and mindful coding. While he believes 
that there is a place for the “shut up and code” mentality in some projects depending on risk, it’s not acceptable to have this perspective when it comes to community sharing of knowledge.
        - Avdi recommends that exercising introspection by reviewing your code and explaining it to someone else (how and why) will make you a better programmer and communicator.

- David Brady

        - David shared that Ruby is not a [block oriented](http://www.functionblocks.org/Introduction.html) [lexically scoped](http://en.wikipedia.org/wiki/Scope_(computer_science)#Lexical_scoping_and_dynamic_scoping) language.
        - He suggests that you should a) learn Ruby as if it’s unlike the other languages you know b) learn CoffeeScript because it 
writes better JavaScript than you will c) join the community and d) don’t be a douchebag (translation: be humble, not arrogant)
because d-bags make a bad stereotype for Rails programmers

- [Josh Susser](http://blog.hasmanythrough.com/)

        - Josh suggests to exercise prudence, or acting with or showing care and thought for the future by building a strong foundation.
        - He also discussed how while he agrees with comments of previous keynotes (loss aversion is pillar of conservatism, experienced
developers have a lower tolerance for technical debt), that he also has the perspective that he has a limited budget for risk 
in projects. From his experience, bundler was a huge win in minimizing risk, but asset pipeline (in its current state) spent all
of his risk budget.

- Charles Max Wood

        - Charles focused on how the Rails community should try to encourage and bring other developers to the community by evangelizing it. We should reach out to other communities and groups to encourage them to try Rails.

### Lightning Talks

The last session I attended at RailsConf was the Lightning Talk session. I know I’ve abused lists in my RailsConf posts a bit, but Lightning Talks are meant to be presented in list form! Here’s a quick rundown of some of the topics presented in the Lightning Talks, which were a mix of 1-minute and 5-minute talks. I’ll update with more links as they become available.

- [NSRails](https://github.com/dingbat/nsrails) is a gem that bridges objective-C and rails, and will give Objective-C a bunch of methods similar to Rails methods (.all,.find(x), CRUD behavior)
- [WindTunnel](https://github.com/thatdutchguy/windtunnel) is a JavaScript testing framework without hassle.
- config.threadsafe is a setting in configuration that allows threading. Tony Arcieri provided a lot more details — I’ll update this post to include a link to the slides later.
- Worker is a threading JavaScript tool.
- [iwanttolearnruby.com](http://iwanttolearnruby.com/) is a resource for Ruby/Rails learning resources
- @marksim talked about how private teams should work like open source by a) doing more code reviews and b) using distributed communication tools like HipChat, Campfire, IRC, message boards, mailing lists, internal blogs, Google+ Hangout, and Skype to have success like open source does.
- [sidekiq](https://github.com/mperham/sidekiq) is a distributed message queue (like resque)
- erd is a gem that was written during RailsConf to allow visualization and changes of the database. I’ll post a link to it when it becomes available.
- [Rowe](http://www.gorowe.com/) is a development technique that means trading results for money (as opposed to time).
- The [job_interview](https://github.com/ruby-jokes/job_interview) gem is a silly (and extremely entertaining) gem created during RailsConf for helping you answer those tough interview questions.
- In Rails Engines, routes should a) always be drawn on the engine, and b) the engine should call isolate_namespace.
- [Tokaido](https://yehudakatz.com/2012/04/13/tokaido-my-hopes-and-dreams/) is a kickstarter project that Yehuda’s been working on.
- [railcar](https://github.com/arcturo/Railcar) is an isolated, compiler-optional Rails environment.
- [ninjascript](https://github.com/LRDesign/NinjaScript) is a JavaScript tool for unobtrusively adding event listeners, and more.
- [tddium](https://twitter.com/tddium) is a continuous testing integration tool.
- [wicked](https://github.com/schneems/wicked) is a gem for rendering wizards.
- [flash_s3_rails](https://github.com/shwoodard/flash_s3_rails) is a gem for embedding a multi-file upload widget into your application.
- [javascript-and-friends](https://groups.google.com/forum/#!forum/javascript-and-friends) is a Google Group for discussing and acting on embedding JavaScript in Ruby.
- [graphite](https://graphiteapp.org/) is a scalable real-time monitoring tool.

### A Little Bit More...

I also attended Yehuda Katz’s talk on Rails: The Next Five Years. I’m saving a write-up on this for another post, because I’d like to wrap it in with some of the other keynotes discussions.


