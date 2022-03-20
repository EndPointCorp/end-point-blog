---
title: "VisionPort Hardware Overview"
author: Alejandro Ramon
github_issue_number: 1826
tags:
- visionport
featured:
  visionport: true
  image_url: /blog/2022/01/visionport-hardware-overview/in-wall-tech-specs.jpg
date: 2022-01-24
---

![A VisionPort system, with labeled servers, wall, displays, and controllers](/blog/2022/01/visionport-hardware-overview/in-wall-tech-specs.jpg)

End Point’s VisionPort has gone through a number of hardware iterations before becoming the system our clients are familiar with today. In this post, we will break down the history of the changes we have made over the years, and how we ended up where we are today.

The latest server specification used for all current VisionPort installations is known internally as the “LGOne” (Liquid Galaxy One): a node that can support up to eight discrete displays as a single desktop. LGOne is now considered the default specification and will guide the direction and future of VisionPort platform development.

### A few definitions before we continue

- **Node**: a single computer/​server.
- **Display node**: A computer that acts as a source for the displays, and runs applications.
- **Head node**: A computer that acts as the “brain” of the system.

### Some history

The original server specification for the Liquid Galaxy (now known as [VisionPort](https://www.visionport.com/)), was developed around **2011** and is now known as “LGClassic”. The LGClassic specification supported one display per node. For the typical seven-screen installation, this meant that eight individual LGClassic display nodes and one head node were required to run our seamless video wall technology with an integrated podium. While the experience was seamless for users, improvements to the performance, flexibility, and overall cost could be made.

Around **2015**, advances in graphics and computing technology allowed us to proceed to the next generation: the LGX. LGX nodes supported up to four discrete displays, and thus brought the number of display nodes necessary to run a typical seven-screen installation down to two. This meant that users could experience improved performance and syncing of applications, fewer points of failure, and more modern components. Around this same time, the CMS (Content Management System, known internally as “Roscoe CMS”) was released with a modern interface and tools that made it easier for users to generate content quickly for their system. Still, there were some nuances that affected performance and made content creation less than ideal, like how a seemingly seamless video wall was in actuality two discrete computer desktops. 

Although the LGX line of systems have been updated with newer graphics cards and processors over the years, there have been few significant changes to the standard server specification since 2016. As of 2021, the majority of existing systems in the field continue to utilize the LGX specification.

Released in early **2020**, LGOne continued the trend towards improved reliability, performance, and feature support. Systems with an LGOne specification can expect: 

- Support for 8 (typical) to 16 (advanced) discrete displays running full-resolution application imagery without the need for expensive AV technology such as digital matrix switchers or video wall processors. 
- A unified desktop experience, greatly simplifying content creation for CMS users. Consider no rules, borders, or needing to split up images to act a specific way. Simply drag and drop the image anywhere on screen to place it. Images, web pages, and videos can easily span all screens as well, if desired. In addition, support for graphic transparency allows presentation creators flexibility in how they present their content to viewers.
- Increased stability and performance of the system with enterprise grade Nvidia Quadro RTX graphics and Intel Xeon processors.
- Reduced server room footprint allows for simpler installation and maintenance with fewer moving parts.
- Support for technology integrations, like native [Video Conferencing](/blog/2021/09/video-conference-integration/) or [Screen Sharing solutions](/blog/2021/09/liquid-galaxy-screen-share-integration/).
- Support for [live view and remote control](/blog/2021/09/introducing-visionport-remote/), for when a user is not in the office.
- Improved window management tricks that allow for improved scene transitions and smarter content switching.

![A server with: Peripheral equipment, network switch, power distribution unit, head node, display node, all in a section called 9U](/blog/2022/01/visionport-hardware-overview/lgone-stack.jpg)  
The LGOne server stack

In addition to all the above, standardization of the spec allows VisionPort systems with the LGOne specification to support all of our future development. This includes an upcoming rewrite to the CMS with a new interface, improved workflow, and a significant change to how content is previewed. As always, any customer with an up-to-date maintenance agreement will receive all updates and support for the above when made available.

Over the years we have received plenty of feedback and insight into how the system is used by our client base. We hope that the changes we are making, and will continue to work on, show the effort to respect our users, encourage excitement in using the system, and provide better tools towards creating dynamic and impactful presentations for your customers and consumers.

Please reach out to [sales@visionport.com](mailto:sales@visionport.com) for any questions about pricing and availability or visit [www.visionport.com](https://www.visionport.com/) to learn more.
