---
author: Jon Jensen
gh_issue_number: 226
tags: hosting, interchange, open-source
title: XZ compression
---



[XZ](https://en.wikipedia.org/wiki/Xz) is a new free compression file format that is starting to be more widely used. The LZMA2 compression method it uses first became popular in the [7-Zip](https://www.7-zip.org/) archive program, with an analogous Unix command-line version called *7z*.

We used XZ for the first time in the [Interchange project](http://www.icdevgroup.org/i/dev) in the [Interchange 5.7.3](http://www.icdevgroup.org/i/dev/news?mv_arg=00039) packages. Compared to gzip and bzip2, the file sizes were as follows:

```nohighlight
interchange-5.7.3.tar.gz   2.4M
interchange-5.7.3.tar.bz2  2.1M
interchange-5.7.3.tar.xz   1.7M
```

Getting that tighter compression comes at the cost of its runtime being about 4 times slower than bzip2, but a bonus is that it decompresses about 3 times faster than bzip2. The combination of significantly smaller file sizes and faster decompression made it a clear win for distributing software packages, leading to it being the format used for packages in [Fedora 12](https://docs.fedoraproject.org/release-notes/f12/en-US/html/).

It’s also easy to use on Ubuntu 9.10, via the standard *[xz-utils](https://tukaani.org/xz/)* package. When you install that with apt-get, aptitude, etc., you’ll get a scary warning about it replacing *lzma*, a core package, but this is safe to do because xz-utils provides compatible replacement binaries /usr/bin/lzma and friends (lzcat, lzless, etc.). There is also built-in support in [GNU tar](https://www.gnu.org/software/tar/) with the new --xz aka -J options.


