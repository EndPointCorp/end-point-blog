---
author: Jeff Boes
title: YAPC::NA 2014, Day One
github_issue_number: 1002
tags:
- conference
- perl
date: 2014-06-23
---

YAPC (Yet Another Perl Conference) is an annual gathering of Perl developers (and non-developers) to talk about Perl: how to do it, how to get other people to do it, and how we will all be doing it next year (or decade, if all goes well). There are flavors of YAPC set in North America, Europe, etc.

I attended my first-ever starting in Orlando, FL today (which apparently makes me a VIP—​Very Important Perl-user, as the community stands on its head the idea that the old fogies are the important people—​it’s the new blood at the conference that gets them all excited).

In no particular order, here’s what I remember of my whirlwind tour of YAPC::NA, Day One.

We were welcomed by Chris Prather, and informed that the conference would be live-streamed on the “yapcna” YouTube channel. Those videos are already up [here](https://www.youtube.com/user/yapcna), so you can follow along or take a detour to the several talks I had to miss.

Dan Wright, treasurer for the Perl Foundation, gave an overview of that virtuous organization’s activities for the past year. Basically, they are the most visible philanthropic facet of the Perl community, giving grants to (among other things) support developers who are engaged in fundamental Perl support.

Mark Keating gave an energetic (almost frenetic) talk on the Life and Death of Perl: at various times in the last 10 years, Perl has been declared “dead”, mostly due to the use of various (flawed and/or skewed) statistics, such as the negative growth in Perl jobs. However, Perl is still being written, written about, and talked about in great volumes: the reports of its demise can be traced to the downturn in programming jobs in general.

Larry Wall (yes, that Larry Wall—​author of the One True Programming Language) spoke at length about Perl RFCs: not to discuss the hundreds of features requested for the language, but to highlight some general principles that emerged as these features were proposed, considered, modified, accepted or rejected. For instance, “YAGNI”: Ya Ain’t Gonna Need It. Sometimes a feature seems so intrinsically cool that you just want to embrace it, but as a language maintainer you realize that its innate usefulness just “ain’t gonna” crop up that often, so convoluting the syntax or semantics isn’t worth the risk.

Much of Larry’s talk dealt with the advent of Perl 6, which is coming soon and will shake up the language at least as much as Perl 5 did when Perl 4 was still what people used. Larry’s “sacred” goal: to keep Perl as Perl-like as possible. Quote:

> 
> “We’ve got a golden opportunity to turn Perl into whatever we like. Let’s not take it.”
> 

This was the first time I’d heard Larry speak. He touched briefly on his bout with cancer, and that he was now one year cancer-free—​which prompted a great, congratulatory outburst from the room.

From here, we jumped into the first round of lightning talks. I can’t do them justice, as they were here and gone almost before I could write down the title. One discussed a “universal” stemming library. [Stemming](https://en.wikipedia.org/wiki/Word_stem) is the process of linguistic analysis to find a root word (usually for search indexing: “hacker”, “hacked”, and “hacking” would all be indexed under “hack”. The library is an attempt to put almost two dozen languages under one umbrella so that code processing a natural language doesn’t care which language it is.

Another talk gave advice on how to write about Perl for a Perl programming audience. Some advice was humorous and tongue-in-cheek: design your article title using the tried and true formula of “$N things every Perl programmer should know!”, “$X ways to do $Y in Perl”. Other bits were more to the point: have an opinion, don’t just report the facts.

I was quite interested in a presentation about Perl on [NetBeans](https://netbeans.org/), which is a kind of universal IDE for programmers (more than just an editor, but a source code analyzer, a configuration manager, a code formatter, documentation support tool, and others). It was particularly interesting since it was developed by an “outsider”: not someone who had decades of Perl experience, but rather who had enough Perl background to know what to do, and sufficient *lack* of expertise to know what a beginner needed. I look forward to installing NetBeans to see what it can do. (I’ve not had much patience with IDEs in the past, but I’m willing to give this one a bit of my time.)

[DTrace](https://en.wikipedia.org/wiki/DTrace) was the subject of another short talk. This one focused on problem-solving (debugging), particularly applications for which a standard static approach wasn’t viable. For instance, a typical approach is to instrument an application with output statements, or to run it in a debugger (such as the capable Perl debugger). But if the problem is in a production system, or the bug-event is hard to predict or reproduce, DTrace can provide many more options. I wasn’t able to follow everything here, but I caught some things about detecting events in the system that you normally wouldn’t be able to instrument: e.g., when such-and-such a file is changed, log a stack trace. This feature allowed the presenter to track down a bug in the system that wasn’t even caused by the code: the file was being altered correctly by the system, but the system administration Puppet configuration was replacing the correct file with a “vanilla” version periodically!

The last of the talks I will report on here concerned a Perl module called [DBIx::Introspector](http://search.cpan.org/~frew/DBIx-Introspector-0.001000/lib/DBIx/Introspector.pm). This provides a means for investigating a database connection (or definition) to determine what type of database it is (e.g., Postgres vs. MySQL). This may sound trivial (why would you not know what your database is?), but in fact since database implementation details can be different in crucial ways (for instance, SQL syntax), any sort of generic database-agnostic module (ORM, utility, etc.) may need to have DB-specific code abstracted out. In an example close-to-home, our very own [DevCamp](http://www.devcamps.org/) tool has need of this sort of abstraction.

Day 2 promises to be just as action-packed. I’m live-tweeting this via @murwiz, and the hashtag [#yapcna](https://twitter.com/search?q=%23yapcna&src=tyah) is our unifying battle-cry.
