---
author: Jon Jensen
gh_issue_number: 85
tags: git, perl
title: Perl 5 now on Git
---

It's awesome to see that the Perl 5 source code repository has been migrated from Perforce to Git, and is now active at [http://perl5.git.perl.org/](http://perl5.git.perl.org/). Congratulations to all those who worked hard to migrate the entire version control history, all the way back to the beginning with Perl 1.0!

Skimming through the history turns up some fun things:

- The last Perforce commit appears to have been on 16 December 2008.
- Perl 5 is still under very active development! (It seems a lot of people are missing this simple fact, so I don't feel bad stating it.)
- Perl 5.8.0 was released on 18 July 2002, and 5.6.0 on 23 March 2000. Those both seem so recent ...
- Perl 5.000 was released on 17 October 1994.
- Perl 4.0.00 was released 21 March 1991, and the last Perl 4 release, 4.0.36, was released on 4 February 1993. For having an active lifespan of only 4 or so years till Perl 5 became popular, Perl 4 code sure kicked around on servers a lot longer than that.
- Perl 1.0 was announced by Larry Wall on 18 December 1987. He called Perl *a "replacement" for awk and sed*. That first release included 49 regression tests.
- Some of the patches are from people whose contact information is long gone, rendered in Git commits as e.g. Dan Faigin, Doug Landauer <unknown@longtimeago>.
- The modern Internet hadn't yet completely taken over, as evidenced by email addresses such as isis!aburt and arnold@emoryu2.arpa.
- The first Larry Wall entry with email address larry@wall.org was 28 June 1988, though he continued to use his jpl.nasa.gov after that sometimes too.
- There are some weird things in the commit notices. For example, it's hard to believe the snippet of Perl code in the following change notice wasn't somehow mangled in the conversion process:

```
commit d23b30860e3e4c1bd7e12ed5a35d1b90e7fa214c
Author: Larry Wall &lt;lwall@scalpel.netlabs.com&gt;
Date:   Wed Jan 11 11:01:09 1995 -0800

   duplicate DESTROY

   In order to fix the duplicate DESTROY bug, I need to remove [the
   modified] lines from sv_setsv.

   Basically, copying an object shouldn't produce another object without an
   explicit blessing.  I'm not sure if this will break anything.  If Ilya
   and anyone else so inclined would apply this patch and see if it breaks
   anything related to overloading (or anything else object-oriented), I'd
   be much obliged.

   By the way, here's a test script for the duplicate DESTROY.  You'll note
   that it prints DESTROYED twice, once for , and once for .  I don't
   think an object should be considered an object unless viewed through
   a reference.  When accessed directly it should behave as a builtin type.

   #!./perl

    = new main;
    = '';

   sub new {
       my ;
       local /tmp/ssh-vaEzm16429/agent.16429 = bless $a;
       local  = ;      # Bogusly makes  an object.
       /tmp/ssh-vaEzm16429/agent.16429;
   }

   sub DESTROY {
       print "DESTROYED\n";
   }

   Larry

sv.c |    4 ----
1 files changed, 0 insertions(+), 4 deletions(-)
```

Yes, it really is that weird. [Check it out for yourself](http://perl5.git.perl.org/perl.git/commit/d23b30860e3e4c1bd7e12ed5a35d1b90e7fa214c).

The [Easy Git](http://www.gnome.org/~newren/eg/) summary information from eg info has some interesting trivia:

```
Total commits: 36647
Number of contributors: 926
Number of files: 4439
Number of directories: 657
Biggest file size, in bytes: 4176496 (Changes5.8)
Commits: 31178
```

And there's a nice new POD document instructing how work with the Perl repository using Git: [perlrepository](http://perl5.git.perl.org/perl.git/blob/HEAD:/pod/perlrepository.pod).

In other news, maintenance release [Perl 5.8.9 is out](http://use.perl.org/articles/08/12/16/1129216.shtml), expected to be the last 5.8.x release. The [change log](http://search.cpan.org/~nwclark/perl-5.8.9/pod/perl589delta.pod) shows most bundled modules have been updated.

Finally, [use Perl also notes](http://use.perl.org/articles/08/12/15/1334253.shtml) that Booking.com is donating $50,000 to further Perl development, specifically Perl 5.10 development and maintenance. They're also hosting the new Git master repository. Thanks!
