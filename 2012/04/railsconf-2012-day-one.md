---
author: Steph Skardal
title: 'RailsConf 2012: Day One'
github_issue_number: 598
tags:
- conference
- javascript
- rails
date: 2012-04-23
---



Today kicks off the official first day of RailsConf 2012, in Austin, Texas (yesterday RailsConf unofficially kicked off with [Ignite Rails](http://railsconf.austinonrails.org/ignite)). This is my fourth RailsConf, and I’ve found that I get increasingly more out of each one as my time working with Rails has accumulated.

The morning started with a keynote by [DHH](https://en.wikipedia.org/wiki/David_Heinemeier_Hansson). DHH talked about progress and keeping an interest in something because it continues to make progress. Initially, the Rails community had a negative reaction to progress like Ruby 1.9, Rails 3, the [Asset Pipeline](http://guides.rubyonrails.org/asset_pipeline.html) and CoffeeScript, but after the initial learning curve, the new tools and progress was appreciated by the community. DHH talked about how there have been many studies on what prevents people from progressing, and one of those causes is loss aversion, meaning that people hate losing or failing enough that it prevents them from advancing. To me, the point of his talk was to prepare everyone for Rails 4 and how it will challenge and break things. Rails 4 is admittedly not coming out anytime soon, so he didn’t touch on any specifics.

### Using Backbone.js with Rails

One session talk I attended was *Using Backbone.js with Rails* by [Sarah Mei](http://www.sarahmei.com/blog/) of Pivotal Labs. Backbone is not an MVC framework in JavaScript, but it is lumped into traditional JavaScript MVC frameworks. It serves as a lightweight infrastructure for organizing code like templates, interactive elements, and events. Because Backbone is a relatively immature framework, like other JavaScript frameworks, there isn’t a standard way of writing code, so the implementation of Backbone varies widely.

Sarah talked about the love story between JS and Rails:

<img border="0" src="/blog/2012/04/railsconf-2012-day-one/image-0.jpeg" width="750"/>

She touched on the basics of Backbone from a Rails perspective:

- Models: Backbone and Rails models are very similar. An application will likely have Backbone models that mirror Rails models.
- Templates: Backbone templates are akin to Rails views or a [mustache template](https://mustache.github.io/).
- Views: Views are similar to Rails controllers. They set a template, class name, and define events.

Next, Sarah talked about two methods of implementation using Backbone.js and went through some code examples:

- Greenfield App

        - This approach tends to be more API driven and makes sense for an API-driven application that also requires buildout of native mobile apps.
        - In this approach, the server side returns [JSON, etc.] data and doesn’t render HTML.
        - Sarah noted that the amount of code required here can be substantial because the framework is lightweight, so she would recommended considering alternatives (such as ember.js).

- “Backbone as Frosting” Implementation

        - In this implementation, there is a mixture of server-side and client-side rendering.
        - Sarah noted here that the lightweightedness of Backbone works nicely.

I haven’t used Backbone.js in any client projects, but I’ve looked into it recently out of interest. I like the general idea of improving JavaScript code organization via the frosting approach described by Sarah. A few code examples were shared during the presentation — check out the slides [here](https://speakerdeck.com/sarahmei/using-backbone-dot-js-with-rails).

### CoffeeScript for the Rubyist

 

Another talk I attended today was *CoffeeScript for the Rubyist* by [Mark Bates](http://metabates.com/). CoffeeScript is a JS meta language
that compiles into JS and can easily integrate with your current JavaScript. It’s easy to read, write, and maintain.
I took the CoffeeScript lesson over at [Code School](https://www.codeschool.com/) recently (highly recommended!). Mark went through a brief history of JavaScript and explained that like
the evolution to early assembly languages to C to Ruby (with a few missing steps), CoffeeScript’s aim is to
be an improved tool for writing readable and maintainable code. The syntax of CoffeeScript is 
a hybrid of Ruby and Python which is simple, uses no semicolons, typically no curly braces, no “function”
keyword, relaxed parenthesis, and significant whitespace.

Mark then went into a review of Ruby-like CoffeeScript behavior. Below are some of the important topics in CoffeeScript that he covered, as well as links to the documentation:

- [conditionals similarity (inline, postfix)](https://coffeescript.org/#conditionals)
- objects and hashes are similar (can’t screw up last comma)
- [ranges](https://coffeescript.org/#slices)
- [string interpolation](https://coffeescript.org/#strings)
- [heredocs](https://coffeescript.org/#strings), (""" works)
- [functions](https://coffeescript.org/#literals) Ruby 1.9 Lamda syntax is similar to CoffeeScript version
- default arguments
- [splats](https://coffeescript.org/#splats) (e.g. first, second, others...)
- loops and comprehensions (for number in numbers)
- combination of loops and comprehensions and conditionals
- [classes](https://coffeescript.org/#classes)
- [inheritence](https://coffeescript.org/#classes) (e.g. class Manager extends Employee)
- [Bound functions](https://coffeescript.org/#fat_arrow) (with a fat arrow)
- Existential operator (e.g. if foo?, if console?.log "foo")

In addition to the talks on Backbone.js and CoffeeScript, I’ll post the links to slides and video for the other talks I attended when they become available.

### What’s Next?

It’s funny (but not surprising) how many of the talks I attended on Day One weren’t actually about Rails or the specifics of Rails. Perhaps I’ll try to pick a few more Rails-centric talks in the next couple of days of the conference and report on those. Stay tuned!


