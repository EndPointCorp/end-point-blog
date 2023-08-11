---
author: Ethan Rowe
title: Hopefully Useful Techniques for Git Rebase
github_issue_number: 341
tags:
- git
- testing
date: 2010-08-20
---



I recently had to spend a few hours merging Git branches to get a development branch in line with the master branch. While it would have been a lot better to do this more frequently along the way (which I’ll do going forward), I suspect that plenty of people find themselves in this position occasionally.

The work done in the development branch represents significant new design/functionality that refactors a variety of older components. My preference was to use a rebase rather than a merge, to keep the commit history clean and linear and, more critically, because the work we’re doing really can be thought of as being “applied to” the master branch.

No doubt there are a variety of strategies to apply here. This worked for me and perhaps it’ll help someone else.

### Some Key Concerns for a Big Rebase

Beyond the obvious concern of having sufficient knowledge of the application itself, so that you can make intelligent choices with respect to the code, there are a number of key operational concerns specific to rebase itself. This list is not exhaustive, but it is not an unreasonable set of key considerations to keep in mind.

#### **Rebase is destructive**

Remember what you’re doing! While a merge literally combines two or more revision histories, a rebase takes a chunk of revision history and applies it on top of another related history. It’s like a cherry-pick on steroids (really nice, friendly steroids that provoke neither rage nor senate hearings): each commit gets logically applied on top of the specified head, and as such gets rewritten. The commits are not the same afterwards. The history of your working tree’s branch is rewritten.

So, before you rebase, protect yourself: *Make sure you have more than one reference (either a branch or a tag) pointing to your current work.*

#### **Conflict resolution can bring about bugs**

When resolving merge conflicts along the way, you’ll need to manually inspect things to try to figure out the right path forward. If it’s been a while since you merged/rebased, you may find that merge conflict resolution is not so simple: rather than picking one version or the other, you’re literally merging them in some logical manner. You may end up writing new code, in other words.

Because you are involved and you are a mammal, there is a decent possibility that you will screw this up.

So, again, protect yourself: *Look at what’s coming before you rebase and take note of likely conflict resolution points.*

#### **Things go wrong and an abort can be necessary**

Some times it becomes quite clear that a mistake has been made along the way, and you need to bail out and regroup. If you’re doing a gigantic rebase in one big shot, this can happen after you’re 15, 45, 90, or 120+ minutes into the task. Do you really want to have to go all the way back to the beginning of your rebase excursion and start fresh?

Don’t let this happen. When approaching the rebase, show humility, expect things to go wrong, and embrace a strategy that lets you recover from mistakes:

*Break the rebase into smaller chunks and proceed through them incrementally*

#### **You may not immediately know that something went wrong**

Unless the code base is pretty trivial or you are 100% committed to that code base all the time, it is unlikely that you’ll be completely on top of everything that’s happened in both revision histories. You can test the stuff you know, you can run test suites, etc., but it’s critical to work defensively.

Prepare for the possibility of delayed mistake revelation: *Keep track of what you do as you go*

### Addressing the Concerns

The technique I’ve come to use to address the stated concerns is fairly simple to learn, understand, and apply in practice. It’s iterative in nature and is therefore **Agile** and therefore grants me **a sense of personal validation**, which is **very, very important**.

For a real-world use case, you’ll probably want to use more helpful, specific branch and tag names than this. The names in this discussion are deliberately simple for illustrative purposes.

Say you have a master branch which represents the canonical state of the code base. You’ve been working on the shiny branch where everything is more awesome. But shiny really needs to keep up with master, it’s been a while, and so you want to rebase shiny onto master.

We’re going to have the following things:

- Multiple stages of rebasing, leading incrementally from shiny to the full rebase of shiny on master.
- A “target” for each stage: the commit from master onto which your rebasing the work from shiny
- A tag providing an intuitive name for each target
- A branch providing the revision history for each stage

Given those things, we can follow a simple process:

1. Make a branch from the latest shiny named for the next stage (i.e. from shiny we make shiny_rebase_01, from shiny_rebase_02 we make shiny_rebase_03, and so on).

When you’re just starting the rebase, this might mean:

```plain
[you@yours repo] git checkout -b shiny_rebase_01 shiny
```

But for the next iteration, you would have shiny_rebase_01 checked out, and use it as your starting place:
```plain
# The use of "shiny_rebase_01" is implied assuming our previous checkout above
[you@yours repo] git checkout -b shiny_rebase_02

# A subsequent one, again assuming we’re on our most recent stage’s branch already
[you@yours repo] git checkout -b shiny_rebase_03
```

And so on.

This addresses concerns 1, 3, and 4: you’re protecting yourself against rebase’s inherent destructiveness, by always working on new branches; you’re facilitating the staging of work in smaller chunks, and you’re keeping track of your work by having a separate branch representing the state of each change.

1. Review the revision history of master, look for commits likely to contain significant conflicts or representing significant inflection points, and pick your next target commit around them; if you have a pile of simple commits, you might want the target to be the last such simple commit prior to a big one, for instance. If you have a bunch of big hairy commits you may want each to be its own target/stage, etc. Use your knowledge of the app.

The git whatchanged command is very useful for this, as by default it lists the files changed in a commit, which is the right granularity for this kind of work. You want to quickly scan the history for commits that affect files you know to be affected by your work in shiny, because they will be a source of conflict resolution points. You don’t want to look at the full diff output of git log -p for this purpose; you simply want to identify likely conflict points where manual intervention will be required, where things may go wrong. After having identified such points, you can of course dig into the full diffs if that’s helpful.

Make your life easy by using the last target tag as the starting place for this review, so you only wade through the commits on master that are relevant to the current rebase stage (since the last target tag is where your branches diverge, it’s where the rebase will start from).

At this point you may say “but I don’t have a last target tag!” The first time through, you won’t have one because you haven’t done an iteration yet. So for the first time, you can start from where git rebase itself would start:

```plain
[you@yours repo] git whatchanged `git merge-base master shiny`..master
```

But subsequent iterations will have a tag to reference (see the next step), so the next couple times through might look like:

```plain
[you@yours repo] git whatchanged shiny_rebase_target_01..master

[you@yours repo] git whatchanged shiny_rebase_target_02..master
```

Etc.

This is addressing items 2 and 3: we’re looking at what’s coming before we leap, and structuring our work around the points where things are likely to be inconvenient, difficult, etc.

1. Having identified the commit you want to use as your next rebasing point, make a tag for it. Name the tags consistently, so they reflect the stage to which they apply. So, if this is our first pass through and we’ve determined that we want to use commit a723ff127 for our first rebase point, we say:

```plain
[you@yours repo] git tag shiny_rebase_target_01 a723ff127
```

This gives us a list of tags representing the different points in the master onto which we rebased shiny in our staged process. It therefore addresses item 4, keeping track as you go.

1. You’re now on a branch for the current stage, you have a tag representing the point from master onto which you want to rebase. So do it, but capture the output of everything. Remember: mistakes along the way may not be immediately apparent. You will be a happier person if you’ve preserved all the operational output so you can review to track down where things potentially went wrong.

So, for example:

```plain
[you@yours repo] git rebase shiny_rebase_target_01 >> ~/shiny_rebase_work/target_01.log 2>&1
```

You would naturally update the tag and logfile per stage.

Review the logfile in your pager of choice. Is there a merge conflict reported at the bottom? Well, capture that information *before* you dive in and resolve it:

```plain
# Log the basic info about the current state
[you@yours repo] git status >> ~/shiny_rebase_work/target_01.log 2>&1
# Log specifically what the conflicts are
[you@yours repo] git diff >> ~/shiny_rebase_work/target_01.log 2>&1
```

Now go and resolve your conflicts per usual, but remember to preserve your output when you resume:

```plain
[you@yours repo] git rebase --continue >> ~/shiny_rebase_work/target_01.log 2>&1
```

This addresses point 4: keeping track of what happened as you go.

1. Now you finished that stage of the rebase, you resolved any conflicts along the way, you’ve preserved history of what happened, what was done, etc. So the final step is: test.

Run the test suite. You did implement one, right?

Test the app manually, as appropriate.

Don’t put it off until the end. Test as you go. Seriously. If something is broken, use git blame, git bisect, and your logs and knowledge of the system to figure out where the problem originates. Consider blowing away the branch you just made, going back to the previous stage’s branch, selecting a new target, and moving forward with a smaller set of commits. Etc. But make sure it works as you go.

This does not necessarily fit any specific point, but is more to ensure the veracity of the overall staged rebase process. The point of iterative work is that each iteration delivers a small bit of *working* stuff, rather than a big pile of broken stuff.

1. Repeat this process until you’ve successfully finished a rebase stage for which the target is in fact the head of master. Done.

So, that’s the process I’ve used in the past. It’s been good for me, maybe it can be good for you. If anybody has criticisms or suggestions I’d love to hear about them in comments.


