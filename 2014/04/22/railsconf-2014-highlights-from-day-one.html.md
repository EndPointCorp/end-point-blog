---
author: Steph Skardal
gh_issue_number: 967
tags: conference, ruby, rails
title: 'RailsConf 2014: Highlights from Day One'
---

<div class="separator" style="clear: both; float: right; padding-bottom: 1em; text-align: center; width: 300px; margin-left: 1em;"><img border="0" src="/blog/2014/04/22/railsconf-2014-highlights-from-day-one/image-0.jpeg" style="margin-bottom:2px;" width="300"/>
<small>The Best Conference Sidekick</small></div>

I’m here in Chicago for RailsConf 2014, my fifth RailsConf! This time I’m attending the conference with my sidekick, and of course my sidekick’s babysitter, so I’m having an experience a bit different than previous attendance.

### The Bees Knees

One of the first talks I attended today was *Saving the World (literally) with Ruby on Rails* by Sean Marcia.

Sean works with a Professor at George Mason University who researches bees and dying colonies. Armed with [Raspberry Pis](https://www.raspberrypi.org/) powered by solar panels, Sean uses the following technologies to monitor beehive metrics:

- gpio, pi_piper, wiringpi-ruby
- [dashing](http://dashing.io)
- Ruby & Sinatra. Sean had previously used Rails but found it a bit too heavyweight and went with a lighter Sinatra app.
- 3 Cronjobs to record data
- passenger, isc-dhcp-server, hostapd, iw for server configuration

Hive temperature, hive weight, outside temperature, and humidity are monitored in hopes of collecting metrics for identifying collapsing hives. The project is quite young, but the hope is to collect more metrics (e.g. gas permeability) and more actionable data as time goes on.

### Views as Objects

Another interesting and relevant talk I attended today was *Where did the OO go? Views should be objects too!* by Andrew Warner. Andrew believes the Rails Holy Grail is an app that provides the best user experience and the best development experience. What is the best user experience? One with fast page loads or rather, one that does not require full page loads. What is the best dev experience? One that is developer friendly, DRY, allows for a client with logic (what Andrew called a thick client), mostly one language, and one that has good SEO.

In the [node.js](https://nodejs.org/) space, [rendrjs](https://github.com/rendrjs) is a popular tool that addresses all the main points, except it’s not in Rails. Andrew then went on to discuss the current approaches in Rails:

- duplicate code that lives on client & server (e.g. a mustache template and an erb template). This approach doesn’t follow DRY and is not written utilizing one language.
- [turbolinks](https://github.com/rails/turbolinks): covers everything except thick client
- the ember / angular / backbone approach, where the entire app lives on client. This approach is not SEO friendly and not in one language.

Each of these above options has a key tradeoff when measured against the main criteria. The lowest common denominator between the client and server (i.e. the dumbest possible templates) would be mustache, which happens to be available in Ruby and JavaScript. Mustache has tags, booleans, and loops, so it has the most simple “logic” that one might need in a view.

Andrew created a gem called [perspectives](https://rubygems.org/gems/perspectives), which is a Ruby class that returns JSON or HTML based on the type of request based on a single mustache template. The Ruby class accepts objects and arguments and outputs and renders an HTML request for initial requests and JSON for subsequent requests. Perspectives also offers a nice separation of concerns, because the view is quite dumb it can’t contain advanced logic other than basic conditionals and loops, so this logic is contained in the perspective object. The output of perspectives is easy to test, and it leverages Rails Russian doll caching strategy.

Andrew didn’t focus too much on his gem, but the story that he told regarding the problem and various approaches was accurate and relevant to experiences I’ve had. I’d love to see how I can leverage the tool that he’s written.

### Arel

Another very technical talk I attended today was *Advanced aRel: When ActiveRecord Just Isn’t Enough* by Cameron Dutro. This is one of those talks that ended up being something different than I expected, but the technical points were interesting and in depth. aRel is not the same thing as ActiveRecord. Here are several points that Cameron touched on during the talk:

- aRel is relational algebra that allows you to build SQL queries, applies query optimizations, and enables chaining.
- aRel knows nothing about your models and database and does not retrieve or store data (which is what ActiveRecord does)
- aRel generates ASTs, which are trees that represent queries
- aRel has many methods for selects, supports methods like .minimum, .maximum, and .sum, but also supports other arbitrary methods supported by the database such as length.
- aRel supports subqueries.
- aRel supports where methods like eq, not_eq, gt, lt, gteq, lteq
- aRel supports outer joins, has and belongs to many relationships.
- aRel supports fuzzy matching (e.g. matches('%test%'))
- The use of aRel is chainable and does not use strings.
- aRel has a query builder that is essentially an module that has encapsulated finder methods which provides cleaner and more reusable methods

Cameron created [scuttle-rb](https://github.com/camertron/scuttle-rb), which is a Ruby library for converting raw SQL into ActiveRecord/aRel queries, and he runs this library on a server that is publicly accessible. There were many great code examples but it was hard to catch a lot of them, so I’ll provide a link to the talk when it’s available.

Stay tuned for more blog posts on the remaining three days of the conference!
