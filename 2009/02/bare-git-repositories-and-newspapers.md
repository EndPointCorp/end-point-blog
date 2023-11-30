---
author: Steven Jenkins
title: Bare Git repositories and newspapers
github_issue_number: 104
tags:
- git
date: 2009-02-19
---

During a recent discussion about Git, I realized yet again that previous knowledge of a version control system (VCS) actively hinders understanding of Git. This is especially challenging when trying to understand the difference between bare vs non-bare repositories.

An analogy might be helpful: Assume a modern newspaper, where the actual contents of the physical pages are stored in a database; i.e., the database might store contents of articles in one table, author information in another, page layout information in yet another table, and information on how an edition is built in yet another table, or perhaps in an external program. Any particular edition of the paper just happens to be a particular instantiation of items that live in the database.

Suppose an editor walks in and tells the staff “Create a special edition that consists of the front pages of the past week’s papers.” That edition could easily be created by taking all the front page articles from the past week from the database. No new content would be needed in the content tables themselves, just some metadata changes to label the new edition and description of how to build it.

One could consider the database, then, to be the actual newspaper.

Let’s apply that analogy to Git:

A Git repository is the newspaper database. A particular Git branch is the equivalent of a particular day’s paper: e.g., the edition for February 5, 2009 consisting of a set of articles, glued together by a layout specification, tied to a label ‘February 5, 2009’. In Git terms, that would be blobs of data, glued together by references, perhaps labeled by either a branch or a tag.

A bare Git repository, then, is the newspaper database itself, not a huge stack of all the editions ever printed. That’s a large contrast to some other VCSs where a repository is the first edition ever printed, with diffs stored on top of that. Running `git clone` is equivalent to a database copy of all the tables of the database. Doing a `git checkout` of a branch is the equivalent of asking the newspaper factory to read in the metadata and content from the database and produce a physical paper instance of the newspaper.
