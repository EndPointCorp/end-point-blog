---
author: Josh Williams
gh_issue_number: 948
tags: ssh, sysadmin
title: Scripting ssh master connections
---

<a href="http://www.flickr.com/photos/pennstatelive/4947288981/" title="Elephant Parade 005 by pennstatenews, on Flickr"><img alt="Elephant Parade 005" height="138" src="/blog/2014/03/17/scripting-ssh-master-connections/image-0.jpeg" width="240"/></a>

At End Point, security is a top priority. We just phased out the last of the 1024-bit keys for all of our employees—​those of us in ops roles that have keys lots of places had done so a long while back. Similarly, since we’ll tend to have several sessions open for a long while, a number of us will use ssh-agent’s -c (confirm) option. That forces a prompt for confirmation of each request the agent gets. It can get a little annoying (especially since it takes the focus over to one monitor, even if I’m working on the other) but it combats SSH socket hijacking when we have the agent forwarded to remote servers.

Working on server migrations is where it gets really annoying. I like to write little repeatable scripts that I can tweak and re-run as needed. They’re usually simple little things, starting with a bunch of rsync’s or pipe-over-ssh’s for pg_dump or any other data we need to move across. With any more than a couple of those ssh connections in there, repeatedly hitting the confirm button gets irritating fast. And if a large transfer takes a while, I’ll go off to do something else, later getting an unexpected confirmation box when I’m not thinking about the running script. Unexpected SSH auth confirmations, of course, get denied. So the script has to be re-run, and the vicious cycle repeats anew.

ssh has a neat ability to multiplex over a single connection. I have it set to do that locally in auto mode, and that made me wonder if it could be used in these scripts so I only have to authorize the connection once. Well, of course it can, and it turns out to be nothing special. But here’s what I got to work:

```
ssh
    -o ControlPath=~/.ssh/user@server.domain.foo  <em># Set the socket location</em>
    -M  <em># Defines master mode for the client</em>
    -N  <em># Don't bother to do anything remotely yet</em>
    -f  <em># Drop into the background so we can continue on</em>
    user@server.domain.foo  <em># And the typical connection username/host</em>
```

At the end of the script, remember to shut down the control socket by passing it an exit command, otherwise it’ll leave a connection hanging around out there:

```
ssh -o ControlPath=~/.ssh/user@server.domain.foo -O exit user@server.domain.foo
```

In between, it’s just a matter of using the ControlPath option. It can get a little repetitive, so a variable can be helpful. The latest iteration I have wraps the ssh command together with its -o ControlPath option, which can be executed directly or passed to rsync, as below.

As an example, here’s a somewhat stripped-down version of the script we used to move [bucardo.org](https://bucardo.org) to a new host, minus some error handling and such:

```
#!/bin/bash

MSSH="ssh -o ControlPath=~/.ssh/root@bucardo.org" 
$MSSH -MNf bucardo.org

# Tell rsync to use ssh pointed at the master socket
rsync -e "$MSSH" -aHAX --del bucardo.org:/var/lib/git/ /var/lib/git/

# Pipe pg_dump (or whatever you need) over ssh
$MSSH bucardo.org 'su - postgres -c "pg_dump -c wikidb"' | su - postgres -c "psql wikidb"

# sed -i commands or anything else that's needed to fix up the local configuration

$MSSH -O exit bucardo.org
```
