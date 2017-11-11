---
author: Joshua Tolley
gh_issue_number: 631
tags: chef, devops, puppet
title: Chef and Puppet Overview
---



<a href="http://www.flickr.com/photos/80083124@N08/7184275615/" title="IMG_0741.JPG by endpoint920, on Flickr"><img align="right" alt="IMG_0741.JPG" height="240" src="/blog/2012/06/13/chef-and-puppet-overview/image-0.jpeg" width="320"/></a>

 I started a job several years ago as a "configuration manager", but had to admit when I started that I didn't have any idea what "configuration management" really meant. The idea, as I soon learned, was to make sure all the servers, configurations, accounts, and other components of a system work together systematically. I'm not sure "configuration management" tools as such existed at the time, but we certainly never used them, though they'd begun to have a presence online before leaving that job for another opportunity.

In systems we run at End Point, whether for ourselves or other clients, such configuration management tools have become critical, in particular for our Liquid Galaxy systems, which require a great deal of repetitive configuration.  So Kiel and Josh Williams have a fair bit of experience with these tools, and I was glad to hear their discussion of Chef and Puppet specifically.

These tools have a common heritage, and are both Ruby-based. Ruby is a particularly good language for writing domain-specific languages (DSLs) like the one Puppet uses, so it's interesting that Chef's developers apparently abandoned the DSL idea, so Chef instructs its users run Ruby directly. Chef is newer, spawned by dissatisfied Puppet developers and users. We're generally shifting toward Chef after concluding we share many of those dissatisfactions, but both have proven very time saving, for us.

<a href="http://www.flickr.com/photos/80083124@N08/7184274097/" title="IMG_0740.JPG by endpoint920, on Flickr"><img align="right" alt="IMG_0740.JPG" height="240" src="/blog/2012/06/13/chef-and-puppet-overview/image-0.jpeg" width="320"/></a>

 Kiel told of one client whose dozens of app servers we rebuilt in a day, essentially one at a time, simply by kicking off Puppet tasks on each one in turn. As mentioned above, the Liquid Galaxy uses Chef as well. Whereas it used to take a fully day of manual work building what's called the Galaxy's "head node", now, in combination with scripted, automatic operating system installations, we can set up a new head node in minutes. We're still working to get everything into Chef, but in particular all the monitoring scripts and tools used on a Liquid Galaxy are built from Chef recipes, so every new head node is all ready to monitor from the beginning. Since we deploy these systems all over the world, and must manage them remotely, this is critically important.

Building "recipes" for these tools -- that is, sets of instructions that tell the tool what to build -- can be a detailed and difficult process. Kiel and Josh recommended being explicit about the configuration you actually want, rather than simply accepting defaults, principally because later on, it's difficult to know precisely what the original author intended. They also recommend starting with small, easily tested services, such as NTP. For many systems, breaking NTP for a while won't cause problems, so it can be a good service to begin playing with.

One attendee was curious to know how many servers a system needed to involve for Chef or Puppet to be worth considering. The rule of thumb is, apparently, about 10, but Josh Williams suggested having "more than one" was enough to start writing recipes. I guess I'm sold.


