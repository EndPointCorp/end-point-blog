---
author: David Christensen
gh_issue_number: 304
tags: git
title: Continuing an interrupted git-svn clone
---

I’ve run into the issue before when using git-svn to clone a large svn repo; something interrupts the transfer, and you end up having to restart the git-svn clone process again. Attempting to git-svn clone from a partially transferred svn clone directory results in error messages from git-svn, and it’s not immediately clear what you need to do to pick the process back up from where you left off.

In the past I’ve just blown away the partially-transferred repo and started the clone over, but that’s a waste of time and server resources, not to mention *extremely* frustrating, particularly if you’re substantially into the clone process.

Fortunately, this is not necessary; just go into your partially retrieved git-svn repo and execute git-svn fetch. This continues fetching the svn revisions from where you left off. When the process completes, you will have empty directory with just the .git directory present. Looking at git status shows all of the project files deleted (oh noes!), however this is just misdirection. At this point, you just need to issue a git reset --hard to check out the files in the HEAD commit.

More illustratively:

```bash
$ git svn clone http://svn.example.com/project/trunk project
# download, download, download, break!
$ cd project; ls -a
.git
$ git svn fetch
# download, download, download, success!
$ ls -a
.git
$ git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       deleted:    foo.c
#       deleted:    foo.h
#
$ git reset --hard; ls -a1
.git
foo.c
foo.h
</file>
```
