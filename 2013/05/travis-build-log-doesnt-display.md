---
author: Brian Gadoury
title: Travis build log doesn’t display
github_issue_number: 805
tags:
- browsers
- tips
date: 2013-05-23
---



Remember when “clear your cookies and try it again” was the first suggestion when a webpage was behaving badly? I remember that time of darkness, that time of early Internet Explorer, well, *existing*. I remember it being the only browser allowed in some offices and even being mandatory for some major websites. Remember that? Pepperidge Farm remembers.

But we’ve evolved. These are brighter days. Around these parts, “Did you clear your cookies?” is typically only said in jest. So, imagine my surprise when I accidentally discovered that clearing my cookies was exactly what resolved my issue with our Travis-CI.org build logs failing to display. Seriously. Imagine it. Go ahead, I’ll wait.

On March 21st 2013, the beautiful and talented Travis CI service deployed a bad build of their own app. It contained [a bug that caused build logs to fail to display](https://status.travis-ci.com/incidents/5fgmx0h0m930). You could still see the builds and statuses under the Build History tab, but never any logs. This was right about the same time I had pushed a big refactor that used a new config file format for our app. It passed all our tests locally, but it was driving me nuts that I couldn’t find out why it was failing on Travis. It was also displaying that sad-trombone <img alt="Build: Failing" border="0" src="/blog/2013/05/travis-build-log-doesnt-display/image-0.png" title="Build: Failing"/> image in our GitHub repo’s README.md.

The Travis crew actually fixed their bug just a few hours after it was discovered, but the issue persisted for me for a few days. I was confident enough in our local integration tests that I didn’t roll back, but it was driving me nuts. I believe it was Socrates that said, “It’s only after we’ve lost everything that we’re free to do anything.” So that’s what I did—​I cleared my cookies for no rational reason, and it worked. Travis logs, both old and new, started displaying correctly. Bam.

Lessons learned: It’s important to appreciate the classics (and also to [subscribe to Travis updates](https://status.travis-ci.com/).)


