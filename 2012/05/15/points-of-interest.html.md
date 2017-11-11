---
author: Brian Buchalter
gh_issue_number: 614
tags: mysql, rails, vim
title: Points of Interest
---



It's been a fairly straight forward week at work, but I have stumbled a few interesting finds along the way this week.

### [Vim Adventures](http://vim-adventures.com/)

Finally!  A game based approach to learning Vim keyboard commands.  I was hoping someone would do this.  It's just getting started (only two levels) and sadly, it looks like it'll be charging money to unlock higher levels.  However, some things are worth paying for.  I've found just playing the first two levels a few times have helped retrain my brain to not take my fingers off the home row. It's still quite buggy and seems to only work in Chrome.  I found several times I needed to close all my Chrome windows after playing.  Also, incognito mode seems to help with the bugs, as it disables all extensions you may have installed.

### [MySQL query comments in Rails](http://37signals.com/svn/posts/3130-mini-tech-note-mysql-query-comments-in-rails)

Ever wanted to know where that slow query was being called from?  Well, if you're using MySQL with your Rails 2.3.x or 3.x.x app, you can get debug information about what controller's action made the call.  Check out 37Signals new [marginalia](https://github.com/37signals/marginalia) gem.

### [How to use EC2 as a web proxy](http://kev.inburke.com/kevin/how-to-use-ec2-as-a-web-proxy/)

Kevin Burke provides a very detailed HOWTO article for working around restrictions you may experience in the course of an Internet based life.  Pretty amazing what Amazon's [free usage tier](http://aws.amazon.com/free) puts out there; of course it's only free for 12 months.

### [Include PIDs in your Logs](http://help.papertrailapp.com/discussions/suggestions/18-include-pids-in-rails-productionlog)

For many Rails developers we get comfortable looking at development log files.  Sometimes when I have to investigate a customer issue on a production server using logs, I wished I had the level of detail the development logger had.  While that's a wish, I'm finding it mandatory to include PID numbers in my production logs.  In production systems with multiple requests being handled simultaneously, Rails logs start to become unusable.  It's not clear which log lines are from which requests.  Adding a PID in front of the time stamp can help untangle the mess.  Here are some example approaches to this for [Rails 3.x.x](http://andre.arko.net/2011/08/18/pid-numbers-for-rails-3-logs/) and [Rails 2.3.x](http://nhw.pl/wp/2009/09/15/logger-simple-yet-powerful-rails-debugging-tool).  Also, if you're really a log-lover and manage a lot of servers, check out [Papertrail](https://papertrailapp.com/), it looks very impressive for $7/mo.

### [Spectrum Shortages - Why it's happening and what can be done](http://s4gru.com/index.php?/blog/1/entry-160-spectrum-shortages-why-its-happening-and-what-can-be-done/)

Telecom is not an area I have much familiarity with, but I found this article to be an interesting read.  For example did you know that that largest owner of spectrum licenses are "under-capitalized or unwilling to build out networks" to use the spectrum?  So while AT&T and Verizon struggle to meet the iPhone 4S's data demands (twice as much as iPhone 4!), "there are some companies that have spectrum, but they're struggling financially. Or they aren't quite sure what to do with the spectrum. And others that have the money and business model, but need the spectrum."  It seems the way out of the mess is 4G, offering to improve the efficiency of spectrum use by 700 percent.


