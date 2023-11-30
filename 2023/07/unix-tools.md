---
title: Unix tools & tips
author: Muhammad Najmi bin Ahmad Zabidi
github_issue_number: 1988
date: 2023-07-05
tags:
- linux
- tools
featured:
  image_url: /blog/2023/07/unix-tools/idaho-mountains.webp
---

![The view from a mountain ridge. the sky is light blue and partially covered in clouds. Green ridges covered in pine trees lead down to a flat valley populated by a small town.](/blog/2023/07/unix-tools/idaho-mountains.webp)

<!-- Photo by Seth Jensen, 2023. -->

The command line interface (CLI) programs/​tools found on UNIX-like (\*NIX) systems are among the most useful tools available to system administrators. CLI tools allow a system administrator to handle the \*NIX systems either remotely or locally without needing to install Graphical User Interface (GUI) packages.

Almost twenty years ago, I bought two O'Reilly books: "sed & awk, second edition," written by Dale Dougherty & Arnold Robbins, and "Mastering Regular Expressions," written by Jeffrey E.F. Friedl. These two books were printed in the late '90s, and I bought them in 2004. I remembered them recently when my co-workers and I held a few study sessions to learn regular expressions. When a page and chapter are mentioned in this post, I'm referring to the editions of these books printed in that particular year.

In this blog post, I'll detail some common use cases I encounter day to day, as well as some related tools that help me handle them.

### sed

During my regular work as a system administrator, I usually use **sed** (“**s**tream **ed**itor”) to do string replacement across files and **awk** for log files or file analysis with arbitrary strings as the input field separator using the -F flag.

One common use case for sed I've found is updating config files for the Icinga monitoring system. Let's say that we have a file named server101.cfg and we want to use the same config for server 102. One way to solve this on the command line is doing a simple search and replace with sed:

```console
$ cp server101.cfg server102.cfg
$ sed 's/server101/server102/g' server102.cfg
$ icinga -v /etc/icinga/icinga.cfg # This will check that Icinga is able to understand the newly copied file
```

Make sure you use diff or another similar tool to make sure this doesn't accidentally modify anything it's not supposed to. You can get more detailed with your regular expressions to avoid such issues, but that's beyond the scope of this post.

### awk

Sometimes I need to use awk for scripting, but most of the time, I use it for parsing things like IP addresses in log files, or any other string in logs. For example, you can check for plaintext passwords or credit card details in places they're not supposed to be.

The sed & awk book started with the introduction of ed, an ancient line editor. Then it touched on the field separator, which is represented by the `-F` flag.

In the following example, I ran the `blkid` command in order to check the UUID of the SCSI devices that connected to my computer, then used awk to only show the output I needed.

```console
$ sudo blkid /dev/sd{d,e,g}
/dev/sdd: UUID="7eb6302f-e727-4433-8c49-8a7842d18e1e" TYPE="crypto_LUKS"
/dev/sde: UUID="68b2382e-13b8-4bdb-a6cb-15f6844d464b" TYPE="crypto_LUKS"
/dev/sdg: UUID="7237cc7d-0483-4c2a-a503-a11ea88b3690" TYPE="crypto_LUKS"
```

```console
$ sudo blkid /dev/sd{d,e,g} | awk -F "\"" {'print $2'}
7eb6302f-e727-4433-8c49-8a7842d18e1e
68b2382e-13b8-4bdb-a6cb-15f6844d464b
7237cc7d-0483-4c2a-a503-a11ea88b3690
```

During my day-to-day work I seldom use both `sed` and `awk` together, but there are many situations where it can be useful to do so. See page 23 of the sed & awk book for one such example where both of these tools can be used together.


### Using regular expressions in \*NIX tools

The sed & awk book touches on regular expression syntax, since system administrators might have to use regular expressions in cases where large/​repetitive tasks are involved. I do not remember who suggested buying this pair of books, but I am really grateful for the person's suggestion.

To search a file using regular expressions, I use the program "grep." I often use the `-r` flag for recursive parsing, the `-w` flag to match whole words only, and the `--color=always` flag to colorize the terminal output. Recent versions of GNU grep use the `--color=auto` option by default so I don't have to explicitly specify it when sending output straight to a terminal. We can also use `--color=never` if we want to remove the color matching.

```console
$ grep 1 -w  --color=never tmp/file.txt
Mon Aug  1 11:30:01 AM +08 2022
Thu Sep  1 11:30:01 AM +08 2022
Sat Oct  1 11:30:01 AM +08 2022
Tue Nov  1 11:30:01 AM +08 2022
Thu Dec  1 11:30:01 AM +08 2022
Sun Jan  1 11:30:01 AM +08 2023
Wed Feb  1 11:30:01 AM +08 2023
Wed Mar  1 11:30:01 AM +08 2023
```

To extend the capability of grep for regular expression's usage, I used `-E`, but then I learned about the `-P` flag, which lets you use Perl-compatible regular expressions (PCREs), which I prefer.

Say I have a file named `fruit.txt` with the following contents:

```plain
apple banana orange
apple orange papaya
durian rambutan
starfruit
```

To find lines starting with "durian":

```console
$ grep -P '^durian' fruit.txt
durian rambutan
```

To find lines ending with "papaya":

```console
$ grep -P "papaya$" fruit.txt
apple orange papaya
```

To find lines with three words separated by two spaces:

```console
$ grep -P '\w+ \w+ \w+' fruit.txt
apple banana orange
apple orange papaya
```

To find all lines containing a word starting with "a" or "d":

```console
$ grep -P '\b(a|d)\w+' fruit.txt
apple banana orange
apple orange papaya
durian rambutan
```

These are just a few examples of what `grep` can do; it's very capable especially when you use PCREs.

Apart from sed, awk and grep, there are many other useful tools for text processing. Some that I commonly use are the sort and uniq programs.

### sort

sort and uniq are frequently used together. sort, as its name implies, is used to sort the parsed text per whatever options are provided.

Assume that we have the following file, "prices.csv":

```console
$ cat prices.csv
chicken,$1.50
duck,$1.20
beef,$6.10
chicken,$1.50
lamb,$3.20
fish,$4.09
```

Using the `sort` command, we could sort the items according a specified text separator (`-t`) and the column (key) that we want to prioritize (`-k`). Here, I want to sort the item based on data in the second column:

```console
$ sort -t "," -k 2 prices.csv
duck,$1.20
chicken,$1.50
chicken,$1.50
lamb,$3.20
fish,$4.09
beef,$6.10
```

Without the other parameters, sort will just sort the lines alphabetically.

```console
$ sort prices.csv
beef,$6.10
chicken,$1.50
chicken,$1.50
duck,$1.20
fish,$4.09
lamb,$3.20
```

We can use uniq to eliminate repeated lines. Running `uniq` without sorting will have no effect, since the duplicate lines `chicken,$1.50` do not appear sequentially:

```console
$ uniq prices.csv
chicken,$1.50
duck,$1.20
beef,$6.10
chicken,$1.50
lamb,$3.20
fish,$4.09
```

To merge them and clean up the data, we can sort first:

```console
$ sort prices.csv | uniq
beef,$6.10
chicken,$1.50
duck,$1.20
fish,$4.09
lamb,$3.20
```

### find

Say I want to search a full hard disk to check for files that are not needed anymore. I would use the following command, with each option detailed below the output:

```console
$ find . -maxdepth 1 -mtime +3000 -type d -exec ls {} -ld \;
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./Terminal
drwxrwxrwx  3 najmi najmi 4096 Dis  27  2012 ./gnome-disk-utility
drwxrwxrwx  8 najmi najmi 4096 Nov  27  2012 ./xfce4
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./libaccounts-glib
drwxrwxrwx  2 najmi najmi 4096 Dis   1  2012 ./sakura
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./software-center
drwxrwxrwx  4 najmi najmi 4096 Nov  25  2012 ./evolution
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./update-notifier
drwxrwxrwx  2 najmi najmi 4096 Dis  22  2012 ./Thunar
drwxrwxrwx  3 najmi najmi 4096 Nov  25  2012 ./compiz-1
drwxrwxrwx  2 najmi najmi 4096 Dis  28  2012 ./tracker
drwxrwxrwx  3 najmi najmi 4096 Dis   9  2012 ./menus
drwxrwxrwx  3 najmi najmi 4096 Dis  27  2012 ./gnome-control-center
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./goa-1.0
drwxrwxrwx  2 najmi najmi 4096 Nov  28  2012 ./enchant
drwxrwxrwx  2 najmi najmi 4096 Dis   8  2012 ./Pinta
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./gmusicbrowser
drwxrwxrwx  3 najmi najmi 4096 Dis  14  2012 ./audacious
drwxrwxrwx  3 najmi najmi 4096 Dis  27  2012 ./gnome-session
drwxrwxrwx  5 najmi najmi 4096 Nov  28  2012 ./mate
drwxrwxrwx  2 najmi najmi 4096 Nov  25  2012 ./ristretto
drwxrwxrwx 31 najmi najmi 4096 Dis  24  2012 ./chromium
drwxrwxrwx  5 najmi najmi 4096 Dis   8  2012 ./mono.addins
drwxrwxrwx  3 najmi najmi 4096 Nov  25  2012 ./mate-session
drwxrwxrwx  3 najmi najmi 4096 Nov  25  2012 ./ibus
drwxrwxrwx  4 najmi najmi 4096 Nov  25  2012 ./libreoffice
drwxrwxrwx  3 najmi najmi 4096 Nov  25  2012 ./caja
drwxrwxrwx  2 najmi najmi 4096 Dis  18  2012 ./Empathy
```

* In this case I search in the current directory with the dot `.` notation.
* The `-maxdepth 1` option means the search task must not be done beyond the current directory.
* `-mtime +3000` means only show directories that have not been modified within the last 3000 days.
* `-type d` means match directories, but not files (to only match files, use the `-type f` flag).
* The `-exec ls {} -ld \;` arguments mean it will run the `ls -ld` command for each match. This will show the modification time of the directory passed by the `{}` placeholder, which is replaced by the file name of the current search result.

> Note: In Linux with GNU tools it is possible to order the flags like either `ls {} -ld` or `ls -ld {}`, but I realized that in some other \*NIX variants, you always need to put the flag before the variable/parameter; that is, `ls -ld {}`.

### Conclusion

There are newer tools which may be provided by more recent Linux distros or BSD variants, but in this short write-up I wanted to stick to the basics which are useful to anyone using \*NIX. It is more than worth your time to learn these tools in detail.

> For further reading, I would also recommend "UNIX and Linux System Administration Handbook" by Nemeth, E., Snyder, G., Hein, T., Whaley, B., & Mackin, D. (2020).
