---
author: Steph Skardal
title: Rails Optimization @RailsConf
github_issue_number: 141
tags:
- conference
- rails
date: 2009-05-07
---

On the second day of [RailsConf 2009](https://conferences.oreilly.com/rails2009), I attended a talk on [Advanced Performance Optimization of Rails Applications](https://conferences.oreilly.com/rails2009/public/schedule/detail/8615). Although it was reminiscent of college as I felt compelled to write down and memorize lots of trivial information, I appreciate that I can actually apply the information. Below is a performance checklist for advanced optimization techniques covered in the talk.

Rails optimization:

- Use [eager](http://api.rubyonrails.org/classes/ActiveRecord/Associations/ClassMethods.html) [loading](http://railscasts.com/episodes/22-eager-loading) (investigate the [virtual attributes](https://github.com/acunote/virtual_attributes/) plugin)
- Avoid [string callbacks](https://web.archive.org/web/20081109165425/http://dev.rubyonrails.org/ticket/11108)
- Minimize view instances of the object and use template inlining. Objects passed through partials can add up and be expensive.

Ruby optimization:

- [Date](https://ruby-doc.org/stdlib-2.5.1/libdoc/date/rdoc/Date.html) is 16* slower than [Time](https://www.ruby-doc.org/core/classes/Time.html)
- Use [Date::Performance](https://web.archive.org/web/20090604020008/https://tomayko.com/src/date-performance/)
- Avoid the string+= method, Use string<< method instead
- Compare like objects—​comparing different types of objects is expensive.

Database optimization:

- Use [explain analyze](https://www.postgresql.org/docs/8.1/static/sql-explain.html)
- Use any(array ()) instead of in()
- Push conditions into subselects and joins—​postgresql doesn’t do that for you.

Environment Optimization:

- Buy more memory, optimize memory, set memory limits for mongrel (with [monit](https://mmonit.com/))
- Competing for memory cache is expensive on a shared server (must avoid database in cold state)
- Use live debugging tools such as [strace](https://en.wikipedia.org/wiki/Strace), [oprofile](http://oprofile.sourceforge.net/about/), [dtrace](https://en.wikipedia.org/wiki/DTrace), monit, [nagios](https://www.nagios.org/)
- Pay attention to [load balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing))

User Environment Optimization:

- Listen to [yslow](http://yslow.org/)
- Inherently slow javascript functions are eval, DOM selectors, css selectors, element.style changes, getElementById, getElementByName, style switching.

Other Topics:

- Upgrade to [ruby 1.9](http://www.ruby-lang.org/en/news/2007/12/25/ruby-1-9-0-released/)
- Investigate using [Jruby](https://web.archive.org/web/20090422032959/http://jruby.codehaus.org/The+JRuby+Tutorial+Part+1+-+Getting+Started)
- Use [Rack](https://rack.github.io/), which has been a hot topic at this RailsConf

Some final tips from the presentation were get benchmarks, use profiling tool like ‘ruby-prof’, optimize memory, pay attention to the garbage collection methods for the language, profile memory and measure! measure! measure!!!

Probably more important than the optimization details covered, the presentation served more valuable to remind me of the following:

Pay attention to all potential areas for optimization. As I’ve grown as a developer I’ve continued to add to my "optimization checklist".

When learning a new language, don’t forget to pay attention to the the little details of the language. I should appreciate specific points that make a language unique from other languages, including inherently expensive functions.

Like other developers, sometimes I produce code to meet the performance criteria, but I don’t have the luxury to spend time examining every area for optimization. I’d like to spend more time throughout a project paying attention to each of these points on my optimization checklist—​and always work on doing it better the second time around.
