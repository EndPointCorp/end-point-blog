---
author: Jon Jensen
title: Efficiency of find -exec vs. find | xargs
github_issue_number: 332
tags:
- hosting
- optimization
date: 2010-07-28
---

This is a quick tip for anyone writing a cron job to purge large numbers of old files.

Without xargs, this is a pretty common way to do such a purge, in this case of all files older than 31 days:

```bash
find /path/to/junk/files -type f -mtime +31 -exec rm -f {} \;
```

But that executes rm once for every single file to be removed, which adds a ton of overhead just to fork and exec rm so many times. Even on modern operating systems that are so efficient with fork, it can easily increase the I/O and load and runtime by 10 times or more than just running a single rm command with a lot of file arguments.

Instead do this:

```bash
find /path/to/junk/files -type f -mtime +31 -print0 | xargs -0 -r rm -f
```

That will run xargs once for each very long list of files to be removed, so the overhead of fork & exec is incurred very rarely, and the job can spend most of its effort actually unlinking files. (The xargs -r option says not to run the command if there is no input to xargs.)

How long can the argument list to xargs be? It depends on the system, but xargs --show-limits will tell us. Here's output from a RHEL 5 x86_64 system (using findutils 4.2.27):

```plain
% xargs --show-limits
Your environment variables take up 2293 bytes
POSIX lower and upper limits on argument length: 2048, 129024
Maximum length of command we could actually use: 126731
Size of command buffer we are actually using: 126731
```

The numbers are similar on Debian Etch and Lenny.

And here's output from an Ubuntu 10.04 x86_64 system (using findutils 4.4.2):

```plain
% xargs --show-limits
Your environment variables take up 1370 bytes
POSIX upper limit on argument length (this system): 2093734
POSIX smallest allowable upper limit on argument length (all systems): 4096
Maximum length of command we could actually use: 2092364
Size of command buffer we are actually using: 131072
```

Roughly 2 megabytes of arguments is a lot. But even the POSIX minimum of 4 kB is a lot better than processing one file at a time.

It doesn't usually make much of a difference, but we can tune even more. Make sure the maximum number of files is processed at one time by first changing to the base directory so that the relative pathnames are shorter:

```bash
cd /path/to/junk/files && find . -type f -mtime +31 -print0 | xargs -0 -r rm -f
```

That way each file argument is shorter, e.g. ./junkfile compared to /path/to/junk/files/junkfile.

The above assumes you're using GNU findutils, which includes find -print0 and xargs -0 for processing ASCII NUL-delimited filenames for safety when filenames include embedded spaces, newlines, etc.
