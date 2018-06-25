---
author: Steven Jenkins
gh_issue_number: 72
tags: conference, community, openafs
title: Ohio Linux Fest AFS Hackathon
---

The one-day [Ohio Linux Fest](https://ohiolinux.org/) AFS Hackathon flew by in a hurry. Those new to OpenAFS got started converting some commented source code into Doxygen-usable format to both improve the code documentation as well as get a feel for some of the subsystems in OpenAFS. Several of the developers took advantage of the time to analyze some outstanding issues in Demand Attach (DAFS). We also worked on some vldb issues and had several good conversations about AFS roadmaps, Rx OSD, the migration from CVS to Git, and the upcoming Google-sponsored AFS hackathon.

The Doxygen gave those new to OpenAFS code a chance to look under the covers of OpenAFS. [Doxygen](http://www.stack.nl/~dimitri/doxygen/) produces pretty nice output from simple formatting commands, so it’s really just a matter of making comments follow some basic rules. Sample Doxygen output (from some previous work) can be seen [here](https://web.archive.org/web/20081028152756/http://charles.endpoint.com/doxygen/html/ubik_8c.html), and some of the new Doxygen changes made to OpenAFS are already.

The Demand Attach work focused on the interprocess communications pieces, namely the FSSYNC & SALVSYNC channels, specifying requirements and outlining the approaches for implementing bi-directional communications so that the failure of one process would not leave a volume in an indeterminate state. Some coding was done to address some specific locking issues, but the design and implementation of better interprocess volume state management is still an open issue.

The OpenAFS Roadmap discussion revolved around 3 major pieces: CVS to Git conversion, Demand Attach, and Rx OSD. DAFS is in the 1.5.x branch currently, but Rx OSD is not. The general consensus was that DAFS plus some of Rx OSD might be able to go into a stable 1.6 release in Q1 of 2009, which would also let the Windows and Unix stable branches merge back together.

However, the major goal in the short term is to get the CVS to Git migration done to make development more streamlined. Derrick Brashear, Mike Meffie, and Fabrizio Manfredi are all working on this.

The 1.6 merge, DAFS, and Rx OSD are all still very much works-in-progress in terms off getting them into a stable release together. While individually, DAFS and Rx OSD have been used by some OpenAFS installations in production, there is a lot more work to be done in terms of getting them integrated into a stable OpenAFS release.

Overall, the hackathon went very well, with some new AFS developers trained, and some progress made on existing projects. Many thanks to the Ohio Linux Fest for their support, and to Mike Meffie specifically for his efforts in coordinating the hackathon.
