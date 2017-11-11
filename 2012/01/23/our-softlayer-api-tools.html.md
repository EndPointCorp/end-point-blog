---
author: Jon Jensen
gh_issue_number: 546
tags: hosting, networking, open-source, sysadmin
title: Our SoftLayer API tools
---

We do a lot of our hosting at [SoftLayer](http://www.softlayer.com/), which seems to be one of the [hosts with the most servers](http://www.datacenterknowledge.com/archives/2009/05/14/whos-got-the-most-web-servers/) in the world -- they claim to have over 100,000 servers as of last month. More important for us than sheer size are many other fine attributes that SoftLayer has, in no particular order:

- a strong track record of reliability
- responsive support
- datacenters around the U.S. and some in Europe and Asia
- solid power backup
- well-connected redundant networks with multiple 10 Gbps uplinks
- gigabit Ethernet pipes all the way to the Internet
- first-class IPv6 support
- an internal private network with no data transfer charge
- Red Hat Enterprise Linux offered at no extra charge
- diverse dedicated server offerings at many price & performance points
- some disk partitioning options (though more flexibility here would be nice, especially with LVM for the /boot and / filesystems)
- fully automated provisioning, without salesman & quote hassles for standard offerings
- 3000 GB data transfer per month included standard with most servers
- month-to-month contracts
- reasonable prices (though we can of course always use lower prices, we'll take quality over cheapness for most of our hosting needs!)
- no arbitrary port blocks (some other providers rate-limit incoming TCP connections on port 22 to slow down ssh dictionary attacks, while others forbid IRC, etc.)
- a web service API for monitoring and controlling many aspects of our account via REST/JSON or SOAP

(No, they're not paying me for writing this! But they really have nice offerings.)

It is this last item, the SoftLayer API, that I want to elaborate on here.

The [SoftLayer Development Network](http://sldn.softlayer.com/) features API information and documentation and once you have an API account set up in the management website (quick and easy to do), you can start automating all sorts of tasks, from provisioning new hosts, monitoring your upcoming invoice or other accounting information, and much more.

I've released as open source two scripts we use: One is for managing secondary DNS domains in SoftLayer's DNS servers, from a primary name server running BIND 9. The other is a Nagios check script for monitoring monthly data transfer used and alerting when over a set threshold or over the monthly allotment.

See the GitHub repository of [endpoint-softlayer-api](https://github.com/jonjensen/endpoint-softlayer-api) if they would be useful to you, or to use as a starting point to interface with other SoftLayer APIs.
