---
author: Daniel Browning
gh_issue_number: 39
tags: development
title: The how and why of Code Reviews
---

Everyone believes that code reviews are highly beneficial to software and web site quality. Yet many of those who agree in principle don’t follow through with them in practice, at least not consistently or thoroughly. To find ways to improve real-world practice, I attended [Code Reviews for Fun and Profit](https://conferences.oreilly.com/oscon/oscon2008/public/schedule/detail/2538), given by Alex Martelli, Über Tech Lead at Google, during OSCON 2008.

One barrier to good reviews is when developers are reluctant to point out flaws in the code of more experienced programmers, perhaps due to culture or personal dynamics. In Open Source projects, and at End Point, the reverse is often true: corrections earn Nerd Cred. But if it is an issue, one good workaround is to ask questions. Instead of “If you use a value of zero, it crashes,” say “What happens if you use a value of zero?”

There are several prerequisites that should be taken care of before code reviews are started. First, a version control system is required (we prefer Git at End Point). Second, a minimal amount of process should be in place to ensure reviews occur, so that some commits do not fall through the cracks. Third, automatable tasks, such as style, test coverage, and smoke tests, should be completed by the computer.

When reviewing code, there are many things to check for. The code should be clear, readable, with consistent, well-named variables and functions. Re-use is important, because the most readable code is the kind that isn’t there: it’s in some other library that’s already tested, reviewed, and proven. Error logs and debug files have clear and consistent messages, exceptions are thrown and caught, returned error values are checked. Also look for memory leaks, security issues, race conditions, premature optimization, and portability issues.

Check for well-written tests, that high level integration tests cover corner cases as well as expected paths, that dependence injection is used correctly when needed. Documentation that is in sync with the source code, has consistent terms, and places ancillary information in external files/links. Terse code comments that explain why, not what, without repeating the code. The UI is clean.

To make code reviews easier and more likely to happen, ensure that they are small. Just 200–400 lines, comments included, depending on the language. Linus rejects large patches out of hand for this reason. Code reviewers should not spend more than 60–90 minutes at a time doing code review, once in the morning and once in the afternoon, because effectiveness drops off quickly. It is not like coding, which is the act of creation; you can spend many hours in that mode without ill effect.

Pair programming doesn’t reduce the need for code review. There is a propensity for good pairs to groupthink, so that they will not see problems that an outsider could. Furthermore, code review must still be done for others to have familiarity with the code.

If you have a mountain of legacy code that needs review, it may be best to start by just changing one small piece at a time, and reviewing that as you go.

The most important tool to assist with code review is e-mail. While one person should always have the responsibility of completing the review, the use of e-mail will allow all team members to become familiar with every part of the codebase, and it encourages them to perform additional review because it takes little time. There are a variety of other software tools:

- [Rietveld](https://github.com/rietveld-codereview/rietveld)
- [Review Board](https://www.reviewboard.org/)
- [Codestriker](http://codestriker.sourceforge.net/)
- [JCR](http://jcodereview.sourceforge.net/) (Java Code Reviewer, not just for Java)

Code reviews have a host of positive benefits: they find bugs, correct inadequate documentation, repair flawed tests, and ensure readable code. They connect team members to each other through code, each becoming better for it. Given enough eyeballs, all bugs are shallow.
