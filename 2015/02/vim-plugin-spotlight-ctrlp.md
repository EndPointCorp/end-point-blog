---
author: Patrick Lewis
title: 'Vim Plugin Spotlight: CtrlP'
github_issue_number: 1087
tags:
- extensions
- vim
date: 2015-02-06
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/02/vim-plugin-spotlight-ctrlp/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/02/vim-plugin-spotlight-ctrlp/image-0.png"/></a></div>

When I started using Vim I relied on tree-based file browsers like netrw and NerdTree for navigating a project’s files within the editor. After discovering and trying the [CtrlP](https://github.com/ctrlpvim/ctrlp.vim) plugin for Vim I found that jumping directly to a file based on its path and/or filename could be faster than drilling down through a project’s directories one at a time before locating the one containing the file I was looking for.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/02/vim-plugin-spotlight-ctrlp/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/02/vim-plugin-spotlight-ctrlp/image-1.png"/></a></div>

After it’s invoked (usually by a keyboard shortcut) CtrlP will display a list of files in your current project and will filter that list on the fly based on your text input, matching it against both directory names and file names. Pressing <control-f> with CtrlP open toggles through two other modes: most recently used files, and current buffers. This is useful when you want to narrow down the list of potential matches to only files you have worked with recently or currently have open in other buffers. I use CtrlP’s buffer mode to jump between open files so often that I added a custom mapping to invoke it in my .vimrc file:

```
map <leader>b :CtrlPBuffer<cr></cr>
```

CtrlP has many configuration options that can affect its performance and behavior, and installing additional plugins can provide different matcher engines that search through a directory more quickly and return more relevant results than the default matcher. Alternate matchers I’ve found include:

- [https://github.com/burke/matcher](https://github.com/burke/matcher)
- [https://github.com/JazzCore/ctrlp-cmatcher](https://github.com/JazzCore/ctrlp-cmatcher)
- [https://github.com/FelikZ/ctrlp-py-matcher](https://github.com/FelikZ/ctrlp-py-matcher)

Of these, I’ve had the best luck with FelixZ’s [ctrlp-py-matcher](https://github.com/FelikZ/ctrlp-py-matcher). It’s easy to install, works on most systems without requiring additional dependencies, and manages to be both faster and return more relevant results than the built-in CtrlP matcher.

CtrlP is well documented in both its README (available on its [GitHub project page](https://github.com/ctrlpvim/ctrlp.vim)) and its Vim documentation (available with **:help ctrlp** within Vim). The documentation covers the different commands and configuration options provided by CtrlP but simply installing the plugin and hitting <control-p> on your keyboard is enough to get you started with a faster way to navigate between files in any codebase.
