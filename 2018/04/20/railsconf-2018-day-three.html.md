---
author: Steph Skardal
title: "RailsConf 2018 Summary: The Train is Still Moving"
tags: rails, ruby, conference
gh_issue_number: 1414
---

<img src="/blog/2018/04/20/railsconf-2018-day-three/railstrain.jpg" width="755" height="435" alt="RailsConf train" />
<small>An actual Duplo creation I built at my house this morning, while my kids are at daycare.</small>

Hi! Here’s my wrap-up summary of [RailsConf 2018](https://railsconf.com/), my 8th time attending. And I say that only to provide some context for my perspective.

### All.The.Analogies.

Code is a theatrical performance and devs are the actors. Code is a craft and senior devs are the artisans who create and innovate on a framework. Code is a house that you live in—​you need to leave it better than how you found it, value improvement over consistency, and communicate more as you *get* to live in this house. Code infrastructure is a Jenga tower waiting to topple. The Rails router is a mail carrier sorting system. A new codebase is a map that you start to navigate once you begin working on it. There have been so many analogies here at RailsConf, I can’t keep track of them anymore.

Here’s my analogy: Rails is a train. It’s a train made out of Lego blocks disguised as Duplos with mostly white bearded guys wearing graphic tees. This train is still getting businesses from point A to B. Some of those businesses care about that train that’s getting them where they need to be, some don’t. But certainly, most businesses that come to RailsConf care about the train and continue to evangelize it. Thanks to things like code school and bootcamps, people are still getting on the train, and people are getting off the train<sup>*</sup>. There are devs riding the train, and there are contributors maintaining and building the train, adding cars, taking them off, making them better.

<sup>*</sup> RailsConf attendance has held steady at 1,300 for some time.

### On Technical Debt

Two talks I went to greatly summarized the technical debt built up over the years of running on Rails.

[Edouard Chin](https://twitter.com/DaroudeDudek) of the the [Shopify](https://www.shopify.com/) production team gave a great talk on how Shopify has handled upgrades over 10+ years at scale. Shopify runs over 600,000 businesses, so any ongoing upgrades obviously affect a large amount of business owners and end users. Examples that he went over during his talk were:

* Using environment variables to drive the Rails gem version, e.g. SHOPIFY_NEXT=1 bundle install. This one is very basic, but it was Edouard’s starting point for working through the path to release to the next version of Rails.
* Stop the bleeding: With the gem versions driven by environment variables, tests will run against different Rails versions. Any tests introduced to the codebase running on the old Rails version that break in the new version of Rails must be fixed in the new version of Rails before merging.
* Componentization: Upgrades were broken down into many components, and individual teams contributed to these manageable elements.
* Shopify practices long-term management of deprecation logging and will soon release a deprecation toolkit gem.
* Best ProTip: Incremental deploys. On deploy, the environment variable SHOPIFY_NEXT_PERCENTAGE was used to incrementally move Shopify businesses to the next version of Rails as issues are monitored. E.g. SHOPIFY_NEXT_PERCENTAGE=5 will force 5% of the shops to be deployed on the next version of Rails, and that value will gradually increase to 100% as issues are resolved.

---

The second great talk on technical debt I attended was by [Jordan Raine](https://twitter.com/jnraine?lang=en), of [Clio](https://www.clio.com/). Clio has been running on Rails for 10+ years as well, and Jordan gave a great visual of the timeline of Rails. As time has passed, keeping up with Rails releases has increasingly lagged. One of his main points was on the topic of dependency management, and the complexity of dependency management over many years. Dependencies aren’t free. The cost of dependencies needs to be acknowledged, which means you have to commit to updating them.

Here’s an example of how dependency management can get complex (and I coincidentally sent an email with this scenario a few weeks ago, sprinkling in some infrastructure limitations): gem-1 of version X requires gem-2 version Y, and that’s where we started. Our codebase references the API for gem-1 (version X) and gem-2 (version Y). Time passes. A new feature is needed from gem-1 (version M), but that requires that gem-2 also be upgraded (to version N). The options here are:

* Don’t upgrade any gems, don’t get new feature.
* Upgrade both gems and blow out the scope.
* Fork gem-1 and downgrade gem-2 dependency (to stay on version Y).

Jordan gave similar examples to Edouard of how to mitigate some of these issues, and you can see them on [his slides](https://speakerdeck.com/jnraine/ten-years-of-rails-upgrades). Both Jordan and Edouard provided excellent perspective on maintaining large Rails applications over a long period of time. I will link to the videos once they become available.

<img src="/blog/2018/04/20/railsconf-2018-day-three/railstrain2.jpg" width="755" height="321" alt="RailsConf train" />

### So, is Rails dying?

The elephant in the room, or the thing that I hear from my coworkers is, “Rails is dying”. In [Eileen](http://eileencodes.com/)’s keynote, she says, “Rails is not dying, it’s maturing.” For Rails 6, she’s solving problems like parallel testing and multi-database management. Someone asked her if these elements will make Rails more bloated. Her compelling answer here is that the better Rails is at providing convention for these problems, the more it will provide long-term value to the end user. As a dev, you won’t have to keep solving the problem at each company and teach them “your solution”, because there is “the Rails solution”.

The train is still moving. There are large companies running on Rails, solving complex problems for large scale businesses. There are plenty of companies looking to hire, as evidenced by the RailsConf job board and speakers who mentioned hiring. Rails isn’t dying, but it may not be the shiny new solution that it was years ago. It has now built up 10+ years of technical debt, so a big rewrite might appeal to those not interested in digging in.

All along while Rails has been maturing, I’ve also grown from a dev with 2 years of experience to a dev with 11+ years of experience into the role of a senior software engineer. I can see the repeating pattern here in adopting shiny, new, everything-baked-in stacks, followed by adoption, long-term technical debt growth, only to repeat the cycle over again.

For many clients in my world of consulting, they care that we use efficient tools that get them from point A to B, but they don’t necessarily care about the choice of tools we use. I still think that the case can be made that convention over configuration in Rails is a big win, but the issues noted above must be mitigated (and better mitigated). As Jordan noted in his talk, “it needs to be easy to do the right thing” and to stay on the maintainable, happy path to allow Rails to thrive.

### Side note: Other Notable Talks

Here are a few other talks I liked:

* [Aaron Patterson](https://twitter.com/tenderlove)’s keynote. I was driving while he gave his keynote, but I’m confident it was funny, thought-provoking, and informative.
* Talks related to [webpacker](https://github.com/rails/webpacker) or [webpack](https://webpack.js.org/), because there are few job descriptions now that don’t mention a JavaScript framework.
* [Who Destroyed Three Mile Island?](https://railsconf.com/program/sessions#session-544) by Nickolas Means. I didn’t attend this talk, but I heard it was great.
* [Re-graphing The Mental Model of The Rails Router](https://railsconf.com/program/sessions#session-564) by Vaidehi Joshi of Tilde. This was a great talk. She has a great way of simplifying and condensing many complex computer science topics into a digestible talk. She also has a [blog and podcast](https://medium.com/basecs) with other CS topics.
* Talks related to security, because that’s a timely and valuable topic.
