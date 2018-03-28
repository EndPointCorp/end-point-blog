---
author: Kiel Christofferson
gh_issue_number: 203
tags: environment, open-source, tips
title: 'GNU Screen: follow the leader'
---

First of all, if you’re not using [GNU Screen](http://www.gnu.org/software/screen/), start now :).

Years ago, [Jon](/team/jon_jensen) and I spoke of submitting patches to implement some form of “follow the leader” (like the children’s game, but with a work-specific purpose) in GNU Screen. This was around the time he was patching screen to raise the hard-coded limit of 40 windows allowed within a given session, which might give an idea of how much screen gets used around here (a lot).

The basic idea was that sometimes we just want to “watch” a co-worker’s process as they’re working on something within a shared screen session. Of course, they’re going to be switching between screen windows and if they forget to announce “I’ve switched to screen 13!” on the phone, then one might quickly become lost. What if the cooperative work session doesn’t include a phone call at all?

To the rescue, Screen within Screen.

Accidentally arriving at one screen session within another screen session is a pretty common “problem” for new screen users. However, creative use of two (or more) levels of nested screen during a shared session allows for a “poor man’s” follow the leader.

If the escape sequence of the outermost screen is changed to something other than the default, then the default escape sequence will pass through and take effect on the inner screen. In this way, anyone attached to the outermost screen will be following whomever is controlling the inner screen session as they flip between windows, grep logs, launch editors and save my [vegan bacon](http://www.lightlife.com/Vegan-Food-Vegetarian-Diet/Smart-Bacon.html)! To “break away” from the co-working session, a user would simply use the chosen non-default escape sequence of the outermost screen to create a new window or disconnect entirely.

Sound confusing? Give some of the following commands a try. You can always just close out all the windows of a screen session and eventually you’ll make it back to your original shell.

Steps:

1. start the outermost screen session (called “followme”) with a non-default escape sequence (pick one that suits you):
```nohighlight
screen -S followme -e ^ee
```

1. from within the “followme” session, start the inner screen where actual work will be performed:
```nohighlight
screen -S work
```

1. get friends and co-workers (logged-in as the same user) to connect to your “followme” screen:
```nohighlight
screen -x followme
```

1. work as normal using the **default**: *CTRL-a* sequences (which ought to affect the inner “work” session).
1. to “break away” from the “work” session: *CTRL-e* sequences (which ought to affect the outer “followme” session). For example, to disconnect from the shared session, one would type *CTRL-e d*

Note: If those sharing the screen session are already acclimated to screen-within-screen, you can skip the non-default escape sequences entirely and use *CTRL-a a* as the escape sequence (another *a* for every level of screen-within-screen). This also happens to be your evasion route for accidental screen-within-screen moments.

Remember that, by default, everyone who wants to share the screen must already be logged-in as the same user (without the use of sudo or su). There are methods of allowing shared screen access between users, but those are outside the scope of this post.

Have fun!

*(Update: Note that tmux by default has every attached viewer follow whoever is driving, and there you have to do extra work to have separate control of windows. tmux was still new and not available in most production systems at the time this article was written.)*
