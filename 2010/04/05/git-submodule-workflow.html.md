---
author: Steph Skardal
gh_issue_number: 285
tags: git
title: 'Git Submodules: What is the Ideal Workflow?'
---

Last week, I asked some coworkers at End Point about the normal workflow for using git submodules. Brian responded and the discussion turned into an overview on git submodules. I reorganized the content to be presented in a FAQ format:

**How do you get started with git submodules?**

You should use git submodule add to add a new submodule. So for example you would issue the commands:

```nohighlight
git submodule add git://github.com/stephskardal/extension1.git extension
git submodule init
```

Then you would git add extension (the path of the submodule installation), git commit.

**What does the initial setup of a submodule look like?**

The super project repo stores a .gitmodules file. A sample:

```nohighlight
[submodule "extension1"]
        path = extension
        url = git://github.com/stephskardal/extension1.git
[submodule "extension2"]
        path = extension_two
        url = git://github.com/stephskardal/extension2.git
```

**When you have submodules in a project, do you have to separately clone them from the master project, or does the initial checkout take care of that recursively for you?**

Generally, you will issue the commands below when you clone a super project repository. These commands will “install” the submodule under the main repository.

```nohighlight
git submodule init
git submodule update
```

**How do you update a git submodule repository?**

Given an existing git project in the “project” directory, and a git submodule extension1 in the the extension directory:

First, a status check on the main project:

```nohighlight
~/project> git status
# On branch master
nothing to commit (working directory clean)
```

Next, a status check on the git submodule:

```nohighlight
~/project> cd extension/
~/project/extension> git status
# Not currently on any branch.
nothing to commit (working directory clean)
```

Next, an update of the extension:

```nohighlight
~/project/extension> git fetch
remote: Counting objects: 30, done.
remote: Compressing objects: 100% (18/18), done.
remote: Total 19 (delta 9), reused 0 (delta 0)
Unpacking objects: 100% (19/19), done.
From git://github.com/stephskardal/extension1
   0f0b76b..9cbb6bd  master     -> origin/master

~/project/extension> git checkout master
Previous HEAD position was 0f0b76b... Added before_filter to base controller.
Switched to branch "master"
Your branch is behind 'origin/master' by 5 commits, and can be fast-forwarded.

~/project/extension> git merge origin/master
Updating f95a2d5..9cbb6bd
Fast forward
 extension.rb                                    |   10 +
 README                                             |   36 +
 TODO                                               |   11 +-
...

~/project/extension> git status
# On branch master
nothing to commit (working directory clean)
```

Next, back to the main project:

```nohighlight
~/project/extension> cd ..
~/project> git status
# On branch master
# Changed but not updated:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       modified:   extension
#
no changes added to commit (use "git add" and/or "git commit -a")
</file></file>
```

Now, a commit to include the submodule repository change. Brian has made it a convention to manually include SUBMODULE UPDATE: extension_name in the commit message to inform other developers that a submodule update is required.

```nohighlight
~/project> git add extension
~/project> git commit
[master eba52d5] SUBMODULE UPDATE: extension
 1 files changed, 1 insertions(+), 1 deletions(-)
```

**What does git store internally to track the submodule? The HEAD position? That would seem to be the minimal information needed to tie the specific submodule-tracked version with the version used in the superproject.**

It stores a specific commit SHA1 so even if HEAD moves the super project’s “reference” doesn’t, which is why updating to the upstream version must be followed by a commit so that the super project is “pinned” to the same commit across repos. You’ll see in the example above that the submodule project was in a detached head state (not on a branch) so HEAD doesn’t really make sense.

It is critical that the super project repo store an exact position for the submodule otherwise you would not be able to associate your own code with a particular version of a submodule and ensure that a given submodule is at the same position across repos. For instance, if you updated to an upgraded version of a submodule and committed it not realizing that it broke your own code, you can check out a previous spot in the repository where the code worked with the submodule.

Hopefully, this discussion on git submodules begins to show how powerful git and submodules can be for making it easy for non-core developers to start sharing their code on an open source project.

Thanks to Brian Miller and [David Christensen](/team/david_christensen) for contributing the content for this post! I reference this article in my article on [Software Development with Spree](/blog/2010/03/31/spree-software-development)—​I’ve found it very useful to use git submodules to install several Spree extensions on recent projects. The Spree extension community has a few valuable extensions including that introduce features such as product reviews, faq, blog organization, static pages, and multi-domain setup.
