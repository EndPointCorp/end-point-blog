---
author: Josh Tolley
gh_issue_number: 419
tags: tips
title: What's the difference?
---



Not long ago a software vendor we work with delivered a patch for a bug we'd been having. I was curious to know the difference between the patch, a .tgz file, and the files it was replacing. I came up with this:

```bash
( \
  for i in `( \
      find new -type f | sed "s/new\///" ; \
      find old -type f | sed "s/old\///" ) | \
      sort | uniq`; do \
    md5sum old/$i new/$i 2>&1; \
  done \
) | uniq -u  -c -w 32
```

Assuming the original .tgz file was unpacked into a directory called "old", and the new one into "new", this tells me which files exist in one directory and not other, and which files exist in both in different forms. Here's an example using a few random files in two directories:

```nohighlight
josh@eddie:~/tmp/transient$ ls -l old new
new:
total 16
-rw-r--r-- 1 josh josh 15 2011-03-01 10:15 1
-rw-r--r-- 1 josh josh 12 2011-03-01 10:14 2
-rw-r--r-- 1 josh josh 13 2011-03-01 10:15 3
-rw-r--r-- 1 josh josh 12 2011-03-01 10:16 4

old:
total 16
-rw-r--r-- 1 josh josh 15 2011-03-01 10:15 1
-rw-r--r-- 1 josh josh  5 2011-03-01 10:06 2
-rw-r--r-- 1 josh josh 13 2011-03-01 10:15 3
-rw-r--r-- 1 josh josh 20 2011-03-01 10:18 5

josh@eddie:~/tmp/transient$ ( \
>   for i in `( \
>       find new -type f | sed "s/new\///" ; \
>       find old -type f | sed "s/old\///" ) | \
>       sort | uniq`; do \
>     md5sum old/$i new/$i 2>&1; \
>   done \
> ) | uniq -u  -c -w 32
      1 432c7f1e40696b4fd77f8fd242679973  old/2
      1 a533139557d6c009ff19ae85e18b1c61  new/2
      1 md5sum: old/4: No such file or directory
      1 6f84c6a88edb7c2a453f0f900348960a  new/4
      1 6f38ac81c6bad77838e38f03745e968b  old/5
      1 md5sum: new/5: No such file or directory
```

Note that this can run into problems when two files in one directory are identical, but that wasn't a likely issue in this case, so I didn't work to avoid that problem.


