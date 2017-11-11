---
author: Jason Dixon
gh_issue_number: 451
tags: conference, hosting, ruby, rails
title: RailsConf 2011 - Day One
---



Today was the first official day of [RailsConf 2011](http://en.oreilly.com/rails2011). As with most technical conferences, this one spent the first day with tutorials and workshops. For those of us without paid access to the tutorial sessions, the BohConf was a nice way to spend our first day of the four-day event.

[BohConf](http://bohconf.com/) is described as the "unconference" of RailsConf. It's a loosely organized collection of presentations, mini-hackathons and barcamp-style meetings. I spent the first half of Monday at the BohConf. Of particular interest to me was Chris Eppstein and Scott Davis' introduction to [Sass](http://sass-lang.com/) and Compass. I've dabbled with Sass in the past but only recently learned of Compass.

Sass is a great way to construct your CSS without the tedious duplication that's typical of most modern spreadsheets. Introducing programming features like variables, inheritance and nested blocks, Sass makes it easy to keep your source material concise and logical. Once your source declarations are ready, compile your production spreadsheets with Sass or Compass.

[Compass](http://compass-style.org/) is effectively a framework for easy construction and deployment of spreadsheets using Sass. To hear Scott describe it, "Compass is to Sass as Rails is to Ruby". Together they're a very attractive combination for the Ruby developer who also dabbles in design (and who doesn't these days?). Truth be told, while I'm very impressed with the capabilities of Sass, I worry about the trend to re-introduce logic and presentation. My mom raised me to abstract the presentation layer for ease on graphic designers, and that rule has suited me well to date. Time will tell.

In the afternoon I wandered into a sponsored workshop from VMware. Dave McCrory and Dekel Tankel led a demonstration of their new [CloudFoundry service](http://cloudfoundry.com/). A nice reward for attending was getting instant approval of your CloudFoundry.com beta registration. Although I felt mildly guilty for it afterwards, I took advantage of this opportunity to get an extra beta account (my personal request had been approved a week earlier). 

Dave introduced everyone to the CloudFoundry beta offering and discussed a vague roadmap for the [open source project](https://github.com/cloudfoundry) and their own commercial VM product slated for early 2012. They emphasized that the CloudFoundry core project will remain open source, and that interested parties can fork it on github, hack on the code, and deploy their own private "micro-clouds". Dave even hinted that at least one startup has based their PHP PaaS service on CloudFoundry.

Once all the attendees had received their beta accounts, [Dekel walked us through](http://support.cloudfoundry.com/entries/20117991-cloud-foundry-workshop-at-railsconf-2011) the installation and basic command-line usage of the **vmc** utility. I was able to immediately **vmc login** with my Beta account credentials and change my password with **vmc passwd**. I should note that before logging in, I had to choose my target server with **vmc target api.cloudfoundry.com**. Why is this important? This will allow developers to easily switch between targeted environments. For example, I could install CloudFoundry on my workstation or development server and "target" it as my development or staging environment. Once my tests pass, I can quickly switch targets and push the changes to production.

They had us follow along by recreating a sample Ruby application designed to check if one Twitter account follows another. The examples were simple and easy to follow. Once we had our Gemfile, controller and views in place, we had to **bundle package** all of the dependencies. Once this was complete, a quick **vmc push *myappname*** and [we were live](http://douchebag123.cloudfoundry.com/follows?user1=obfuscurity&user2=jordansissel)!

Unfortunately, most (if not all) of us encountered a gotcha with this example. Because all of our instantiated applications reside behind the same IP address on CloudFoundry's network, we quickly hit Twitter's API quota. I'm not sure if this will be a problem once CloudFoundry officially launches, but it's something to keep in mind. And while it was useful to **vmc logs *myappname*** to debug this problem, an astute attendee brought up the fact that there was no way to tail application logs in CloudFoundry. This is a glaring oversight and one I hope they rectify before the Beta is finished.

The workshop continued with an introduction into binding services like Redis, Mongo or MySQL. We added new functionality to our existing application that introduced a Redis backend to store leaderboard information for Twitter activity. Lastly, Dekel demonstrated the ease of scaling our applications with **vmc instances *myappname* 5**. This simple command instantiates new copies of the application behind their dynamic load balancer. Coincidentally, they're not currently offering any sort of scalable backend storage, so keep that in mind before you try to launch any production sites on their Beta service. Now you'd **never** do that, would you? ;-)

The first day of RailsConf 2011 was impressive. I came last year as an exhibitor and am really excited that I get to attend this year for the conference sessions. I can't wait to see all the talks tomorrow!


