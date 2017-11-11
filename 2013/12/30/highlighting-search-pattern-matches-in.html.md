---
author: Patrick Lewis
gh_issue_number: 908
tags: vim
title: Highlighting Search Pattern Matches in Vim
---

Vim’s **hlsearch** option is a commonly-used way to enable visual feedback when searching for patterns in a Vim buffer. When highlighting of search matches is enabled (via **:set hlsearch**), Vim will add a colored background to all text matching the current search.

Search highlighting is useful but it’s not obvious how to turn off the highlighting when you’re no longer concerned with the results of your last search. This is particularly true if you didn’t enable the **hlsearch** setting yourself but inherited it from a prebuilt package like [Janus](https://github.com/carlhuda/janus) or copied someone else’s .vimrc file.

One commonly-used way to clear the highlighting is to search for a garbage string by doing something like **/asdfkj** in normal mode. This method will clear the search highlights but has the undesired side effect of altering your search history. 

A better way to disable search highlighting temporarily is with the **:nohlsearch** command (which can be abbreviated to **:noh**). This will clear the highlights temporarily, but they’ll be turned back on the next time you perform a search. Also, you can use the n/N keys to resume your previous search, which isn’t possible if you use the above method of searching for a garbage string.

For more information on highlighting search matches in Vim, check out the [Highlight all search pattern matches](http://vim.wikia.com/wiki/VimTip14) entry on the Vim Tips Wiki.
