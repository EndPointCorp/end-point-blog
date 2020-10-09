---
author: Selena Deckelmann
gh_issue_number: 114
tags: tips, vim
title: 'Vim Tip of the Day: running external commands in a shell'
---

A common sequence of events when editing files is to make a change and then need to test by executing the file you edited in a shell. If you’re using Vim, you could suspend your session (ctrl-Z), and then run the command in your shell.

That’s a lot of keystrokes, though. 

So, instead, you can use Vim’s built-in “run a shell command”!

> `:!{cmd}` Run a shell command, shows you the output and prompts you before returning to your current buffer.

Even sweeter, is to use the Vim special character for current filename: `%`

Here’s `:! %` in action!

<img alt="" border="0" src="/blog/2009/03/10/vim-tip-of-day-running-external/image-0.png" style="margin:0px auto 10px; text-align:center;"/>

<img alt="" border="0" src="/blog/2009/03/10/vim-tip-of-day-running-external/image-1.png" style="margin:0px auto 10px; text-align:center;"/>

A few more helpful shortcuts related to executing things in the shell: 

- `:!` By itself, runs the last external command (from your shell history)
- `:!!` Repeats the last command
- `:silent !{cmd}` Eliminates the need to hit enter after the command is done
- `:r !{cmd}` Puts the output of $cmd into the current buffer.
