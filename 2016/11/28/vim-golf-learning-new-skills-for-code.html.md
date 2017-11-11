---
author: Josh Lavin
gh_issue_number: 1269
tags: vim
title: 'Vim Golf: Learning New Skills for Code Editors'
---

<div class="separator" style="clear: both; text-align: center;"><a href="https://en.wikipedia.org/wiki/File:Vimlogo.svg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" height="240" src="/blog/2016/11/28/vim-golf-learning-new-skills-for-code/image-0.png" width="240"/><br/><small>Vim logo freely licensed from Wikimedia Commons</small></a></div>

[Vim](http://www.vim.org/about.php) is a text-based editor that has been around for 25 years. It comes pre-installed on Linux distributions, so it is a great tool for developing on servers. One of the advantages of Vim is that oft-used keystrokes can be performed without moving your hands from the keyboard (there is no mouse in Vim).

Many of the engineers here at End Point use Vim for our daily development work, and recently, a few of us got together online to try to learn some new tricks and tips from each other. Being efficient with Vim not only improves productivity, it's a lot of fun.

Similar to playing a round of golf, we tested each other with various editing tasks, to see who could perform the task in the fewest number of keystrokes. This is known as "Vim Golf." There is even an [entire website](http://vimgolf.com/) devoted to this.

In this post, we share some of the interesting tricks that were shown, and also some links to further learning about Vim.

### Tips &amp; Tricks

- Indenting text: there are multiple ways to do this, but a few are:

        - Visually-select the lines of text to indent (Ctrl v or Shift v), then > to indent, or < to outdent. Press . to perform this action again and again.
        - Locate the line numbers for the lines you wish to change (:set number to turn on line numbering), then :17,36>> to indent lines 17-36 two indentation levels.
        - Define width of a tab :set tabstop=4 would for example set a tab to 4 spaces.
        - Use spaces defined in tabstop instead of an actual tab character (^I) when the Tab key is pressed :set expandtab or :set et
        - Replace tab settings for current line :retab
        - Replace tab settings for current document :retab!

- Visually-selecting text: Ctrl v will perform a visual column selection, while Shift v will do a row selection.
- :set will show all the currently-set options.
- For paging up or down, use Ctrl b and Ctrl f. You can also use PgUp and PgDn keys if you want to move your hands a bit :-)
- Moving the cursor around the page:

        - Type M  to move the cursor to the **middle** of the screen
        - Type H  to move the cursor to the **top** of the screen
        - Type L  to move the cursor to the **bottom** of the screen
        - Type gg to move the cursor to the **top** of the document
        - Type G  to move the cursor to the **bottom** of the document

- Moving the *page* around the cursor:

        - Type zz to make the current position float to the **middle** of the screen
        - Type zt to make the current position float to the **top** of the screen
        - Type zb to make the current position float to the **bottom** of the screen

- Search and replace:

        - Find and replace all instances of a string: %s/find_this/replace_with_this/g
        - Case-insensitive find and replace all instances of a string: %s/find_this/replace_with_this/gi
        - Find then ask confirmation before replacing: %s/find_this/replace_with_this/c
        - Search history: Vim maintains search history which is easy to access using / or ? then navigation through the list using the up and down arrows.

- Deleting from the current position to the bottom of the file: dG
- Jumping to the first position in the current line: 0
- Find the next occurrence of a character in the current line: f then the character. To search backwards, use F
- Undo a command: u (run this multiple times for additional undo steps)
- Redo your undo: Ctrl r
- Travel back in time to see the document as it was 30 mins ago :earlier 30m then revert with :later 30m
- Reselect the last visual selection gv
- Run a system command from within Vim :! [command]
- Review your previous vim command history q:

### For Further Learning

- Built-in Vim help: use :h name_of_command_or_setting (e.g. :h f)
- View manpage for the word under the cursor: K
- [Cheat sheets](http://www.viemu.com/a_vi_vim_graphical_cheat_sheet_tutorial.html)
- [Vim Tips with Ben](https://www.briefs.fm/vim-tips-with-ben) podcast
- [Vimcasts](http://vimcasts.org/) - free screencasts
- [Tweets from Mastering Vim](https://twitter.com/MasteringVim/)

*With contributions from [Sam Batschelet](/team/sam_batschelet)*
