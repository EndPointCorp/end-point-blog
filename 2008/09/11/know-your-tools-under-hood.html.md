---
author: David Christensen
gh_issue_number: 60
tags: openafs, git
title: Know your tools under the hood
---

Git supports many workflows; one common model that we use here at End Point is having a shared central bare repository that all developers clone from.  When changes are made, the developer pushes the commit to the central repository, and other developers see the relevant changes on subsequent pulls.

We ran into an issue today where after a commit/push cycle, suddenly pulls from the shared repository were broken for downstream developers.  It turns out that one of the commits had been created by root and pushed to the shared repository.  This worked fine to push, as root had read-write privileges to the filesystem, however it meant that the loose objects which the commit created were in turn owned by root as well; fs permissions on the loose objects and the updated refs/heads/branch prevented the read of the appropriate files, and hence broke the pull behavior downstream.

Trying to debug this purely on the reported messages from the tool itself would have resulted in more downtime at a critical time in the client's release cycle.

There are a couple of morals here:

- Don't do anything as root that doesn't need root privileges. :-)
- Understanding how git works at a low level enabled a speedy detection of the (*ahem*) root cause of the problem and led to quick correction of the underlying permissions/ownership issues.
