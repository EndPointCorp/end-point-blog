---
author: Jon Jensen
title: 64-bit Windows naming fun
github_issue_number: 67
tags:
- redhat
- windows
date: 2008-09-30
---



At OSNews.com the article [Windows x64 Watch List](http://www.osnews.com/story/20330/Windows_x64_Watch_List) describes some of the key differences between 64-bit and 32-bit Windows. It’s pretty interesting, and mostly pretty reasonable. But this one caught my eye:

> 
> 
> 
> 
> There are now separate system file sections for both 32-bit and 64-bit code
> 
> 
> 
> 
> 
> Windows x64’s architecture keeps all 32-bit system files in a directory named “C:\WINDOWS\SysWOW64”, and 64-bit system files are place in the the oddly-named “C:\WINDOWS\system32” directory. For most applications, this doesn’t matter, as Windows will re-direct all 32-bit files to use “SysWOW64” automatically to avoid conflicts.
> 
> 
> 
> 
> 
> However, anyone (like us system admins) who depend on VBScripts to accomplish tasks, may have to directly reference “SysWOW64” files if needed, since re-direction doesn’t apply as smoothly.
> 
> 
> 
> 

I’ve been using 64-bit Linux since 2005 and found there to be some learning curve there, with distributors taking different approaches to supporting 32-bit libraries and applications on a 64-bit operating system.

The [Debian Etch approach](https://www.debian-administration.org/articles/534) is to treat the 64-bit architecture as “normal”, for lack of a better word, with 64-bit libraries residing in /lib and /usr/lib as always. It’s recommended to run a 32-bit chroot with important libraries in [the ia32-libs package](https://web.archive.org/web/20090726073930/http://packages.debian.org/stable/ia32-libs) going into /emul/ia32-linux. [Ubuntu is similar](https://web.archive.org/web/20110813093451/https://help.ubuntu.com/community/32bit_and_64bit), but its ia32-libs puts its ia32-libs files into /usr/lib32.

The [Red Hat approach](https://web.archive.org/web/20080915055508/http://www.redhat.com/magazine/009jul05/features/multilib/) called “multilib” keeps 32-bit libraries in /lib and /usr/lib with new 64-bit libraries living in /lib64 and /usr/lib64. (I mentioned this a while back while discussing [building a custom Perl on 64-bit Red Hat OSes](/blog/2008/07/building-perl-on-64-bit/).)

Each way has its tradeoffs, and causes a bit of trouble. That’s just the cost of dealing with multiple architectures in a single running OS, where no such support was previously needed.

But the Windows way? Putting your 32-bit libraries in C:\WINDOWS\SysWOW64 and your 64-bit libraries in C:\WINDOWS\system32? It hurts to see the names be exactly backwards. That’s really tops for confusion.


