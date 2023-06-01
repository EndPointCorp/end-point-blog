The command line interface (CLI) commands/tools in the UNIX-alike (\*NIX) are the most priceless elements for system administrators. CLI allows the system administrator  (or in this writings, I will just use the sysadmin short form) to handle the \*NIX systems either remotely or locally without having the need to install the Graphical User Interface (GUI) packages.

Almost twenty years ago, I bought two O'Reilly books entitled "sed & awk - second edition," written by Dale Dougherty & Arnold Robbins, and "Mastering Regular Expressions," written by Jeffrey E.F. Friedl. These two books are used books that were printed in the late '90s (and I bought them in 2004). In this writing, when the page and book chapter are mentioned, it means that I am referring to the aforementioned books printed in that particular year. It's possible that newer editions have been updated with different chapters or page references. These two books explain in details on the previously mentioned topics. 

Why did I mention these books? This is because previously my co-workers and I had several hourly meetups over several weeks in order to learn (from surface to the details) Regular Expressions. So I remember that I actually have the related books inside my bookshelves which I have not touched for years. 

For the system administration task, usually I just use a simple one-liner. Perhaps it is not even a new thing for the reader, but just in case it is useful to someone else. Apart from that, I would also recommend "UNIX and Linux System Administration Handbook" ( Nemeth, E., Snyder, G., Hein, T., Whaley, B., & Mackin, D. (2020). UNIX and Linux System Administration Handbook (5th ed.). Prentice Hall. )

In this blogpost, I will write the common cases that I encountered from day to day task, together with related tools to handle it.

The authors mentioned in the book’s preface, it is a natural progression to learn grep to sed to awk. `sed,`,`awk` and `grep` are among the tools that are commonly being used by a system administrator.

### sed

During my day to day work as a system administrator, I usually deal with sed (stream editor) for string replacement across files and awk for the log file or file analysis with certain strings as the field separator (hence my favorite is the -F flag). 

The benefit of using sed by copying over the existing, working file is that we could reduce the likeliness of having typos, since we only need to replace several strings.

Use cases:
Updating Icinga’s monitoring file. Let’s say that we have a file name server101.cfg. Since most of the basic Icinga’s check is in this file we simply could use

```console
$ cp server101.cfg server102.cfg
sed ‘s/server101/server102/g’ server102.cfg
icinga -v /etc/icinga/icinga.cfg (this will check for Icinga would be able to understand the newly copied file)
```

### awk
Sometimes there are certain cases where I need to use awk for scripting. But most of the time, I will use awk for parsing IP addresses in the log file, or any other string in the log files (for example if there is any plaintext password in the log file, or any plain credit card details appeared anywhere in the place that it shouldn’t be).

The “sed & awk” book started with the introduction of `ed` - a line editor. Then it touched on the field separator, which is represented by the `-F` flag. 

In the following example, I ran the `blkid` command in order to check the UUID of the SCSI devices that connected to my computer.

Example:
```console
$ sudo blkid /dev/sd{d,e,g}
/dev/sdd: UUID="7eb6302f-e727-4433-8c49-8a7842d18e1e" TYPE="crypto_LUKS"
/dev/sde: UUID="68b2382e-13b8-4bdb-a6cb-15f6844d464b" TYPE="crypto_LUKS"
/dev/sdg: UUID="7237cc7d-0483-4c2a-a503-a11ea88b3690" TYPE="crypto_LUKS"
```

```console
$ sudo blkid /dev/sd{d,e,g}|awk -F "\"" {'print $2'}
7eb6302f-e727-4433-8c49-8a7842d18e1e
68b2382e-13b8-4bdb-a6cb-15f6844d464b
7237cc7d-0483-4c2a-a503-a11ea88b3690
```

During my day-to-day work I seldom use both `sed` and `awk` together. In page 23 of the “sed & awk book”  that I have, the authors showed an example where both of these tools are being used together. 


### Regular expression's usage in \*NIX tools

The sed & awk book touched on the “Understanding Regular Expression Syntax” - which means in some way, system administrator might have to use regular expressions in certain cases where large/repetitive tasks are involved. I do not remember who suggested buying this pair of books which I bought almost twenty years ago, but I am really grateful for the person’s suggestion. 

Previously I just used the `grep` command with `-rw` (for recursive parsing) as well as the `color=always` flag in order to colorize the terminal output. I guess the recent `grep` command already has the "color" option by default and I don't have to explicitly call it anymore. We can also use `--color=never` if we want to remove the color matching. 

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

In order to extend the capability of grep for regular expression's usage, I use `-E`, but then I got to know that we could use `-P` flag to, in order to use Perl-compatible regular expression's characters. 

Apart from the `sed`, `awk` and `grep`, there are other tools as well; tools that I usually use are the `sort` and `uniq` commands. 

### The `sort` command
`sort` and `uniq` are usually being used together, although not compulsory. `sort`, as its name explains, being used to sort the parsed text with the requirement that we put into it.

Assume that we have the following text:

```console
$ cat  pattern.txt 
chicken,$1.50
duck,$1.20
beef,$6.10
lamb,$3.20
fish,$4.09
```

By using the `sort` command we could sort the items according to the text seperator (`-`t) and the column that we want to prioritize (`-k`). Here, I want to sort the item based on data exist on the second column.

```console
$ sort -t"," -k2  pattern.txt 
duck,$1.20
chicken,$1.50
lamb,$3.20
fish,$4.09
beef,$6.10
```

Without the other parameters, `sort` will just use the first column to sort the data - in this case, alphabetically.

```console
$ sort pattern.txt 
beef,$6.10
chicken,$1.50
duck,$1.20
fish,$4.09
lamb,$3.20
```

### The `find` command.

Say I searched from a full hard disk and found several files which I could check whether they are still needed or not.
In this case I search in the the current path with the dot `.` notation, and the `maxdepth 1` means the search task must not be done beyond the current directory (path). `-mtime +3000` means only select the directory that not being modified within the last 3000 days.
`-type d` means directory and not files (files use `-type f` flag). For the `-exec` flag, it will run the `ls -ld` command which will display the value that being passed to the `{}` placeholder. 

```console
$ find . -maxdepth 1  -mtime +3000 -type d -exec ls {} -ld \;
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./Terminal
drwxrwxrwx 3 najmi najmi 4096 Dis  27  2012 ./gnome-disk-utility
drwxrwxrwx 8 najmi najmi 4096 Nov  27  2012 ./xfce4
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./libaccounts-glib
drwxrwxrwx 2 najmi najmi 4096 Dis   1  2012 ./sakura
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./software-center
drwxrwxrwx 4 najmi najmi 4096 Nov  25  2012 ./evolution
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./update-notifier
drwxrwxrwx 2 najmi najmi 4096 Dis  22  2012 ./Thunar
drwxrwxrwx 3 najmi najmi 4096 Nov  25  2012 ./compiz-1
drwxrwxrwx 2 najmi najmi 4096 Dis  28  2012 ./tracker
drwxrwxrwx 3 najmi najmi 4096 Dis   9  2012 ./menus
drwxrwxrwx 3 najmi najmi 4096 Dis  27  2012 ./gnome-control-center
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./goa-1.0
drwxrwxrwx 2 najmi najmi 4096 Nov  28  2012 ./enchant
drwxrwxrwx 2 najmi najmi 4096 Dis   8  2012 ./Pinta
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./gmusicbrowser
drwxrwxrwx 3 najmi najmi 4096 Dis  14  2012 ./audacious
drwxrwxrwx 3 najmi najmi 4096 Dis  27  2012 ./gnome-session
drwxrwxrwx 5 najmi najmi 4096 Nov  28  2012 ./mate
drwxrwxrwx 2 najmi najmi 4096 Nov  25  2012 ./ristretto
drwxrwxrwx 31 najmi najmi 4096 Dis  24  2012 ./chromium
drwxrwxrwx 5 najmi najmi 4096 Dis   8  2012 ./mono.addins
drwxrwxrwx 3 najmi najmi 4096 Nov  25  2012 ./mate-session
drwxrwxrwx 3 najmi najmi 4096 Nov  25  2012 ./ibus
drwxrwxrwx 4 najmi najmi 4096 Nov  25  2012 ./libreoffice
drwxrwxrwx 3 najmi najmi 4096 Nov  25  2012 ./caja
drwxrwxrwx 2 najmi najmi 4096 Dis  18  2012 ./Empathy
```
Note: In Linux it is possible to use `ls {} -ld` or `ls -ld {}` flag assignation, but I realized in some other \*NIX variant, you always need to put the flag before the variable/parameter, that is `ls -ld {}`. 

### Conclusion
There are other tools, which may recently being deployed/provided by the recent Linux distros or BSD variants, so I could not cover them in this short write up. But at least for the person will use/currently use \*NIX, your time will be worth learning more about these tools in detail.
