---
title: "Project On-ramping: Infrastructure and Codebase"
author: Steph Skardal
tags: rails, clients, development
gh_issue_number: 1564
---

![Aerial view of New York City from satellite](/blog/2019/10/21/codebase-on-ramp/nasa.jpg)
Photo by NASA via Unsplash

Living in the consulting world, we often jump into codebases and environments to get quickly up to speed to provide estimates or start fixing bugs right away. Here are some important landmarks I visit along my way to get up to speed on a new project.

### Dev stack

First up, I learn as much as I can about the dev stack a codebase runs on. It used to be the case that LAMP (Linux, Apache, MySQL, PHP) was a pretty common setup in our world, but the number of dev tools and variety in stacks has expanded greatly over time. Many of my End Point clients are now running nginx on Linux, with Ruby on Rails and MySQL or PostgreSQL, but as a company we have both breadth and depth in web stack technologies (hover over the Expertise dropdown above).

Layered on top of the base infrastructure might be a JavaScript framework (e.g. [React](https://reactjs.org/), [Ember.js](https://emberjs.com/)), and other abstractions to improve the dev process (e.g. [Sass](https://sass-lang.com/), [Node.js](https://nodejs.org/en/)). And layered on top of that further is the possibility of other services running on the server locally (e.g. search using [Elasticsearch](https://www.elastic.co/) or [Solr](https://lucene.apache.org/solr/)) and 3rd-party tools running on a server elsewhere (e.g. content delivery networks, monitoring, [Stripe](https://stripe.com/)).

The web stack and 3rd-party tools can be so complex these days that there is a lot of ground to cover before jumping into the code.

### Personnel infrastructure

Next up, I like to understand how our client works with the website and more about their limitations (time, technical, other). Especially in the consulting space where we are supporting existing developers, I think it’s important to exercise empathy over how they’ve gotten to the point they are at, and why they’ve reached out for additional development resources.

Does the client want a solution that enables them to make their own changes moving forward, i.e., a content management solution? Do they want to hand the project off entirely due to time limitations? Is there a hybrid solution that will enable them to make changes and defer to us as a resource for bigger decisions? Is the existing development staff who we should be best supporting and advising on decisions?

### Are there dev instances?

After we have a high-level understanding of the dev stack and personnel involved, the next bridge we cross is to determine dev instance architecture (and how to get access to a dev instance!). It goes without saying (though I’m saying it anyways) that it’s a much lower risk to experiment and play around on a dev instance rather than a production server.

Here at End Point, we have our own in-house tool for spinning up dev instances ([DevCamps](https://www.devcamps.org/)), and we also work with clients who have their own setup for dev environments (e.g. [Docker](https://www.docker.com/), [AWS](https://aws.amazon.com/)) that we can jump into.

### Codebase: Where do I go?

I like to equate learning a new code base to moving to a new city. When you first arrive, you don’t know what you are looking at or where to go, but as you begin to make frequent trips to one location or another, you become familiar with those paths and you become most familiar with the paths that you take most often.

One of my first stops is the database. I review the tables and understand how the application models interface with them, as well as how they reference each other. Another stop (in the Rails world) is to visit `config/routes.rb`, which [maps URLs and dispatches them to a Rails controller](https://guides.rubyonrails.org/routing.html). This immediately informs me of the complexity of the application by the number of different URL requests it handles.

A third favorite stop upon gaining access to the codebase is the code history (hopefully there is one!), which can be telling about the organization as well as frequent code destinations visited.

Another place to visit is the (again, in the Rails space) [Bundler Gemfile](https://bundler.io/gemfile.html), which tells me how many (or how few) dependencies are included in a project.

While I don’t think it’s important to get into the nitty gritty of Rails models, controllers, or views at a first pass, my observations of the database, routing, Git history, and Gemfile can paint a picture of the complexity and dependencies of one project. Outside of the Rails space, many modern web frameworks have comparable code paradigm that I think are similarly revealing.

### Digging deeper

From there, I look to client priorities for where to dig deeper into the code. I have found that in some cases in my consulting experience, the client priorities and convention use in codebase (e.g. with Ruby on Rails) overlaps nicely with my skill set and I’m able to jump right in to make changes, but other client work requires further research into third parties or historical context of the code and changes needed.
