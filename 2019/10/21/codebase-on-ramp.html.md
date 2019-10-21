---
title: "Project on Ramping: Infrastructure and Codebase"
author: Steph Skardal
tags: rails, clients, consulting
---

![](/blog/2019/10/21/codebase-on-ramp/nasa.jpg)
<a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@nasa?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from NASA"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">NASA</span></a>

Living in the consulting world, we often jump into code bases and environments to get quickly up to speed to provide estimates or start fixing bugs right away. Here are some important landmarks I visit along my way to get up to speed on a new project.

### Dev Stack

First up, I learn as much as I can about the dev stack a codebase runs on. It used to be the case that LAMP was a pretty common setup in our world, but the number of dev tools and variety in stacks has expanded greatly over time. Many of my End point clients are now running nginx on Linux, with Ruby on Rails and MySQL or PostgreSQL. Layered on top of that might be a JavaScript framework (e.g. [React](https://reactjs.org/), [Ember.js](https://emberjs.com/)), and other abstractions to improve the dev process (e.g. [Sass](https://sass-lang.com/), [Node.js](https://nodejs.org/en/)). And layered on top of that even more is the possibility of 3rd party tools running on the server locally (e.g. 3rd party search) and 3rd party tools running on a server elsewhere (e.g. content delivery networks, monitoring, [stripe](https://stripe.com/)). The web stack and 3rd party tools can be so complex these days that there is a lot of groundwork to lay before jumping into the code.

### Personnel Infrastructure

Next up, I like to understand how our client works with the website and more about their limitations (time, technical, other). Especially in the consulting space where we are supporting existing developers, I think it's important to exercise empathy over how they've gotten to the point they are at, and why they've reached out for additional development resources. Does the client want a solution that enables them to make changes moving forward (i.e., a content management solution)? Do they want to hand the project off entirely due to time limitations? Is there a hybrid solution that will enable them to make changes and defer to us as a resource for bigger decisions? Is the existing development staff who we should be best supporting and making decisions for?

### Are there Dev Instances?

After we have a high level understanding of the dev stack and personnel involved, the next bridge we cross is to determine dev instance architecture (and how to get access to a dev instance!). It goes without saying (though I’m saying it anyways) that it’s a much lower risk to experiment and play around on a dev instance rather than a production server. Here at End Point, we have our own in-house tool for spinning up dev instances ([DevCamps](https://www.devcamps.org/)), but we’ve also worked with clients who have their own setup for dev environments (e.g. [Docker](https://www.docker.com/), [AWS](https://aws.amazon.com/)) that we jump into.

### Code Base: Where do I go?

I like to equate learning a new code base to moving to a new city. When you first arrive, you don’t know what you are looking at or where to go, but as you begin to make frequent trips to one location or another, you become familiar with those paths and you become most familiar with the paths that you take most often. One of my first stops in a codebase is the database. I review the tables and understand how the application models interface with them, as well as how they reference each other. Another stop [in the Rails world] is to visit config/routes.rb, [which maps URLs and dispatches them to a Rails controller](https://guides.rubyonrails.org/routing.html). This immediately informs me of the complexity of the application by the number of different URL requests it handles. A third favorite stop upon acquiring the codebase is the code history (hopefully there is one!), which can be telling about the organization as well as frequent code destinations visited. Another place to visit is the [again, in the Rails space] [Gemfile](https://bundler.io/gemfile.html), which tells me how many (or how little) dependencies are being included in a project.

While I don’t think it’s important to get into the nitty gritty of Rails models, controllers, or views at a fist pass, my choices of the database, routing, git history, and Gemfile can paint a picture of the complexity and dependencies of one project. Outside of the Rails space, many modern web frameworks have comparable code concepts that I think are equally revealing.

From there, I look to client priorities for where to dig deeper into the code. I have found that in some cases in my consulting experience, the client priorities and convention use in codebase (e.g. with Ruby on Rails) overlaps nicely with my skill set and I’m able to jump right in to make changes, but other client work requires further research into third parties or historical code context. 
