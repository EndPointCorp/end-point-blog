---
author: Muhammad Najmi bin Ahmad Zabidi
gh_issue_number: 1320
tags: shell, linux
title: How to check process duration in Linux with the “ps” command
---

In certain cases we might want to get a certain process’ elapsed time for our own reason. Turns out “ps” command could easily assist us in that. According to “ps” manual, etime could put the duration of time in **[[DD-]hh:]mm:ss. format**, while etimes in seconds.

From “ps” manpage:

```bash
etime       ELAPSED   elapsed time since the process was started, in the form [[DD-]hh:]mm:ss.
etimes      ELAPSED   elapsed time since the process was started, in seconds.
```

To use that, we could use (in [[DD-]hh:]mm:ss. format):

```bash
ps -p "pid" -o etime
```
or in seconds:

```bash
ps -p "pid" -o etimes
```

In this case the “pid” should be replaced with your intended process ID.

The following will help to nicely reporting the output. We can put -o etime or -o etimes with other argument, that is “command”, in order to show the executed command along with its very own absolute path:

```bash
ps -p "28590" -o etime,command
```
```bash
ELAPSED COMMAND
21:45 /usr/bin/perl ./fastcgi-wrapper.pl 7999
```

We can also get the start date of the process’ execution:

```bash
najmi@ubuntu-ampang:~$ ps -p 21745 -o etime,command,start
    ELAPSED COMMAND                      STARTED
 1-19:47:45 /usr/lib/firefox/firefox      Aug 02
```

What if we do not want to manually parsing the PID, instead (since we are very sure) to just get the name of the running application? We could just simply use **pgrep** or **pidof**

```bash
najmi@ubuntu-ampang:~$ ps -p $(pgrep firefox) -o pid,cmd,start,etime
  PID CMD                          STARTED     ELAPSED
21745 /usr/lib/firefox/firefox      Aug 02  2-04:29:36
```

```bash
najmi@ubuntu-ampang:~$ ps -p $(pidof firefox) -o pid,cmd,start,etime
  PID CMD                          STARTED     ELAPSED
21745 /usr/lib/firefox/firefox      Aug 02  2-04:29:42
```

What if the command issued many processes? Take an example of the Chrome browser:

```bash
najmi@ubuntu-ampang:~$ ps -p $(pidof chrome) -o pid,comm,cmd,start,etime
error: process ID list syntax error

Usage:
 ps [options]

 Try 'ps --help <simple|list|output|threads|misc|all>'
  or 'ps --help <s|l|o|t|m|a>'
 for additional help text.

For more details see ps(1).
</s|l|o|t|m|a></simple|list|output|threads|misc|all>
```

The best way (so far) that I could get is by creating a loop. It seems **pidof** is much more accurate when parsing the exact application (string) that we feed into it.

With **pgrep**:

```bash
najmi@ubuntu-ampang:~$ for i in `pgrep chrome`;do ps -p $i -o pid,comm,cmd,start,etime|tail -n +2;done
 2255 chrome          /opt/google/chrome/chrome - 08:05:43    02:55:17
 4990 chrome          /opt/google/chrome/chrome - 10:39:16       21:44
 5567 chrome          /opt/google/chrome/chrome - 10:53:13       07:47
 9448 chrome          /opt/google/chrome/chrome -   Jul 31  3-12:25:08
10033 chrome          /opt/google/chrome/chrome     Jul 27  8-10:43:42
10044 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:43:42
10050 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:43:42
10187 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:43:39
10234 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:43:37
10236 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:43:37
19440 chrome          /opt/google/chrome/chrome - 22:30:34    12:30:26
20229 chrome          /opt/google/chrome/chrome -   Aug 03  1-09:51:25
20514 chrome          /opt/google/chrome/chrome - 22:52:25    12:08:35
20547 chrome          /opt/google/chrome/chrome - 22:52:36    12:08:24
21009 chrome          /opt/google/chrome/chrome -   Aug 03  1-09:27:11
22458 chrome          /opt/google/chrome/chrome -   Jul 27  8-03:44:07
22474 chrome-gnome-sh /usr/bin/python3 /usr/bin/c   Jul 27  8-03:44:07
23681 chrome          /opt/google/chrome/chrome -   Aug 03  1-03:33:45
23691 chrome          /opt/google/chrome/chrome -   Aug 03  1-03:33:45
23870 chrome          /opt/google/chrome/chrome - 00:15:15    10:45:45
24544 chrome          /opt/google/chrome/chrome - 00:40:17    10:20:43
25116 chrome          /opt/google/chrome/chrome - 00:51:31    10:09:29
25466 chrome          /opt/google/chrome/chrome - 00:59:55    10:01:05
29060 chrome          /opt/google/chrome/chrome - 02:15:42    08:45:18
```
With **pidof**:

```bash
najmi@ubuntu-ampang:~$ for i in `pidof chrome`;do ps -p $i -o pid,comm,cmd,start,etime|tail -n +2;done
29060 chrome          /opt/google/chrome/chrome - 02:15:42    08:47:40
25466 chrome          /opt/google/chrome/chrome - 00:59:55    10:03:27
25116 chrome          /opt/google/chrome/chrome - 00:51:31    10:11:51
24544 chrome          /opt/google/chrome/chrome - 00:40:17    10:23:05
23870 chrome          /opt/google/chrome/chrome - 00:15:15    10:48:07
23691 chrome          /opt/google/chrome/chrome -   Aug 03  1-03:36:07
23681 chrome          /opt/google/chrome/chrome -   Aug 03  1-03:36:07
22458 chrome          /opt/google/chrome/chrome -   Jul 27  8-03:46:29
21009 chrome          /opt/google/chrome/chrome -   Aug 03  1-09:29:33
20547 chrome          /opt/google/chrome/chrome - 22:52:36    12:10:46
20514 chrome          /opt/google/chrome/chrome - 22:52:25    12:10:57
20229 chrome          /opt/google/chrome/chrome -   Aug 03  1-09:53:47
19440 chrome          /opt/google/chrome/chrome - 22:30:34    12:32:48
10236 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:45:59
10234 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:45:59
10187 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:46:01
10050 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:46:04
10044 chrome          /opt/google/chrome/chrome -   Jul 27  8-10:46:04
10033 chrome          /opt/google/chrome/chrome     Jul 27  8-10:46:04
 9448 chrome          /opt/google/chrome/chrome -   Jul 31  3-12:27:30
 5567 chrome          /opt/google/chrome/chrome - 10:53:13       10:09
 4990 chrome          /opt/google/chrome/chrome - 10:39:16       24:06
 2255 chrome          /opt/google/chrome/chrome - 08:05:43    02:57:39
```

There is other tool, called as **stat** which records the timestamp of a file but for slightly different purpose. Stay tuned for the next blogpost!
