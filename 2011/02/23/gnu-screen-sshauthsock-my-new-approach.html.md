---
author: David Christensen
gh_issue_number: 414
tags: environment, sysadmin, tips, tools
title: GNU Screen + SSH_AUTH_SOCK; my new approach
---



Over the years, I’ve played around with several different methods of keeping my forwarded SSH-Agent authentication socket up-to-date in long-running screen sessions (referenced via the $SSH_AUTH_SOCK shell variable). The basic issue here is that Screen sees the process environment at the time it was initially launched, not that which exists when reattaching in a subsequent login session. This means that the $SSH_AUTH_SOCK variable as screen sees it will refer to a socket which no longer exists (as it was removed when you logged out after detaching on the initial login when starting screen).

Some of my previous methods have included a hard-coded variable for the socket itself (downsides: if it’s a predictable name you’re potentially opening some security issues, plus if you open multiple sessions to the same account, you kill the latest socket), symlinking the latest $SSH_AUTH_SOCK to a hard-coded value on login (similar issues), dumping $SSH_AUTH_SOCK to a file, and aliasing ssh and scp to first source said file to populate the local window’s enviroment (doesn’t work in scripts, too much manual setup when adapting to a new system/environment, won’t work with any other subsystem not already explicitly handled, etc).

Recently though, I’ve come up with a simple approach using screen’s -X option to execute a screen command outside of screen and just added the following to my .bashrc:

```bash
screen -X setenv SSH_AUTH_SOCK "$SSH_AUTH_SOCK"
```

While not perfect, in my opinion this is a bit of an improvement for the following reasons:

- It’s dirt-simple. No complicated scripts to adjust/maintain, just a command that’s almost completely self-explanatory.
- It doesn’t kill the environment for existing screen windows, just adjusts the $SSH_AUTH_SOCK variable for new screen windows. This ends up matching my workflow almost every time, as unless a connection dies, I leave the screen window open indeterminately.
- If you have multiple sessions open to the same account (even if not running both in screen), you’re not stomping on your existing socket.
- Did I mention it’s dirt-simple?

There are presumably a number of other environment variables that would be useful to propagate in this way. Any suggestions or alternate takes on this issue?


