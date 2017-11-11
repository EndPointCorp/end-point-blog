---
author: Jeff Boes
gh_issue_number: 684
tags: git
title: 'Git: Delete your files and keep them, too'
---

I was charged with cleaning up a particularly large, sprawling set of files comprising a git repository. One whole "wing" of that structure consisted of files that needed to stay around in production (they were various PDFs, PowerPoint presentations, and Windows EXEs that were only ever needed by the customer's partners, and downloaded from the live site – our [developer camps](http://www.devcamps.org/) never wanted to have local copies of these files, which amounted to over 280 MB (and since we have dozens of camps shadowing this repository, all on the same server, this will save a few GB at least).

I should point out that our preferred deployment is to have production, QA, and development all be working clones of a central repository. Yes, we even push from production, especially when clients are the ones making changes there. (Gasp!)

So: the aim here is to make the stuff vanish from all the other clones (when they are updated), but to preserve the stuff in one particular clone (production). Also, we want to ensure that no future updates in that "wing" are tracked.

```bash
# From the "production" clone:
 $ cd stuff
 $ git rm -r --cached .
 $ cd ..
 $ echo "stuff" >>.gitignore
 $ git commit ...
 $ git push ...
```

Now, everything that was in the "stuff" tree remains, for "production", but every other clone will remove these files when they update from the central repository:

```bash
$ git pull origin master
 ...
 delete mode 100644 stuff/aaa
 delete mode 100644 stuff/aab
 ...
```
