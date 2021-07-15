---
author: Jon Jensen
title: Avoid 2:00 and 3:00 am cron jobs!
github_issue_number: 785
tags:
- devops
- linux
- sysadmin
date: 2013-04-08
---



A word to the wise: **Do not set any cron jobs for 2:00 am or 3:00 am on Sunday morning!** Or to be safe, on other mornings besides Sunday as well, since jobs originally set to run on some particular day may eventually be changed to run on another day, or every day.

Most of the time such cron jobs will run fine, but if they run every Sunday morning, then twice per year they will run at the exact time daylight savings time (aka summer time) kicks in or ends, sometimes with very strange results.

On Linux with vixie-cron we saw two cron jobs run something like once per second between 3:00 and 3:01 when the most recent daylight savings time began. Thus they ran about 60 times, stepping all over each other and making a noisy mess in email. No serious harm was done, but that’s only because they were not tasks capable of causing serious harm.

Feel free to wish for or agitate for or fund or write a better open source job scheduler that everyone will use, one that will ensure no overlapping runs, allow specifying time limits, etc. Better tools exist, but until one of them achieves cron’s level of ubiquity, we have to live with cron at least some places and sometimes.

Alternatively, where possible set the server timezone to UTC so that no daylight savings changes will happen at all.

Or most preferable: Governments of the world, stop the twice-yearly dance of daylight saving time altogether.

But in the meantime this particular problem can be entirely avoided by just not scheduling any cron jobs to run on Sunday morning at 2:00 or 3:00 server time.


