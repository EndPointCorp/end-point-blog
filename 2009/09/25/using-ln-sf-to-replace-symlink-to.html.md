---
author: Jon Jensen
gh_issue_number: 204
tags: hosting, tips
title: Using ln -sf to replace a symlink to a directory
---



When you want to forcibly replace a symbolic link on some kind of Unix (here I’m using the version of ln from GNU coreutils), you can do it the manual way:

```nohighlight
rm -f /path/to/symlink
ln -s /new/target /path/to/symlink
```

Or you can provide the -f argument to ln to have it replace the existing symlink automatically:

```nohighlight
ln -sf /new/target /path/to/symlink
```

(I was hoping this would be an atomic action such that there’s no brief period when /path/to/symlink doesn’t exist, as when mv moves a file over top of an existing file. But it’s not. Behind the scenes it tries to create the symlink, fails because a file already exists, then unlinks the existing file and finally creates the symlink.)

Anyway, that’s convenient, but I ran into a gotcha which was confusing. If the existing symlink you’re trying to replace points to a directory, the above actually creates a symlink inside the dereferenced directory the old symlink points to. (Or fails if the referent is invalid.)

To replace an existing directory symlink, use the -n argument to ln:

```nohighlight
ln -sfn /new/target /path/to/symlink
```

That’s always what I have wanted it to do, so I need to remember the -n.


