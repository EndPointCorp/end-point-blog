---
author: David Christensen
gh_issue_number: 113
tags: interchange
title: Interchange jobs caveat
---

I’d used [Interchange](http://www.icdevgroup.org/i/dev)’s jobs feature to handle sending out email expirations and re-invites for a client. However I found out the hard way that scratch variables persisted between individual sub-jobs in the job set. I’d tested each of the two sub-jobs in isolation and had had no issues.

This bit me because I’d assumed each job component was run in isolation and variables were initialized with sensible (aka empty) content. In my case it fortunately only affected the reporting of each piece of the job system, but definitely could have affected larger pieces of the system.

The lessons? 1) Always explicitly initialize your variables; you don’t know the ultimate context they’ll be run in. 2) Individual component testing is no substitute for testing a system as a whole; you can reveal bugs that would otherwise slip through.


