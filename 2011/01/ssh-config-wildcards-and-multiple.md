---
author: Greg Sabino Mullane
title: SSH config wildcards and multiple Postgres servers per client
github_issue_number: 394
tags:
- clients
- linux
- postgres
- ssh
- sysadmin
- tips
date: 2011-01-07
---



The SSH config file has some nice features that help me to keep my sanity among a wide variety of servers spread across many different clients. Nearly all of my Postgres work is done by using SSH to connect to remote client sites, so the ability to connect to the various servers easily and intuitively is important. I’ll go over an example of how a ssh config file might progress as you deal with an ever‑expanding client.

Some quick background: the ssh config file is a per‑user configuration file for [the SSH program](https://www.openssh.com/). It typically exists as **~/.ssh/config**. It has two main purposes: setting global configuration items (such as ForwardX11 no), and setting things on a host‑by‑host basis. We’ll be focusing on the latter.

Inside the ssh config file, you can create **Host** sections which specify options that apply only to one or more matching hosts. The sections are applied if the host name you type in as the argument to the ssh command matches what is after the word “Host”. As we’ll see, this also allows for wildcards, which can be very useful.

I’m going to walk through a hypothetical client, Acme Corporation, and show how the ssh config can grow as the client does, until the final example mirrors an actual section of my ssh config section file.

So, you’ve just got a new Postgres client called Acme Corporation, and they are using Amazon Web Services (AWS) to host their server. We’re coming in as the postgres user, and have our public ssh keys already in place inside **~postgres/.ssh/authorized_keys** on their server. The hostname is **ec2‑456‑55‑123‑45.compute‑1.amazonaws.com**. So, generally, we would connect by running:

```bash
$ ssh postgres@ec2‑456‑55‑123‑45.compute‑1.amazonaws.com
```

That’s a lot to type each time! We could create a bash alias to handle this, but it’s better to use the ssh config file instead. We’ll add this to the end of our ssh config:

```nohighlight
##
## Client: Acme Corporation
##

Host  acmecorp
User postgres
Hostname  ec2-456-55-123-45.compute-1.amazonaws.com
```

Now we can simply use ‘acmecorp’ in place of that ugly string:

```bash
$ ssh acmecorp
```

Notice that we don’t need to specify the user anymore: ssh config plugs that in for us. We can still override it if we need to connect as someone else:

```bash
$ ssh greg@acmecorp
```

The next week, Acme Corporation decides that rather than allow anyone to SSH to their servers, they will use iptables or something similar to restrict access to select known hosts. Because different people with different IPs at End Point may need to access Acme, and because we don’t want to have Acme have to open a new hole each time we connect from a different place, we will connect from a shared company box. In this case, the box is **vp.endpoint.com**. Acme arranges to allow SSH from that box to their servers, and each End Point employee has a login on the vp.endpoint.com box. What we need to do now is create a SSH tunnel. Inside of the ssh config file, we add a new line to the entry for ‘acmecorp’:

```nohighlight
Host  acmecorp
User  postgres
Hostname  ec2-456-55-123-45.compute-1.amazonaws.com
ProxyCommand  ssh -q greg@vp.endpoint.com nc -w 180 %h %p
```

Now, when we run this:

```bash
$ ssh acmecorp
```

...everything looks the same to us, but what we are really doing is connecting to vp.endpoint.com, running the nc (netcat) command, and then connecting to the amazonaws.com box over the new netcat connection. (The arguments to netcat specify that the connection should be closed if there is the connection goes away for 180 seconds, and the host and port should be echoed along). As far as amazonaws.com is concerned, we are connecting from vp.endpoint.com. As far as *we* are concerned, we are going directly to amazonaws.com. A nice side effect, and a big reason why we don’t simply use bash aliases, is that the **scp** program will use these aliases as well. So we can now do something like this:

```bash
$ scp check_postgres.pl acmecorp:
```

This will copy the [check_postgres.pl program](https://bucardo.org/check_postgres/) from our computer to the Acme one, going through the tunnel at vp.endpoint.com.

Business has been good for Acme lately and they finally have conceded to your strong suggestion to set up a warm standby server (using [Postgres’ Point In Time Recovery system](https://www.postgresql.org/docs/current/static/continuous-archiving.html)). This new server is located at **ec2‑456‑55‑123‑99.compute‑1.amazonaws.com**, and the internal host name they give it is **maindb‑replica** (the original box is known as **maindb‑db**). This new server requires another host entry to ssh config. Rather than copy over the same ProxyCommand, we’ll refactor the information out into a separate host entry. What we end up with is this:

```nohighlight
Host  acmetunnel
User  greg
Hostname  vp.endpoint.com

Host  acmedb
User  postgres
Hostname  ec2-456-55-123-45.compute-1.amazonaws.com
ProxyCommand  ssh -q acmetunnel nc -w 180 %h %p

Host  acmereplica
User  postgres
Hostname  ec2-456-55-123-99.compute-1.amazonaws.com
ProxyCommand  ssh -q acmetunnel nc -w 180 %h %p
```

We also changed the name from acmecorp to just “acme” as that’s enough to uniquely identify among our clients, and who wants to type more than they have to?

Next, the company adds a QA box they want End Point to help setup. This box, however, is *not* reachable from outside their network; it can be reached only from other hosts in their network. Luckily, we already have access to some of those. What we’ll do is extend our tunnel by one more host, so that the path we travel from us to the Acme QA box is:

**Local box → vp.endpoint.com → acreplica → acqa**

Here’s the section of the ssh config after we’ve added in the QA box:

```nohighlight
Host  acmetunnel
User  greg
Hostname  vp.endpoint.com

Host  acmedb
User  postgres
Hostname  ec2-456-55-123-45.compute-1.amazonaws.com
ProxyCommand  ssh -q acmetunnel nc -w 180 %h %p

Host  acmereplica
User  postgres
Hostname  ec2-456-55-123-99.compute-1.amazonaws.com
ProxyCommand  ssh -q acmetunnel nc -w 180 %h %p

Host  acmeqa
User  postgres
Hostname  qa
ProxyCommand  ssh -q acreplica nc -w 180 %h %p
```

Note that we don’t need the full hostname at this point for the “acmeqa” Hostname, as we can simply say ‘qa’ and the acreplica box knows how to get there.

There is still some unwanted repetition in the file, so let’s take advantage of the fact that the “Host” item inside the ssh config file will take wildcards as well. It’s not really apparent until you use wildcards, but a ssh host can match more than one “Host” section in the ssh config file, and thus you can achieve a form of inheritance. (However, once something has been set, it cannot be changed, so you always want to set the more specific items first). Here’s what the file looks like after adding a wildcard section:

```nohighlight
Host  acme*
User  postgres
ProxyCommand  ssh -q greg@vp.endpoint.com nc -w 180 %h %p

Host  acmedb
Hostname  ec2-456-55-123-45.compute-1.amazonaws.com

Host  acmereplica
Hostname  ec2-456-55-123-99.compute-1.amazonaws.com

Host  acmeqa
User  root
Hostname  qa
ProxyCommand  ssh -q acreplica nc -w 180 %h %p
```

Notice that the file is now simplified quite a bit. If we run this command:

```bash
$ ssh acmereplica
```

...then the **Host acme*** section sets up both the **User** and the **ProxyCommand**. It then also matches on the **Host acmereplica** section and applies the **Hostname** there.

Note that we have removed the “acmetunnel” section. Now that all the ProxyCommands are in a single place, we can simply go back to the original ProxyCommand and specify the exact user and host.

All of the above presumes we want to login as the postgres user, but there are also times when we need to login as a different user (e.g. ‘root’). We can again use wildcards, this time to match the *end* of the host, to specify which user we want. Anything ending in the letter **“r”** means we log in as user root, and anything ending in the letter **“p”** means we log in as user postgres. Our final ssh config section for Acme is now:

```nohighlight
##
## Client: Acme Corporation
##

Host  acme*
ProxyCommand  ssh -q greg@vp.endpoint.com nc -w 180 %h %p
Host  acme*r
User  root
Host  acme*p
User  postgres

Host  acmedb*
Hostname  ec2-456-55-123-45.compute-1.amazonaws.com

Host  acmereplica*
Hostname  ec2-456-55-123-99.compute-1.amazonaws.com

Host  acmeqa*
Hostname  qa
ProxyCommand  ssh -q acreplica nc -w 180 %h %p
```

From this point on, if Acme decides to add a new server, adding it into our ssh config is as simple as adding two lines:

```nohighlight
Host  acmedev*
Hostname  ec2-456-55-999-45.compute-1.amazonaws.com
```

This automatically sets up two hosts for us, **“acmedevr”** and **“acmedevp”**. What if we leave out the ending “r” or “p” and just ssh to **“acmedev”**? Then we’ll connect as the default user, or **$ENV{USER}** (in my case, “greg”).

Have fun configuring your ssh config file, don’t be afraid to leave lots of comments inside of it, and of course keep it in version control!


