---
author: Greg Sabino Mullane
title: SSH ProxyCommand with netcat and socat
github_issue_number: 790
tags:
- networking
- ssh
- sysadmin
date: 2013-04-24
---

<a href="/blog/2013/04/socat-and-netcat-proxycommand-ssh/image-0-big.jpeg" imageanchor="1"><img border="0" src="/blog/2013/04/socat-and-netcat-proxycommand-ssh/image-0.jpeg"/></a>

[Picture](https://www.flickr.com/photos/tambako/5880777651/) by [Tambako the Jaguar](https://www.flickr.com/photos/tambako/)

Most of my day to day is work is conducted via a terminal, using 
[Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell) 
(SSH) to connect to various servers. I make extensive use of the local SSH
configuration file, **~/.ssh/config** file, both to reduce typing by aliasing connections,
and to allow me to seamlessly connect to servers, even when a direct connection
is not possible, by use of the **ProxyCommand** option.

There are many servers I work on that cannot be directly reached, and this is
where the ProxyCommand option really comes to the rescue. It allows you to
chain two or more servers, such that your SSH connections bounce through the
servers to get to the one that you need. For example, some of our clients only allow
SSH connections from specific IPs. Rather than worry about which engineers need to connect, and
what IPs they may have at the moment, engineers can access servers through certain 
trusted shell servers. Then our engineers can SSH to one of those servers, and from
there on to the client’s servers. As one does not want to actually SSH twice every time a
connection is needed, the ProxyCommand option allows a quick tunnel to be created. Here’s
an example entry for a `.ssh/config` file:

```nohighlight
Host proxy
User greg
HostName proxy.example.com

Host acme
User gmullane
HostName pgdev.acme.com
ProxyCommand ssh -q proxy nc -w 180 %h %p
```

So now when we run the command **ssh acme**, ssh actually first logs into proxy.example.com
 as the user “greg”, runs the nc (netcat) command (after plugging in the host and port parameters for us),
and then logs in to gmullane@pgdev.acme.com from proxy.example.com. We don’t see any of this
happening: one simply types “ssh acme” and gets a prompt on the pgdev.acme.com server.

Often times more than one “jump” is needed, but it is easy to chain servers together,
such that you can log into a third server by running two ProxyCommands. Recently,
this situation arose but with a further wrinkle. There was a server, we’ll call
it **calamity.acme.com**, which was not directly reachable via SSH from the outside world, as
it was a tightly locked down production box. However, it was reachable by other boxes
within the company’s intranet, including pgdev.acme.com. Thus to login as gmullane
on the calamity server, the .ssh/config file would normally look like this:

```nohighlight
Host proxy
User greg
HostName proxy.example.com

Host acme
User gmullane
HostName pgdev.acme.com
ProxyCommand ssh -q proxy nc -w 180 %h %p

Host acme_calamity
User gmullane
## This is calamity.acme.com, but pgdev.acme.com cannot resolve that, so we use the IP
HostName 192.168.7.113
ProxyCommand ssh -q acme nc -w 180 %h %p
```

Thus, we’d expect to run **ssh acme_calamity** and get a prompt on the calamity box.
However, this was not the case. Although I was able to ssh from proxy to acme,
and then from acme to calamity, things were failing because acme did not have the nc (netcat)
program installed. Further investigation showed that it was not even available
via packaging, which surprised me a bit as netcat is a pretty old, standard,
and stable program. However, a quick check showed that the
[socat program](http://www.dest-unreach.org/socat/doc/socat.html) was available, so I installed that instead.
The socat program is similar to netcat, but much more advanced. I did not need
any advanced functionality, however, just a simple bidirectional pipe which
the SSH connections could flow over. The new entry in the config file thus
became:

```nohighlight
Host acme_calamity
User gmullane
HostName 192.168.13.123
ProxyCommand ssh -q acme socat STDIN TCP:%h:%p
```

After that, everything worked as expected. It’s perfectly fine to mix socat and
netcat as we’ve done here; at the end of the day, they are simple dumb pipes
(although socat allows them to be not so simple or dumb if desired!). The arguments
to socat are simply the two sides of the pipe. One is stdin (sometimes written as
stdio or a single dash), and the other is a TCP connection to a specific host
and port (which SSH will plug in). You may also see it written as TCP4, which
simply forces IPv4 only, where TCP encompasses IPv6 as well.

The options to netcat are very similar, but shorter as it already defaults to
using stdin for the one side, and because it defaults to a TCP connection,
so we can leave that out as well. The “-w 180” simply establishes a three minute
timeout so the connection will close itself on a problem rather than hanging out
until manually killed.

Even if both netcat and socat were not available, there are other solutions.
In addition to other programs, it is easy enough to write a quick Perl script
to create your own bidirectional pipe!
