---
author: Ethan Rowe
gh_issue_number: 130
tags: git
title: That Feeling of Liberation? It's Git.
---

In the last few weeks, a few of us have been working on a [project for Puppet](http://groups.google.com/group/puppet-dev/browse_thread/thread/12875331120b13c0/811da1ae485628e4) involving several lines of concurrent development.  We've relied extensively on the distributed nature of Git and the low cost of branching to facilitate this work.  Throughout the process, I occasionally find myself pondering a few things:

- How do teams ever coordinate work effectively when their version control system lacks decent branching support?
- The ease with which commits can be sliced and diced and tossed about (merge, rebase, cherry-pick, and so on) is truly delightful
- It is not unreasonable to describe Git as "liberating" in this process: here is a tool with which the the logical layer (your commit histories) largely reflect reality, with which the engineer is unencumbered in his/her ability accomplish the task at hand, and from which the results' cleanliness or messiness is the product of the engineering team's cleanliness or messiness rather than a by-product of the tool's deficiencies

The current process, in accordance with practices in use within the [Puppet project](http://reductivelabs.com/trac/puppet/wiki) itself, basically involves:

- One "canonical" branch in a particular repository, into which all work is merged by a single individual
- Engineers do work in their own branches/repositories, which they "publish" (in this case, on [Github](http://github.com)) through occasional pushes
- Different lines of development take place on different branches, keeping the logical threads of development separate until any given piece progresses sufficiently to warrant merging back into the canonical branch

Seemingly-speculative development efforts are worth more in this approach, because the most seemingly-speculative work can go out on an independent branch, starting from the common history, to be used later (or not) according to need.  The ease of sharing the work, of keeping it cleanly isolated but generally low-cost to integrate later, all reduce the "speculative" part of speculation.

Much of the public discussion of distributed development in practice, using Git, revolves around Linux kernel development.  That's of course a massive project with many contributors and a great many lines of development.  It's easy to look at distributed version control and the related development practices and say "this is not necessary; my project isn't that complex and doesn't need all this fanciness."  Such a conclusion, while understandable, ignores the most important factor in all software development work: human beings do the work.

Human beings can mentally envision complex structures, relationships, processes with instantaneous ease.  While our thought processes on a given thread may move along serially, our general approach to problems often involves a graph or web rather than a single line.  Furthermore, concurrent processing is second-nature to all of us, depending on the situation:

- The car driver guides the steering wheel such that over the course of traveling forty feet, the car smoothly achieves a ninety-degree change of direction, while coordinating the changing of gears and acceleration through manipulation of clutch, accelerator, and gear shift, all while chatting with the child in the back seat
- The singer performing a Bach aria manipulates diaphragm, jaw, tongue, lips, etc., to achieve the ideal resonance for the current vowel across a intricate repeated sequence of pitch relationships, while focusing on the sound of the organ for tuning and ensemble, and while envisioning the expansive overarching shape of the phrase to ensure the large-scale dynamic fits the musical expression needed
- The child in the outfield hums quietly, thinking about the cartoons he watched yesterday, while intently watching to see if the tee-ball will ever be coming his way

In my experience, when speaking about development tasks with my peers, the most common situation is for the conversation to be muddied by an excess of ideas and possibilities.  Too many topics and ways forward bubble about in our collective head, and development forces us to shed these until we arrive at the stripped-bare essentials.  Furthermore, it is similarly common that certain questions cannot be answered in the abstract, and require the rolling-up of sleeves to arrive at a solution.  Along the way to that solution, how often does one come upon implementation choices that were not previously considered, the implications of which requiring further assessment?

We often think, individually or collectively, in webs of relationships.  A tool that requires us to develop serially defies our basic humanity.  This is the true liberation Git brings: concurrent development -- by a team of many, a few, or one -- can be sanely achieved.  Put the new thing in a branch and move on.  Merging it later will very possibly be easy, but even if it's not, it is always possible.

To quote a special fella, "[freedom's untidy](http://www.cnn.com/2003/US/04/11/sprj.irq.pentagon/)".  Development tools that facilitate multiple lines of concurrent development mean that one ends up in the situation of dealing with, well, multiple lines of development.  The technical problem (no branching!) becomes a meatspace problem (aagh!  branches!).  There's no magical elixir for that problem, as it requires social solutions, such as email or a wiki.  The meatspace problems exist in any case, Git simply forces you to recognize them and plan for them.
