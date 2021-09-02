---
author: Steph Skardal
title: A Git and symlink mistake
github_issue_number: 928
tags:
- git
- linux
date: 2014-02-17
---

A couple of times, I’ve accidentally created an infinite symlink loop and lost files from that directory from a single Git commit. Here’s how it happened:

1. First, on the production app, images tied to products in a database were uploaded to the server. Let’s say I was working on a Rails app, so these images were uploaded to the RAILS_ROOT/public/system/ directory. I added “public/system/” to my .gitignore file, and all appeared to be good.
2. Next on a [camps instance](https://www.devcamps.org/), I created a symlink from CAMP_ROOT/public/system pointing to the production app public/system directory. This is common practice in End Point’s camps setup because we often don’t need the redundancy of uploaded files on our dev camp instance, and we don’t want the extra disk space used up for these types of files. The *make camp* script is designed to allow a user to toggle symlink functionality on and off for various directories during the make camp process.
3. Next, I accidentally committed and push the public/system symlink from my development instance.
4. Finally, I pulled the commit onto my production instance. The pull resulted in public/system symlinking to itself, and all of the files vanished (poof). Since they were Git-ignored in the first place, I couldn’t recover them from Git.

This is a pretty simple mistake to mitigate or avoid completely:

### Backups

Have backups! Have backups! Did I say have backups?! Our awesome hosting team here at End Point was able to recover the lost files from the nightly backups when this has happened.

### Gitignore Update

Second, .gitignore should be modified to ignore “public/system” which includes the symlink and the directory, instead of the directory only with “public/system/”. In the case of Rails, the Rails app will automatically create the “system” directory if it does not exist, so that directory does not need to be committed with a hidden file (e.g. .empty). But in other cases where the directory is not automatically created, it might make sense to include “public/some_folder”, “public/some_folder/*”, and “!public/some_folder/.empty” in your gitignore so that the symlink and directory contents (except for .empty) are ignored.

It seems silly that a thing such as a single character (a “/” in this case) can wreak havoc on websites for me more than once, but such is life in programming. Backups and attention to detail are important!
