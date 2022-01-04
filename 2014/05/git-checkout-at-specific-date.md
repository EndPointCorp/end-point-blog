---
author: Greg Sabino Mullane
title: git checkout at a specific date
github_issue_number: 983
tags:
- git
date: 2014-05-19
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/05/git-checkout-at-specific-date/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/git-checkout-at-specific-date/image-0.jpeg"/></a>
<br/><small><a href="https://flic.kr/p/eqKF87">Porcupine</a> via <a href="https://www.flickr.com/photos/pinti1/">Flickr user Holly Occhipinti</a></small></div>

There are times when you need to view a git repository as it was at a certain point in time. For example, someone sends your project an error report and says they were using the git head version from around January 17, 2014. The short (and wrong!) way to do it is to pass the date to the checkout command like so:

```bash
$ git checkout 'HEAD@{Jan 17 2014}' ## do not do this
```

While I used to rely on this, I no longer do so, as I consider it somewhat of a footgun. To understand why, you first have to know that the ability to checkout using the format above only works for a short window of time, as defined by the git parameter **gc.reflogExpire**. This defaults to a measly 90 days. You can view yours with **git config gc.reflogExpire**. The problem is that when you go over the 90 day limit, git outputs a warning, but them spews a mountain of output as it performs the checkout anyway! It uses the latest entry it has in the reflog (e.g. 90 days ago). This commit has no relation at all with the date you requested, so unless you catch the warning, you have checked out a repository that is useless to your efforts.

For example, the Bucardo project can be cloned via:

```bash
$ git clone git://bucardo.org/bucardo.git/
```

Now let’s say we want to examine the project as it looked on January 17, 2014. As I am writing this, the date is May 19, 2014, so that date occurred about four months ago: well over 90 days. Watch what happens:

```bash
$ git checkout 'HEAD@{Jan 17 2014}' ## do not do this
warning: Log for 'HEAD' only goes back to Sat, 22 Feb 2014 11:47:33 -0500.
Note: checking out 'HEAD@{Jan 17 2014}'.

You are in ‘detached HEAD’ state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b new_branch_name

HEAD is now at d7f89dd... Bucardo now accepts pg_service for databases
```

So, we get the warning that HEAD only goes back to Feb 22, but then git goes ahead and checks us out anyway! If you were not paying attention—​perhaps because you only glanced over that perfectly ordinary looking last line—​you might not realize that the checkout you received is not what you requested.

Since this behavior cannot, to my knowledge, be turned off, I avoid this method and use other ways to checkout the repo as it existed on a certain date. The simplest is to find the closest commit by viewing the output of **git log**. In smaller projects, you can simply do this in a text editor and search for the date you want, then find a good commit sha-1 hash to checkout (i.e. **git log > log.txt; emacs log.txt**). Another somewhat canonical way is to use git-rev-list:

```bash
$ git checkout `git rev-list -1 --before="Jan 17 2014" master`
```

This command works fine, although it is a little clunky and hard to remember. It’s requesting a list of all commits on the master branch, which happened before the given date, ordered by date, and stop once a single row has been output. Since I deal with SQL all day, I think of this as:

```sql
SELECT repository WHERE commit_id = 
  (SELECT commit
   FROM rev-list
   WHERE commit_date <= 'Jan 10, 2014'
   AND branch = 'master'
   ORDER BY commit_date DESC
   LIMIT 1
  );
```

This is one of the cases where the date IS inclusive. With git, you should always test when using date ranges if the given date is inclusive or exclusive, as reading the fine manual does not always reveal this information. Here is one way to prove the date is inclusive for the rev-list command:

```plain
$ git rev-list -1 --before="Jan 17 2014" master --format=medium
commit d4b565bf46b6f478b969a378578b0cff3b24e82d
Author: Greg Sabino Mullane <greg@endpoint.com>
Date:   Fri Jan 17 10:49:09 2014 -0500

    Make our statement_chunk_size default match up.
```

As a final nail in the coffin for doing a checkout via the reflog date, the reflog actually is local to you and will pull the date of the repo as it existed for you at that point in time. This may or may not line up with the commits, depending on how often you are syncing with other people via git pull or other methods! So play it safe and request a specific commit by sha-1 hash, or use the rev-list trick.
