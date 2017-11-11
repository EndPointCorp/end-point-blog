---
author: Greg Sabino Mullane
gh_issue_number: 1052
tags: git
title: Finding specific git commit at a point in time
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2014/11/10/finding-specific-git-commit-at-point-in/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/11/10/finding-specific-git-commit-at-point-in/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/fFXKMu">Some car</a> by <a href="https://www.flickr.com/photos/wwarby/">William Warby</a></small></div>

When using git, being able to track down a particular version of a file is an important debugging skill. The common use case for this is when someone is reporting a bug in your project, but they do not know the exact version they are using. While normal software versioning resolves this, bug reports often come in from people using the HEAD of a project, and thus the software version number does not help. Finding the exact set of files the user has is key to being able to duplicate the bug, understand it, and then fix it.

How you get to the correct set of files (which means finding the proper git commit) depends on what information you can tease out of the user. There are three classes of clues I have come across, each of which is solved a different way. You may be given clues about:

1. **Date**: The date they downloaded the files (e.g. last time they ran a **git pull**)
1. **File**: A specific file's size, checksum, or even contents.
1. **Error**: An error message that helps guide to the right version (especially by giving a line number)

### Finding a git commit by date

This is the easiest one to solve. If all you need is to see how the repository looked around a certain point in time, you can use git checkout with git-rev-parse to get it. I covered this in detail in [an earlier post](http://blog.endpoint.com/2014/05/git-checkout-at-specific-date.html), but the best answer is below. For all of these examples, I am using the public Bucardo repository at git clone git://bucardo.org/bucardo.git

```
$ DATE='Sep 3 2014'
$ git checkout `git rev-list -1 --before="$DATE" master`
Note: checking out '79ad22cfb7d1ea950f4ffa2860f63bd4d0f31692'.
<small>
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b new_branch_name

HEAD is now at 79ad22c... Need to update validate_sync with new columns</small>
```

Or if you prefer xargs over backticks:

```
$ DATE='Sep 3 2014'
$ git rev-list -1 --before="$DATE" master | xargs -Iz git checkout z
```

What about the case in which there were multiple important commits on the given day? If the user doesn't know the exact time, you will have to make some educated guesses. You might add the **-p** flag to git log to examine what changes were made and how likely they are to interact with the bug in question. If it is still not clear, you may just want to have the user mail you a copy or a checksum of one of the key files, and use the method below.

Once you have found the commit you want, it's a good idea to tag it right away. This applies to any of the three classes of clues in this article. I usually add a lightweight git tag immediately after doing the checkout. Then you can easily come back to this commit simply by using the name of the tag. Give it something memorable and easy, such as the bug number being reported. For example:

```
$ git checkout `git rev-list -1 --before="$DATE" master`
## Give a lightweight tag to the current commit
$ git tag bug_23142
## We need to get back to our main work now
$ git checkout master
## Later on, we want to revisit that bug
$ git checkout bug_23142
## Of course, you may also want to simply create a branch
```

### Finding a git commit by checksum, size, or exact file

Sometimes you can find the commit you need by looking for a specific version of an important file. One of the "main" files in the repository that changes often is your best bet for this. You can ask the user for the size, or just a checksum of the file, and then see which repository commits have a matching entry.

#### Finding a git commit when given a checksum

As an example, a user in the Bucardo project has encountered a problem when running HEAD, but all they know is that they checked it out of sometime in the last four months. They also run "md5sum Bucardo.pm" and report that the MD5 of the file Bucardo.pm is 
767571a828199b6720f6be7ac543036e. Here's the easiest way to find what version of the repository they are using:

```
$ SUM=767571a828199b6720f6be7ac543036e
$ git log --format=%H \
  | xargs -Iz sh -c \
    'echo -n "z "; git show z:Bucardo.pm | md5sum' \
  | grep -m1 $SUM \
  | cut -d " " -f 1 \
  | xargs -Iz git log z -1
xargs: sh: terminated by signal 13
commit b462c256e62e7438878d5dc62155f2504353be7f
Author: Greg Sabino Mullane <greg@endpoint.com>
Date:   Fri Feb 24 08:34:50 2012 -0500

    Fix typo regarding piddir</greg@endpoint.com>
```

I'm using variables in these examples both to make copy and paste easier, and because it's always a good idea to save away constant but hard-to-remember bits of information. The first part of the pipeline grabs a list of all commit IDs: **git log --format=%H**.

We then use xargs to feed list of commit ids one by one to a shell. The shell grabs a copy of the Bucardo.pm file as it existed at the time of that commit, and generates an MD5 checksum of it. We echo the commit on the line as well as we will need it later on. So we now generate the commit hash and the md5 of the Bucardo.pm file.

Next, we pipe this list to grep so we only match the MD5 we are looking for. We use -m1 to stop processing once the first match is found (this is important, as the extraction and checksumming of files is fairly expensive, so we want to short-circuit it as soon as possible). Once we have a match, we use the **cut** utility to extract just the commit ID, and pipe that back into **git log**. Voila! Now we know the very last time the file existed with that MD5, and can checkout the given commit. (The "terminated by signal 13" is normal and expected)

You may wonder if a sha1sum would be better, as git uses those internally. Sadly, the process remains the same, as the algorithm git uses to generate its internal SHA1 checksums is sha1("blob " . length(file) . "\0" . contents(file)), and you can't expect a random user to compute that and send it to you! :)

#### Finding a git commit when given a file size

Another piece of information the user can give you very easily is the size of a file. For example, they may tell you that their copy of Bucardo.pm weighs in at 167092 bytes. As this file changes often, it can be a unique-enough marker to help you determine when they checkout out the repository. Finding the matching size is a matter of walking backwards through each commit and checking the file size of every Bucardo.pm as it existed:

```
$ SIZE=167092
$ git rev-list --all \
  | while read commit
 do if git ls-tree -l -r $commit \
  | grep -q -w $SIZE
 then echo $commit
 break
 fi
 done
d91807d59a6326e48077311e96e4d5730f24304c
```

The git ls-tree command generates a list of all blobs (files) for a given commit. The -l option tells it to also print the file size, and the -r option asks it to recurse. So we use git rev-list to generate a list of all the commits (by default, these are output from newest to oldest). Then we pass each commit to the ls-tree command, and use grep to see if that number appears anywhere in the output. If it does, grep returns truth, making the if statement fire the echo, which shows is the commit. The break ensures we stop after the first match. We now have the (probable) commit that the user checked the file out of. As we are not matching by filename, it's probably a good idea to double-check by running git ls-tree -l -r on the given commit.

#### Finding a git commit when given a copy of the file itself

This is very similar to the size method above, except that we are given the file itself, not the size, so we need to generate some metadata about it. You could run a checksum or a filesize and use one of the recipes above, or you could do it the git way and find the SHA1 checksum that git uses for this file (aka a blob) by using 
[git hash-object](https://www.kernel.org/pub/software/scm/git/docs/git-hash-object.html). Once you find that, you can use git ls-tree as before, as the blob hash is listed next to the filename. Thus:

```
$ HASH=`git hash-object ./bucardo.clue`
$ echo $HASH
639b247aab027b79bda788182c8b6785ed319662
$ git rev-list --all \
  | while read commit
 do if git ls-tree -r $commit \
  | grep -F -q $HASH
 then echo $commit
 break
 fi
 done
cd1d776307204cb77a731aa1b15c3c43a275c70e
```

### Finding a git commit by error message

Sometimes the only clue you are given is an error message, or some other snippet that you can trace back to one or more commits. For example, someone once mailed the list to ask about this error that they received:

```
DBI connect('dbname=bucardo;host=localhost;port=5432',
  'bucardo',...) failed: fe_sendauth: no password supplied at 
  /usr/local/bin/bucardo line 8627.
```

A quick glance at line 8627 of the file "bucardo" in HEAD showed only a closing brace, so it must be an earlier version of the file. What was needed was to walk backwards in time and check that line for every commit until we find one that could have triggered the error. Here is one way to do that:

```
$ git log --format=%h \
  | xargs -n 1 -I sh -c \
  "echo -n {}; git show {}:bucardo | head -8627 | tail -1" \
  | less
## About 35 lines down:
379c9006     $dbh = DBI->connect($BDSN, 'bucardo'...
```

Therefore, we can do a "git checkout 379c9006" and see if we can solve the user's problem.

These are some of the techniques I use to hunt down specific commits in a git repository. Are there other clues you have run up against? Better recipes for hunting down commits? Let me know in the comments below.


