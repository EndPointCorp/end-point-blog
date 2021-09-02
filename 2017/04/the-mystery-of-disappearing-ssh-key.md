---
author: Greg Sabino Mullane
title: The mystery of the disappearing SSH key
github_issue_number: 1300
tags:
- security
- ssh
date: 2017-04-13
---

<div class="separator" style="clear: both; float: right; text-align: center; padding: 0 0 2em 1em"><a href="/blog/2017/04/the-mystery-of-disappearing-ssh-key/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2017/04/the-mystery-of-disappearing-ssh-key/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/SnZgVF">Photo</a> by <a href="https://www.flickr.com/photos/50663863@N02/">Jay Huang</a></small></div>

SSH ([Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell)) is one of the programs I use every single day at [work](/), primarily to connect
to our client’s servers. Usually it is a rock-solid program that simply
works as expected, but recently I discovered it behaving quite strangely -
a server I had visited many times before was now refusing my attempts
to login. The underlying problem turned out to be a misguided decision by the developers
of [OpenSSH](https://www.openssh.com/) to deprecate [DSA](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm) keys. How I discovered this problem is described below
(as well as two solutions).

The use of the ssh program is not simply limited to logging in and connecting
to remote servers. It also supports many powerful features, one of the most
important being the ability to chain multiple connections with the
ProxyCommand option. By using this, you can “login” to servers
that you cannot reach directly, by linking together two or more servers behind the scenes.

As as example, let’s consider a client named “Acme Anvils” that strictly
controls access to its production servers. They make all SSH traffic
come in through a single server, named dmz.acme-anvils.com, and only on port 2222.
They also only allow certain public IPs to connect to this server, via whitelisting.
On our side, End Point has a server, named portal.endpoint.com, that I can use as a jumping off point,
which has a fixed IP that we can give to our clients to whitelist.
Rather than logging in to “portal”, getting a prompt, and then logging in to “dmz”, I can
simply add an entry in my ~/.ssh/config file to automatically create a tunnel between
the servers -
at which point I can reach the client’s server by typing “ssh acmedmz”:

```text
##
## Client: ACME ANVILS
##

## Acme Anvil's DMZ server (dmz.acme-anvils.com)
Host acmedmz
User endpoint
HostName 555.123.45.67
Port 2222
ProxyCommand ssh -q greg@portal.endpoint.com nc -w 180s %h %p
```

Notice that the “Host” name may be set to anything you want. The connection
to the client’s server uses a non-standard port, and the username
changes from “greg” to “endpoint”, but all of that is hidden away from
me as now the login is simply:

```text
[greg@localhost]$ ssh acmedmz
[endpoint@dmz]$
```

It’s unusual that I’ll actually need to do any work on the dmz server, of course,
so the tunnel gets extended another hop to the db1.acme-anvils.com server:

```text
##
## Client: ACME ANVILS
##

## Acme Anvil's DMZ server (dmz.acme-anvils.com)
Host acmedmz
User endpoint
HostName 555.123.45.67
Port 2222
ProxyCommand ssh -q greg@portal.endpoint.com nc -w 180s %h %p

## Acme Anvil's main database (db1.acme-anvils.com)
Host acmedb1
User postgres
HostName db1
ProxyCommand ssh -q acmedmz nc -w 180s %h %p

```

Notice how the second ProxyCommand references the “Host” of the section
above it. Neat stuff. When I type “ssh acemdb1”, I’m actually connecting to
the portal.endpoint.com server, then immediately running the netcat (nc) command
in the background, then going through netcat to dmz.acme-anvils.com and
running a second netcat command on *that* server, and finally going through
both netcats to login to the db1.acme-anvils.com server. It sounds a little complicated,
but quickly becomes part of your standard tool set once you wrap your head around it.
After you update your .ssh/config file, you soon forget about
all the tunneling and feel as though you are connecting directly to all your servers. That is, until
something breaks, as it did recently for me.

The actual client this happened with was not “Acme Anvils”, of course, and it
was a connection that went through four servers and three ProxyCommands,
but for demonstration purposes let’s pretend it happened on a simple
connection to the dmz.acme-anvils.com server. I had not connected to
the server in question for a long time, but I needed to make some adjustments
to a [tail_n_mail](https://bucardo.org/wiki/Tail_n_mail) configuration file. The first login attempt failed
completely:

```text
[greg@localhost]$ ssh acmedmz
endpoint@dmz.acme-anvils.com's password:
```

Although the connection to portal.endpoint.com worked fine, the connection
to the client server failed. This is not an unusual problem: it usually signifies that either ssh-agent is not running,
or that I forgot to feed it the correct key via the ssh-add program. However, I quickly discovered
that ssh-agent was working and contained all my usual keys. Moreover, I was able to
connect to other sites with no problem! On a hunch, I tried breaking down the connections
into manual steps. First, I tried logging in to the “portal” server. It logged me in
with no problem. Then I tried to login from there to dmz.acme-anvils.com—​which also logged
me in with no problem! But trying to get there via ProxyCommand still failed.
What was going on?

When in doubt, crank up the debugging. For the ssh program, using the
-v option turns on some minimal debugging. Running the
original command from my computer with this option enabled quickly revealed the problem:

```text
[greg@localhost]$ ssh -v acmedmz
OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017
debug1: Reading configuration data /home/greg/.ssh/config
debug1: /home/greg/.ssh/config line 1227: Applying options for acmedmz
debug1: Reading configuration data /etc/ssh/ssh_config
...
debug1: Executing proxy command: exec ssh -q greg@portal.endpoint.com nc -w 180s 555.123.45.67 2222
...
debug1: Authenticating to dmz.acme-anvils.com:2222 as 'endpoint'
...
debug1: Host 'dmz.acme-anvils.com' is known and matches the ECDSA host key.
...
debug1: Skipping ssh-dss key /home/greg/.ssh/greg2048dsa.key - not in PubkeyAcceptedKeyTypes
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering RSA public key: /home/greg/.ssh/greg4096rsa.key
debug1: Next authentication method: password
endpoint@dmz.acme-anvils.com's password:
```

The problem is that my DSA key (the “ssh-dss key”) was rejected by
my ssh program. As we will see below, DSA keys are rejected by default in recent versions
of the OpenSSH program. But why was I still able to login when not hopping through
the middle server? The solution lays in the fact that when I use the ProxyCommand,
*my* ssh program is negotiating with the final server, and is refusing to use my DSA
key. However, when I ssh to the portal.endpoint.com server, and then on to the next one,
the second server has no problem using my (forwarded) DSA key! Using the -v option on the connection
from portal.endpoint.com to dmz.acme-anvils.com reveals another clue:

```text
[greg@portal]$ ssh -v endpoint@dmz.acme-anvils.com:2222
...
debug1: Connecting to dmz [1234:5678:90ab:cd::e] port 2222.
...
debug1: Next authentication method: publickey
debug1: Offering RSA public key: /home/greg/.ssh/endpoint2.ssh
debug1: Authentications that can continue: publickey,password
debug1: Offering DSA public key: /home/greg/.ssh/endpoint.ssh
debug1: Server accepts key: pkalg ssh-dss blen 819
debug1: Authentication succeeded (publickey).
Authenticated to dmz ([1234:5678:90ab:cd::e]:2222).
...
debug1: Entering interactive session.
[endpoint@dmz]$
```

If you look closely at the above, you will see that we first offered an RSA key, which
was rejected, and then we successfully offered a DSA key. This means that the
endpoint@dm account has a DSA, but not a RSA, public key inside of its
~/.ssh/authorized_keys file. Since I was able to connect
to portal.endpoint.com, its ~/.ssh/authorized_keys file
must have my RSA key.

For the failing connection, ssh was able to use my RSA key to connect
to portal.endpoint.com, run the netcat command, and then continue on to
the dmz.acme-anvils.com server. However, this connection failed as the only key my local ssh
program would provide was the RSA one, which the dmz server did not have.

For the working connection, ssh was able to connect to portal.endpoint.com
as before, and then into an interactive prompt. However, when I then connected
via ssh to dmz.acme-anvils.com, it was the ssh program on portal, not my local computer,
which negotiated with the dmz server. It had no problem using a DSA key, so I
was able to login. Note that both keys were happily forwarded to portal.endpoint.com,
even though my ssh program refused to use them!

The quick solution to the problem, of course, was to upload my RSA key to the dmz.acme-anvils.com
server. Once this was done, my local ssh program was more than happy to login
by sending the RSA key along the tunnel.

Another solution to this problem is to instruct your SSH programs to recognize DSA
keys again. To do this, add this line to your local SSH config file
($HOME/.ssh/config), or to the global SSH config file
(/etc/ssh/config):

```text
PubkeyAcceptedKeyTypes +ssh-dss
```

As mentioned earlier, this whole mess was caused by the OpenSSH program deciding
to deprecate DSA keys. Their rationale for targeting all DSA keys seems a little weak at best: certainly
I don’t feel that my 2048-bit DSA key is in any way a weak link. But
the writing is on the wall now for DSA, so you may as well replace your DSA
keys with RSA ones (and an [ed25519 key](https://en.wikipedia.org/wiki/EdDSA) as well, in anticipation of when ssh-agent
is able to support them!). More information about the decision to force out
DSA keys can be found in [this great analysis of the OpenSSH source code](https://security.stackexchange.com/questions/5096/rsa-vs-dsa-for-ssh-authentication-keys).
