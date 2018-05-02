---
author: Steph Skardal
gh_issue_number: 279
tags: conference, rails, ruby
title: MountainWest RubyConf 2010 - Steph's Notes
---

Last Thursday and Friday, I attended [MountainWest RubyConf](http://mtnwestrubyconf.org/2010/) in Salt Lake City. As usual with any conference, my notebook is full of various tools and tips jotted down for later investigation. I thought I'd summarize some of the topics that grabbed my interest and go more in depth on a couple of topics in the next couple of weeks.

- **Lambda:** In a talk early in the conference, lambda in Ruby came up. I had a hard time coming up with use cases for its use in Rails or a web app in another server side language with equivalent functionality (Python, Perl), but I'd like to look into it. An example was presented using Ruby's lambda to calculate Google's PageRank value, which is particularly appealing to my interest in SEO.
- **Chef:** I've heard of [Chef](http://wiki.opscode.com/display/chef/Home) since I started working with Rails, but have yet to use it. After my recent adventures with [Spree on Heroku](/blog/2010/03/08/spree-heroku-development-environment), I see the value in becoming more familiar with Chef or another configuration management software tool such as [Puppet](http://reductivelabs.com/products/puppet/). I'm particularly interested in creating some Chef recipes for Spree.
- **RVM:** [RVM](http://rvm.beginrescueend.com/), or Ruby Version Manager, is a nice tool to work with multiple Ruby environments from interpreters to sets of gems. For a couple of I/O-intensive Rails apps that I work on, I'm interested in performance benchmarking across different Ruby environments to investigate the business case for updating Ruby. RVM also provides functionality for gem bundle management, which might be of particular value when testing code and applications running from different gem versions.
- **Rails 3:** I'm pretty excited for Rails 3. [Yehuda Katz](http://yehudakatz.com/) talked about Rails topics such as [method aliasing](http://whynotwiki.com/Ruby_/_Method_aliasing_and_chaining) and method lookup. He talked a bit about how the lack of modularity hurts development, and modularity in code may be defined as reducing assumptions to increase reuse. He also struck a chord with me when he talked about premature optimization: making decisions about modularity or functionality before it's needed and how this can be a mistake. I read some documentation on Rails 3 over the weekend and am looking forward to its release.
- **Rack and Sinatra:** I haven't spent much time playing around with Rack or Sinatra, but have certainly heard a lot about these tools. There was a nice lightning talk given on how to create a simple ecommerce site in a very short time using the active merchant gem (also used by Spree), Sinatra, Rack, and the Rack/Payment gem. I'd like to expand on this in a blog post later.
- **NoSQL:** While Jon and I attended this conference, Ethan Rowe attended the [NoSQL Live](http://nosqlboston.eventbrite.com/) conference in Boston that he blogged about [here](/blog/2010/03/12/nosql-live-dynamo-derivatives-cassandra) and [here](/blog/2010/03/11/quick-thoughts-on-nosql-live-boston). There was a decent talk at MWRC on MongoDB with some examples on data interactions. The speaker discussed how NoSQL data "would be great" for CMS systems because of the diversity and amount of unknown attributes. I'm not quite sure I agree with that statement, but I'm interested in learning more about the business cases for NoSQL.
- **A couple of random book recommendations:**

        - [Programming from the Ground Up](http://www.amazon.com/Programming-Ground-Up-Jonathan-Bartlett/dp/0975283847) - recommended as a decent book for high-level programmers interested in learning about low-level programming
        - [Design Patterns](http://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612) - includes **no** examples of Java, with examples of C++ and Smalltalk
        - [Refactoring](http://www.amazon.com/Refactoring-Improving-Design-Existing-Code/dp/0201485672) - another recommended read

- **Random tools:**

        - git hooks with gitty
        - git instaweb to browse git file structure and commit history without an internet connection
        - memprof - profiler to watch for object allocations in Rails
        - yardoc - documentation tool for ruby
        - ruby-processing - a data visualization tool

- **Productivity and Happiness:** A common principle that comes up in Ruby/Rails conferences: A happy developer yields good productivity which leads to a happy developer. And Ruby/Rails makes developers happy, right? Well, I can't speak for anyone else, but I like Ruby.

As I said before, I hope to dig more into a couple topics and blog about them later.
