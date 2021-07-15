---
author: Jon Jensen
title: File names the same except for capitalization
github_issue_number: 1189
tags:
- sysadmin
- tips
date: 2016-01-07
---



Most Unix filesystems, including all the common Linux ones, are fully case-sensitive, meaning you can have two files in the same directory that differ only by case:

- a-very-nice-image.png
- a-VERY-nice-image.png

However, this is not true on Windows and Mac OS X. They will preserve your chosen capitalization, but each file name must be unique regardless of the case.

I don’t know of situations where it would be wise to have such conflicting mixed-case files even on Linux where it works fine. But for various reasons this can happen in the messy real world. If you then send those files to someone on Windows or Mac OS X in a zip file, or via Git version control, they’re going to be confused.

When unzipping, usually the last file to be extracted will overwrite the earlier one with the nearly-same name. So a file that is perhaps important will just be mysteriously gone.

When pulling in files with Git, the same thing happens, but you also immediately have an unclean working copy that Git will tell you about:

```bash
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   a-VERY-nice-image.png
```

To fix that, it’s easiest to go back to the (presumably) Linux system where the conflicting files were created, and remove one of them. Then on the Windows or Mac OS X side, remove both files (with normal rm) and then git pull or at least git checkout . to write the surviving file to disk.

If you have a large set of files with several conflicting names scattered throughout and want an easy way to see them all at once so you can clean them up, there’s a simple Unix pipeline you can run at the shell:

```bash
find . | sort -f | uniq -Di
```

That is a variation of one of the suggestions from [a Stack Exchange discussion](http://unix.stackexchange.com/questions/85410/how-to-find-file-directory-names-that-are-the-same-but-with-different-capitaliz), but changed to show both file names with the uniq -D option that is only in the GNU version of uniq. Other versions have uniq -d which is almost as good but shows just one of the pair of other-than-case-duplicated names.

Happy new year, and I hope you never have need for any of this advice. :)


