---
author: Greg Davidson
gh_issue_number: 815
tags: browsers, conference, javascript
title: "JSConf US — Day 2"
---

## Choose Your Own Adventure

For day two of [JSConf](http://2013.jsconf.us/), the organizers decided to try something new. Rather than a day of scheduled talks, attendees could choose from a variety of activities. There was kayaking, golf, segway tours, scavenger hunts or you could just hang out at the pool if you like. There was also the opportunity to hack on [NodeBots](http://nodebots.io/) or [Node Copters](http://nodecopter.com/). While the outdoor stuff sounded awesome, I opted to hack on and play with the nodecopters.

## Node Copter

With the help of [nodejitsu](http://nodejitsu.com/), Chris Williams was able to bring 50 [Parrot AR Drone](http://ardrone2.parrot.com/) quadcopters for teams to play with and hack on with JavaScript. [Felix Geisendorfer](http://ardrone2.parrot.com/) and a contingent of volunteers showed us how to fly the quadcopters (with either an iOS or Android device) and how they could be controlled with JavaScript code. Felix is the author of the [ar-drone](https://github.com/felixge/node-ar-drone) node.js module which makes this possible. With a laptop connected to the quadcopter, the following code is all you need to have it take off, rotate a little bit, perform a flip and then land:

```
var arDrone = require('ar-drone');
var client = arDrone.createClient();

client.takeoff();

client
  .after(5000, function() {
    this.clockwise(0.5);
  })
  .after(3000, function() {
    this.animate('flipLeft', 15);
  })
  .after(1000, function() {
    this.stop();
    this.land();
  });
```

## The Challenge

I worked in a team with [Ryan Seddon](http://www.thecssninja.com/) and [John Buckley](http://jbuckley.ca/) on a challenge set out at the beginning of the day by Felix. We used [Open CV](http://opencv.org/) (Computer Vision library) initially and later the on-board compass data to have the nodecopter take off, locate a marked line on the floor, fly to the end of the line and then land in the prescribed location. We were close several times but did not successfully complete the challenge in the end. This was dissappointing *but* we still had a blast working on it throughout the day.

<blockquote class="twitter-tweet"><p>Hacking on nodecopters! So rad <a href="https://twitter.com/search/%23jsconf">#jsconf</a> <a href="http://t.co/d71G94MpaJ" title="http://twitter.com/ryanseddon/status/340145777525542913/photo/1">twitter.com/ryanseddon/sta…</a></p>— Ryan Seddon (@ryanseddon) <a href="https://twitter.com/ryanseddon/status/340145777525542913">May 30, 2013</a></blockquote><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

## Demos

At the end of the day, many of the teams demonstrated what their team had come up with. This was a lot of fun to watch. Typically, each nodecopter operates as a wifi access point. To control the nodecopter, you connect your computer to that wireless network and then gain control. This works well but has the limitation of only operating one nodecopter at a time. Several teams worked on hacks to enable multiple nodecopters to fly at the same time. This short clip I filmed, shows one such squadron of nodecopters flying in unison.

<iframe allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/PKlHj3nKA8U" width="560"></iframe>

Many thanks to [Felix](http://felixge.de/) and his team, [Chris](http://voodootikigod.com/) for bringing in so many nodecopters (and batteries), and to [nodejitsu](http://nodejitsu.com/) for sponsoring this great event!
