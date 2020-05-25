---
author: Mike Farmer
gh_issue_number: 655
tags: git
title: Moving a Commit to Another Branch in Git
---

Perhaps you’ve made the same mistake I have. You’re right in the middle of developing a feature when a request comes up to fix a different completely unrelated problem. So, you jump right in and fix the issue and then you realize you forgot to start a new git feature branch. Suddenly you realize that you need to merge just the fix you made, but don’t want to merge the commits from the previous feature your working on.

Git rocks at manipulating branches and I knew this, but I wasn’t sure how to just move one commit to the master branch. After some digging and a little trial and error, I finally figured it out. This may not be the simplest approach, but it worked for me and wanted to share. 

The branches I’ll be working with are master and feature. In the current scenario, the feature branch is 4 commits ahead of the master and the branch that I want to bring over is just the most recent. 

First things first, I need to ensure my master branch is up to date.

```
git checkout master
git pull origin master
```

Then I’ll checkout my feature branch and make sure it’s completely up to date with the master branch.

```
git checkout feature
git rebase origin/master
```

Next, I’ll create a temporary feature branch that I’ll use later on to bring over the commit that I want.

```
git checkout -b feature_tmp
```

I’ll do the same for master so that I can perform my merging and rebasing in isolation from the master branch.

```
git checkout master
git checkout -b master_tmp
```

Now I’m going to merge the two tmp branches so that I have a history that contains all of my commits. This will give me the history that I want, but will include the 3 commits I don’t want.

```
git merge feature_tmp
```

Here’s where the magic happens. I’m going to rebase this branch using interactive mode. I want to rebase everything back to the last commit on the master branch. For simplicity in the commands here, we’ll just use SHA-MASTER in place of the actual SHA1 hash.

```
git rebase -i SHA-MASTER
```

This loads the commits into my editor and from here I just delete the 3 commits that I didn’t want on my master branch. This will give me the history I want with the 4th commit coming right after the last commit on the master branch. After deleting the commits, I just save and quit my editor.

Next, I merge my tmp branch into the master branch.

```
git checkout master
git merge master_tmp
git log
```

Now in the log, I can see the history is in the correct order, just how I wanted it. To finish things up, I’ll just push my changes and then rebase my feature branch which will reorder my commits to match the master branch and place my feature commits as the last three commits in the log.

```
git push origin master
git checkout feature
git rebase origin/master
git log
```

The last thing to do is delete my tmp branches.

```
git branch -D tmp_master
git branch -D tmp_feature
```
