---
author: Greg Sabino Mullane
gh_issue_number: 99
tags: perl, postgres, git
title: Test::Database Postgres support
---

At our recent company meeting, we organized a 'hackathon' at which the company was split into small groups to work on specific projects. My group was Postgres-focused and we chose to add Postgres support to the new Perl module [Test::Database](http://search.cpan.org/dist/Test-Database/).

This turned out to be a decent sized task for the few hours we had to accomplish it. The team consisted of myself (Greg Sabino Mullane), [Mark Johnson](/team/mark_johnson), [Selena Deckelmann](http://www.chesnok.com/daily/), and [Josh Tolley](/team/josh_tolley). While I undertook the task of downloading the latest version and putting it into a local git repository, others were assigned to get an overview of how it worked, examine the API, and start writing some unit tests.

In a nutshell, the Test::Database module allows an easy interface to creating and destroying test databases. This can be a non-trivial task on some systems, so putting it all into a module make sense (as well as the benefits of preventing everyone from reinventing this particular wheel). Once we had a basic understanding of how it worked, we were off.

While all of our tasks overlapped to some degree, we managed to get the job done without too much trouble, and in a fairly efficient manner. We made a new file for Postgres, added in all the required API methods, wrote tests for each one, and documented everything as we went along. The basic method to create a test database is to use [the initdb program](http://www.postgresql.org/docs/current/static/app-initdb.html) to create a new
[Postgres cluster](http://www.postgresql.org/docs/8.3/static/creating-cluster.html), then modify the cluster to use a local Unix socket in the newly created directory (this side-stepping completely the problem of using an already occupied port). Then we can start up the new cluster via
[the pg_ctl command](http://www.postgresql.org/docs/current/static/app-pg-ctl.html), and create a new database.

At the end of the day, we had a working module that passed all of its tests. We combined our git patches into a single one mailed it to the author of the module, so hopefully you'll soon see a new version of Test::Database with Postgres support!
