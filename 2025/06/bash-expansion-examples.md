---
author: "Seth Jensen"
title: "Bash expansion techniques for a more efficient workflow"
date: 2025-05-09
description: Pratical examples of Bash expansion, with a summary of the different types
featured:
  image_url:
github_issue_number: 
tags:
- linux
- shell
- tips
---

For any project, you need a quick and efficient way to wrangle your files. As a Unix user, Bash and Zsh provide are powerful tools to help achieve this.

I recently needed to rename a file so that all its underscores were replaced with dash characters, to match the convention of the project. I could do this manually pretty quickly, but I knew there was a bash built-in one-liner waiting to be discovered, so I went down the rabbit hole to learn about Bash's [shell expansions](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html) and [history expansion](https://www.gnu.org/software/bash/manual/html_node/History-Interaction.html). See the "history expansion" section for how I solved the underscore/dash issue.

Bash has seven types of expansion:

- brace expansion
- tilde expansion
- parameter and variable expansion
- command substitution
- arithmetic expansion
- word splitting
- filename expansion 

The documentation is good and concise for each of these, so rather than try to recreate it, I'll go over examples of how I use some of them.

### Shell parameter expansion

#### Example: batch converting images to WebP

I use parameter expansion frequently while maintaining this blog. We serve images in [WebP format](/blog/2014/01/webp-images-experiment-on-end-point/), so I generally loop over all the JPEGs and/or PNGs (after cropping and/or scaling) and convert them using [cwebp](https://developers.google.com/speed/webp/docs/cwebp):

```bash
for f in *.png; do
  cwebp -q 80 $f -o ${f%png}webp
done
```

This makes use of parameter expansion (`${}`) and the `%` character, which deletes the shortest occurrence of the *word* it precedes (`png`) from the end of the *parameter* (`$f`, the filename). Then, you can insert a string immediately after the expansion and Bash will concatenate them together, making a new output filename.

If you use `%%` instead, it deletes the longest occurrence of the *word* from the end, instead of the shortest.

You can use the `#` character to remove a *word* from the beginning of the string, sort of the converse of `%` removes a match from the end.

> The formal definition of *word* in [the Bash manual](https://www.gnu.org/software///bash/manual/bash.html) is "A sequence of characters treated as a unit by the shell. Words may not include unquoted metacharacters."
>
> I looked this up so I would know the distinction between *words* and [*parameters*](https://www.gnu.org/software///bash/manual/bash.html#Shell-Parameters). Parameters are more specific: mainly just variables, positional parameters, and a few special parameters.

#### Example: counting file endings

I haven't used this one as often, but you can use `##` to count the number of each file ending in the current directory:

`${file/pattern/replacement}`

```bash
for f in *.*; do
  echo ${f##*.}
done | sort | uniq -c
```

It's not especially robust (e.g., it would show `.tar.gz` as simply `.gz`), but this is an example of a lightweight and versatile script with just Bash builtins and standard commands. Knowing the tools you're working with allows you to adapt them to your current situation.

* https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html

### History Expansion

Another type of expansion I use frequently is history expansion. The history expansion character is `!`, and there are several useful ways to use history within Bash commands:

`!!` repeats the most recent command. This is especially useful if you need to rerun a command with `sudo`. I often find myself running `sudo !!` after accidentally trying to install a program without `sudo`.

You can also expand any argument from the previous command using `!:n`, where n is the argument from the previous command, numbered from 0. More often than this, I use the shorthand `!$` which references the last argument from the previous command.

For example, if you've just run `diff really\ long\ filename\ I\ really\ don\'t\ want\ to\ type.txt other.txt`, you can edit the first file by typing `vim !:1`, without having to retype the long filename.

You can also reference previous words in the current command using the `!#` event designator:

```plain
echo words and more !#1
```

#### Example: Replacing underscores with dashes in a filename

Here's how I solved the underscore/dash issue, as promised. I used the `s` modifier to search and replace within the backreferenced word within the current command:

```plain
mv synthesized_beef_menu.md !#:1:gs/_/-
```

So simple! We just reference the second word (index `1`) in the current command and globally subsitute `-` for `_`.

Notice that history expansion works differently from the `${}` parameter expansion notation we saw previously. Rather than using the delimiter as a command, in history expansion you can use one or more modifiers separatd by `:` characters. If you have two files named `green-old.txt` and `green-new` (no file ending), you can make the second out of the first:

```plain
cat green-old.txt
cat !:1:r:s/old/new
```

This references word `1` from the previous command, removes the filename extension, leaving the root filename, then replaces "old" with "new". Not terribly useful for a single file, but this type of expansion could easily be used in scripting to move a large number of files into a new format.

To replace globally (not just once per line), you have to put the modifier *before* the search/replace pattern. This is different from sed-style search and replace flags, which go at the end after a terminal slash.

```plain
!!:0:gs/pattern/replacement
```

* https://www.gnu.org/software/bash/manual/html_node/History-Interaction.html

### Other types of expansion

I recommend looking through the [documentation](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html) for expansions and applying it to your own routines. A little goes a long way! If you get in the habit of noticing inefficiency and fixing it with the shell, you'll find yourself finishing menial tasks quicker. More time to spend solving problems that matter.
