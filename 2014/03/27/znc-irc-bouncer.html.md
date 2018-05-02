---
author: Greg Davidson
gh_issue_number: 953
tags: tips, tools
title: 'ZNC: An IRC Bouncer'
---



### Kickin’ it Old Skool

At End Point, we use IRC extensively for group chat and messaging. Prior to starting here I had been an occasional IRC user—asking questions about various open source projects on [Freenode](http://freenode.net/) and helping others as well. When I began to use IRC daily, I ran into a few things that bugged me and thought I would write about what I have done to mitigate those. While it might not be as fancy as [Campfire](https://campfirenow.com/), [HipChat](https://www.hipchat.com/) or [Slack](https://slack.com/) I’m happy with my setup now.

### What did I miss?

The first thing that annoyed me about IRC was the lack of *persistence*. If I wasn’t logged on to the server, I missed out on the action. This was exacerbated by the fact that I live in the Pacific Time zone and lots of discussion takes place before my work day begins. Some people on our team solve this issue by running a terminal-based IRC client (like [irssi](https://irssi.org/) or [WeeChat](https://weechat.org/) inside a tmux or GNU Screen session on a remote server. This approach works well until the server needs to be rebooted (e.g. for OS or kernel updates etc.). It also introduces the limitation of using a terminal-based client which isn’t for everyone.

### Test Driving IRC Clients

The next challenge was finding a good IRC client. In my attempt to test-drive several clients side-by-side I quickly discovered that each client with a direct connection to the server requires its own unique nick (e.g. greg, greg_, greg_2 etc.). I also wanted to be able to use an IRC client on my phone without having to use multiple nicks. At this point I did a little research and determined that a bouncer might be helpful.

### Enter the Bouncer

A bouncer connects to an IRC server on your behalf and maintains a persistent connection. Rather than connecting directly to IRC server you connect to the bouncer. This allows you to remain connected to IRC while you are offline.

<img alt="Bouncers" border="0" height="389" src="/blog/2014/03/27/znc-irc-bouncer/image-0.png" title="bouncers.png" width="609"/>

[ZNC](https://wiki.znc.in/ZNC) is the bouncer software I have been using and it has been great. Using ZNC allows you to connect multiple clients at the same time. E.g. a phone and laptop using a single nick. ZNC also maintains a buffer of the most recent conversations while your clients are not connected. The buffer can be configured to suit your needs (per-channel, per-server etc.). In my case it’s buffering the past 100 messages and when I connect my IRC client they are automatically played back and the buffer is cleared. This has solved my issue with missing discussions and context when my IRC client isn’t running.

### IRC to go

Another benefit of this setup has been the ability to connect to IRC on my phone (with the same nick as my laptop). I have used Mobile Colloquy and Palaver on iOS and both work quite well. There are also ZNC modules on GitHub that enable ZNC to send push notifications for mentions and private messages. Mobile Colloquy does a good job of this—I have not yet tried this with Palaver yet.

### Modules

ZNC comes with a number of built in modules and allows users to develop their own as well (Perl, C++, Python or Tcl). The following are some of the ones I use:

- chansaver: keeps you connected to all of the channels you’ve joined
- simple_away: update your away message when all of your clients have disconnected / detached
- autoreply
- log: logs all discussions
- web admin: web interface for viewing and editing your ZNC config

### Running ZNC

ZNC is easy to compile and install and there are also packages available for some Linux distros. After testing it out locally for a while I installed it on a small VPS and that has been working well. [Digital Ocean](https://digitalocean.com/) has published an article on [how to install ZNC on a Ubuntu VPS](https://www.digitalocean.com/community/articles/how-to-install-znc-an-irc-bouncer-on-an-ubuntu-vps) if you are interested in learning more about it. Also, the [ZNC wiki](http://wiki.znc.in/ZNC) has lots of helpful information on how to install and configure ZNC.


