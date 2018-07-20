---
author: Greg Sabino Mullane
gh_issue_number: 258
tags: git, open-source, postgres
title: 'Postgres: Hello git, goodbye CVS'
---

It looks like 2010 *might* be the year that Postgres officially makes the jump to [git](https://git-scm.com/). Currently, the project uses [CVS](https://www.nongnu.org/cvs/), with a script that moves things to the now canonical Postgres git repo at [git.postgresql.org](https://git.postgresql.org/gitweb/). This script has been causing problems, and is still continuing to do so, as CVS is not atomic. Once the project flips over, CVS will still be available, but CVS will be the slave and git the master, to put things in database terms. The conversion from git to CVS is trivial compared to the other way around, so there is no reason Postgres cannot continue to offer CVS access to the code for those unwilling or unable to use git.

On that note, I’m happy to see that the number of developers and committers who are using git—​and publicly stating their happiness with doing so—​has grown sharply in the last couple of years. Peter Eisentraut (with some help from myself) set up git.postgresql.org in 2008, but interest at that time was not terribly high, and there was still a lingering question of whether git was really the replacement for CVS, or if it would be some other version control system. There is little doubt now that git is going to win. Not only for the Postgres project, but across the development world in general (both open and closed source).

To drive the point home, Andrew has announced he is working on git integration with [the Postgres build farm](https://buildfarm.postgresql.org/). Of course, I submitted a patch to do just that back in March 2008, but I was ahead of my time :). Besides, mine was a simple proof of concept, while it sounds like Andrew is actually going to do it [the right way](https://web.archive.org/web/20100128034053/http://people.planetpostgresql.org/andrew/index.php?/archives/56-Back-to-the-buildfarm+git-future.html). Go Andrew!

Of all the projects I work on, the great majority are using git now. We’ve been using git at End Point as our preferred VCS for both internal projects and client work for a while now, and are very happy with our choice. There is only one other project I work on besides Postgres that uses CVS, but it’s a small project. I don’t know of any other project of Postgres’ size that is still using CVS (anyone know of any?). Even emacs [recently switched away from CVS](https://news.slashdot.org/story/09/12/28/0057231/GNU-Emacs-Switches-From-CVS-To-Bazaar), although they went with [bazaar](https://bazaar.canonical.com/en/) instead of git for some reason. Subversion is still being used by a substantial minority of the projects I’m involved with, mostly due to the historical fact that there was a window of time in which CVS was showing its limitations, but subversion was the only viable option. Sure would be nice if perl.org would offer git for Perl modules, as they do for subversion currently (/hint). Finally, there are a few of my projects that use something else (mercurial, monotone, etc.). Overall, git accounts for the lion’s share of all my projects, and I’m very happy about that. There is a very steep learning curve with git, but the effort is well worth it.

If you want to try out git with the Postgres project, first start by installing git. Unfortunately, git is still new enough, and actively developed enough, that it may not be available on your distro’s packaging system, or worse, the version available may be too old to be useful. Anything older than 1.5 should *not* be used, period, and 1.6 is highly preferred. I’d recommend taking the trouble to install from source if git is older than 1.6. Once installed, here’s the steps to clone the Postgres repo.

```bash
git clone git://git.postgresql.org/git/postgresql.git postgres
```

This step may take a while, as git is basically putting the entire Postgres project on your computer—​history and all! It took me three and a half minutes to run, but your time may vary.

Once that is done, you’ll have a directory named “postgres”. Change to it, and you can now poking around in the code, just like CVS, but without all the ugly CVS directories. :)

For more information, check out the [“Working with git”](https://wiki.postgresql.org/wiki/Working_with_Git) page on the Postgres wiki.

Here’s to 2010 being the year Postgres finally abandons CVS!
