---
author: Emanuele “Lele” Calò
gh_issue_number: 1288
tags: conference, open-source, cloud
title: 'FOSDEM 2017: experience, community and good talks'
---

In case you happen to be short on time: my final overall perspective about FOSDEM 2017 is that it was awesome... with very few downsides.

If you want the longer version, keep reading cause there’s a lot to know and do at FOSDEM and never enough time, sadly.

This year I actually took a different approach than last time and decided to concentrate on one main track per day, instead of (literally) jumping from one to the other. While I think that overall this may be a good approach if most of the topics covered in a track are of your interest, that comes at the cost of missing one of the best aspects of FOSDEM which is “variety” in contents and presenters.

### Day 1: Backup & Recovery

For the first day I chose the Backup & Recovery track which hosted talks revolving around three interesting and useful projects: namely [REAR (Relax and Recovery)](http://relax-and-recover.org), [DRLM](http://drlm.org), a wrapper and backup management tool based on REAR and [Bareos](https://www.bareos.org/en/), which is a backup solution forked from [Bacula](http://blog.bacula.org/) in 2010 and steadily proceeding and improving since then. Both REAR and DLRM were explained and showcased by some of the respective projects main contributors and creators. As a long time system administrator, I particularly appreciated the pride in using Bash as the main “development platform” for both projects. As **Johannes Meixner** correctly mentioned, using bash facilitates introduces these tools into your normal workflow with knowledge that you’ll most likely already have as a System Administrator or DevOps, thus allowing you to easily “mold” these scripts to your specific needs without spending weeks to learn how to interact with them.

During the Day 1 Backup & Recovery track there were also a few speeches from two Bareos developers (**Jörg Steffens** and **Stephan Dühr**) that presented many aspects of their great project, ranging from very introductory topics, to providing a common knowledge ground for the audience, up to more in depth topics like software capabilities extension through Python Plugins, or a handful of best practices and common usage scenarios. I also enjoyed the speech about automated testing in REAR, presented by **Gratien D’haese**, which showed how to leverage common testing paradigms and ideas to double-check a REAR setup for potential unexpected behaviors after updates or on new installations or simply as a fully automated monitoring tool to do sanity checks on the backup data flow. While this testing project was new, it’s already functional and impressive to see at work.

### Day 2: Cloud Microservices

On the second day I moved in a more *“cloudy”* section of the FOSDEM where most of the conferences revolved around **Kubernetes**, **Docker** and more in general the microservices landscape. **CoreOS** (the company behind the open source distribution) was a major contributor and I liked their Kubernetes presentation by **Josh Wood** and **Luca Bruno** which respectively explained the new Kubernetes Operators feature and how containers work under the hood in Kubernetes.

Around lunch time there was a “nice storm of lightning talks” which kept most of the audience firmly on their seats, especially since the Microservices track room didn’t have a free seat for the entire day. I especially liked the talk from **Spyros Trigazis** about how CERN created and is maintaining a big OpenStack Magnum (the container integrated version of OpenStack) cloud installation for their internal use.

Then it was **Chris Down’s** turn and, while he’s a developer from Facebook, his talk gave the audience a good perspective on the future of CGROUPs in the Linux kernel and how they are already relatively safe and usable, even if not yet officially marked as production ready. While I already knew and used “sysdig” in past as a troubleshooting and investigation tool, it was nice to see one of the main developers, **Jorge Salamero**, using it and showing alternative approaches such as investigating timeout issues between Kubernetes Docker containers by just sysdig and its many modules and filters. It was really impressive seeing how easy it is to identify cross-containers issues and data flow.

### Atmosphere

There were a lot of Open Source communities with “advertising desks” and I had a nice talk with a few interesting developers from the CoreOS team or from FSFE (Free Software Foundation Europe). Grabbing as many computer stickers as possible is also mandatory at FOSDEM, so I took my share and my new Thinkpad is way more colorful now. In fact, on a more trivial note, this year the FOSDEM staff decided to sell on sale all the laptops that were used during the video encoding phase for the streaming videos before the upload. These laptops were all IBM Thinkpad X220 and there were only a handful of them (~30) at a very appealing price. In fact, this article is being written from one of those very laptops now as I was one of the lucky few which managed to grab one before they were all gone within an hour or so. So if you’re short of a laptop and happen to be at FOSDEM next year, keep your eyes open cause I think they’ll do it again!

So what’s not to like in such a wonderful scenario? While I admit that there was a lot to be seen and listened to, I sadly didn’t see any “ground-shaking” innovation this year at FOSDEM. I did see many quality talks and I want to send a special huge “thank you” to all the speakers for the effort and high quality standards that they keep for their FOSDEM talks—​but I didn’t see anything extraordinarily new from what I can remember.

Bottom line is that I still have yet to find someone who was ever disappointed at FOSDEM, but the content quality varies from presenter to presenter and from year to year, so be sure to check the presentations you want to attend carefully before hand.

I think that the most fascinating part of FOSDEM is meeting interesting, smart, and like-minded people that would be difficult to reach otherwise.

In fact, while a good share of the merit should be attributed to the quality of the content presented, I firmly believe that the community feeling that you get at FOSDEM is hard to beat and easy to miss when skipped even for one year.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/02/13/fosdem-2017-experience-community-and/image-0.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="480" src="/blog/2017/02/13/fosdem-2017-experience-community-and/image-0.jpeg" width="640"/></a></div>

I’ll see you all next year at FOSDEM then.
