---
author: Jeff Boes
gh_issue_number: 720
tags: perl
title: Getting Started with the Perl Debugger
---

 

The [Perl debugger](http://search.cpan.org/dist/perl-5.10.0/pod/perldebug.pod) is not an easy system to leap into unprepared, especially if you learned to program in the "modern era", with [fancy, helpful GUIs](http://pwnwear.com/wp-content/uploads/2009/09/wowscrnshot071207223240gn2-1.jpg) and other such things. 

<img src="/blog/2012/11/07/getting-started-with-perl-debugger/image-0.jpeg" style="display: block; margin: auto; width: auto;"/> 

So, for those of us who are old school, and those who   aren't but wondering what the fuss is about, here's a very   gentle introduction to debugging Perl code interactively. 

First, an aside. You may think to yourself, "Hey, command-line   scripting is passé; nobody does that any more. All my code   runs within a website (maybe a modern MVC framework), so how can I   make use of a command-line debugger?" 

Well, that's where   [   test-driven development](http://en.wikipedia.org/wiki/Test-driven_development) and its related methodologies come   in. If you have developed using a Perl   [   test framework](http://search.cpan.org/~mschwern/Test-Simple-0.98/lib/Test/More.pm), you can use the approach outlined here. 

The debugger is invoked by using the "-d" switch on the command line. You control the execution of your code with the "n" command: 

 $ perl -d debug.pl  Loading DB routines from perl5db.pl version 1.33 Editor support available.  Enter h or `h h' for help, or `man perldebug' for more help.  main::(debug.pl:1): my $x = 1;   DB<1> n1 main::(debug.pl:2): $x = $x + 1;  

"n" steps you through the code from line to line. To step *into* a subroutine call, use "s", e.g., 

 $ perl -d debug.pl ... main::(debug.pl:1): my $x = fx(1);   DB<1> s1 main::fx(debug.pl:4):   return;  

You can switch back and forth between step-over ("n") and step-into ("s") mode; just issue the command you want to use. 

Next, let's talk about *breakpoints*. These are places in   the code where you'd like the execution to stop so you can look   around and take stock. 

You can issue a "temporary" breakpoint with the "c" command: 

 main::(debug.pl:1): ...   DB<1> c 231 main::(debug.pl:23): ...  

You can set a permanent breakpoint with the "b" command: 

 main::(debug.pl:1): ...   DB<1> b 231   DB<2> c2 main::(debug.pl:23): ...   DB<2> c2 main::(debug.pl:23): ...  

And note how the "c" command is used to mean "run until breakpoint (or exit)". 

If all you could do with the Perl debugger was step through your program, that would be enough.   (You could use "print" statements to see what was going on, but it would be awkward to go back   and forth between the debugger and your editor.) Of course, we can do more: 

 main::(debug.pl:23): $x = get_complex_data_structure($arg);   DB<1> x $x1 0  HASH(0x1e123c8)    'a' => 1    'b' => 2   DB<2> x [1, 2, { b => sin(0.5) } ]2 0  ARRAY(0x1e8e7c0)    0  1    1  2    2  HASH(0x19ff298)       'b' => 0.479425538604203  

You can even evaluate complex expressions on the fly! Or invoke your code directly: 

   DB<1> x get_complex_data_structure($arg)1 0  HASH(0x1e123c8)    'a' => 1    'b' => 2  

Or set a breakpoint within your code, then invoke it: 

   DB<1> b My::Pkg::_routine   DB<2> x get_complex_data_structure($arg)   My::Pkg::_routine(My/Pkg.pm:99): ...21  

I hope this brief introduction whetted your appetite for the debugger. It's a powerful system   for exploring unfamiliar code, verifying assumptions about data structures, or tracking down bugs.   There are many more debugger commands than I've outlined here, but this should get you started. 

  Happy debugging! 


