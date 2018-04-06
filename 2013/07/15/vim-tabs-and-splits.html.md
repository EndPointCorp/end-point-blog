---
author: Mike Farmer
gh_issue_number: 833
tags: vim
title: VIM - Tabs and Splits
---



[Vim](http://www.vim.org/) is my go-to code editor these days. After many years of using different editors, I’ve settled on vim as my editor of choice. There are some things I’ve done to make using vim more enjoyable and usable and this blog post is dedicated to some of those things that I use everyday.

### Tabs

I love using tabs in vim. I know there are some who are opposed to tabs, but I find them invaluable. The default shortcuts for manipulating tabs are a little cumbersome, which I believe deters many users. Here are some modifications that I added to my [vimrc](https://github.com/mikefarmer/dotfiles/blob/master/vimrc).

```nohighlight
nmap <silent> tt :tabnew<CR>
nmap <silent> [g :tabprevious<CR>
nmap <silent> ]g :tabnext<CR>
nmap <silent> [G :tabrewind<CR>
nmap <silent> ]G :tablast<CR>
```

First, I’m using nmap here which says to only map these keys in normal mode. Next, I use <silent> which keeps my editor clean of any distractions while performing the task. I find that the double tap short-cuts (see more below) tt work really well for normal mode and I love their simplicity. Double-tap t and you have a new tab. Using the bracket navigation is something that I’ve stolen from [Tim Pope’s](https://github.com/tpope) [vim-unimpaired](https://github.com/tpope/vim-unimpaired) plugin. Using g and G work for me, but you can use whatever you like.

### Splits

I believe most vim users use splits often. At first, I found that splitting my current buffer was also cumbersome using the default method in vim (:split and :vsplit). So utilizing the double-tap method I used for tabs, I created my own shortcuts:

```nohighlight
nmap <silent> vv :vsp<CR>
nmap <silent> ss :sp<CR>
```

Once you have a split, navigating between them can be a little bit of a pain as well. Here’s my optimization:

```nohighlight
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l
```

After using vim’s splitting capability for a while, I noticed I didn’t always like where the split occurred. Sometimes above, sometimes to the left. To ensure that you have consistency, try these settings:

```
set splitright " When splitting vertically, split to the right
set splitbelow " When splitting horizontally, split below
```

Using splits and tabs give you a lot of flexibility in managing the code you are currently working. Adding just a few shortcuts and optimizations to your vimrc can really speed up your workflow and help you navigate your code more quickly.

### One more thing

Want a quick way to get to your vimrc?

```nohighlight
:e $MYVIMRC
```

