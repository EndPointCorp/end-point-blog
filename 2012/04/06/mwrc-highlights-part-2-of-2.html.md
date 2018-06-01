---
author: Brian Gadoury
gh_issue_number: 583
tags: conference, ruby, rails
title: MWRC Highlights Part 2 of 2
---

This is Part 2 of my [2012 Mountain West Ruby Conference Highlights](/blog/2012/03/22/mwrc-highlights-part-1-of-2) article I posted the week of the conference. To date, I **still** have a ton of TODO reading from the conference. Here are some of the things mentioned during [Day 2 of the conference](http://mtnwestrubyconf.org/2012/schedule) that are on that list.

### Rollout: a gem that enables/disables sets of features for certain conditions, users, etc.

- Rollout is a very slick way to activate or deactivate features within your web app programmatically. Perhaps you want to deploy a new feature in production, but only for internal IP addresses, or certain @users, or a percentage of your @users. Perhaps you do and that feature blows up in production, but it’s no big deal because with Rollout it only takes one line of code to turn that feature off for everyone. Perhaps it doesn’t “blow up” as much as “melt down” and you’d like your app to turn off that feature *automagically* before you get an angry call from your CTO? [Check out the Degrade gem for that](https://github.com/jamesgolick/degrade), Rollout’s awesome superhero sidekick.
- By [James Golick](http://jamesgolick.com/2010/8/1/introducing-rollout-condionally-roll-out-features-with-redis..html)
- Get it: [https://github.com/jamesgolick/rollout](https://github.com/jamesgolick/rollout)
- Mentioned by: [Matt White](https://github.com/whitethunder) in his “Continuous Deployment” talk

### Vagrant: an open source tool that manages virtual machines and their development environments to facilitate, well, development

- There are a lot of good reasons for checking out Vagrant. Fully working dev environments are portable between team members. They are reproducible. They are compartmentalized and switch-off-able.

<div class="separator" style="clear: right; float: right; text-align: center; margin-left:1em;"><a href="/blog/2012/04/06/mwrc-highlights-part-2-of-2/image-0-big.jpeg" imageanchor="1" style="margin-bottom:1em"><img border="0" height="256" src="/blog/2012/04/06/mwrc-highlights-part-2-of-2/image-0.jpeg" width="190"/></a><br/><span style="font-weight: normal; font-size: 8pt; color: #000">The Rock, leading the charge.</span></div>

Spend a few weeks working on client B’s project with its specific environment needs, halt or suspend-to-disk that VM and instantly fire up client A’s VM and its customized stack and pick up where you left off on that project.
- Behind the scenes, it uses Virtualbox and Chef or Puppet for VM creation and provisioning, so it’s not reinventing the wheel. Smart.
- I started developing Ruby on Rails at End Point, so I’ve always had the luxury of developing on a [SpreeCamps](http://www.spreecamps.com) server or at least in a [DevCamps environment](http://www.spreecamps.com/camps) on a client’s server. (At the risk of shilling for my employer on their own blog, I’ll point out that those are both End Point creations and they are frickin’ sweet.) Previous to working at End Point, I have taken the ride on that emotional roller coaster that is setting up a local dev environment (for other languages) with a bunch of dependencies . I’ve done it more than once, in fact. If you’re like me and you had to do it *without* The Rock leading the way, you know it’s no fun. If for some reason I couldn’t use SpreeCamps or DevCamps, I’d definitely go with Vagrant.
- By [Mitchell Hashimoto](https://twitter.com/mitchellh) and [John Bender](http://nickelcode.com/)
- Get it: [vagrantup.com](https://www.vagrantup.com)
- Recommended by: [Mitchell Hashimoto](https://twitter.com/mitchellh) during his “Rack Middleware as a General Purpose Abstraction” talk

### New Relic

- If you’re thinking I must be the last person on earth to hear about New Relic, you’re wrong. I checked and my mother has also never heard of it and that woman is a saint with a heart of gold so you show some respect. Also she reads my blog. New Relic is a free* service that provides some pretty deep and valuable analytics and monitoring for your web app. Create an account on their site, install their gem and a YAML file with your account key, and restart your app. Their site has a great UI for presenting data on application code, database, front-end performance, etc. While I have signed up for a free New Relic account, I haven’t started using it yet so I can’t speak to how well it all works in reality. But, more than one MWRC speaker made an informal endorsement, so it’s definitely worth checking out, especially for free.
- *Their Free account provides basic functionality and their Standard and Pro accounts are Non-Free, but offer additional functionality. If you’re running a Standard or Pro account, please let me know what you think about the additional features and their bang for the buck.
- By [New Relic](https://newrelic.com/)
- Get it: Surprise! [New Relic](https://newrelic.com/)
- Mentioned by [BJ Clarke](https://twitter.com/RobotDeathSquad) and others

### Hstore data-type in Postgres

- Much like New Relic, Postgres’s hstore data-type is not “new” in the traditional sense, but more in a “new to me” sense. Simply put, the hstore data-type in Postgres allows you to store structured key/value data in an indexable column such that the structure itself is intelligently queryable in Postgres.
- Described by Will Leinweber as a solution for data that would be pain to store and work with in strict third normal form. To be honest, I’ve only abandoned third normal form in a small number of cases and it was for performance reasons. So using hstore columns seems a little “wild, wild west” to me. Nevertheless, after seeing Will’s examples of using hstore columns, I’m going to keep the idea in mind for the nastier schema challenges out there.
- By [Postgres](https://www.postgresql.org/download/)
- Get it: It’s been a [Postgres extension](https://www.postgresql.org/docs/9.0/static/hstore.html) since Postgres 8.2.
- Mentioned by [Will Leinweber](http://bitfission.com/) during his [“Schemaless SQL—​The Best of Both Worlds” talk](https://www.youtube.com/watch?v=r4lE4bxMJmk)

This concludes my personal list of highlights for the Mountain West Ruby Conference. I urge you to check out the tools and people I’ve mentioned here and in [Part I](/blog/2012/03/22/mwrc-highlights-part-1-of-2). Both Part I and Part II actually took me quite a while to write, as there was so much interesting reading to be had once I hit these people’s blogs and GitHub pages. I would definitely invite you to, as Bruce Dickinson once said, “really explore the space.” Last but not least, here’s a shout out to Mike Farmer’s excellent review of the conference’s various [discussions on dealing with Rails application complexity](/blog/2012/03/23/dealing-with-rails-application).
