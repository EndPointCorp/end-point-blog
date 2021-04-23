---
author: Ron Phipps
gh_issue_number: 735
tags: terminal
title: tmux and SecureCRT settings
---

Richard gave me a call today to show the wonders of tmux. I am using Windows, and unfortunately, right off the bat I couldn’t see color and there were a bunch of accented `a`s dividing the panes.

After some trial and error and finding [this post](https://stackoverflow.com/questions/8483798/tmux-borders-displayed-as-x-q-instead-of-lines) on the subject we got it working. The key is to configure SecureCRT to use xterm + ANSI colors and set the character set to UTF-8 and “Use Unicode line drawing code points”.

Hooray! I’ll be trying out tmux in day-to-day use to see if it will replace or augment screen for me.
