---
author: Selena Deckelmann
gh_issue_number: 114
tags: tips, vim
title: 'VIM Tip of the Day: running external commands in a shell'
---



A common sequence of events when editing files is to make a change and then need to test by executing the file you edited in a shell. If you're using vim, you could suspend your session (ctrl-Z), and then run the command in your shell.

That's a lot of keystrokes, though. 

So, instead, you could use vim's built-in “run a shell command”!

> 
> :!{cmd} Run a shell command, shows you the output and prompts you before returning to your current buffer.
> 

Even sweeter, is to use the vim special character for current filename: %

Here's `:! %` in action!

<a href="http://2.bp.blogspot.com/_lsIXJbnz6n8/SbaJSmAHiXI/AAAAAAAAABs/z_sOCKeFEaw/s1600-h/Terminal+%E2%80%94+vim+%E2%80%94+80%C3%9728-1.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5311583763061770610" src="/blog/2009/03/10/vim-tip-of-day-running-external/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 229px;"/></a>

<a href="http://4.bp.blogspot.com/_lsIXJbnz6n8/SbaJZ8Usz6I/AAAAAAAAAB0/Mjf7ekC3oSA/s1600-h/Terminal+%E2%80%94+vim+%E2%80%94+80%C3%9728-4.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5311583889312763810" src="/blog/2009/03/10/vim-tip-of-day-running-external/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 229px;"/></a>

A few more helpful shortcuts related to executing things in the shell: 

- `:!` By itself, runs the last external command (from your shell history)
- `:!!` Repeats the last command
- `:silent !{cmd}` Eliminates the need to hit enter after the command is done
- `:r !{cmd}` Puts the output of $cmd into the current buffer.
