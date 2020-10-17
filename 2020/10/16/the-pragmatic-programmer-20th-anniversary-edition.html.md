---
author: "Jon Jensen"
title: "The Pragmatic Programmer book, 20th anniversary edition"
tags: books, programming, development
gh_issue_number: 1673
---

![Photo of the original and 20th anniversary editions of The Pragmatic Programmer book, atop lawn and fall leaves](/blog/2020/10/16/the-pragmatic-programmer-20th-anniversary-edition/20201016_130906-sm.jpg)

The Pragmatic Programmer is a now-classic book about software development, first published in 1999. It is old enough that it predates the famous [Agile Manifesto](https://agilemanifesto.org/) of 2001. The authors of the book, Andy and Dave, were two of the 14 authors of that manifesto.

For its 20th anniversary in 2019, Dave and Andy created a new edition. They updated things that had become dated, such as mentions of programming languages, tools, operating systems, websites, etc. That was, I imagine, the easy part. They went on to extensively revise the entire text and incorporate new lessons learned in the past two decades.

### A classic

This book is part of our company’s [“work philosophy canon”](https://www.endpoint.com/blog/2018/05/07/work-philosophy-canon) and that I ask every software developer at End Point to read, so for that reason and others I wanted to be familiar with the new edition and make sure it is still something I want to recommend so broadly.

The book is also required reading for university courses at Cornell ([CS 3110: Data Structures and Functional Programming](https://www.cs.cornell.edu/courses/cs3110/2020sp/reflections.html)) and the University of Washington ([CSE 331: Software Design and Implementation](https://courses.cs.washington.edu/courses/cse331/19au/quizzes.html)).

I first read this book 19 years ago and really enjoyed it. I found that it clearly expressed many useful concepts I had stumbled upon in my own programming experience. More importantly, it showed me other helpful tips and warned of pitfalls. Having that all collected in book form with concise, memorable chapter names and tips gave me and others a shared vocabulary to use in our work.

I also enjoyed reading the new 20th anniversary edition. It did not have the same personal impact, which is to be expected since I am at a very different point in my programming career, technical reading, and life experience. But I think the book has great or even increased power for new readers.

### Overview of changes

The authors estimate that around 75% of the text has changed, and that seems about right. A few areas that stood out to me were:

* The now widely-known adage “don’t repeat yourself” originally meant primarily not to duplicate knowledge, that each piece of data should appear in only one canonical location. Over time, “don’t repeat yourself” has been more often used to preach against copying and pasting code. While that is also a good general rule, it has been oversimplified and turned into a blanket prohibition. Dave & Andy mention cases where duplicating code is the right thing to do, because the problem space is not the same and factoring out all such code duplication will make later changes far more complicated and the code more difficult to change.

* Computer security was not nearly as big of a concern when they were writing the first edition in the late 1990s, and now that almost every computer is networked and attackers are motivated to reach every system from anywhere in the world, they gave the topic more attention.

* Concurrency gets much more discussion, as is sensible in a time where scaling up typically means using many more CPU cores and processors.

* Unit testing was far less common in the late ’90s, and there were few good test frameworks, so they recommended you write your own. Now there are many good test frameworks for every language, so they of course recommend you choose one of those and use it.

* Dave writes “A Confession” on page 223, telling us that writing tests for 30+ years made testing so much a part of the way he thinks and programs, that he now writes testable interfaces even when he doesn’t write tests. He isn’t saying that testing is no longer important, but rather that it’s not a religion, that it can and should be examined by experienced programmers, and it has important effects on the programmer aside from the tests themselves.

* The old edition had checklists scattered throughout, and collected in the pull-out card at the end. The new edition doesn’t have checklists anymore, except the Debugging Checklist on page 97. I think that’s ok. They weren’t something I ever referred back to.

### Tips

The old edition had 70 tips that appear throughout the chapters. The new edition has 100 tips. In both cases they are extracted and collected on a pull-out card at the end of the book. What changed?

#### Removed or heavily reworked tips

* Write Code That Writes Code
* Use Exceptions for Exceptional Problems
* Design Using Services
* Separate Views from Models
* Don’t Use Wizard Code You Don’t Understand
* Abstractions Live Longer than Details
* Costly Tools Don’t Produce Better Designs

#### Tips that changed slightly

* “Use a Single Editor Well” is now “Achieve Editor Fluency”
* “Don’t Panic When Debugging” is now simply “Don’t Panic”
* “Minimize Coupling Between Modules” is now “Decoupled Code Is Easier to Change”
* “Configure, Don’t Integrate” is now “Parameterize Your App Using External Configuration”
* “Don’t Gather Requirements—Dig for Them” is now “Requirements Are Learned in a Feedback Loop”
* “Organize Teams Around Functionality” is now “Organize Fully Functional Teams”
* “Gently Exceed Your Users’ Expectations” is now “Delight Users, Don’t Just Deliver Code”
* “Put Abstractions in Code, Details in Metadata” is now “Policy Is Metadata”
* “Always Design for Concurrency” is now “Random Failures Are Often Concurrency Issues”
* “Listen to Nagging Doubts—Start When You’re Ready” is now “Listen to Your Inner Lizard”
* “Don’t Be a Slave to Formal Methods” is now “Do What Works, Not What’s Fashionable”
* “Some Things Are Better Done than Described” transformed to “Agile Is Not a Noun; Agile Is How You Do Things”

#### New tips

* You Have Agency
* Good Design Is Easier to Change Than Bad Design
* Forgo Following Fads
* Failing Test Before Fixing Code
* Read the Damn Error Message
* Act Locally
* Take Small Steps—Always
* Avoid Fortune-Telling
* Tell, Don’t Ask
* Don’t Chain Method Calls
* Avoid Global Data
* If It’s Important Enough To Be Global, Wrap It in an API
* Programming Is About Code, But Programs Are About Data
* Don’t Hoard State; Pass It Around
* Don’t Pay Inheritance Tax
* Prefer Interfaces to Express Polymorphism
* Delegate to Services: Has-A Trumps Is-A
* Use Mixins to Share Functionality
* Shared State Is Incorrect State
* Use Actors For Concurrency Without Shared State
* Testing Is Not About Finding Bugs
* A Test Is the First User of Your Code
* Build End-To-End, Not Top-Down or Bottom Up
* Use Property-Based Tests to Validate Your Assumptions
* Keep It Simple and Minimize Attack Surfaces
* Apply Security Patches Quickly
* Name Well; Rename When Needed
* No One Knows Exactly What They Want
* Programmers Help People Understand What They Want
* Don’t Go into the Code Alone
* Maintain Small Stable Teams
* Schedule It to Make It Happen
* Deliver When Users Need It
* Use Version Control to Drive Builds, Tests, and Releases
* First, Do No Harm
* Don’t Enable Scumbags
* It’s Your Life. Share it. Celebrate it. Build it. **And have fun!**

The new edition’s PDF version does not include the pull-out card with tips that comes with the printed book. That’s too bad, because the tips were what I most often referred to in the old edition after I finished reading it. At least Andy and Dave have published on their website a list of the 100 updated tips. It would be even nicer to have a PDF of the book’s pull-out card as they did for the old edition.

### Upgrade?

As you can see, there are many new tips. The text has been updated. It is still of excellent quality. So should you get the new edition?

I mentioned earlier two university courses that use the book. In both courses the professors allowed students to use either the original 2000 version or the 2019 version. That seems like the right thing to do to me as well.

If you already have the old edition of the book, I don’t think it’s necessary to rush out and buy the new edition. The old one is still quite good and relevant, and you’ll be learning a bit of software development history by reading the older one.

If you do not yet have the book, or if you will be going over it with others who are new to it, it is probably best for you to get the new edition as well so you can be familiar with the new tips and the ways Dave & Andy describe things now.

### Summing up

I am glad that Dave and Andy updated their book. Their updates make sense and make the book more relevant to present-day readers.

Relatedly, it would be good to also see an update of the book *Practices of an Agile Developer* by Venkat Subramaniam and Andy. That is coming up on 15 years old itself. Perhaps some of its topics have been incorporated in the new edition of *The Pragmatic Programmer*, but as I review the table of contents, it looks like it is still mostly additive. I have cited its important maxim “Different Makes a Difference” so often that I thought it was from *The Pragmatic Programmer* instead!

I’ll close with this good observation and advice from Andy in their Changelog podcast interview:

> Was it Dijkstra who had the Turing Award lecture about the very humble programmer? That is a critical piece of early literature… And you talk about things that haven’t changed. This was 1972? … And he makes the very important point that complexity will overwhelm us if we don’t take a very humble, very measured approach. And it’s been 30–40 years and everyone—present company included—has ignored this wonderful advice.
>
> Humility is difficult in our environment, in our culture, and it is probably, of all the human factorsy things that you need to be a good developer, I would submit that being humble, realizing you don’t know all the answers, that you need to find out, that you need to experiment, get feedback, try it.
>
> This part of our headlong rush into the shiny new thing is this kind of faith that “Well, that’s gonna be better. I can do it better. I’m better than this/​that.” Yeah, maybe… But you should validate that. You should try it. You should go back and read these things. You should try these other experiments.

Thanks, Andy & Dave!

### Reference

#### All tips from each edition

* [Quick reference 70 tips (and checklists) from original edition](https://blog.codinghorror.com/a-pragmatic-quick-reference/)
* [Quick reference 100 tips from new edition](https://pragprog.com/tips/)

#### Interviews

* [Functional Geekery Episode 126 – Andy Hunt and Dave Thomas from July 2, 2019](https://www.functionalgeekery.com/episode-126-andy-hunt-and-dave-thomas/) by Steven Proctor
* [The Changelog – Episode #352: The Pragmatic Programmers with Andy Hunt & Dave Thomas](https://changelog.com/podcast/352) by Adam Stacoviak & Jerod Santo
* [CodeNewbie Podcast season 9 episode 8 from August 26, 2019: Why you should read the new edition of the Pragmatic Programmer with Andy Hunt, Dave Thomas](https://www.codenewbie.org/podcast/why-you-should-read-the-new-edition-of-the-pragmatic-programmer) by Saron Yitbarek (author of the new edition’s foreword)

#### Other comparisons of the two editions

* [Sections added, changed significantly, and removed](https://www.kevinhooke.com/2020/05/06/the-pragmatic-programmer-1st-edition-vs-20th-anniversary-edition-what-are-the-major-changes/) by Kevin Hooke
* [The Pragmatic Programmer Book 2nd Edition Differences by Miranda Limonczenko](https://booksoncode.com/articles/pragmatic-programmer-comparison) (very detailed, but covers only the first 3 chapters)

#### Book pages

* [The Pragmatic Programmer, 20th Anniversary Edition](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) book home page, errata, source code downloads, and links to buy
* [Practices of an Agile Developer](https://pragprog.com/titles/pad/practices-of-an-agile-developer/) book home page, samples, pull-out card, and [review by Ethan Rowe](/blog/2006/06/20/review-practices-of-agile-developer)
