---
author: Greg Davidson
gh_issue_number: 734
tags: linux, screen, tips, tmux
title: Update Your (Gnu) Screen Config on the Fly
---



## An Indispensable Tool

I use [Screen](http://www.gnu.org/software/screen/) constantly in my work at End Point. It is an indispensable tool that I would not want to operate without. It's so handy to resume where I left off after I've detached or when my connection drops unexpectedly. This is likely preaching to the choir but if you are not already using [Screen](http://www.gnu.org/software/screen/) and/or [tmux](http://tmux.sourceforge.net/), start now.

 

## The Scenario

I often find myself in the following situation: 

1. SSH into a server
1. Fire up a new Screen session
1. Create several windows for editing files, tailing logs etc
1. Realize the default Screen configuration is inadequate or does not exist.
1. Facepalm \O/

While my needs are fairly minimal, I do like to bump up the scrollback buffer and display the list of windows in the status line.

<img alt="Screen example" border="0" height="470" src="/blog/2012/12/14/update-your-gnu-screen-config-on-fly/image-0.png" title="screen-example.png" width="563"/> 

There are a couple of options at this point. I could put up with the default / non-existent configuration or create a config file and manually re-create the session and all of the windows to pick up the configuration changes. Neither of these options was desirable. I wanted to be able to update the configuration and have **all** of the **existing windows** pick up the changes. After asking around a little I ended up taking a look at [the manual](http://www.gnu.org/software/screen/manual/) and discovered the `source` command.  

## Use the source (command)

The source command can be used to load or reload a Screen configuration file. It can be invoked from inside a Screen session like so: 

```
C-a :source /absolute/path/to/config_file
```

It is important to note that you must use the absolute path to the config file. There are exceptions which can be found in the Screen man pages but I found it easier to just use the absolute path. Once the source command has been issued, the configuration will be applied to **all** existing windows! This was exactly what I was looking for. Armed with this information I copied my local .screenrc to the system clipboard, created a new config file on server and applied it to my session using the `source` command.

## Works with tmux too

I like to use [tmux](http://tmux.sourceforge.net/) as well and was happy to [find](http://www.openbsd.org/cgi-bin/man.cgi?query=tmux&sektion=1) it had a similar feature. The source-file command (`source` is aliased as well) is invoked in the exactly the same way: 

```
C-prefix :source /absolute/path/to/config_file
```

After issuing the source-file command, all of the windows and panes in the current session will pick up the configuration changes.

## Changing the Default Directory

Another related issue I often run into is wishing I had started my Screen or tmux session in a different directory. By default, when you start a Screen or tmux session, all new windows (and panes) will be opened from the same directory where Screen or tmux was invoked. However, this directory can be changed for existing sessions.

For Screen, the chdir command can be used: 

```
C-a :chdir /some/new/directory
```

In tmux, the default-path command can be used: 

```
C-prefix :default-path /some/new/directory
```

After issuing the chdir or default-path commands, all new windows and panes will be opened from the specified directory.

I hope this has been helpful — feel free add your own Screen and tmux tips in the comments!


