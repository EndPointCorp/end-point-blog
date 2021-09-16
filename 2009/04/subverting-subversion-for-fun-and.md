---
author: David Christensen
title: Subverting Subversion for Fun and Profit
github_issue_number: 127
tags:
- camps
- interchange
- git
date: 2009-04-07
---

One of our clients recently discovered a bug in a little-used but vital portion of the admin functionality of their site. (Stay with me here...) After traditional debugging techniques failed on the code in question, it was time to look to the VCS for identifying the regression.

We fortunately had the code for their site in version control, which is obviously a big win. Unfortunately (for me, at least), the repository was stored in Subversion, which means that my bag o’ tricks was significantly diminished compared to my favorite VCS, git. After attempting to use 'svn log/svn diff -c' to help identify the culprit based on what I *thought* the issue might be, I realized that svn was just not up to the task.

Enter git-svn. Using git svn clone file://path/to/repository/trunk, I was able to acquire a git-ized version of the application’s repository. For this client, we use [DevCamps](http://devcamps.org) exclusively, so the entire application stack is stored in the local directory and run locally, including apache instance and postgres cluster. These pieces are necessarily unversioned, and are ignored in the repository setup. I was able to stop all camp services in the old camp directory (svn-based), rsync over all unversioned files to the new git repository (excluding the .svn metadata), replace the svn-based camp with the new git-svn based one, and fire up the camp services again. Started up immediately and worked like a charm. I now had git installed and working in what had previously only been svn-capable before.

Now that I had a git installation, I was able to pull one of my favorite tools from my toolbox when fighting regressions: git-bisect. In my previous svn contortions, I had located a previous revision several hundred commits back which did not exhibit the regression, so I was able to start the bisect with the following command: git bisect start *bad* *good*. In this case, bad was master and good was the revision I had found previously. Using git svn find-rev r*number*, I found the SHA1 commit for the good ref as git saw it.

From this point, I was able to quickly identify the commit which introduced the regression. In reviewing the diff, there was nothing that I would have expected to cause the issue at hand; the code did not touch any of the affected area of the admin. But git had never lied to me before. I compared the code currently in master with that introduced in the implicated commit and saw that most of it was still in place. I began selectively commenting out pieces of the code the commit introduced, and was able to enable/disable the bug with increasingly fine granularity. Finally, I was able to identify the single line which when removed caused the issue to evaporate. This was a line in an innocuous template which had a simple variable interpolation (inside an HTML comment, nonetheless); however, this line (which was in a file which was included with every document, added in the implicated commit) revealed a bug in the parser of the app-server which was causing the symptoms in the unrelated admin area.

It’s certain that I would never have been able to find the source of this issue without git-bisect, as manual bisection with svn would have been too tedious to even consider. I am able to happily interact with the rest of the development team with git being my secret weapon; git svn dcommit enables me to push my commits upstream, and git svn fetch/git svn rebase enable me to pull in the upstream changes. I’ll never need to tell my subversive secret (except, you know, on the company blog), and my own happiness and productivity has increased. Profit!!11 all around.
