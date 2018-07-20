---
author: Brian J. Miller
gh_issue_number: 344
tags: ssh
title: Long Lasting SSH Multiplexing Made Simplish
---



### My Digression

To start off digressing just a little, I am primarily a developer, lately on longer projects of relatively significant size which means that I stay logged in to the same system for weeks (so long as my X session, local connection, and remote server allow it). I’m also a big believer in lots of screen real estate and using it all when you have it, so I have two monitors running high resolutions (1920x1200), and I use anywhere from 4-6 virtual pages/desktops/screens/(insert term of preference here). On 2-3 of those spaces I generally keep 8 "little black screens" (as my wife likes to call them) or terminals open in 2 rows of 4 windows. In each of those terminals I stay logged in to the same system as long as those aforementioned outside sources will allow me. A little absurd I know...

If you are still with me you may be thinking "why don’t you just use `screen`?", I do, in each of those terminals for the inevitable times when network hiccups occur, etc. Next you’ll ask, "why don’t you just use separate tabs/windows/partitions/(whatever they are called) within screen?", I do, generally I have 2-3 (or more) in each screen instance set to multiple locations on the remote file system. In general I’ve just found being able to look across a row of terminals at various different libs, a database client, tailed logs, etc. is much faster than toggling between windows (heaven forbid they’d be minimized), screen pages, virtual desktops, or even shell job control (though I use a good bit of that too). Inevitably I also seem to pop up an additional window (or two) every now and again and ssh into the same remote destination for the occasional one off command (particularly since I’ve never quite gotten the SSH key thing figured out with long running screens, potential future blog post?). So the bottom line, for any given sizable project I probably ssh to the same location a minimum of 8 times each time I set up my desktop and over the course of a particular X session maybe 20 (or more) times? (End digression)

### The Point

As fast as SSHing is, waiting for a prompt when doing it that many times (particularly over the course of a year, or career) really starts to make the clock tick by (or at least it seems that way). Enter "multiplexing" which is essentially a wonderful feature in newer SSH that allows you to start one instance with a control channel that handles many of the slow parts (such as authentication) and so long as it is still running when you connect to the same remote location the new connection uses the existing control channel and is lightning fast getting you to the prompt. Simple enough, to turn on multiplexing you can add the following to your ~/.ssh/config:

```bash
# for multiplexing
ControlMaster auto
ControlPath ~/.ssh/multi/master-%r@%h:%p
```

The above indicates that a master should be used for each connection, and the location of where to store the master’s control socket file. The %r, %h, and %p are expanded to the login, host, and port respectively which is usually enough to make it unique. This should be enough to start using multiplexing, but...and you knew there had to be one...when the master’s control connection is lost all of the slaves to that connection lose their’s as well. With the occasional hung terminal window, or accidental closing of it (if you can remember which is master to begin with), etc. you quickly find that when you normally would not lose connection in a separate terminal window you all of a sudden have lost all of your connections (8+ in my case) which is really painful. Here is where the fun comes in, I use the "-n" and "-N" flags to SSH in a terminal window when I first load up an X session and background the process:

```bash
> ssh -Nn user@remote &
```

The above redirects stdin from /dev/null (a necessary evil when backgrounding SSH procs), prevents the execution of a remote command (meaning we don’t want a shell), and puts the new process in the local shell’s background. Unfortunately, and the part that took me the longest to figure out, is that SSH really likes to have a TTY around (we aren’t using the daemon after all) so simply killing the original terminal window will cause the SSH process to die and zap there went your control connection and all the little children. To get around this little snafu I follow the backgrounding of my SSH process with a bash specific built in disassociating it from the TTY:

```bash
> disown
```

Now I am free to close the original terminal window, the SSH process lives on in the background (as if it were a daemon) and keeps the control connection open so that whenever I use SSH to that remote location (or ‘scp’, etc.) I get an instant response.

### Other notes

I could probably set this up to occur when I start X initially automatically, but with a flaky connection I end up needing to do it a few times per X session anyways and you would have to watch out for the sequence of events making sure it occurred after any ssh-agent set up was required.

I tried using ‘nohup’ and can’t remember if I ran into an actual show stopper problem, or if I could just never quite get it to do what I wanted before I stumbled on bash’s disown.


