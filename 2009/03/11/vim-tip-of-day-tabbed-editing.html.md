---
author: Christopher Nehren
gh_issue_number: 115
tags: tips, vim
title: 'VIM Tip of the Day: tabbed editing'
---

How many tabs does your browser have open? I have 17 tabs open in Firefox presently (and opened / closed about 12 while writing this post). Most users will agree that tabs have changed the way they use the Web. Even IE, which has spawned a [collection](http://www.avantbrowser.com/) of [shells](http://www.maxthon.com/) for [tabbed](http://www.netcaptor.com/) [browsing](http://www.runecats.com/), now supports it natively. Tabs allow for a great saving in screen real-estate, and in many cases, better interaction among the various open documents. Considering how much time programmers spend in their text editors, it therefore seems logical that the editor should provide the same functionality. 

And the VIM developers agree. Although VIM calls them "tab-pages", the functionality is there, waiting to be used. Before reading any further, ensure that your VIM supports tabs. You can do this by running this command, on anything resembling Unix: vim --version | fgrep '+windows', which will check for the required windows feature. If you don't see any output, check your vendor's packaging system for something like 'vim-full'. If you don't have a VIM available with the windows feature, go get one and come back.

Now that you can use tabs, let's get started. One way to open tabs is via the command line. vim uses the -p option to determine how many tab-pages to open. This functions like the -[oO] options for windows in that it accepts a numeric argument, but defaults to one for each specified file. Thus, let's propose a hypothetical situation. I want to compare the implementation of has() in both Moose and Mouse. Therefore, it might be convenient to have the two files open in two tab-pages in VIM. Presuming I'm in the same directory as both files, I would open vim with a tab-page for each file like so: vim -p Moose.pm Mouse.pm.

There will be a bar at the top of the terminal: That's the tab bar. It has every open tab, plus an X at the far right. That's great, and all, but how does one use this? There are a number of ways, depending upon your configuration. First, there's the basic tab page commands. These are:

- gt Advance to the next rightmost tab, cycling back to the first.- gT Advance to the next leftmost tab, cycling back to the last.- {count}gt Go to the {count} tab.

These commands work in both command-line VIM (for those of you working on remote machines) and in GVIM (for those of you writing new code). Additionally, GVIM and VIMs that recognize mouse input on a terminal (:help mouse-using) recognize clicks on the tabs or the X in the upper right. This tip has touched on the very basics of tab-pages, but the information covered here is enough to be useful (and is all I use on a regular basis). However, the curious should definitely read the VIM reference manual for more info, with :help tabpage.

