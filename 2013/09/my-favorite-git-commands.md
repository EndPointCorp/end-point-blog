---
author: Steph Skardal
title: My Favorite Git Commands
github_issue_number: 852
tags:
- git
date: 2013-09-16
---

Git is a tool that all of us End Pointers use frequently. I was recently reviewing history on a server that I work on frequently, and I took note of the various git commands I use. I put together a list of the top git commands (and/or techniques) that I use with a brief explanation.

**git commit -m "****"**

This is a no-brainer as it commits a set of changes to the repository. I always use the -m to set the git commit message instead of using an editor to do so. **Edit:** [Jon](/team/jon-jensen) recommends that new users not use *-m*, and that more advanced users use this sparingly, for good reasons described in the comments!

**git checkout -b branchname**

This is the first step to setting up a local branch. I use this one often as I set up local branches to separate changes for the various tasks I work on. This command creates and moves you to the new branch. Of course, if your branch already exists, *git checkout branchname* will check out the changes for that local branch that already exists.

**git push origin branchname**

After I’ve done a bit of work on my branch, I push it to the origin to a) back it up in another location (if applicable) and b) provide the ability for others to reference the branch.

**git rebase origin/master**

This one is very important to me, and our blog has featured a couple of articles about it ([#1](/blog/2010/10/git-branches-and-rebasing) and [#2](/blog/2009/05/git-rebase-just-workingness-baked-right)). A rebase rewinds your current changes (on your local branch), applies the changes from origin/master (or whatever branch you are rebasing against), and then reapplies your changes one by one. If there are any conflicts along the way, you are asked to resolve the conflicts, skip the commit, or abort the rebase. Using a rebase allows you to avoid those pesky merge commits which are not explicit in what changes they include and helps you keep a cleaner git history.

**git push -f origin branchname**

I use this one sparingly, and **only** if I’m the only one that’s working on branchname. This comes up when you’ve rebased one of your local branches resulting in an altered history of branchname. When you attempt to push it to origin, you may see a message that origin/branchname has X commits different from your local branch. This command will forcefully push your branch to origin and overwrite its history.

**git merge --squash branchname**

After you’ve done a bit of work on branchname and you are ready to merge it into the master branch, you can use the *--squash* argument to squash/smush/combine all of your commits into one clump of changes. This command **does not** perform the commit itself, therefore it must be followed by a) review of the changes and b) git commit.

**git branch -D branchname**

If you are done with all of your work on branchname and it has been merged into master, you can delete it with this command! **Edit:** Phunk tells me that there is a difference between *-D* and *-d*, as with the latter option, git will refuse to delete a branch with unmerged changes, so *-d* is a safer option.

**git push origin :branchname**

Want to delete branchname from the origin? Run this command. You can leave branchname on the origin repository if you want, but I like to keep things clean with this command.

**git checkout -t origin/someone_elses_branch**

Use this command to set up a local branch to track another developers branch. As the acting technical project manager for one of my clients, I use this command to track [Kamil’s](/blog/authors/kamil-ciemniewski) branch, in combination with the next command (cherry-pick), to get his work cleanly merged into master.

**git cherry-pick hashhashhash**

Git cherry-pick applies changes from a single commit (identified by hash) to your current working branch. As noted above, I typically use this after I’ve set up a local tracking branch from another developer to cherry-pick his or her commits onto the master branch in preparation for a deploy.

**git stash, git stash apply**

I only learned about *git stash* in the last year, however, it’s become a go-to tool of mine. If I have some working changes that I don’t want to commit, but a client asks me to commit another quick change, I will often stash the current changes (save them but not commit them), run a rebase to get my branch up to date, then push out the commit, then run *git stash apply* to restore my uncommitted changes.

Admittedly, several of my coworkers are Git experts and have many more Git tools in their toolboxes—​I should ask one of them to follow-up on this article with additional advanced git commands I should be using! Also take note that for us End Pointers, [DevCamps](http://www.devcamps.org/) may influence our Git toolbox because it allows us to have multiple instances (and copies of the production database) running at a time, which may require less management of Git branches.
