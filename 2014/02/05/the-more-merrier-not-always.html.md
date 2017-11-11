---
author: Richard Templet
gh_issue_number: 921
tags: camps, imagemagick, performance
title: The more the merrier? Not always...
---



Recently we were working on an image manipulation function for a customer that used [ImageMagick](http://www.imagemagick.org/script/index.php)'s convert command. We had spent tons of time working on the program and the associated system that was going to use it. Everything was working fine. The whole system was nice and snappy. Great job everyone!

Until we moved it into production where the page load times were 8 to 10 times slower than in our [camps](http://www.devcamps.org) development system ...

We all sprang into action to try to figure out why the page load times were so slow now. We reviewed system settings, configuration files for the database and application, and anything else we could think of. We made sure the OS packages, ImageMagick version, and various other things were the same, and everything looked right. The production hardware has twice the RAM and 4 times the number of processors as development does. So what the heck is going on?

To distract ourselves and hope for more insight, we tried to optimize the code a bit and while making it a bit better we were still 6 to 8 times slower than in development. We deactivated the section of the site overnight so we could sleep on it. Luckily this was a new product line so it wasn't tragic to turn it off.

The next morning while discussing, a co-worker mentioned that the larger number of processors in production could be relevant. At first I was a bit taken aback because this goes against everything we think about more being better. How could it be that having 4 times the number of processors was a bad thing?!

Well, it turns out that ImageMagick is a threaded program and will use as many processors in parallel as it can to accomplish whatever task it is asked to do. In doing this instead of splitting up the convert over 8 processors, it was now splitting it up over 32 processors. The extra work it was taking to manage the work being split between those extra 24 processors actually greatly slowed down the processing work!

Luckily ImageMagick respects an environment variable setting to limit the maximum number of threads it will use. We set the OMP_NUM_THREADS environment variable to 4, re-ran the code, and then it performed as expected in production. It could be set to more or less threads, but we found that was fine and aside from keeping performance high, it keeps this one process from dominating CPU usage while it is running.

It was a very interesting riddle to solve so I figured I'd share it.


