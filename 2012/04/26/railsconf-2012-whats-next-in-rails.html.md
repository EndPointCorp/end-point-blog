---
author: Steph Skardal
gh_issue_number: 602
tags: conference, rails
title: 'RailsConf 2012: What''s Next in Rails?'
---



I tend to walk away from every RailsConf feeling that there was a trend for each conference. In 2009, I thought the trend was Passenger, in 2010, NoSQL and Rails 3 was all the rage, and in 2011, many of the talks were related to CoffeeScript and SASS. While there was some of these technical specifics at this conference, I felt that the overarching trend this year is that several folks that are extremely involved in Rails ([DHH](http://en.wikipedia.org/wiki/David_Heinemeier_Hansson), [Yehuda Katz](http://yehudakatz.com/), [Aaron Patterson](http://tenderlovemaking.com/), etc.) are very passionately involved in the course correction needed to keep Rails relevent.

As I mentioned in my [blog article on Day 1](http://blog.endpoint.com/2012/04/railsconf-2012-day-one.html), DHH talked about progress. DHH focused on the limitations of progress ([loss aversion](http://en.wikipedia.org/wiki/Loss_aversion)) and how and why people move from curious to suspicious when working with technology. He didn't delve into any of the Rails 4 details, but simply ended by sharing that Rails 4 will break and challenge things.

On Day 2, Aaron Patterson covered a discussion about what it means to incur technical debt, and how developers have different thresholds of how much technical debt is tolerated.

<img border="0" src="/blog/2012/04/26/railsconf-2012-whats-next-in-rails/image-0.jpeg" width="750"/>

He talked about the types of refactoring needed to reduce technical debt. He ended his talk with a slide that said, "be prepared", which I understood to mean that there's a lot of movement, deep consideration, and no doubt passion. Aaron also participated in a Rails core panel on Day 2. While it was thoroughly entertaining (coloring book contest included!), there was some discussion over where Rails is going and the various perspectives. Aaron talked about how he is critical of Rails because he cares a lot, and the critical analysis of Rails is happening to keep Rails relevent in the future.

On Day 3, Yehuda Katz presented his talk on [Rails: The Next Five Years](http://dl.dropbox.com/u/2285145/The%20Next%20Five%20Years.pdf). Katz noted that his perspective is not representative of the core team nor of his employer, that he comes from the perspective of developing very rich client-side web applications (that may also translate to mobile applications), *and* that part of the justification of his talk was to evangelize some of the technical features that he believes should be included in the core to keep Rails relevant.

For him, every time his company starts a new project and reevaluates whether Rails meets their needs means that something about Rails isn't working right now. Yehuda covered his examination of why Rails was great in the first place. And the underlying answer to that is convention over configuration. Rails eliminates trivial choices like code organization, assets, naming, routing, etc. and there is a shared benefit in this solution with convention. Gaining deep knowledge about hard problems is hard (e.g. [CSRF prevention](http://en.wikipedia.org/wiki/Cross-site_request_forgery)) and Rails makes these decisions for us with convention. Yehuda's perspective is [now] that any convention is better than no convention, because adding any convention upfront will allow something to be built out and improved incrementally over time rather than introducing divergent paths for trivial decisions.

<sidebar>

Yehuda took a short time in his talk to discuss justification for getting things in the core, even if they need follow-up iterations:

1. Getting new features into core gets a lot of eyeballs on it.
1. More importantly, getting new features into core gets a lot of eyeballs attached to people who 
have a lot of domain expertise on the problem that the feature is solving.
1. Getting new features into core helps reveal conceptual blindspots and additional required functionality.

</sidebar>

After talking about Rails and his desire to get new relevent features into Rails from at a high level,
Yehuda dug into a few specific wants:

- serialization: This took up a large proportion of the talk. I can't give justice to everything 
covered here, so check out [the slides](http://t.co/G4j1Xdrl) and I'll post a link to the video later.
- bulk editing
- better convention for application structure (e.g. assets)
- API between JS framework and Rails, as the popularity of JS frameworks grows

<img border="0" src="/blog/2012/04/26/railsconf-2012-whats-next-in-rails/image-1.jpeg" width="750"/>
Coding with convention (middle) allows developers* to avoid making diverging trivial decisions (left). Conventions provide the ability to share resources and domain expertise and add new features quickly, even if course correction (right) is needed on those conventions.

* not to be confused with sperm :)

### What Now?

I think what Yehuda said during QnA resonated with me most: **Decoupling the data from the representation is really important because the data then becomes represented in a variety of ways.** Because of the extremely quick growth in technology and tools of various media consumption devices (browser, mobile web, native client apps), data is represented in an increasing number of ways and with varied degrees of interactivity, so what I took away from the conference is the view-level is where there may be some serious surgery in Rails. Obviously, there are a lot of core members looking at a variety of things in the stack, but I perceive that Rails needs to solve the problem of offering a strong convention for data representation to keep it relevant to new and growing technologies, while allowing Rails to continue to flourish.


