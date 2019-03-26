---
author: Jon Jensen
gh_issue_number: 355
tags: database, hosting, postgres, redhat
title: PostgreSQL 8.4 in RHEL/CentOS 5.5
---

The [announcement of end of support](https://www.postgresql.org/about/news/1214/) coming soon for PostgreSQL 7.4, 8.0, and 8.1 means that people who’ve put off upgrading their Postgres systems are running out of time before they’re in the danger zone where critical bugfixes won’t be available.

Given that PostgreSQL 7.4 was released in November 2003, that’s nearly 7 years of support, quite a long time for free community support of an open-source project.

Many of our systems run [Red Hat Enterprise Linux](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) 5, which shipped with PostgreSQL 8.1. All indications are that Red Hat will continue to support that version of Postgres as it does all parts of a given version of RHEL during its support lifetime. But of course it would be nice to get those systems upgraded to a newer version of Postgres to get the performance and feature benefits of newer versions.

For any developers or DBAs familiar with Postgres, upgrading to a new version with RPMs from the PGDG or other custom Yum repository is not a big deal, but occasionally we’ve had a client worry that using a packages other than the ones supplied by Red Hat is riskier.

For those holdouts still on PostgreSQL 8.1 because it’s the “norm” on RHEL 5, Red Hat gave us a gift in their RHEL 5.5 update. It now includes [separate PostgreSQL 8.4 packages](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/5.5_release_notes/ar01s08) that may optionally be used on RHEL 5 instead of PostgreSQL 8.1. (Both can’t be used on the same system at the same time.)

I know that getting these packages from Red Hat shouldn’t be necessary, but for those who feel jittery about using 3rd-party packages, it’s a good nudge to switch to Postgres 8.4 using Red Hat’s supported packages. Thanks to [Tom Lane](https://en.wikipedia.org/wiki/Tom_Lane_(computer_scientist)) at [Red Hat](https://www.redhat.com/en) for making this happen. Though I don’t know whose idea it was, Tom is the author of all the RPM commitlog messages, so thanks, Tom!

This brings up a few other rhetorical questions: Will RHEL 6 ship with PostgreSQL 9.0? Will RHEL 5.6 have backported PostgreSQL 9.0 in similar postgresql90 packages? It’d be great to see each new PostgreSQL release have supported packages in RHEL so that there’s even less reason to start a new project on an older version of Postgres. RHEL 5.5 with PostgreSQL 8.4 is a nice start in that direction.
