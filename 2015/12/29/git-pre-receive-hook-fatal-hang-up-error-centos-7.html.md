---
author: Marco Matarazzo
gh_issue_number: 1185
tags: redhat, git
title: 'Git: pre-receive hook error on CentOS 7'
---

We recently had to move a git repository from an old CentOS 5 to a new CentOS 7 server.

On the old CentOS 5 we had a recent, custom compiled version of git while on the new server we are using the system default old 1.8 version, shipped by the official CentOS repositories. And, as usual when you tell yourself "What could possibly go wrong?", something did: every push began to return the dreaded "fatal: The remote end hung up unexpectedly" error.

After some time spent trying to debug the problem, we managed to isolate the problem to the pre-receive hook, specifically active on that repository. The script was very simple:

```bash
 #!/bin/bash
 read_only_users="alice bob"
 for user in $read_only_users
 do
     if [ $USER == $user ]; then
         echo "User $USER has read-only access, push blocked."
         exit 1
     fi
 done
```

... which apparently had no visible mistakes. On top of the lack of errors, this very same script used to work perfectly for years on the old server. Unfortunately, and quite disappointingly, even changing it to a simple:

```bash
 #!/bin/bash
 echo "These are not the droids you are looking for. Move along."
```

...did not help and the error still persisted.

Searching for clues around forums and wikis, we found [this](https://spuder.wordpress.com/2014/03/26/git-pre-receive-hooks/) blog post talking about parameters passed through stdin.

On [Git docs](https://git-scm.com/docs/githooks), we read that pre-receive hooks takes no arguments, but for each ref to be updated it receives on standard input a line of the format: **<old-value> SP <new-value> SP <ref-name> LF**.

At that point, we tried with a sample script that actually reads and does something with stdin:

```bash
 #!/bin/bash
 while read oldrev newrev refname
 do
   echo "OLDREV: $oldrev - NEWREV: $newrev - REFNAME: $refname"
 done
```

...and voilà: pushes started working again. Lesson learned: never ignore stdin.
