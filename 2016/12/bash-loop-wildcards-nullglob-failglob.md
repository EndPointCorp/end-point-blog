---
author: Marco Matarazzo
title: 'Bash: loop over a list of (possibly non-existing) files using wildcards with
  nullglob (or failglob) option'
github_issue_number: 1275
tags:
- shell
- linux
date: 2016-12-12
---

Let’s say you’re working in **Bash**, and you want to loop over a list of files, using wildcards.

The basic code is:

```bash
#!/bin/bash
for f in /path/to/files/*; do
  echo "Found file: $f"
done
```

Easy as that. However, there could be a problem with this code: if the wildcard does not expand to actual files (i.e. there’s no file under /path/to/files/ directory), $f will expand to the path string itself, and the **for** loop will still be executed one time with $f containing “/path/to/files/*”.

How to prevent this from happening? **Nullglob** is what you’re looking for.

**Nullglob**, quoting [shopts man page](http://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html), “allows filename patterns which match no files to expand to a null string, rather than themselves”.

Using **shopt -s** you can enable BASH optional behaviors, like **Nullglob**. Here’s the final code:

```bash
#!/bin/bash
shopt -s nullglob
for f in /path/to/files/*; do
  echo "Found file: $f"
done
```

Another interesting option you may want to check for, supported by Bash since version 3, is **failglob**.

With **failglob** enabled, quoting again, “patterns which fail to match filenames during filename expansion result in an expansion error”. Depending on what you need, that could even be a better behavior.

Wondering why **nullglob** it’s not the default behavior? Check [this very good answer](http://unix.stackexchange.com/a/204944/55408) to the question.
