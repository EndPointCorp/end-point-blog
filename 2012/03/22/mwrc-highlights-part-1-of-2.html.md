---
author: Brian Gadoury
gh_issue_number: 575
tags: conference, ruby, rails
title: MWRC Highlights Part 1 of 2
---

I attended the [2012 Mountain West Ruby Conference](http://mtnwestrubyconf.org/) in Salt Lake City last week. There were a lot of cool topics presented at this conference, but I've been suffering serious analysis paralysis trying to pick one topic to focus on here. So, I'm taking the easy way out. I'm going to run through some of the projects and tools mentioned during the conference that I flagged in my notes to check out further.

### Sidekiq, a multi-threaded drop-in replacement for Resque

- Sidekiq requires *much* less RAM to do the same amount of work as the single-threaded Resque, while providing a very similar API to Resque. It’s been designed to behave like Resque as much as possible and as such, would be a very easy transition for anyone that’s used Resque before.
- By [Mike Perham](http://blog.carbonfive.com/2011/09/16/improving-resques-memory-efficiency/)
- Get it at: [mperham.github.com/sidekiq](http://mperham.github.com/sidekiq/)
- Recommended by: [Tony Arcieri](http://www.unlimitednovelty.com/)

### Book: Growing Object-Oriented Software Guided by Tests (aka GOOS)

- The "GOOS book" was recommended by a number of speakers at the conference. One downside (for me) is that the Auction Sniper app developed in the book is done in Java. However, there are now ports of that code available in Ruby, Scala, C# and Groovy. Check out the book's website. The table of contents is very detailed, so you know what you're getting into.
- By Steve Freeman and Nat Pryce
- Get it at [www.growing-object-oriented-software.com](http://www.growing-object-oriented-software.com)
- Recommended by: Multiple presenters

### PRY, a very powerful irb replacement and Rails debugging tool

- It's difficult to describe PRY without using the word "powerful" in every sentence. It really is, well, that powerful. It speeds up some of the things you already do when writing Ruby code. It also enables you to do things you wish you could do when writing Ruby and Rails code. The [8-minute Ryan Bates Railscast on PRY](http://railscasts.com/episodes/280-pry-with-rails) shows it better than I can describe it.
- Core team: [John Mair](https://github.com/banister), [Conrad Irwin](https://github.com/conradirwin) and [Ryan Fitzgerald](https://github.com/rwfitzge)
- Get it at [pry.github.com](http://pry.github.com)
- Recommended by: [Corey Woodcox](https://github.com/cwoodcox)

### "Ruby is a tool that gets out of your way. Build **that** for your clients."

- More an ethos than a project or tool, this is a relatively direct quote from Jamis Buck in his talk entitled, "It's the Little Things." Part of what he talked about were the features or patterns of Ruby that tickle part of our brain and just feel right, natural or easy-flowing. The tools or apps that we build for our clients should have for that same sense of flow. I think achieving that requires a perspective shift that's not easy for many developers, but it's absolutely something worth aspiring to. Our clients deserve that.
- As said by Jamis Buck from [37Signals.com](http://37signals.com/)

Attending this conference was honestly pretty inspiring. It was my first Ruby conference, and it was exciting to hear some very knowledgeable people speak passionately about what they work on and how they work. I definitely have a lot more reading and investigation to do. Part 2 of this article will cover the remaining conference topics that I felt deserved a shout out. I'll probably do that in the next day or two.
