---
author: Szymon Lipiński
title: Reverting Git Commits
github_issue_number: 605
tags:
- git
date: 2012-05-02
---

Git is great, but it’s not always easy to use. For example, reverting a commit is a very nice feature. There are git commands for reverting a commit which has not been pushed to the main repository. However after pushing it, things are not so easy.

While I was working for one of our clients, I made about 20 commits and then I pushed them to the main repository. After that I realised that I was working on a wrong branch.
The new branch I should have used wasn’t created yet. I had to revert all my commits, create the new branch, and load all my changes into it.

Creating the branch named NEW_BRANCH is as easy as:

```nohighlight
$ git branch NEW_BRANCH
```

Now the harder part... how to delete the commits pushed to the main repo. After reading through tons of documentation it turned out that it is not possible. You cannot just delete a pushed commit. However you can do something else.

As an example of this, I created a simple file, added a couple of lines there, and made four commits. The git log looks like this:

```nohighlight
$ git log
commit dc47a884f7b303fc8b207550104f5a1de192c91c
Author: Szymon Guz
Date:   Mon Apr 30 12:14:21 2012 +0200

    replaced b with d

commit 68f56d3321324bd14cd1e73d003b1e151c4d43b4
Author: Szymon Guz
Date:   Mon Apr 30 12:14:05 2012 +0200

    added c

commit a77427d8151f143cacb85f00eb6c8170079dc290
Author: Szymon Guz
Date:   Mon Apr 30 12:13:58 2012 +0200

    added b

commit 73e586bb6d401f4049cf977703f25bf47c93b227
Author: Szymon Guz
Date:   Mon Apr 30 12:13:49 2012 +0200

    added a

```

Now let’s move the last 3 commits to another branch. I will create one diff for reverting the changes and one for replaying them on the new branch.
Let’s call these the ‘down’ and ‘up’ diff files: ‘down’ for reverting, and ‘up’ for recreating the changes.

The up diff can be created with:

```nohighlight
$ git diff 73e586bb6d401f4049cf977703f25bf47c93b227 dc47a884f7b303fc8b207550104f5a1de192c91c
diff --git a/test b/test
index 7898192..3171744 100644
--- a/test
+++ b/test
@@ -1 +1,3 @@
 a
+d
+c
```

The down diff can be created using exactly the same command, but with switched parameters:

```nohighlight
$ git diff dc47a884f7b303fc8b207550104f5a1de192c91c 73e586bb6d401f4049cf977703f25bf47c93b227
diff --git a/test b/test
index 3171744..7898192 100644
--- a/test
+++ b/test
@@ -1,3 +1 @@
 a
-d
-c
```

I saved the diffs into files called ‘up.diff’ and ‘down.diff’.

On the old branch I want to revert the changes, after doing this I will just commit the changes and the branch will look like it was before all the commits. However all the commits stay in the branch. This something like a revert commit.

I reverted the changes on current branch with:

```nohighlight
$ patch -p1 < down.diff
patching file test
$ git commit -a -m "reverted the changes, moved to another branch"
```

Now let’s move the changes into the new branch.
I need to create the new branch from the repo after the first commit:

```nohighlight
$ git branch NEW_BRANCH 73e586bb6d401f4049cf977703f25bf47c93b227
```

Switch to the new branch:

```nohighlight
$ git checkout NEW_BRANCH
```

Apply the up.diff patch to the new branch:

```nohighlight
patch -p1 < up.diff
```

And commit the changes:

```nohighlight
$ git commit -a -m "Applied changes from the other branch"
```

I know that all the steps can be replaced with different ones, however this solution worked for me pretty well and without any problem.
