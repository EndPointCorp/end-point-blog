---
author: Jason Dixon
gh_issue_number: 406
tags: monitoring, performance, sysadmin
title: Monitoring with Purpose
---



If you work on Internet systems all day like we do, there’s a good chance you use some sort of monitoring software. Almost every business knows they need monitoring. If you’re a small company or organization, you probably started out with something free like [Nagios](https://www.nagios.org/). Or maybe you’re a really small company and prefer to outsource your alerts to a web service like [Pingdom](https://www.pingdom.com/). Either way, you understand that it’s important to know when your websites and mailservers are down. But do you monitor with ***purpose***?

All too often I encounter installations where the Systems Administrator has spent countless hours setting up their checks, making sure their thresholds and notifications work as designed, without really considering what their response might be in the face of disaster (or an inconvenient page at 3am). Operations folk have been trained to make sure their systems are pingable, their CPU temperature is running cool and the system load is at a reasonable level. But what do you do when that alert comes in because the website load is running at 10 for the last 15 minutes? Is that bad? How can you be certain?

The art of monitoring isn’t simply reactive in nature. A good SysAdmin will understand that real monitoring takes an active presence. Talk to your DBAs, software engineers and architects. Learn how the various components of your system(s) interact and relate, both in good times and bad. Review your performance trends (graphs) to see how each metric evolves over time. Without understanding the functional scope of your systems, you can’t expect to set meaningful thresholds on them.

Last but not least, ***every alert ******should be******actionable***. Getting paged because your application server is down is useless unless you have the proper remediation path documented and tested. Know what actions are needed, who should perform them, and what parties to escalate to in case the remediation fails. Focusing your energies on purposeful monitoring results in fewer false alarms, faster recovery from failures and regression, and an acute understanding of your entire application stack.


