---
author: Jeff Boes
gh_issue_number: 1194
tags: shell
title: Breaking Bash
---

Recently I managed to break the bash shell in an interesting and puzzling way. The initial symptoms were very frustrating: a workflow process we use here (creating a development camp) failed for me, but for no one else. That was at least a clue that it was me, not the workflow process.

Eventually, I narrowed down the culprit to the "grep" command (and that was more through luck than steadfast Sherlock-like detective work).

```bash
$ grep foo bar

grep: foo: No such file or directory
```

Eh? grep is mis-parsing the arguments! How does *that* happen?

So I began to study my bash environment. Eventually I came up with this fascinating little typo:

```bash
export GREP_OPTIONS='—color=auto'
```

That's supposed to be:

```bash
export GREP_OPTIONS='--color=auto'
```

but it got recorded in my .bashrc as a em-dash, not a double-dash. (My guess is that I cut-and-pasted this from a web page where someone over-helpfully "typeset" this command.)

Ironically, this typo is innocuous under Bash 3.x, but when you slot it into a Bash 4.x installation, all heck busts loose.
