---
author: Josh Williams
gh_issue_number: 1020
tags: conference, postgres, python
title: 'PyOhio 2014: Python FTW!'
---

<div class="separator" style="clear: both; float:right; margin-bottom: 1em; margin-left: 1em;"><img src="http://joshwilliams.name/PLPython/2014/badge.jpg"/></div>

Just got back from [PyOhio](http://www.pyohio.org/) a couple of days ago.  Columbus used to be my old stomping grounds so it's often nice to get back there.  And PyOhio had been on my TODO for a number of years now, but every time it seemed like something else just got in the way.  This year I figured it was finally time, and I'm quite glad it worked out.

While of course everything centered around usage with Python, much of the talks surrounded other tools or projects.  I return with a much better view of good technologies likes [Redis](http://redis.io/), [Ansible](http://www.ansible.com/), [Docker](http://docker.com/), [ØMQ](http://zeromq.org/), [Kafka](http://kafka.apache.org/), [Celery](http://celeryproject.org/), [asyncio in Python 3.4](https://docs.python.org/3/library/asyncio.html), [Graphite](http://graphite.wikidot.com/), and much more that isn't coming to mind at the moment.  I have lots to dig into now.

It also pleased me to see so much Postgres love!  I mean, clearly, once you start to use it you'll fall in love, that's without question.  But the hall track was full of conversations about how various people were using Postgres, what it tied in to in their applications, and various tips and tricks they'd discovered in its functionality.  Just goes to prove that Postgres == ♥.

Naturally PostgreSQL is what I spoke on; PL/Python, specifically.  It actually directly followed a talk on PostgreSQL's LISTEN/NOTIFY feature.  I was a touch worried about overlap considering some of the things I'd planned, but it turns out the two talks more or less dovetailed from one to the other.  It was unintentional, but it worked out very well.

Anyway, the [slides are available](http://joshwilliams.name/PLPython/2014/), but the talk wasn't quite structured in the normal format of having those slides displayed on a projector.  Instead, in a bit of an experiment, the attendees could hit a web page and bring up the slides on their laptops or such.  That slide deck opened a long-polling socket back to the server, and the web app could control the slide movement on those remote screens.  That let the projector keep to a console session that was used to illustrate PL/Python and PostgreSQL usage.  As you might expect, the demo included a run through the PL/Python and related code that drove that socket.  Hopefully the video, when it's available, caught some of it.

The sessions were recorded on video, but one thing I hadn't expected was how that influenced which talks I tried to attend.  Knowing that the more software-oriented presentations will be available for viewing later, where available I opted for more hardware-oriented topics, or other talks where being present seemed like it would have much more impact.  I also didn't feel rushed between sessions, on the occasions where I got caught in a hall track conversation or checked out something in the open spaces area (in one sense,a dedicated hall track room.)

Overall, it was a fantastic conference and a great thank you goes out to everyone that helped make it happen!
