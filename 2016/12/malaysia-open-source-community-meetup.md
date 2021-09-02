---
author: Muhammad Najmi bin Ahmad Zabidi
title: Malaysia Open Source Community Meetup Quarter 4 2015 (MOSCMY Q4 2015)
github_issue_number: 1274
tags:
- community
- open-source
date: 2016-12-09
---



After a year, finally I decided to publish this post to all of you!

On November 26th 2015 I had a chance to give a talk in a local open source conference here in Malaysia. The organizer requested me to specifically deliver a talk on “remote work”. This meetup was organized by Malaysian Development Corporation (MDEC) with the sponsorship of Microsoft Malaysia. Microsoft recently started to become more “open source friendly” given that they are in the effort of pushing their cloud based product, Azure. The full schedule of the event can be referred [here](http://lanyrd.com/2015/moscmy2015/).

The conference was divided into two sessions; where the morning session was held in Petronas Club, Tower One of Kuala Lumpur City Centre (KLCC) and the other session was held in Microsoft Malaysia’s office  in Tower Two KLCC. Generally the morning session was for non parallel track (including my track) and the afternoon sessions were two parallel sessions slot.

## Morning Session

The morning session started with a talk by Dinesh Nair, as the Director of Developer Experience and Evangelism, Microsoft Malaysia.  The second session in the morning was delivered by Mr Izzat M. Salihuddin, from Multimedia Development Corporation (MDeC), Malaysia. He spoke on the behalf of MDeC explaining the effort by MDeC as a government wing to realize the local cloud infrastructure. One of the challenges that being mentioned by Mr Izzat was the readiness of physical infrastructure as well as the broadband connectivity for the public. The final slot in the morning was delivered by me in which I explained much of the way of how End Pointers do their job, open source software that we used, as well as how we accomplish our job remotely. The morning session was adjourned with a lunch break.

<a href="/blog/2016/12/malaysia-open-source-community-meetup/image-0-big.jpeg" imageanchor="1"><img border="0" src="/blog/2016/12/malaysia-open-source-community-meetup/image-0.jpeg"/></a>

*Just in case if you are wondering, this is me delivering the talk on that day*

## Afternoon Session

The afternoon session was a parallel track session, where I chose to attend a talk on Ubuntu’s [Juju](http://www.ubuntu.com/cloud/juju) service. The talk was delivered by Mr Khairul Aizat Kamarudzaman from Informology. Mr Aizat’s slides for his talk could be read [here](http://www.slideshare.net/fenris/informology-introduction-to-juju). Later, Mr Sanjay shared his Asterisk skills in which the server is hosted on the Azure platform. Mr Sanjay showed to us how make phone call from the computer to the mobile phone. Asterisk is different from Skype because it is using an open protocol (SIP) and with open clients. Mr Sanjay showed a demo on his implementation, in which it looks like the setup is to compete with the typical PABX phone system.

For the next slot I decided to enter the slot on TCPTW kernel patch which was delivered by Mr Faisal from Nexoprima. As far as I understood, Mr Faisal reintroduced his own patch for the Linux kernel in order to handle TCP TIME_WAIT issue which was happened due to extremely busy HTTP requests. Since connection in TIME_WAIT state hold a local port for 1 minute and in many distro the default ports are up to 30,000, the effort put to search for free port(s) will use intensive CPU and it could was CPU cycle to purge tons of TIME_WAIT connections.

<a href="/blog/2016/12/malaysia-open-source-community-meetup/image-1-big.jpeg" imageanchor="1"><img border="0" src="/blog/2016/12/malaysia-open-source-community-meetup/image-1.jpeg"/></a>

*Mr Faisal gave his talks on TCPTW kernel patch*

Mr Faisal’s TCPTW patch for CentOS 7 could be viewed [here](https://github.com/efaisal/linuxtcptw/blob/master/centos/linux-3.10.0-229.1.2.el7.eafaisal.patch). His presentation slides could be viewed [here](http://www.scribd.com/doc/291238152/TIME-WAIT-Hack-for-High-Performance-Ephemeral-Connection-in-Linux-TCP-Stack).

Before went back home, I decided to enter a talk on “Dockerizing IOT Service” by Mr Syukor. In this talk Mr Syukor gave a bit theoretical background on Docker and how it can be used on Raspberry Pi board. You can view his slides [here](http://www.slideshare.net/msyukor/dockerizing-iot-services). My personal thought is that Raspberry Pi is versatile enough to run any modern operating system and Docker should not be much an issue.


