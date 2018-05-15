---
author: Jeff Boes
gh_issue_number: 892
tags: testing
title: Testing Your Imagination
---

The usual blog post follows a particular format:

“I learned something new, as part of a task that I succeeded at. Here’s what I did, here’s why it worked so well, thank you for reading.”

This one’s a little different. I made a mistake, it seemed like a pretty simple thing, and then it got me thinking about why I (and in general, we software types), fall into that mistake, and how hard it is to correct.

Here’s the background: I was working on a very small bit of code that was supposed to check a ZIP code and do one of two things. The test was, in Perl,

```perl
$zip =~ /^94|95/
```

***Screetch!***

Perhaps you have already spotted the bug. Don’t feel so smug just yet. The particulars here are vital to understanding my point, but the bug could have been something more complex, or even simpler, and I am willing to bet a cubic yard of [virtual cash](https://www.google.com/?q=bitcoin#q=bitcoin) that you have made equally embarrassing errors. I’m just more willing to talk about mine, that’s all.

Back to our tale. I wrote that mistaken bit of code (and worse, it’s not the first time I’ve made that mistake in code), and then I proceeded to test it.

- Set $zip to '12345', doesn't match, no false positive. Check!
- Set $zip to '94001', does match. Check!
- Sest $zip to '95001', does match. Check!

(If you got this far and still haven’t figured out the punch line: the regular expression matches “94” at the beginning of a string, which is good, but it matches “95” anywhere in the string, which is bad. So $zip containing “89501” would match, which is ... not good.)

It doesn’t matter if you tested this in an external script, or went through the motions of operating the larger system (an e-commerce checkout) with the appropriate values of $zip, or wrote a full [test-driven development](http://search.cpan.org/~rjbs/Test-Simple-1.001002/lib/Test/More.pm) exercise—​the problem isn’t the testing methodology, it’s the imagination of the person desiging the test. I “knew” (nope) what the regular expression was written to do, so I tested to make sure it did that.

The only ways to catch this particular bug would be (a) exhaustively testing all values from 00000–99999, or (b) *imagining* ways that the regular expression might be broken. And that’s the challenge here, pertaining to my title. How do you rig your imagination to construct test cases that are “outside the box”?

Darned good question. If my brain continues to write

```perl
$zip =~ /^94|95/
```

instead of

```perl
$zip =~ /^(?:94|95)/
```

then that same brain will continue to construct test cases that are “close but not quite”. And if your assumptions about your code can be flawed in a simple case, how much more so when you are dealing with 100 lines? 1,000? An [arbitrarily large](http://en.wikipedia.org/wiki/Mars_Climate_Orbiter#Cause_of_failure) system, or [one that had “special” challenges?](https://www.healthcare.gov/)

I don’t have an answer here, and I suspect no one does. Certainly it helps if you have a fellow engineer get involved and review your code (and your testing!), but not every project has a budget for that. Certainly it helps if your client gets involved, and can test with their (hopefully!) better understanding of business rules and conditions. (And when I say “test”, I mean both “actually operate the system” and “actively contribute to test cases” such as “have you tried 89501? Have you tried A1A 1A1?”)

I just know that we have to find a better way to construct test cases than relying on the imagination from the same brain that made the bug in the first place, before we start putting software in charge of important things like [this](http://en.wikipedia.org/wiki/Unmanned_combat_air_vehicle) or [this](http://www.fox.com/almost-human/) Thank you for raeding. Er, reading.
