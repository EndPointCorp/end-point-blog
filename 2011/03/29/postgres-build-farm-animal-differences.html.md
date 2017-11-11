---
author: Greg Sabino Mullane
gh_issue_number: 435
tags: community, database, open-source, postgres, testing
title: Postgres Build Farm Animal Differences
---



I'm a big fan of the [Postgres Build Farm](http://wiki.postgresql.org/wiki/PostgreSQL_Buildfarm_Howto), a distributed network of computers that are constantly installling, building, and testing Postgres to detect any problems in the code. The build farm works best when there is a wide variety of operating systems and architectures testing. Thus, while I have a rather common x86_64 Linux box available for testing, I try to make it a little unique to get better test coverage.

One thing I've been working on is [clang](http://clang.llvm.org/) support (clang is an alternative to gcc). Unfortunately, the latest version of clang has a bug that prevents it from building Postgres on Linux boxes. I submitted a small patch to the Postgres source to fix this, but it was decided that we'll wait until clang fixes their bug. Supposedly they have in their svn head, but I've not been able to get that to compile successfully.

So I also just installed [gcc 4.6.0](http://gcc.gnu.org/gcc-4.6/changes.html), the latest and greatest. Installing it was not easy (nasty problems with the mfpr dependencies), but it's done now and working. It probably won't make any difference as far as the results, but at least my box is somewhat different from all the other x86_64 Linux boxes in the farm. :)

I've asked before on the list (with no response) about what sort of configuration changes could be made to expand the range of testing. The build farm itself provides a handful of things to choose from, and [most of the animals in the farm have most of them configured](http://buildfarm.postgresql.org/cgi-bin/show_status.pl) (I have everything except "pam" and "vpath" enabled). However, one thing I've thought about changing is NAMEDATALEN. It's basically a compile-time option that sets the maximum number of characters things like table names can have. It is set by default to 64, while the SQL spec wants it to be 128. The problem is that this causes some tests to fail, as they have a hard-coded assumption about the length. The real problem of course is that Postgres' 'make check' is a very crude test. I've got some ideas on how to fix that, but that's another post for another day. So, anyone have other ideas on how to make my particular build farm member, and others like it, more useful?


