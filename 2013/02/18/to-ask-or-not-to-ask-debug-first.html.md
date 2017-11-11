---
author: Miguel Alatorre
gh_issue_number: 763
tags: programming
title: To ask or not to ask? Debug first.
---



Jumping head first into a project, the ramp up will likely lead to questions galore. In the eagerness of getting things done, it seems like the best thing to do when stuck is to just ask the seasoned developers to tell you how to move forward. After all, they did build the application. However, when to reach out for help can be dependent on the deadline and priority of the task at hand as well as your subjective definition of "stuck." Knowing when it's too early, just right, or too late to get help can be a tricky thing. Here are some things to consider when reaching out for help early:

Pros.

 1. Time/money is of the essence and getting a quick answer is best.

 2. Time saved debugging a particular issue that does not further your understanding of the application can be applied elsewhere.

Cons.

 1. You risk a learning opportunity by throwing in the towel too early.

 2. You risk looking lazy or unprepared if the person whom you are reaching out to believes you could have done more.

 3. Developers are busy, too.

All cases being different, there is no right time to reach out for help but steps can be taken to ensure that you have your part. First, get better at reading source code. The more you practice reading and making sense of other people's code, the quicker you will build your complete mental model of the application, and the quicker you'll be able to debug. Brandon Bloom (snprbob86) wrote an [excellent post](http://news.ycombinator.com/item?id=3769446) regarding this. Second, create your own stack trace. The application may have many entry points. Pick one, feed it some input and trace it down the rabbit hole. A white board may come in handy here. Third, make heavy use of the logs. The code should already be sprinkled with plenty of log messages, but feel free to add more wherever you feel they will be useful.

These three tips will go a long way in helping you debug smarter, which should allow you to find solutions more quickly. In the event that a white flag must be raised and another developer's help requested, the efforts you made attempting to debug will have a positive impact on your productivity as well as your team's perception of you as a programmer.


