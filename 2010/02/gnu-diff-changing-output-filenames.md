---
author: David Christensen
title: 'GNU diff: changing the output filenames'
github_issue_number: 269
tags:
- tips
date: 2010-02-15
---



I was working on a script to monitor/compare remote versions of a file and compare against our local mirror; part of this work involved fetching the remote file to a temporary location and doing a diff -u against the local file to see if there were any changes. This worked fine, but the temporary filename was less-than descriptive.

The man page for diff was somewhat cryptic when it came to changing the displayed output filenames themselves, however based on some figuring-out, you can pass the -L (--label) flag to diff. You need to pass it twice; the first -L will replace the filename in the --- output line and the second -L replaces the file in the +++ line.

```bash
$ wget -qO /tmp/grocerylist
$ diff -u /path/to/local/grocerylist -L /path/to/local/grocerylist /tmp/grocerylist -L http://mirrorsite.com/grocerylist

--- /path/to/local/grocerylist
+++ http://mirrorsite.com/grocerylist
@@ -11,7 +11,7 @@
potatoes
bread
eggs
-    milk
+    soda
oranges
apples
celery
```

Obvious shortcomings in this approach are the fact that you need to specify a redundant -L line to the first file; in my case, this was all handled programatically, so I just substituted the same parameter in both places. Also, you lose the default output label which shows the current modification date/time for each. In my case, I didn’t care about when, just if there were differences and what they were.


