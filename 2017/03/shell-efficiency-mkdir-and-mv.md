---
author: Jon Jensen
title: 'Shell efficiency: mkdir and mv'
github_issue_number: 1291
tags:
- shell
- tips
date: 2017-03-10
---

Little tools can be a nice improvement. Not everything needs to be thought-leaderish.

For example, once upon a time in my Unix infancy I didn’t know that `mkdir` has the `-p` option to make intervening directories automatically. So back then, in order to create the path a/b/c/ I would’ve run:

```shell
mkdir a; mkdir a/b; mkdir a/b/c
```

when I could instead have simply run:

```shell
mkdir -p a/b/c
```

In working at the shell, particularly on my own local machine, I often find myself wanting to move one or several files into a different location, to file them away. For example:

```shell
mv -i ~/Downloads/Some\ Long\ File\ Name.pdf ~/some-other-long-file-name.tar.xz ~/archive/new...
```

at which point I realize that the subdirectory of ~/archive that I want to move those files into does not yet exist.

I can’t simply move to the beginning of the line and change `mv` to `mkdir -p` without removing my partially-typed `~/archive/new...`.

I can go ahead and remove that, and then after I run the command I have to change the `mkdir` back to `mv` and add back the `~/archive/new...`.

In one single day I found I was doing that so often that it became tedious, so I re-read the GNU coreutils manpage for mv to see if there was a relevant option I had missed or a new one that would help. And I searched the web to see if a prebuilt tool is out there, or if anyone had any nice solutions.

To my surprise I found nothing suitable, but I did find some discussion forums full of various suggestions and many brushoffs and ill-conceived suggestions that either didn’t work for me or seemed much overengineered.

The solution I came up with was very simple. I’ve been using it for a few months and am happy enough with it to share it and see if it helps anyone else.

In zsh (my main local shell) add to ~/.zshrc:

```shell
mkmv() {
    mkdir -p -- "$argv[-1]"
    mv "$@"
}
```

And in bash (which I use on most of the many servers I access remotely) add to ~/.bashrc:

```shell
mkmv() {
    mkdir -p -- "${!#}"
    mv "$@"
}
```

To use: Once you realize you’re about to try to move files or directories into a nonexistent directory, simply go to the beginning of the line (^A = control-A in standard emacs keybindings) and type `mk` in front of the `mv` that was already there:

```shell
mkmv -i ~/Downloads/Some\ Long\ File\ Name.pdf ~/some-other-long-file-name.tar.xz ~/archive/new...
```

It creates the directory (or directories) and then completes the move.

There are a few important considerations that I didn’t foresee in my initial naive implementation:

- Having the name be *something*mv meant less typing than something requiring me to remove the mv.
- For me, it needs to support not just moving one thing to one destination, but rather a whole list of things. That meant accessing the last argument (the destination) for the mkdir.
- I also needed to allow through arguments to `mv` such as `-i`, `-v`, and `-n`, which I often use.
- The `--` argument to mkdir ensures that we don’t accidentally end up with any other options and that we can handle a destination with a leading `-` (which does occasionally come up).
- The mv command needs to have a double-quoted `"$@"` so that the original parameters are each expanded into double-quoted arguments, allowing for spaces and other shell metacharacters in the paths. (See the zsh and bash manpages for details on the important difference in behavior of `"$@"` compared to `"$*"` and either of them unquoted.)

This doesn’t support GNU extensions to mv such as the option `--target-directory` that precedes the source paths. I don’t use that interactively, so I don’t mind.

Because this is such a small thing, I avoided for years bothering to set it up. But now that I use it all the time, I’m glad I have it!
