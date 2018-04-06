---
author: Jeff Boes
gh_issue_number: 760
tags: camps, git
title: Git as rsync
---



I had a quick-and-dirty problem to solve recently:

The clients had uploaded many assorted images to a development [camp](http://devcamps.org), but the .gitignore meant those updates were not picked up when we committed and pushed and rolled out to the live site. Normally, one would just rsync the files, but for various reasons this was not practical.

So my solution, which I think can get filed under “Stupid ‘git’ tricks (as opposed to Tricks of a Stupid Git)”:

(on the source repo)

```
$ git checkout -b images_update
$ git add -f path-to-missing-images
$ git commit -m 'Do not push me! I'm just a silly temporary commit'
```

(“add -f” forces the images into the index, overriding our gitignore settings)

(on the target repo)

```
$ git remote add images /path/to/source/repo
$ git fetch
$ git checkout -f images/images_update path-to-missing-images
$ git remote rm images
$ git reset HEAD path-to-missing-images
```

That last “git reset” is because the newly-restored images will be git-added by default, and we didn’t want them committed to the central repo.

So what did we do here? For those dumbfounded by the level of silly, we used git to record the state of all the files in a certain path; then we pulled them back out into another location without disturbing anything already there. But as a benefit, we do have a record of what happened, in case we need to reproduce it.


