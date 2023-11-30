---
author: Ethan Rowe
title: Messaging, Information, and Making Assertions About Stuff You Cannot See
github_issue_number: 129
tags:
- rails
date: 2009-04-09
---



My coworker/friend/distractobot Jon pointed me at this most interesting public HTML resource:

> 
> [http://www.unlimitednovelty.com/2009/04/twitter-blaming-ruby-for-their-mistakes.html](http://www.unlimitednovelty.com/2009/04/twitter-blaming-ruby-for-their-mistakes.html)
> 

We’ve done a fair amount of investigation in recent years of the free, open messaging field to try to identify the “best” free/open messaging solution. “Best” in quotes because, in software, the belief that one has found the “best” solution for given problem X often says a lot more about the person holding the belief than it says about the solution itself or problem X.

In a survey of messaging options done for a client last year, we determined (at that time) that [ActiveMQ](https://activemq.apache.org) was likely a good solution for the client’s needs. For simple deployments/usage, setup is quite straightforward. There’s good cross-language client support (particularly thanks to native STOMP support). There’s positive feedback out in the community about ActiveMQ. It’s an active project that’s been making decent progress over the years. Etc.

But then the little horror stories pop up. You hear/read that ActiveMQ falls down in various situations. Without getting any visibility into the specifics, it’s impossible to know what the problem is, or effectively use the information to intelligently inform any decisions regarding messaging solution selection. You’re left with creeping fear and its wonderful offspring: indecision. Yay.

This is what I find so interesting about the blog article (and subsequent comments) mentioned above: the author reads about Twitter moving away from Ruby and towards Scala, and embracing another custom-made messaging solution, and the author has the audacity/courage/hubris/expertise to offer an at-times withering critique of the reasons presented by Twitter, the design decisions evident in Starling, and so on. All done without visibility into the organization itself, but with expert knowledge of many of the tools involved in the discussion. It’s rather awe-inspiring to see somebody publicly rip into an organization in this way in such circumstances (“awe” is what it is, neither good nor bad). I personally cannot imagine going after somebody else’s technical decisions in a public forum like this, given only the results of their work (the source code to Starling, for instance) and a few out-of-context quotes from an interview. I suppose it’s reasonably sane to criticize Microsoft publicly for their absurd decisions (Windows 95/98/XP/Vista? Are you serious?), but that’s about as satisfying and informative at this point as mocking Britney Spears.

Anyway, back to the original point: the author offers this intelligent, partially-informed critique, and the Twitter guys jump in and offer feedback and more information in the comments. Beyond that, a guy from the [the RabbitMQ community](http://www.rabbitmq.com) joins in the fun to defend the Twitter folks and to offer some additional background. The end result is a satisfying 30 minutes’ read that was far more informative and enlightening to me on the subject of messaging in particular than any of the research I had done previously.

Nothing escapes unscathed, except perhaps Scala and Kestrel. ActiveMQ, RabbitMQ, Starling, etc. all have problems within the context of Twitter. So, going back to the creeping fear: uh oh, all of these fell down, does that mean they’re all lame?

No. It means they’re software. Perfect isn’t an option. You only need stuff that’s good enough, and the definition of “good enough” varies by business need.

When you search around for information on message brokers and client support in Ruby, you get a lot of seemingly-helpful-yet-ultimately-near-useless blog articles. To generically paraphrase:

> 
> Messaging is really important these days, and I searched around for the right messaging solution for my app. I took these steps to get ActiveMQ working, and it Just Works. Now the 6 people worldwide who use my really awesome Rails app will get really, really awesome results.
> 

“Technology Solution X: It ‘Just Works’ for Apps with No Users.”

That’s a little harsh, since the ease of deployment/integration of any given software component is a relevant consideration for any project with a budget or timeline. People solving problems for modest applications still contribute meaningfully to the community overall by sharing their experiences with setup, configuration, etc. But this kind of information is not very helpful when making decisions for systems that really matter to lots of people. Which is why the cited blog article and its comment thread is so terrific; no breathless endorsements or cheerleaderisms, just technically-informed discussion that tells you a lot more about the products discussed than does a “look how easy it was to use this” article.

Ultimately, it boils down to a truth that ought to be self-evident at all times. The awesomeness of a given solution depends primarily upon the need to which it is applied. If I need to add 3 to 7, my calculator Just Works. So does my network of brain cells. Which solution is better? It depends on what you need to do with the answer.

So, is ActiveMQ a great solution? Is, perhaps, RabbitMQ a better choice? Should I perhaps put on my hot pantz and get cracking with [Kestrel](https://github.com/twitter-archive/kestrel)? At present, my response is: better for what? “Messaging” alone isn’t an answer. The data available in the public sphere does not give a compelling answer, from what I can see, and my own (limited) experience does not give a clear answer either. Perhaps the more relevant question is “which can be made to work in my environment more easily”? And the most important consideration of all remains: how good are your people?


