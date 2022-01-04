---
author: Josh Tolley
title: Using psql \o to append to a file
github_issue_number: 280
tags:
- postgres
date: 2010-03-22
---



I had a slow query I was working on recently, and wanted to capture the output of EXPLAIN ANALYZE to a file. This is easy, with psql’s \o command:

```plain
5432 josh@josh# \o explain-results
```

Once EXPLAIN ANALYZE had finished running, I wanted the psql output back in my psql console window. This, too, is easy, using the \o command without a filename:

```plain
5432 josh@josh# \o
```

But later, after adding an index or two and changing some settings, I wanted to run a new EXPLAIN ANALYZE, and I wanted its output appended to the explain-analyze file I built earlier. At least on my system, \o will normally overwrite the target file, which would mean I’d lose my original results. I realize it’s simple to, say, pipe output to a new file (“explain-analyze-2”), but I wasn’t interested. Instead, because \o can also accept a pipe character and a shell command to pipe its output to, I did this:

```plain
5432 josh@josh# \o | cat - >> explain-results
```

Life is good.

Update: A helpful commenter pointed out I hadn’t actually used the same files in the original post. Oops. Fixed.


