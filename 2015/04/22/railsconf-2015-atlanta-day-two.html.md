---
author: Steph Skardal
gh_issue_number: 1120
tags: conference, rails
title: 'RailsConf 2015 — Atlanta: Day Two'
---

It’s day 2 of [RailsConf 2015](https://railsconf.com/2015/) in Atlanta! I made it through day 1!

The day started with [Aaron Patterson](https://twitter.com/tenderlove)’s keynote ([watch it here](http://confreaks.tv/videos/railsconf2015-keynote-day-2-opening)). He covered features he’s been working on including auto parallel testing, cache compiled views, integration test performance, and “soup to nuts“ performance. Aaron is always good at starting his talk with self-deprecation and humor followed by sharing his extensive performance work supported by lots of numbers.

### On Hiring

One talk I attended today was “Why We’re Bad At Hiring (And How To Fix It)” by [@kerrizor](https://twitter.com/kerrizor) of Living Social ([slides here](https://speakerdeck.com/kerrizor/why-were-bad-at-hiring-and-how-to-fix-it), [video here](http://confreaks.tv/videos/railsconf2015-why-we-re-bad-at-hiring-and-how-to-fix-it)). I was originally planning on attending a different talk, but a fellow conference attendee suggested this one. A few gems (not Ruby gems) from this talk were:

- Imagine your company as a small terrarium. If you are a very small team, hiring one person can drastically affect the environment, while hiring one person will be less influential for larger companies. I liked this analogy.
- Stay away from monocultures (e.g. the banana monoculture) and avoid hiring employees just like you.
- Understand how your hiring process may bias you to reject specific candidates. For example, requiring a GitHub account may bias reject applicants that are working with a company that can’t share code (e.g. security clearance required). Another example: requiring open source contributions may bias reject candidates with very little free time outside of their current job.
- The interview process should be well organized and well communicated. Organization and communication demonstrate confidence in the hiring process.
- Hypothetical scenarios or questions are not a good idea. I’ve been a believer of this after reading some of [Malcolm Gladwell’s](https://en.wikipedia.org/wiki/Malcolm_Gladwell) books where he discusses how circumstances are such a strong influence of behavior.
- Actionable examples that are better than hypothetical scenarios include:
    1. ask an applicant to plan an app out (e.g. let’s plan out strategy for an app that does x)
    1. ask an applicant to pair program with a senior developer
    1. ask the applicant to give a lightning talk or short presentation to demonstrate communication skills
- After a rejected interview, think about what specifically might change your mind about the candidate.
- Also communicate the reapplication process.
- Improve your process by measuring with the goal to prevent false negatives. One actionable item here is to keep tabs on people – are there any developers you didn’t hire that went on to become very successful & what did you miss?
- Read [this book](https://www.amazon.com/Smart-Gets-Things-Done-Technical/dp/1590598385).

Interview practices that Kerri doesn’t recommend include looking at GPA/SAT/ACT scores, requiring a Pull request to apply, speed interviews, giving puzzle questions, whiteboard coding & fizzbuzz.

While I’m not extremely involved in the hiring processes for End Point, I am interested in the topic of growing talent within a company. The notes specifically related to identifying your own hiring biases was compelling.

### Testing

I also attended a few talks on testing. My favorite little gem from one of these talks was the idea that when writing tests, one should try to balance between readability, maintainability, and performance, see:

<img border="0" src="/blog/2015/04/22/railsconf-2015-atlanta-day-two/image-0.jpeg"/>

Eduardo Gutierrez gave a talk on Capybara where he went through explicit examples of balancing maintainability, readability, and performance in Capybara. I’ll update this post to include links to all these talks when they become available. Here are the videos & slides for these talks:

- [Ambitious Capybara by Eduardo Gutierrez](http://confreaks.tv/videos/railsconf2015-ambitious-capybara) — [slides](https://speakerdeck.com/ecbypi/ambitious-capybara)
- [RSpec: It’s Not Actually Magic by Noel Rappin](http://confreaks.tv/videos/railsconf2015-rspec-it-s-not-actually-magic) — [slides](https://speakerdeck.com/noelrap/rspec-it-isnt-actually-magic)
- [Ruby on Rails on Minitest by Ryan Davis](http://confreaks.tv/videos/railsconf2015-ruby-on-rails-on-minitest) — [slides (pdf)](http://www.zenspider.com/presentations/2015-railsconf.html)
