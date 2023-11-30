---
author: Mike Farmer
title: Git Workflows
github_issue_number: 628
tags:
- git
date: 2012-06-13
---

[David Christensen](/blog/authors/david-christensen/) is talking today about Git workflows.

<a href="https://www.flickr.com/photos/80083124@N08/7369039912/" title="IMG_0721.JPG by endpoint920, on Flickr"><img alt="IMG_0721.JPG" height="375" src="/blog/2012/06/git-workflows/image-0.jpeg" width="500"/></a>

There are different ways that you can work with Git. Git doesn’t dictate a certain workflow so you are free to implement one that works best for you. Understanding git and how it works will help you develop an effective workflow.

The Git object model provides Git’s flexibility and is as follows:

- trees, blobs
- commits
- named commits: tags, branches

Branch flexibility comes through combining of branches (merges, rebase).

Good commits are key to flexibility/tools and should encapsulate the smallest logical change and a good log message describing the commit. It’s important to provide the why in your commit message in addition to what was fixed so that it’s clear to future developers.

Branches contain all the magic of Git in that it’s just a pointer to a commit.

Topic branches are convention driven branches that are merged off the master branch. They usually deal with a single topic and can be rebased onto master to provide a clean history. They can also be thrown away later so they don’t clutter up the repository.

Integration branches are usually for different levels of the application integration, for example, staging and production. They can be used to resolved conflicts and other small issues with the code.

Git also makes it easy to get quick version control ‘git init; git add’ is all you need. Then you can use ‘git grep’, which is faster than ‘grep -R’ for searching. A helpful command for understanding Git workflows is ‘git help workflows’.
