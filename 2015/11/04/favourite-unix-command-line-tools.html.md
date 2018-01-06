---
author: Ramkumar Kuppuchamy
gh_issue_number: 1174
tags: shell
title: Top 15 Best Unix Command Line Tools
---

Here are some of the Unix command line tools which we feel make our hands faster and lives easier. Let’s go through them in this post and make sure to leave a comment with your favourite!

### 1. Find the command that you are unaware of

In many situations we need to perform a command line operation but we might not know the right utility to run. The command (apropos) searches for the given keyword against its short description in the unix manual page and returns a list of commands that we may use to accomplish our need.

If you can not find the right utility, then Google is our friend :)

```bash
$ apropos "list dir"
$ man -k "find files"
```

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="188" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-0.png" width="640"/></a></div>

### 2. Fix typos in our commands

It’s normal to make typographical errors when we type so fast. Consider a situation where we need to run a command with a long list of arguments and when executing it returns “command not found” and you noticed that you have made a typo on the executed command.

Now, we really do not want to retype the long list of arguments, instead use the following to simply just correct the typo command and execute `^typo_cmd^correct_cmd`:

```bash
$ dc /tmp
$ ^dc^cd
```

The above will navigate to /tmp directory.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="182" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-1.png" width="640"/></a></div>

### 3. Bang and its Magic

Bang quite useful, when we want to play with the bash history commands. Bang helps by letting you execute commands in history easily when you need them:

- `!!` — Execute the last executed command in the bash history
- `!*` — Execute the command with all the arguments passed to the previous command
- `!ˆ` — Get the first argument of the last executed command in the bash history
- `!$` — Get the last argument of the last executed command in the bash history
- `!` — Execute a command which is in the specified number in bash history
- `!?keyword?` — Execute a command from bash history for the first pattern match of the specified keyword
- `!-N` — Execute the command that was Nth position from the last in bash history  

<br/>

```bash
$ ~/bin/lg-backup
 $ sudo !!
```

In the last part of the above example we didn’t realize that the lg-backup command had to be run with `sudo`. Now, Instead of typing the whole command again with sudo, we can just use `sudo !!` which will re-run the last executed command in bash history as sudo, which saves us lot of time.

### 4. Working with Incron

This incron configuration is almost like crontab setup, but the main difference is that incron monitors a directory for specific changes and triggers future actions as specified

```bash
Syntax: $directory $file_change_mask $command_or_action
```

```bash
/var/www/html/contents/ IN_CLOSE_WRITE,IN_CREATE,IN_DELETE /usr/bin/rsync –exclude ’*.tmp’ -a /home/ram/contents/ user@another_host:/home/ram/contents/
 /tmp IN_ALL_EVENTS logger "/tmp action for #file"
```

The above example shows triggering an rsync event whenever there is a change in `/var/www/html/contents` directory. In cases of immediate backup implementations this will be really helpful. Find more about incron [here](https://www.cyberciti.biz/faq/linux-inotify-examples-to-replicate-directories/).

### 5. Double dash

There are situations where we end up in creating/deleting the directories whose name start with a symbol. These directories can not be removed by just using `rm -rf` or `rmdir`. So we need to use the “double dash” (--) to perform deletion of such directories:

```bash
$ rm -rf -- $symbol_dir
```

There are situations where you may want to create a few directory that starts with a symbol. You can just these create directories using double dash(--) and starting the directory name with a symbol.

```bash
$ mkdir -- $symbol_dir
```

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="276" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-2.png" width="640"/></a></div>

### 6. Comma and Braces Operators

We can do lot with comma and braces to make our life easier when we are performing some operations, lets see few usages:

- Rename and backup operations with comma & braces operator
- Pattern matching with comma & braces operator
- Rename and backup (prefixing name) operations on long file names

To backup `httpd.conf` to `httpd.conf.bak`:

```bash
$ cp httpd.conf{,.bak}
```

To revert the file from `httpd.conf.bak` to `httpd.conf`:

```bash
$ mv http.conf{.bak,}
```

To rename the file with prefix “old”:

```bash
$ cp exampleFile old-!#ˆ
```

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-3-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="194" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-3.png" width="640"/></a></div>

### 7.  Read only vim

As we all know, vim is a powerful command line editor. We can also use vim to view files in read only mode if you want to stick to vim:

```bash
$ vim -R filename
```

We can also use the `view` tool which is nothing but read only vim:

```bash
$ view filename
```

### 8. Push and Pop Directories

Sometimes when we are working with various directories and looking at the logs and executing scripts we find alot of our time is spent navigating the directory structure. If you think your directory navigations resembles a stack structure then use push and pop utilities which will save you lots of time

- Push the directory using `pushd`
- List the stack directories using the command `dirs`
- Pop the directories using `popd`

<br/>
This is mainly used in navigating between directories:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-4-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="326" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-4.png" width="400"/></a></div>

### 9. Copy text from Linux terminal (stdin) to the system clipboard

Install xclip and create the below alias:

```bash
$ alias pbcopy=’xclip -selection clipboard’
$ alias pbpaste=’xclip -selection clipboard -o’
```

We need to have the X window system running it to work. In Mac OS X, these pbcopy and pbpaste commands are readily available to you.

To Copy:

```bash
$ ls | pbcopy
```

To Paste:

```bash
$ pbpaste > lstxt.txt
```

### 10. TimeMachine like Incremental Backups in Linux using rsync --link-dest

This means that it will not recopy all of the files every single time a backup is performed. Instead, only the files that have been newly created or modified since the last backup will be copied. Unchanged files are hard linked from prevbackup to the destination directory.

```bash
$ rsync -a –link-dest=prevbackup src dst
```

### 11. To display the ASCII art of the Process tree

Showing your processes in a tree structure is very useful for confirming the relationship between every process running on your system. Here is an option which is available by default on most of the Linux systems:

```bash
$ ps -aux –forest
```

`–forest` is an argument to `ps` command, which displays ASCII art of process tree:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-5-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="74" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-5.png" width="640"/></a></div>

<br/>

There are many commands available like `pstree` and `htop` to achieve the same thing.

### 12. Tree view of git commits

If you want to see git commits in a repo as tree view to understand the commit history better, the below option will be super helpful. This is available with the git installation and you do not need any additional packages.

```bash
$ git log –graph –oneline
```

### 13. Tee

Tee command is used to store and view (at the same time) the output of any other command.

(ie) At the same time it writes to the STDOUT, and to a file. It helps when you want to view the command output and at the time same time if you want to write it into a file or using pbcopy you can copy the output

```bash
$ crontab -l | tee crontab.backup.txt
```

The tee command is named after plumbing terminology for a T-shaped pipe splitter. This Unix command splits the output of a command, sending it to a file and to the terminal output. Thanks Jon for sharing this.

### 14. ncurses disk usage analyzer

Analysing disk usage with nurses interface, is fast and simple to use.

```bash
$ sudo apt-get install ncdu
```

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-6-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="313" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-6.png" width="400"/></a></div>

### 15. hollywood

You all have seen the hacking scene on hollywood movies. Yes, there is a package which will let you create that for you.

```bash
$ sudo apt-add-repository ppa:hollywood/ppa
$ sudo apt-get update
$ sudo apt-get install hollywood
```

```bash
$ hollywood
```

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/11/04/favourite-unix-command-line-tools/image-7-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="350" src="/blog/2015/11/04/favourite-unix-command-line-tools/image-7.png" width="640"/></a></div>
