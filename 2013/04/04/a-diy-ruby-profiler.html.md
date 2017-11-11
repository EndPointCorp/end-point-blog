---
author: Mike Farmer
gh_issue_number: 779
tags: conference, ruby
title: A DIY Ruby Profiler!
---

A simple profiler can be nice to help detect how often different parts of our code are being run by using some statistical analysis and a few threading tricks. [New Relic](http://newrelic.com/) developer [Jason Clark](http://twitter.com/jasonrclark) talks about how it’s more efficient to take samples than to use ruby profiler to profile every call and then walks us through building your own profiler.

This was a very insightful talk on how to analyze the backtrace of currently active threads. You can find the code for his DIY profiler on [github](github/jasonrclark/diy_profile).
