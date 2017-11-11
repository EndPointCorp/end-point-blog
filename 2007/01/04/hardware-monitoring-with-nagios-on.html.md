---
author: Jon Jensen
gh_issue_number: 15
tags: networking, monitoring, openbsd
title: Hardware Monitoring with Nagios on OpenBSD
---

At End Point we use Nagios and its remote client, NRPE, to monitor servers we manage and alert us to any problems. Aside from the usual monitoring of remote accessibility of services such as a website, database, SSH, etc., it's very helpful to have monitoring of memory usage, disk space, number of processes, and CPU load.

[In this detailed article](http://www.kookdujour.com/blog/details/21) Dan Collis-Puro shows how to go even further and monitor the CPU and case temperature, and fan speeds, to alert administrators to hardware failures so they can be remedied before they become catastrophic.
