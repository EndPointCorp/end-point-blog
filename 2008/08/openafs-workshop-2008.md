---
author: Steven Jenkins
title: OpenAFS Workshop 2008
github_issue_number: 43
tags:
- conference
- open-source
- openafs
date: 2008-08-13
---

This year’s [Kerberos and OpenAFS Workshop](http://workshop.openafs.org/afsbpw08/) was very exciting. It was the first I’ve attended since the workshop was large enough to be held separately from USENIX LISA, and it was encouraging to see that this year’s workshop was the largest ever, with well over 100 in attendance, and over 10 countries represented. Jeff Altman of [Secure Endpoints](http://www.secure-endpoints.com) did a great job on coordinating the workshop. Kevin Walsh and others at New Jersey Institute of Technology did a fantastic job in hosting, providing the workshop with a good venue and great service.

My summary of the workshop is “energy and enthusiasm” as several projects that have been in the development pipeline are starting to bear fruit.

On the technical side, the workshop keynote kicked off the week with a presentation from Alistair Ferguson from Morgan Stanley, where he noted that the work on demand attach file servers has reduced their server restart times from hours, down to seconds, greatly easing their administrative overhead while making AFS even more highly-available.

Of particular technical note, Jeff Altman reported that the Windows client has had lots of performance and stability changes, with major strategic changes being delivered later this year. Specifically, support for Unicode objects is coming in June, support for disconnected operation is coming in the Fall, and a long-awaited native file system driver will be delivered in December. This work will combine to make the Windows client not just a full-featured AFS client, but also a more solid Windows application.

Hartmut Reuter presented another exciting development work: Object Storage for AFS. This extension to both the AFS client and file server allows for AFS data to be striped across multiple servers (thus allowing for higher network utilization) as well as mirrored (giving higher availability). While this work is not yet in OpenAFS, it is in production at [CERN](https://home.cern/) and [KTH](https://www.kth.se/), and work is underway to integrate it into an OpenAFS release.

A major organizational boost was discussed during the workshop: OpenAFS was accepted as a sponsoring organization in the Google Summer of Code and received support for 6 students. Among other projects, these students will be working on support for disconnected operations, enhancements to the Windows client, and improving the kafs implementation of the AFS client sponsored by Red Hat.

The most significant announcement at the workshop is that work is underway to create an organizational entity to support OpenAFS. The OpenAFS Elders have announced the intention to have a 501(c)(3) corporation started in July that will serve as the legal entity behind OpenAFS. From a code standpoint, the licensing of OpenAFS will not change, but from an operational standpoint, people will be able to donate goods, services, and intellectual property to OpenAFS, something that is not currently possible. The foundation will not offer support services as there are currently several companies doing so, but it will be focused on the non-profit components of AFS.

There were several other very interesting talks at the workshop, but the overall message was clear: users and developers are extending OpenAFS and keeping it fresh and viable as the distributed filesystem of choice.
