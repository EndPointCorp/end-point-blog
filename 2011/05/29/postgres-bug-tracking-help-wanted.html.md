---
author: Greg Sabino Mullane
gh_issue_number: 460
tags: community, database, open-source, postgres
title: Postgres Bug Tracking - Help Wanted!
---



Once again there is talk in the Postgres community about adopting the use of a bug tracker. The latest [thread, on pgsql-hackers](http://postgresql.1045698.n5.nabble.com/How-can-I-check-the-treatment-of-bug-fixes-td4431752.html), was started by someone asking about the status of their patch. Or rather, asking an even better meta-question about how one finds out the status of a PostgreSQL bug report or patch. Sadly, the answer is that there is no standard way, other than sending emails until someone replies one way or another. The current process works something like this:

1. Someone finds a bug1. They send an email to pgsql-bugs@postgresql.org **OR** they use the web form, which grabs a sequential number and mails the report to pgsql-bugs@postgresql.org. Nothing else is done/stored, it just sends the email.1. Someone replies about the bug **OR** nobody replies about the bug.1. After a fix is found, which may involve some emails on other mailing lists, someone replies that the bug is fixed on the original thread. Maybe.

As you can see, there is some room for improvement there. Some of the most major and glaring holes in the current system:

- No way to search previous / existing bugs- No way to tell the status of a bug- No way to categorize and group bugs (per version, per platform, per component, per severity, etc.)- No way to know who is working on a bug- No way to prevent things from slipping through the cracks

Luckily, the above problems have been solved for many many years now but a wide variety of bug tracking software. There have traditionally been three problems to getting a bug tracker working for the Postgres
project:

### Inertia

The current system is, in a very literal sense, "good enough", so it's hard to impose the inevitable short-term pain of a new system when there always seem to be more pressing matters to attend to.

### Doesn't Make Julienne Fries

Everyone wants a different set of features, and getting all the hackers involved to agree on even a simple subset of desired features is pretty difficult. This is sort of similar to the crusade by myself and others to get git as the replacement version control system; there were some strong voices for competing systems (e.g. mercurial).

### Who Will Put the Bell on the Cat?

Everyone talks about the problem, and there have even been some attempts over the years to implement some sort of system, but the problem remains that setting up such a system, getting it smoothly integrated into the project's work flow, and then maintaining said system is a non-trivial task. Especially when you can't be assured of buy-in from some of the major players.

I'm hopeful that the recent thread indicates a slight shift of late in global acceptance of the need for a bug tracking system. The question is, which one, and who is going to take the time to write something? I'm really hoping
someone who has been lurking in the background will step up and help create something wonderful (okay, we can start with 'decent' :) Perhaps even someone with experience setting up bug tracking systems. Certainly Postgres must be one of the last major open source projects without a bug tracker; there is plenty of hard-won experience out there to be learned from. It would also be ideal if the person or persons was *not* a Postgres hacker of any sort, as taking the time to build and maintain this system would definitely take time away from their other hacking tasks. On the other hand, one could argue that a bug tracker is a vital piece of project infrastructure that is potentially as important as any other work that goes on. I certainly think so.


