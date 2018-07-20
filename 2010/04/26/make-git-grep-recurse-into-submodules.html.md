---
author: David Christensen
gh_issue_number: 294
tags: git
title: Make git grep recurse into submodules
---

If you’ve done any major work with projects that use submodules, you may have been surprised that `git grep` will fail to return matches that match in a submodule itself. If you go into the specific submodule directory and run the same `git grep` command, you will be able to see the results, so what to do in that case?

Fortunately, `git submodule` has a subcommand which lets us execute arbitrary commands in all submodule repos, intuitively named `git submodule foreach`.

My first attempt at a command to search in all submodules was:

```bash
$ git submodule foreach git grep {pattern}
```

This worked fine, except when {pattern} was multiple words or otherwise needed shell escaping. My next attempt was:

```bash
$ git submodule foreach git grep "{pattern}"
```

This properly passed the escapes to the shell (ending up with “'multi word phrase'” in my case), however an additional problem surfaced; the return value of the command resulted in an abort of the foreach loop. This was solved via:

```bash
$ git submodule foreach "git grep {pattern}; true"
```

A more refined version could be created as a git alias, automatically escape its arguments, and union with the results of `git grep`, thus providing the submodule-aware `git grep` I’d been hoping existed already. I leave this as an exercise to the reader... :-)

It’s also worth noting that the file paths reported are relative to the containing submodule, so you would need to incorporate the `git submodule foreach`-supplied $path variable to pinpoint the full paths of the files in question.
