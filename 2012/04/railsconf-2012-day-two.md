---
author: Steph Skardal
title: 'RailsConf 2012: Day Two'
github_issue_number: 600
tags:
- conference
- performance
- ruby
- rails
date: 2012-04-24
---

I’m here in Austin for Day 2 of RailsConf 2012. Here’s a quick run-down of a few talks I attended today. Read about a couple of sessions I attended on Day 1 [here](/blog/2012/04/railsconf-2012-day-one/).

### Let’s Make the Web Faster

One of the talks I attended on Day 2 was *Let’s Make the Web Faster — tips from the trenches @ Google* by [Ilya Grigorik](https://www.igvita.com/). Ilya works on the MTWF (make the web faster) team at Google; one of their goals is not only to make Google’s web applications faster, but also to make a bigger impact on web performance by developing and contributing to tools. I found a few main takeaways from Ilya’s talk:

- [Navigation Timing Spec](https://web.archive.org/web/20120504042036/http://test.w3.org/webperf/specs/NavigationTiming/): The navigation timing spec defining an interface for web applications to access timing information related to navigation and elements. You can look at this timing information by checking out the performance object in a console:

<img border="0" src="/blog/2012/04/railsconf-2012-day-two/image-0.jpeg" width="600"/>
Example output of navigation timing spec data.

- Site Speed Tools in Google Analytics: Google Analytics now has elements of the page speed broken down that allows you to compare page load times and examine what the bottlenecks in the system are. To get there, you go to Content => Site Speed => Page Timings in Google Analytics. You can also measure and examine this data using Segments and Advanced segments.
<img border="0" src="/blog/2012/04/railsconf-2012-day-two/image-1.png" width="600"/>
Example metrics shown on Google Site Speed breakdown.
- [WebPageTest.org](https://www.webpagetest.org/) is a tool that we’ve blogged about before a few times. Now it also provides a video of how the page loads to examine how the page load is perceived.
- [Speed Index](https://sites.google.com/a/webpagetest.org/docs/using-webpagetest/metrics/speed-index): Speed index is a new metric for measuring “visual completeness” of a page loading. This is an interesting/valuable metric to look at when you want to try to understand and improve user perceived latency. For example, can you force loading some images before peripheral scripts to improve the user perceived latency?
- A few Google tools that Ilya reviewed were [PageSpeed Online](https://developers.google.com/speed/pagespeed/insights/) and its API, [PageSpeed SDK](https://code.google.com/archive/p/page-speed/wikis/DownloadPageSpeed.wiki), and [PageSpeed Service](https://developers.google.com/speed/pagespeed/service), which is in beta mode.
- Ilya’s recap was that you should a) measure performance b) optimize performance (with specific attention to
improve user perceived latency) and c) use tools to automate performance.

Check out the full presentation [here](https://www.igvita.com/slides/2012/railsconf-making-the-web-faster/#1).

### Presenters and Decorators: A Code Tour

Another talk I attended was *Presenters and Decorators: A Code Tour* by [Mike Moore](http://blowmage.com). He started with a brief explanation of the justification (more later) for presenters — as a “pain driven developer”, Mike tries to reduce the pain of advanced view logic with presenters. Mike then went through a complex example of rendering which mapped through a view to a helper to an app/component file to a class in the library back to the app to a haml view; this is painful to dissect, maintain, and test, so presenters are a good option here to avoid this spaghetti code.

Mike then went through coding examples and thought processes that lead to using a presenter-like solution. He presented an example where a view contained view-specific logic and instantiation and use of variables. The natural first step for refactoring the view here would be to pull the logic into the model, but the argument against this is that because it’s view specific (as opposed to domain specific), it should not live in the model. Another progression step in pulling the logic out of the view would be to create a class that’s initialized in the view, and the various instance methods on that class are called in the view. Here Mike introduced the [ActiveDecorator](https://github.com/amatsuda/active_decorator) plugin. This plugin automagicallly includes class decorators for instances in the view, which eliminates the need for instantiation of the presenter object. Mike also reviewed a standard serialization example, where a JSON-ified view can have logic that should probably live elsewhere. One option here is to create a class serializer option which has methods to render data to json. Another option here is to use [ActiveModel::Serializers](http://api.rubyonrails.org/classes/ActiveModel/Serializers.html) which looks for the rendering of JSON to remove logic from the JSON rendering view. These examples and another thorough code example are best
viewed [in the slides](https://speakerdeck.com/blowmage/presenters-and-decorators-a-code-tour).

Mike explained that it’s difficult to define Presenters and that he perceives presenters on a spectrum between the model and view which is an object that represents state and behavior of the view. The justification for presenters is to write easier to read, easier to maintain, easier to hand off to a designer, and easier to test code. Mike also noted that this isn’t something that a Rails noob should get into *and* also that if it’s a problem that you don’t see in your code base, it’s not a problem you necessarily need to solve.

### Ten 42 Things You Didn’t Know Rails Could Do

Another fun talk I attended on Day 2 was *Ten Things You Didn’t Know Rails Could Do* by
[James Edward Gray II](http://graysoftinc.com/). In list-presentation style, James
reviewed 42 things you can do with Rails that you might not know about [which work in Rails 3.2.3 and may or may not work in previous versions of Rails]. This talk reminded me of some of the protips I picked up from taking the Rails Best Practices course over at [Code School](https://www.codeschool.com/) because there were so many usable tips. I summarized the presentation into my own list of takeaways, but note that I left out some of the advanced tips that required extensive code examples. View the slides [here](https://speakerdeck.com/jeg2/10-things-you-didnt-know-rails-could-do).

- The command rake notes will output all your FIXME, TODO, and OPTIMIZE notes in your Rails application. You can also
pass in custom annotations to output here as well.
- In the console, you can call helper methods (e.g. helper.number_to_currency(100)
- You can automagically add indexes via migration shorthand (e.g. rails g resource user name:index). And you can
automagically add associations (e.g. rails g resource article user:references or rails g resource article:belongs_to)
via migration shorthand.
- rake db:migrate:status will tell you where your migration is at
- You can use the pluck command instead of the map command. (e.g. User.pluck(:email), User.uniq.pluck(:email))
- You can override association methods to “hook” in custom behavior.
- You can use limitless strings in PostgreSQL. This requires a bit of code shared in the presentation. I know, my fellow PostgreSQL expert coworkers are going to balk that this is on the list, but unfortunately Rails doesn’t allow this without some code.
- You can utilize PostgreSQL’s full text search with a bit of code.
- You can use a different database for each user. This one could be great for multi-domain ecommerce, which I [recently blogged about](/blog/2012/02/multi-store-architecture-ecommerce/).
- You can merge nested hashes via the [deep_merge](https://apidock.com/rails/Hash/deep_merge) method.
- You can remove a specific key from a hash via the [except](https://apidock.com/rails/Hash/except) method.
- You can add defaults to a hash without overriding via the [reverse_merge](https://apidock.com/rails/Hash/reverse_merge) method.
- You can override form helpers, and a lot of other view stuff, but this was a little hard to encapsulate in a blog post, so it’ll be best viewed in the slides.
- You can route exceptions (e.g. match “/404”, to “errors#not_found”)
- You can route to Sinatra. The example James gave here was to allow display of the Resque web interface inside a Rails application, but we have another client who would benefit from this technique as well.

### Ta Da

Hopefully this article was more Rails-ey than yesterday’s [RailsConf 2012: Day One](/blog/2012/04/railsconf-2012-day-one/) post which focused on Backbone.js and CoffeeScript. I’m looking forward to a couple of tomorrow’s sessions—​and hopefully they will be blogworthy. Stay tuned!
