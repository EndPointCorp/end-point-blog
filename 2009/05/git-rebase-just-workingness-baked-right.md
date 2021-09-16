---
author: Ethan Rowe
title: 'Git rebase: Just-Workingness Baked Right In (If you’re cool enough)'
github_issue_number: 154
tags:
- spree
- git
date: 2009-05-28
---

Reading about rebase makes it seem somewhat abstract and frightening,
but it’s really pretty intuitive when you use it a bit. In terms of how
you deal with merging work and addressing conflicts, rebase and merge
are very similar.

Given branch “foo” with a sequence of commits:

```nohighlight
foo: D --> C --> B --> A
```

I can make a branch “bar” off of foo: (git branch bar foo)

```nohighlight
foo: D --> C --> B --> A
bar: D --> C --> B --> A
```

Then I do some development on bar, and commit. Meanwhile, somebody else
develops on foo, and commits. Introducing new, unrelated commit structures.

```nohighlight
foo: E --> D --> C --> B --> A
bar: X --> D --> C --> B --> A
```

Now I want to take my “bar” work (in commit X) and put it back upstream
in “foo”.

- I can’t push from local bar to upstream foo directly because it is not
a fast-forward operation; foo has a commit (E) that bar does not.
- I therefore have to either merge local bar into local foo and then
push local foo upstream, or rebase bar to foo and then push.

A merge will show up as a separate commit. Meaning, merging bar into
foo will result in commit history:

```nohighlight
foo: M --> X --> D --> C --> B --> A
      \
       E --> D --> C --> B --> A
```

(The particulars may depend on conflicts in E versus X).

Whereas, from branch “bar”, I could “git rebase foo”. Rebase would look
and see that “foo” and “bar” have commits in common starting from D.
Therefore, the commits in “bar” more recent than D would be pulled out
and applied on top of the full commit history of “foo”. Meaning, you
get the history:

```nohighlight
bar: X' --> E --> D --> C --> B --> A
```

This can be pushed directly to “foo” upstream because it contains the
full “foo” history and is therefore a fast-forward operation.

Why does X become X’ after the rebase? Because it’s based on the
original commit X, but it’s not the same commit; part of a commit’s
definition is its parent commit, and while X originally referred to
commit D, this derivative X’ refers instead to E. The important thing
to remember is that the content of the X’ commit is taken initially from
the original X commit. The “diff” you would see from this commit is the
same as from X.

If there’s a conflict such that E and X changed the same lines in some
file, you would need to resolve it as part of rebasing, just like in a
regular merge. But those changes for resolution would be part of X’,
instead of being part of some merge-specific commit.

### Considerations for choosing rebase versus merge

Rebasing should generally be the default choice when you’re pulling from
a remote into your repo.

```nohighlight
git pull --rebase
```

Note that it’s possible to make --rebase the default option for pulling for a given branch. From Git’s pull docs:

>   To make this the default for branch *name*, set configuration branch.*name*.rebase to true.

However, as usual with Git, saying “do this by default” only gets you so
far. If you assume rebase is always the right choice, you’re going to
mess something up.

Probably the most important rule for rebasing is: do not rebase a branch that has been pushed upstream, unless you are positive nobody else is using it.

Consider:

- Steph has a [Spree fork on GitHub](http://github.com/stephskardal/spree/tree). So on her laptop, she has a repo that has her GitHub fork as its “origin” remote.
- She also wants to easily pull in changes from the canonical Spree GitHub repo, so she has that repo set up as the “canonical” remote in her local repo.
- Steph does work on a branch called “address_book”, unique to her GitHub fork (not in the canonical repo).
- She pushes her stuff up to “address_book” in origin.
- She decides she needs the latest and greatest from canonical. So she fetches canonical. She can then either: rebase canonical/master into address_book, or merge.

The merge makes for an ugly commit history.

The rebase, on the other hand, would make her local address_book branch
incompatible with the upstream one she pushed to in her GitHub repo.
Because whatever commits she pushed to origin/address_book that are
specific to that branch (i.e. not on canonical/master) will get rebased
on top of the latest from canonical/master, meaning they are now
**different** commits with a different commit history. Pushing is now not
really an option.

In this case, making a different branch would probably be the best choice.

Ultimately, the changes Steph accumulates in address_book should indeed
get rebased with the stuff in canonical/master, as the final step
towards making a clean history that could get pulled seamlessly onto
canonical/master.

So, in this workflow, a final step for publishing a set of changes
intended for upstream consumption and potential merge into the main
project would be, from Steph’s local address_book branch:

```nohighlight
# get the latest from canonical repo
git fetch canonical
# rebase the address book branch onto canonical/master
git rebase canonical/master
# work through any conflicts that may come up, and naturally test
# your conflict fixes before completing
...
git push origin address_book:refs/heads/address_book_release_candidate
```

That would create a branch named “address_book_release_candidate” on
Steph’s GitHub fork, that has been structured to have a nice commit
history with canonical/master, meaning that the Spree corefolks could
easily pull it into the canonical repo if it passes muster.

What you would not **ever** do is:

```nohighlight
git fetch canonical
# make a branch based off of canonical/master
git branch canonical_master canonical/master
# rebase the master onto address_book
git rebase address_book
```

As that implies messing with the commit history of the canonical master
branch, which we all know to be published and therefore must not be
subject to history-twiddling.
