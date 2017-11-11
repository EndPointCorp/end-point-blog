---
author: Spencer Christensen
gh_issue_number: 982
tags: conference, devops
title: Highlights of OpenWest conference 2014
---

Last week I was able to not only attend the [OpenWest](http://www.openwest.org/) conference, held in Orem, UT at the [UVU](http://www.uvu.edu/) campus, but I was also able to be a presenter.  This year's conference had their largest attendance to date and also their most diverse list of tracks and presentations.  Many of the presentations are posted on [YouTube](https://www.youtube.com/channel/UC0wbcfzV-bHhABbWGXKHwdg).

My own presentation was on **Git Workflows That Work** ([previous blog post](http://blog.endpoint.com/2014/05/git-workflows-that-work.html), [talk slides](https://speakerdeck.com/localfilmmaker/git-workflows-that-work)). It was part of the "Tools" track and went pretty well.  Rather than recap my own presentation, I'd like to briefly touch on a few others I enjoyed.

### Building a Scalable Codebase using Domain Driven Design

The folks at [Insidesales.com](http://www.insidesales.com/) presented on Domain Driven Design.  This was something I had heard of but wasn't very familiar with.  The main principles of DDD are: understand the business purpose (not just the app requirements), rigorous organization (of code, services, design, etc.), distinct layers, and functional cohesion.  The biggest point I got was that all business logic should be located in a "domain" separated from the application and separated from the data.  The application is then just a thin wrapper around API calls to the business logic within the domain.  DDD is different from MVC though because each layer is distinct and could have its own design.  Thus MVC could be a smaller piece within a given layer.

As I listened to this presentation I remembered a project I worked on at a previous job building a Feeds Admin to create and manage product feeds to third parties (search engines, shopping portals, etc).  I had built that using DDD without realizing it at the time.  It came naturally as I wanted to cleanly organize and separate the logic for each feed (with different data pulled from the database, different feed formats, different transport methods, etc.). So I definitely have seen the benefits and principles of DDD in practice.

### Mentoring Devs into DevOps

This presentation by Justin Carmony discussed how his team has been going through a transition of empowering developers to also do some Ops work.  They had roughly 30 developers, 2 operations admins, and over 300 servers in their infrastructure.  They also had several different tools and ways of doing things between the different teams of developers; for example, some used Capistrano and some used Ansible, and some used Jenkins and others Travis CI, some used Vagrant and some didn't, etc.).  They considered hiring for a new DevOps position to own and mentor everyone in standardizing tools and processes, but instead promoted one of their star developers to that role.  This was a tough decision because it meant that they would not be able to use his skills a developer.  But Justin said it was definitely worth it because within just 3 months this developer had helped everyone to standardized on tools and release procedures, making the entire team more productive and efficient.

They also switched to using [Salt](http://www.saltstack.com) for configuration management for all servers at this same time.  And to empower the developers and expose them to the world of Ops, they switched to using Vagrant managed by Salt for all development environments.  Developers were able to make some Salt changes if needed to their own environment, and then submit a git pull request to Ops for peer review of the Salt configuration and Ops would then merge it and deploy it to production if they accepted the changes.

Justin mentioned that it is still an on-going transition for them.  Ultimately the main points he presented are:

- There is a long continuum or gradient of skill level and access level between Dev and Ops and it is better to think of DevOps as a continuum as well and not a strict role with strict access levels.  Some Devs can have access to dashboards and graphs of systems while others can manage build tools and configuration.  "DevOps" can be spread out.
- Team culture matters.  It can be very difficult to improve processes and get people to embrace change for the better, so positive influences by everyone involved can make a big difference.  Business owners need to be supportive as well.

### Retrospectus

Daniel Evans gave an interesting presentation on retrospective meetings.  For those not familiar with these meetings, they are for discussing "what went well" and "what could be improved" over the last project/sprint/time period/etc.  I've participated in these types of meetings for many years and have seen the benefits that can come from them.  Daniel also talked about what these meetings are **not**: they are not meant for deep dives into problems, blame, or griping.  They should be focused on the good that has been done and on solutions to fix problems going forward.  And even then, if the solutions are not quickly apparent then you should not spend too much time trying to find them.  Those conversations should happen outside of this meeting.

His presentation was quite short and didn't really cover much that I didn't know already.  However, at the end he then turned the rest of the time into a retrospective meeting reviewing his presentation, with everyone participating.  This turned out to be pretty fun and was a good exercise, and covered a lot more then a regular Q &amp; A session would have.

### Other Links

- [Keynote speech by Lt. Governor of Utah, Spencer J. Cox](https://www.youtube.com/watch?v=TiEddaKOwo4)
- [Conference schedule and list of presenters](http://www.openwest.org/schedule/)
