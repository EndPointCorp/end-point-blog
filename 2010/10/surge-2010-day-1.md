---
author: Jon Jensen
title: Surge 2010 day 1
github_issue_number: 359
tags:
- conference
- hosting
- performance
- scalability
date: 2010-10-01
---



Today (technically, yesterday) was the first day of the [Surge 2010](https://web.archive.org/web/20101015004118/http://omniti.com/surge/2010/) conference in Baltimore, Maryland. The Tremont Grand venue is perfect for a conference. The old Masonic lodge makes for great meeting rooms, and having a hallway connect it to the hotel was nice to avoid the heavy rain today. The conference organization and scheduling and Internet have all been solid. Well done!

There were a lot of great talks, but I wanted to focus on just one that was very interesting to me: [Artur Bergman](https://web.archive.org/web/20101127040749/http://omniti.com/surge/2010/speakers/artur-bergman)’s on scaling Wikia. Some points of interest:

- They (ab)use Google Analytics to track other things besides the typical pages viewed by whom, when. For example, page load time as measured by JavaScript, with data sent to a separate GA profile for analysis separately from normal traffic. That is then correlated with exit rates to give an idea of the benefit of page delivery speed in terms of user stickiness.

- They use the excellent Varnish reverse proxy cache.

- 500 errors from the origin result in a static page served by Varnish, with error data hitting a separate Google Analytics profile.

- They have both geographically distributed servers and team.

- They’ve found SSDs (solid state disks) to be well worth the extra cost: fast, using less power in a given server, and requiring fewer servers overall. They have to use Linux software RAID because no hardware RAID controllers they’ve tested could keep up with the speed of SSD. They have run into the known problems with disk write performance dropping as they fill and recycle, but haven’t found it to be a problem when used on replaceable cache machines.

- They run their own CDN, with nodes running Varnish, Quagga (for BGP routing), BIND, and Scribe. But they use Akamai for static content.

- Even running Varnish with 1 second TTL can save your backend app servers when heavy traffic arrives! One hit per second is no problem; thousands may mean meltdown.

- Serving stale cached content when the backend is down can be a good choice. It means most visitors will never know anything was wrong. (Depends on the site’s functions, of course.)

- Their backup datacenter in Iowa is in a former nuclear bunker. See [monitoring graphs](https://web.archive.org/web/20101030001235/http://ganglia.wikia.net/iowa/) for it.

- Wikia ops staff interact with their users via IRC. This “crowdsourced monitoring” has resulted in a competition between Wikia ops people and the users to see who can spot outages first.

- Having their own hardware in multiple redundant datacenters has meant much more leverage in pricing discussions with datacenters. “We can just move.”

- They own their own hardware, and run on bare metal. At no time does user traffic pass through any virtualized systems at all. The performance just isn’t there. They do use virtual machines for some external monitoring stuff.

- They use Riak for N-master inter-datacenter synchronization, and RiakFS for sessions and files. RiakFS is for the “legacy” MediaWiki need for POSIX access to files, but they can serve those files to the general public from Riak’s HTTP interface via Varnish cache.

- They use VPN tunnels between datacenters. Sometimes using their own routes, even over multiple hops, leads to faster transit than going over the public Internet.

- Lots of interesting custom VCL (Varnish Configuration Language) examples.

This had plenty of interesting things to consider for any web application architecture.


