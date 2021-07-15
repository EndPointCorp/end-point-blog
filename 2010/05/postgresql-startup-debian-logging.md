---
author: David Christensen
title: PostgreSQL startup Debian logging failure
github_issue_number: 299
tags:
- postgres
date: 2010-05-05
---



I ran into issues with debugging why a fresh PostgreSQL replica wasn’t starting on Debian. This was with a highly-customized postgresql.conf file with custom logging location, data_directory, etc. set.

The system log files were not showing any information about the failed pg_ctlcluster output, nor was there any information in /var/log/postgresql/ or the defined log_directory.

I was able to successfully create a new cluster with pg_createcluster and see logs for the new cluster in /var/log/postgresql/. The utility pg_lsclusters showed both clusters in the listing, but the initial cluster was still down, showing up with a custom log location. After reviewing the Debian wrapper scripts (fortunately written in Perl) I disabled log_filename, log_directory, and logging_collector, leaving log_destination = stderr. I was then finally able to get log information spit out to the terminal.

In this case, it was due to a fresh Amazon EC2 instance lacking appropriate sysctl.conf settings for kernel.shmmax and kernel.shmall. This particular error occurred before the logging was fully set up, which is why we did not get logging information in the postgresql.conf-designated location.

Once I had the log information, it was a short matter to correct the issue. It just goes to show that often finding the problem is 90% of the work. Hopefully this comes in handy to someone else.


