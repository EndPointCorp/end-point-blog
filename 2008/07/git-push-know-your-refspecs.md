---
author: Ethan Rowe
title: 'Git push: know your refspecs'
github_issue_number: 33
tags:
- git
date: 2008-07-30
---

The ability to push and pull commits to/from remote repositories is obviously one of the great aspects of Git. However, if you’re not careful with how you use git-push, you may find yourself in an embarrassing situation.

When you have multiple remote tracking branches within a Git repository, any bare git push invocation will attempt to push to all of those remote branches out. If you have commits stacked up that you weren’t quite ready to push out, this can be somewhat unfortunate.

There are a variety of ways to accommodate this:

- use local branches for your commits, only merging those commits into your remote tracking branches when you’re ready to push them out;
- push remote tracking branches out whenever you have something worth committing.

However, even with sensible branch management practices, it’s worthwhile to know exactly what it is you’re pushing. Therefore, if you want to have a sense of what you’re potentially doing in calling a bare git push, always call it with the --dry-run option first. This will show you what a the push will send out, where the conflicts are, and so on, all without actually performing the push.

It is ultimately best, though, to understand the different ways of invoking git push so you can control things precisely and only change exactly what you want to change.

```
 git push some_repo some_branch
```

This will identify the ref named some_branch within your repository and push it out to the some_repo repository. If you are good about having your remote tracking branches use the same name as the source branch in the relevant remote ref, this is a simple, effective way of ensuring that you’re pushing out one branch and only one branch. However, it does require that you know the purpose of some_repo; it doesn’t do any magic for deciding what the “right” repository to push to is based on some_branch.

To be extremely precise, you can use a full refspec in your push call:

```
 git push some_repo local_branch:refs/heads/new_branch
```

This would take the local branch local_branch and push it out to within the remote ref identified by some_repo, but pushing it to the branch name new_branch within some_repo. This is a very useful invocation to understand in order to create new branches in bare repositories to be shared between developers/repositories. While both examples shown here will create the branch in some_repo if it does not already exist, the second example gives the programmer full control over the branch names.

If you’re sharing your work with multiple developers/repositories, it can become unwieldy if not impossible to keep your tracking branch names consistent with source branch names in your remote refs. In which case, knowing these invocations of git push is an absolute necessity.

Check out the documentation on git push for a full explanation, and for an example of how to delete a branch in a remote ref. There are considerably more options for the command than what is explained here, but the refspec documentation can be a bit confusing to newcomers, in which case hopefully this discussion provides a bit more clarity. (Then again, perhaps it doesn’t.)
