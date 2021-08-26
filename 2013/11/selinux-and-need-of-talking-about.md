---
author: Emanuele “Lele” Calò
title: SELinux and the need of talking about problems
github_issue_number: 873
tags:
- redhat
- selinux
date: 2013-11-05
---

It’s known common sense that when there’s a problem you should talk about it

Well sometimes it seems like **SELinux** doesn’t agree, so that it quietly blocks your software and silently fail.

In this case the issue with SELinux is that since it’s usually a very talkative type of software (through */var/log/audit/auditd.log* and sometimes */var/log/messages*), the poor busy system administrator would kinda take it for granted that when there will be a problem SELinux will shout it out as usual.

Unfortunately that’s not the case if the permission/property involved has the *dontaudit* setting applied.

So a quick solution is to **temporarily** set SELinux to “permissive” so to check that it is actually causing the problem; basically if your script works after setting SELinux to permissive and stops again when resetting to enforce, then you’re on the good path to find your solution.

The next step would be to temporarily disable dontaudit settings with

```
semodule -DB
```
And then start to manually collect all the failing rules related to your problem and crafting a new custom SELinux module with these.

After finishing creating your module, follow your usual SELinux pluggable module management workflow and set it to work.

Just remember to re-enable the dontaudit silencing feature with

```
semodule -B
```
before moving on with the rest of your work to avoid having too many messages in your usual log files.
