---
author: David Christensen
gh_issue_number: 112
tags: git
title: 'Emacs Tip of the Day: ediff-revision'
---

I recently discovered a cool feature of emacs: M-x ediff-revision. This launches the excellent ediff-mode with the defined version control system’s concept of revision spelling. In my case, I was wanting to compare all changes between two git branches introduced several commits ago relative to each branches’ head.

M-x ediff-revision prompted for a filename (defaulting to the current buffer’s file) and two revision arguments, which in vc-git’s case ends up being anything recognized by git rev-parse. So I was able to provide the simple revisions master^ and otherbranch^{4} and have it Do What I Mean™.

I limited the diff hunks in question to those matching specific regexes (different for each buffer) and was able to quickly and easily verify that all of the needed changes had been made between each of the branches.

As usual, C-h f ediff-revision is a good jumping off point for finding more about this useful editor command, as is C-h f ediff-mode for finding more about ediff-mode in general.
