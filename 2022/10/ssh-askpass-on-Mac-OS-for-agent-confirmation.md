---
author: "Bharathi Ponnusamy"
date: 2022-10-26
title: "Ssh-askpass on Mac OS for the agent confirmation"
github_issue_number: 
tags:
- ssh 
- ssh-askpass
- mac
- security
---

![On a summer evening](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/banner.jpg)
[Photo](https://flic.kr/p/2nUPsJQ) by [Kristoffer Trolle](https://www.flickr.com/people/kristoffer-trolle/), [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

At End Point Dev we mostly use the SSH keys for authentication when connecting to remote servers and Git services. The majority of the time, the servers we are trying to visit are barred from direct access and require a middle "jump server" instead.

Enabling SSH Agent Forwarding makes it easier to reuse the SSH private keys. It keeps the private keys on our local machine to authenticate with each server in the chain without entering a password.

However, this approach comes with an inherent risk where the agent can be hijacked. This means a bad guy could use the SSH keys to compromise downstream servers.

In this post, we’ll cover a simple way to protect against SSH Agent Hijacking. Also, we will see in detail how to configure a system-wide agent that runs under GUI for agent confirmation using ssh-askpass.

## ssh-askpass - Agent Confirmation

![agent confirmation dialog](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/ssh-askpass.png)

It is strongly recommended to use the `-c` option on `ssh-add` command when adding your ssh keys to the ssh-agent in order to protect yourself against SSH Agent Hijacking.

Agent forwarding has some inherent risk, however, this risk may be significantly reduced by using this `-c` option.

When utilizing the ssh-askpass, a prompt will show on your local computer to confirm the usage of the key each time a request is made to use the private key loaded in the SSH agent. Doing this makes it harder for an attacker to utilize the private key without permission.

If case if you don’t want to use agent confirmation, then it’s best to use ProxyJump instead of agent forwarding.


## Installation

### [Homebrew](https://brew.sh/)

```
    $ brew tap theseal/ssh-askpass
    $ brew install ssh-askpass

```
* Follow caveats

### [MacPorts](https://www.macports.org)

```
    $ sudo port install ssh-askpass
```

### Without Homebrew/MacPorts

```
$ cp ssh-askpass /usr/local/bin/
$ cp ssh-askpass.plist ~/Library/LaunchAgents/
$ launchctl load -w ~/Library/LaunchAgents/ssh-askpass.plist

```

## To start the ssh-askpass now and restart at login

```
$ brew services start theseal/ssh-askpass/ssh-askpass

```
## Configure the ssh-agent with `-c` option

* Let's first verify that the ssh-agent is running and then add the private key with ` -c `option.

![ssh-add -c](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/ssh-add-c.png)
* The Identity will get added if you provided the correct passphrase for the key. This can be confirmed by listing the keys again.

## ssh-askpass agent confirmation
* Let's log into a remote server
* It will be prompted to confirm the private key’s usage with the pop-up window.
![agent confirmation dialog](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/ssh-askpass.png)


## Keyboard shortcuts
For security reasons ssh-askpass defaults to cancel since it's too easy to
press the spacebar and accept a connection or other actions which might use
ssh-keys. To make it easier to press `OK`:

* Go to `System Preferences` and then `Keyboard`.

#### 10.15+
* At the bottom of the `Shortcuts` tab, check the option ` Use keyboard navigation to move focus between controls `.

![keyboard shortscuts](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/keyboard_shortscuts.png)

#### 13.0 Ventura
* Turn on the option ` Use keyboard navigation to move focus between controls `
![keyboard shortscuts](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/keyboard_shortscuts_on_ventura.png)


Now you can press the tab ⇥ and then the spacebar to press `OK`.

Enjoy!

