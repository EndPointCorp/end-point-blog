---
author: Jeff Boes
gh_issue_number: 371
tags: git
title: Git branches and rebasing
---

Around here I have a reputation for finding the tiniest pothole on the path to Git happiness, and falling headlong into it while strapped to a bomb ...

But at least I’m dedicated to learning something each time. This time it involved branches, and how Git knows whether you have merged that branch into your current HEAD.

My initial workflow looked like this:

```bash
$ git checkout -b MY_BRANCH
  (some editing)
$ git commit
$ git push origin MY_BRANCH
  (later)
$ git checkout origin/master
$ git merge --no-commit origin/MY_BRANCH
  (some testing and inspection)
$ git commit
$ git rebase -i origin/master
```

This last step was the trip-and-fall, although it didn’t hurt me so much as launch me off my path into the weeds for a while. Once I did the “git rebase”, Git no longer knows that MY_BRANCH has been successfully merged into HEAD. So later, when I did this:

```bash
$ git branch -d MY_BRANCH
error: the branch 'MY_BRANCH' is not fully merged.
```

As I now understand it, the history is no longer a subset of the history associated with MY_BRANCH, so Git can’t tell the two are related and refuses to delete the branch unless you supply it with -D. A relatively harmless situation, but it set off all sorts of alarms for me, as I thought I messed up the merge somehow.
