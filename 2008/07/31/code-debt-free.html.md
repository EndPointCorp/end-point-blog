---
author: Ethan Rowe
gh_issue_number: 35
tags: perl, tips
title: Code Debt-Free
---



Every now and then, the opportunity arises to write debt-free code (meaning free of [technical debt](https://en.wikipedia.org/wiki/Technical_debt)). When such opportunities come, we must seize them.

I recently had the distinct pleasure of cranking out some Perl modules in the following order:

1. Write documentation for the forthcoming functionality

1. Implement unit tests for the aforementioned forthcoming functionality
1. Verify that the unit tests fail
1. Implement the awaited functionality
1. Verify (jumping back to step 4 as necessary) that the unit tests work.

Timelines, interruptions, and other pressures often get in the way of this short-term development cycle. The cycle can feel tedious; it makes the task of implementing even simple functions seem unpleasantly large and drawn out. When an implementation approach flashes into the engineer’s mind, leaping to step 4 (implementation) feels natural and immediately gratifying. The best-intentioned of us can fall into this out of habit, out of inertia, out of raw enthusiasm.

Documentation, though, demonstrates that you know what you’re trying to achieve. It is not a nicety, it is proof that you understand the problem at hand. Unit tests, as hard as they can sometimes be to implement, offer proof that you in fact achieved the documented aspirations. Both serve to illustrate intent, purpose. That intent, and the thinking that informed it, is arguably more important than the code itself. It is the code’s reason for being.

Many engineers at many companies in many circumstances have, do, and will sing praises to test-driven development, unit testing, and the Path to Software Engineering Enlightenment. Few of those engineers will actually do it. It is not natural for human beings to expend energy on a multi-step process when they believe—​falsely—​that a one-step process would achieve the same ends.

Here is what is necessary to ensure that we don’t let our weaker nature subvert our perfect plans:

- self-discipline

That is all.


