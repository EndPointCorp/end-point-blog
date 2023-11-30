---
author: Patrick Lewis
title: 'vim-airline: A lightweight status/tabline for Vim'
github_issue_number: 989
tags:
- vim
date: 2014-06-02
---

My standard Vim configuration makes use of around 30 different plugins and I consider [vim-airline](https://github.com/bling/vim-airline) to be one of the most indispensable because of its built-in functionality and superb integration with a variety of other Vim plugins. It’s a great starting point for anyone looking to extend their Vim setup with additional plugins.

I became interested in vim-airline the first time I saw screenshots of it; the color schemes, custom glyphs[[1]](#footnote1) and indicators immediately revealed value beyond the basic status bar that a stock Vim installation provides. After installing and spending some time using vim-airline I discovered additional benefits due to its integration with other plugins such as [Fugitive](https://github.com/tpope/vim-fugitive), [Syntastic](https://github.com/scrooloose/syntastic) and [CtrlP](https://github.com/kien/ctrlp.vim). vim-airline provides a common platform for integrating the display indicators of plugins from various authors into one view and presents them all with consistent a consistent style.

A quick comparison of Vim with vim-airline installed:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/06/vim-airline-lightweight-statustabline/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/06/vim-airline-lightweight-statustabline/image-0.png"/></a></div>

vs. a standard Vim installation:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/06/vim-airline-lightweight-statustabline/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/06/vim-airline-lightweight-statustabline/image-1.png"/></a></div>

reveals new indicators for the current Vim mode, git branch, open buffers, and line endings. Integrating other plugins can add additional indicators for syntax errors, trailing whitespace, and more.

Using vim-airline also helped me adopt the usage of built-in Vim functionality that I had previously overlooked. I had not used Vim’s tab features, favoring a single split window, but after enabling vim-airline’s tabline feature I am now in the habit of using a combination of tabs and split windows to organize my workspace and have found that I am more easily able to keep track of multiple files at a time.

I recommend reading through the documentation for vim-airline, trying it out and then installing some of the [other plugins](https://github.com/bling/vim-airline#seamless-integration) that it integrates with in order to develop your own preferred set of Vim plugins. I spend most of my workday in a Vim session and consider it a good investment to research different plugins and features that can increase productivity and developer happiness.

<a id="footnote1">[1]</a> Note that some of the nice-looking but non-standard characters available in vim-airline require the use of a patched font; pre-patched versions of many popular monospaced fonts are available in the [powerline-fonts](https://github.com/Lokaltog/powerline-fonts) repository on GitHub and are easy to install (I’m a fan of Adobe’s Source Code Pro font).
