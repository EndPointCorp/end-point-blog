---
author: Jon Jensen
gh_issue_number: 1111
tags: git, open-source
title: Happy 10th birthday, Git!
---

Git’s birthday was yesterday. It is now 10 years old! Happy birthday, Git!

Git was born on 7 April 2005, as its creator [Linus Torvalds recounted in a 2007 mailing list post](http://marc.info/?l=git&m=117254154130732). At least if we consider the achievement of self-hosting to be “birth” for software like this. :)

Birthdays are really arbitrary moments in time, but they give us a reason to pause and reflect back. Why is Git a big deal?

Even if Git were still relatively obscure, for any serious software project to survive a decade and still be useful and maintained is an accomplishment. But Git is not just surviving.

Over the past 5–6 years, Git has become the standard version control system in the free software / open source world, and more recently, it is becoming the default version control system everywhere, including in the proprietary software world. It is amazing to consider how fast it has overtaken the older systems, and won out against competing newer systems too. It is not unreasonable these days to expect anyone who does software development, and especially anyone who claims to be familiar with version control systems, to be comfortable with Git.

So how did I get to be friends with Git, and end up at this birthday celebration?

After experimenting with Git and other distributed version control systems for a while in early and mid-2007, I started using Git for real work in July 2007. That is the earliest commit date in one my personal Git repositories (which was converted from an earlier CVS repository I started in 2000). Within a few weeks I was in love with Git. It was so obviously vastly superior to CVS and Subversion that I had mostly used before. It offered so much more power, control, and flexibility. The learning curve was real but tractable and it was so much easier to prevent or repair mistakes that I didn’t mind the retraining at all.

So I’m sounding like a fanboy. What was so much better?

First, the design. A distributed system where all commits were objects with a SHA-1 hash to identify them and the parent commit(s). Locally editable history. Piecemeal committing thanks to the staging power of the Git index. Cheap and quick branching. Better merging. A commit log that was really useful. Implicit rename tracking. Easy tagging and commit naming. And nothing missing from other systems that I needed.

Next, the implementation. Trivial setup, with no political and system administrative fuss for client or server. No messing with users and permissions and committer identities, just name &amp; email address like we’re all used to. An efficient wire protocol. Simple ssh transport for pushes and/or pulls of remote repositories, if needed. A single .git directory at the repository root, rather than RCS, CVS, or .svn directories scattered throughout the checkout. A simple .git/config configuration file. And speed, so much speed, even for very large repositories with lots of binary blobs.

The speed is worth talking about more.

The speed of Git mattered, and was more than just a bonus. It proved true once again the adage that a big enough quantitative difference becomes a qualitative difference. Some people believed that speed of operations wasn’t all that important, but once you are able to complete your version control tasks so quickly that they’re not at all bothersome, it changes the way you work.

The ease of setting up an in-place repository on a whim, without worrying about where or if a central repository would ever be made, let alone wasting any time with access control, is a huge benefit. I used to administer CVS and Subversion repositories and life is so much better with the diminished role a “Git repository administrator” plays now.

Cheap topic branches for little experiments are easy. Committing every little thing separately makes sense if I can later reorder or combine or split my commits, and craft a sane commit before pushing it out where anyone else sees it.

Git subsumed everything else for us.

RCS, despite its major limitations, stuck around because CVS and Subversion didn’t do the nice quick in-place versioning that RCS does. That kind of workflow is so useful for a system administrator or ad-hoc local development work. But RCS has an ugly implementation and is based on changing single files, not sets. It can’t be promoted to real distributed version control later if needed. At End Point we used to use CVS, Subversion, and SVK (a distributed system built on top of Subversion), and also RCS for those cases where it still proved useful. Git replaced them all.

Distributed is better. Even for those who mostly use Git working against a central repository.

The RCS use case was a special limited subset of the bigger topic of distributed version control, which many people resisted and thought was overkill, or out of control, or whatever. But it is essential, and was key to fixing a lot of the problems of CVS and Subversion. Getting over the mental block of Git not having a single sequential integer revision number for each commit as Subversion did was hard for some people, but it forces us to confront the new reality: Commits are their own objects with an independent identity in a distributed world.

When I started using Git, Mercurial and Bazaar were the strongest distributed version control competitors. They were roughly feature-equivalent, and were solid contenders. But they were never as fast or compact on disk, and didn’t have Git’s index, cheap branching, stashing, or so many other niceties.

Then there is the ecosystem.

GitHub arrived on the scene as an unnecessary appendage at first, but its ease of use and popularity, and social coding encouragement, quickly made it an essential part of the Git community. It turned the occasional propagandistic accusation that Git was antisocial and would encourage project forks, into a virtue, by calling everyone’s clone a “fork”.

Over time GitHub has played a major role in making Git as popular as it is. Bypassing the need to set up any server software at all to get a central Git repository going removed a hurdle for many people. GitHub is a centralized service that can go down, but that is no serious risk in a distributed system where you generally have full repository mirrors all over the place, and can switch to other hosting any time if needed.

I realize I’m gushing praise embarrassingly at this point. I find it is warranted, based on my nearly 8 years of using Git and with good familiarity with the alternatives, old and new.

Thanks, Linus, for Git. Thanks, Junio C Hamano, who has maintained the Git open source project since early on.

Presumably someday something better will come along. Until then let’s enjoy this rare period of calm where there is an obvious winner to a common technology question and thus no needless debate before work can begin. And the current tool stability means we don’t have to learn new version control skills every few years.

To commemorate this 10-year birthday, [Linux.com interviewed Linus](http://www.linux.com/news/featured-blogs/185-jennifer-cloer/821541-10-years-of-git-an-interview-with-git-creator-linus-torvalds) and it is a worthwhile read.

You may also be interested to read more in the [Wikipedia article on Git](https://en.wikipedia.org/wiki/Git_(software)) or the [Git wiki’s history of Git](https://git.wiki.kernel.org/index.php/GitHistory).

Finally, an author named Stephen has written an article called [The case for Git in 2015](http://www.netinstructions.com/the-case-for-git/), which revisits the question of which version control system to use as if it were not yet a settled question. It has many good reminders of why Git has earned its prominent position.
