---
author: Tim Case
title: How to pick a Ruby gem
github_issue_number: 706
tags:
- ruby
- rails
date: 2012-10-15
---

RubyGems are one of the big benefits of developing in the Ruby environment as they can provide you with a powerful set of building blocks that were created by some great developers. Earlier in my Ruby career I used to think of RubyGems as a quick way to get some "free" code into my applications and I would spend a tremendous amount of time trying to see what kind of apps I could concoct by stacking gem on top of gem. In practice this turned out to be foolish because rather than gaining a stack of "free" code what I was instead doing was "paying" for each gem by having to learn how each of these gems worked and what kind of assumptions and gotchas they were bringing into my apps. I changed my ideas about gems and now I opt by default to avoid adding gems to my projects, but when I do decide that a piece of functionality might be better served through a gem, I make sure to put potential candidates through a rigorous vetting process.

When looking for a gem the question I keep in mind is, "Does adding this gem to my project benefit me more than just writing these features by hand?" I measure the gem up against some criteria and if the answer remains yes then I'll add the gem.

### Criteria for gem evaluation

1. Does this gem support my application's Rails version?

The first thing I like to do when I find a gem is to check out the README on Github and see if Rails version information is included with the gem installation instructions. This gives me an idea about how up to date the gem is.

2. When was the last commit and how much recent activity does the gem have?

Again I'm trying to make a decision if the gem is still fresh or if it's exceeded its expiration date. The Rails world changes pretty fast and if a gem hasn't been touched in recent months then that's a good indication that the gem is out of date. Unfortunately Rubygems, especially gems for Rails have unwritten expiration dates and an old gem past its prime doesn't automatically get dropped off of github or rubygems.org, instead it just sits around without any activity.

3. Does the code look like what I expect it to?

Generally I can come up with a quick idea about how I think the gem should work and then I'll quickly scan through the gem's contents to see how my idea of the gem and its actual internals match up. If my understanding of how the gem should be and its actual implementation are too far off then this is an indicator that the gem might be more expensive to add in terms of maintenance and the learning I'll need to invest. If the gem's code is extremely complex and I barely understand how it works then that is a red flag that maybe this gem is going to take me on a wild ride.

4. Does it pass its unit tests and do the tests show me how the gem works?

I like to use unit tests as documentation that can show me quickly how a gem is intended to be used. I'll run the unit tests and if they pass that's kind of a gold bond measurement for me that the gem is worth using. I'll still consider using a gem even if the tests fail because sometimes a gem's tests will fail or be difficult to execute and that still won't be a deal breaker for me so long as I can reasonably follow why the tests might be failing.

After a gem has passed its vetting process I'll still keep an awareness about how the gem feels in my app and how much time I'm spending integrating it with what I'm trying to do. If I get the feeling that I'm spending too much time fighting with the gem and that it's not quite fitting with what I'm doing then I will consider pulling the plug and either using a different gem or writing the functionality by hand.

If you liked this discussion of picking out Ruby gems then I encourage you to check out the always excellent Railscasts by RyanB [who recently posted a video](http://railscasts.com/episodes/384-exploring-rubygems) about this very same topic.
