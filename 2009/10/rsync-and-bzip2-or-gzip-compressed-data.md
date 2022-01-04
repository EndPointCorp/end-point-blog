---
author: Jon Jensen
title: rsync and bzip2 or gzip compressed data
github_issue_number: 205
tags:
- hosting
- git
- compression
date: 2009-10-06
---

A few days ago, I learned that gzip has a custom option --rsyncable on Debian (and thus also Ubuntu). This [old write-up](http://beeznest.wordpress.com/2005/02/03/rsyncable-gzip/) covers it well, or you can just `man gzip` on a Debian-based system and see the --rsyncable option note.

I hadn't heard of this before and think it's pretty neat. It resets the compression algorithm on block boundaries so that rsync won't view every block subsequent to a change as completely different.

Because bzip2 has such large block sizes, it forces rsync to resend even more data for each plaintext change than plain gzip does, as [noted here](http://blog.arithm.com/2008/09/06/rsync-and-bzip2compressed-data/).

Enter [pbzip2](http://compression.ca/pbzip2/). Based on how it works, I suspect that pbzip2 will be friendlier to rsync, because each thread's compressed chunk has to be independent of the others. (However, pbzip2 can only operate on real input files, not stdin streams, so you can't use it with e.g. tar cj directly.)

In the case of gzip --rsyncable and pbzip2, you trade a little lower compression efficency (< 1% or so worse) for reduced network usage by rsync. This is probably a good tradeoff in many cases.

But even more interesting for me, a couple of days ago Avery Pennarun posted an article about his experimental code to use the same principles to [more efficiently store deltas of large binaries in Git repositories](http://alumnit.ca/~apenwarr/log/?m=200910#04). It's painful to deal with large binaries in any version control system I've used, and most people simply say, "don't do that". It's too bad, because when you have everything else related to a project in version control, why not some large images or audio files too? It's much more convenient for storage, distribution, complete documentation, and backups.

Avery's experiment gives a bit of hope that someday we'll be able to store big file changes in Git much more efficiently. (Though it doesn't affect the size of the initial large object commits, which will still be bloated.)
