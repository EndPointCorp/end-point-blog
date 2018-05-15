---
author: Steph Skardal
gh_issue_number: 1121
tags: conference, rails
title: 'RailsConf 2015—​Atlanta: Day Three'
---

Today, [RailsConf](https://railsconf.com/2015/) concluded here in Atlanta. The day started with the reveal of this year’s [Ruby Heroes](http://rubyheroes.com/), followed by a Rails Core panel. Watch the video [here](http://confreaks.tv/videos/railsconf2015-ruby-heroes-awards).

### On Trailblazer

One interesting talk I attended was [See You on The Trail](http://confreaks.tv/videos/railsconf2015-trailblazer-a-new-architecture-for-rails) by [Nick Sutterer](https://github.com/apotonick), sponsored by [Engine Yard](https://www.engineyard.com/), a talk where he introduced [Trailblazer](https://github.com/apotonick/trailblazer). Trailblazer is an abstraction layer on top of Rails that introduces a few additional layers that build on the MVC convention. I appreciated several of the arguments he made during the talk:

- MVC is a simple level of abstraction that allows developers to get up and running efficiently. The problem is that everything goes into those three buckets, and as the application gets more complex, the simplified structure of MVC doesn’t answer on how to organize logic like authorization and validation.
- Nick made the argument that DHH is wrong when says that microservices are the answer to troublesome monolithic apps. Nick’s answer is a more structured, organized OO application.
- Rails devs often say “Rails is simple”, but Nick made the argument that Rails is easy (subjective) but not simple (objective). While Rails follows convention with the idea that transitioning between developers on a project should be easy if conventions have been followed, in actuality, there is still so much interpretation into how and where to organize business logic for a complex Rails application that makes transition between developers less straightforward and not simple.
- Complex Rails tends to include fat models (as opposed to fat controllers), and views with [not-so-helpful] helpers and excessive rendering logic.
- Rails doesn’t introduce convention on where dispatch, authorization, validation, business logic, and rendering logic should live.
- Trailblazer, an open source framework, introduces a new abstraction layer to introduce conventions for some of these steps. It includes [Cells](https://github.com/apotonick/cells) to encapsulate the OO approach in views, and [Operations](https://github.com/apotonick/trailblazer#operation) to deserialize and validate without touching the model.

There was a Trailblazer demo during the talk, but as I mentioned above, the takeaway for me here is that rather than focus on the specific technical implementation at this point, this buzzworthy topic of microservices is more about good code organization and conventions for increasingly complex applications, that encourages readability and maintenance on the development side.

I went to a handful of other decent talks today and will include a summary of my RailsConf experience sharing links to popular talks on this blog.
