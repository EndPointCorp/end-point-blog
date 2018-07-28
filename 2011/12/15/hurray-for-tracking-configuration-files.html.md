---
author: Josh Williams
gh_issue_number: 527
tags: git, monitoring
title: Hurray for tracking configuration files in source control
---



In a number of places we’ve started tracking configuration files in git. It’s great for Postgres configs, Apache or nginx, DNS zone files, Nagios, all kinds of things. A few clients have private offsite repos we push to, like at GitHub, but for the most part they’re independent repos. It’s still great for keeping track of what was changed when, and by whom.

In one case we have a centralized Nagios instance that does little more than receive passive checks from a number of remote systems. I’d set the checks on the remote systems but not loaded that configuration in yet. However while getting the central system set up, muscle memory kicked in and I suddenly had a half-red console as it’s loading in stale data.

We don’t need a flood of false alerts over email, but I don’t want to completely revert the config and lose all those services...

```nohighlight
[root nagios]# git stash; service nagios restart; git stash apply
Saved working directory and index state WIP on master: 0e9113b Made up commit for blog
HEAD is now at 0e9113b Made up commit for blog
Running configuration check...done.
Stopping nagios: .done.
Starting nagios: done.
# On branch master
# (etc)
```

Green! A small victory, for sure, but it shows one more advantage of modern SCM’s.


