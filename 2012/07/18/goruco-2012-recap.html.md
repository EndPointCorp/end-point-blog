---
author: Brian Buchalter
gh_issue_number: 671
tags: conference, ruby
title: GoRuCo 2012 Recap
---

A few weeks ago, End Point graciously agreed to send me to [GoRuCo](http://goruco.com/), “the premier Ruby conference in New York City”. I was excited to try and apply the lessons from our own [Greg Sabino Mullane](/team/greg_sabino_mullane), who gave a talk about attending conferences during End Point’s 2012 Company Meeting. He emphasized a focus on interacting with the speakers and attendees instead of the presentation content.

### Pre Party at Pivotal Labs

The pre-party was located just blocks away from our offices, making it a convenient after work stop. On my walk to the party, I tried to think about the type of connections I wanted to make and the topics I wanted to discuss. I was intrigued by Pivotal Lab’s policy on [pair programming](https://web.archive.org/web/20120527192714/http://pivotallabs.com/how/pair_programming), but realized I could continue to read up about that extensively online. What was a question I could ask that would be interesting for both asker and askee, providing me something a Google search couldn’t?

After the usual introductory chit chat, I found myself asking, “so, what are you struggling with in your work right now?” It was broad and open, giving the speaker a chance to perhaps go somewhere outside of the normal conversation. I asked [Haris Amin](https://www.youtube.com/watch?v=Ahwb_PU5WxY) this question and got what would become a fairly typical answer. He summarized his struggle as one of keeping up with the firehose of his interests. So many great technologies are springing from all corners of creation, there simply aren’t enough hours in the day to investigate them all. This resonated against our own [Jon Jensen’s](/team/jon_jensen) comments during the company meeting about it being a golden age for technology.

I also got to meet and chat with [Coby Randquist](https://twitter.com/kobier), the creator of [Confreaks](http://www.confreaks.com/). It was great learning about his transition from implementer to manager. As a manager, he found he loved that he could solve much bigger problems than as a developer by bringing together talent and keeping “everyone else out of their way”.

### A Sampling of the Main Event

Of course there were so many great presentations, which you can [watch at your leisure](https://vimeo.com/album/1988817/sort:preset/format:detail), but because there are always more presentations than time, I’ll focus on one that I found particularly interesting. [Dr. Nic](https://web.archive.org/web/20120627044259/http://goruco.com/speakers/2012/05/22/williams-nic.html) gave a talk called [The Future of Deployment](https://vimeo.com/album/1988817/video/44807823) ([slides](https://speakerdeck.com/u/drnic/p/future-of-deployment-goruco-2012)) which he laid out an argument for being able to able to version control and deploy not only our applications, but the infrastructure which supports them, all with a unified tool.

He lays out some interesting demands of this tool, including:

- An explicit description of all infrastructure dependencies
- The ability to manage all parts of this infrastructure, from the size of our AWS instances, to the particular version of Nginx we’re running.
- Full version control/history of these descriptions
- A central API for all activities

As if this weren’t challenging enough, he mentions it’d be nice to have:

- Independent install paths; if we can use .../releases/TIMESTAMP for Capistrano deployments, why not the same for Ruby and Nginx?
- Portable enterprise deployments; we should be able to offer our applications as a self building system *behind* the firewall

So what’s the magical tool which will finally solve all our deployment problems? He offers [BOSH](https://bosh.io/docs/), “an open source tool chain for release engineering, deployment and lifecycle management of large scale distributed services”. It was created to manage *really* big deployments, so Dr. Nic argues perhaps it can also meet our smaller needs. BOSH is kind of a bear to get your head around, so Dr. Nic helpfully created a more palatable [Getting Started](https://github.com/cloudfoundry-community-attic/LEGACY-bosh-getting-started) series that can help bootstrap your experience.

If you’re interested in hearing more about why we should care about BOSH, I’d say watch [the presentation](https://vimeo.com/album/1988817/video/44807823), but if you don’t need to be sold on the idea and know you need it, the presentation is *not* about BOSH really at all, outside of it offering to address some of Dr. Nic’s requirements above.
