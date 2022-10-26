---
author: "Bharathi Ponnusamy"
date: 2022-10-26
title: "Ssh-askpass on MacOS for the agent confirmation"
github_issue_number: 
tags:
- ssh 
- ssh-askpass
- mac
- security
---

![On a summer evening](/blog/2022/10/ssh-askpass-on-mac-os-for-agent-confirmation/night-street.webp)
[Photo](https://flic.kr/p/2nUPsJQ) by [Kristoffer Trolle](https://www.flickr.com/people/kristoffer-trolle/), [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

At End Point Dev we mostly use the SSH keys for authentication when connecting to remote servers and Git services. The majority of the time, the servers we are trying to visit are barred from direct access and require a middle "jump server" instead.

Enabling SSH Agent Forwarding makes it easier to reuse the SSH private keys. It keeps the private keys on our local machine to authenticate with each server in the chain without entering a password.

However, this approach comes with an inherent risk where the agent can be hijacked. This means a bad guy could use the SSH keys to compromise downstream servers.

In this post, we’ll cover a simple way to protect against SSH Agent Hijacking. Also, we will see in detail how to configure a system-wide agent that runs under GUI for agent confirmation using ssh-askpass.

## ssh-askpass - Agent Confirmation

![agent confirmation dialog](/blog/2022/10/ssh-askpass-on-mac-os-for-agent-confirmation/ssh-askpass.webp)

It is strongly recommended to use the `-c` option on `ssh-add` command when adding your ssh keys to the ssh-agent in order to protect yourself against SSH Agent Hijacking.

Agent forwarding has some inherent risk, however, this risk may be significantly reduced by using this `-c` option.

Every time a request is made to utilize the private key stored in the SSH agent, the ssh-askpass will display a prompt on your local computer asking you to approve the usage of the key. By doing this,  it becomes more difficult for a remote attacker to use the private key without authorization.

It is recommended to utilise ProxyJump rather than agent forwarding if you don't want to use the ssh-askpass agent confirmation.

### Install ssh-askpass with Homebrew
```
$ brew tap theseal/ssh-askpass
$ brew install ssh-askpass
```
You might see some warnings. Go ahead and proceed with them.

### Install ssh-askpass with MacPorts
```
$ sudo port install ssh-askpass
```

### Install ssh-askpass from Source Code
```
$ cp ssh-askpass /usr/local/bin/
$ cp ssh-askpass.plist ~/Library/LaunchAgents/
$ launchctl load -w ~/Library/LaunchAgents/ssh-askpass.plist
```

## Start the Homebrew Services
Note that it’s a `brew service` not just a regular daemon service.

```
$ brew services start theseal/ssh-askpass/ssh-askpass
=> Successfully started `ssh-askpass` (label: homebrew.mxcl.ssh-askpass)

```
Behind the scenes, it just sets the `SSH_ASKPASS` and `SUDO_ASKPASS` environment variables and stops `ssh-agent`,  so that the ssh-agent can pick up these environment variables when it restarts.


To List the services and make sure it’s started
```
$ brew services list | grep ssh-askpass
ssh-askpass started ~/Library/LaunchAgents/homebrew.mxcl.ssh-askpass.plist
```

## Configure the ssh-agent with `-c` option

* Let's first verify that the ssh-agent is running and then add the private key with ` -c `option.

![ssh-add -c](/blog/2022/10/ssh-askpass-on-mac-os-for-agent-confirmation/ssh-add-c.webp)
* The Identity will get added if you provide the correct passphrase for the key. This can be confirmed by listing the keys again.

## ssh-askpass agent confirmation
* Let's log into a remote server
* It will be prompted to confirm the private key’s usage with the pop-up window.
![agent confirmation dialog](/blog/2022/10/ssh-askpass-on-mac-os-for-agent-confirmation/ssh-askpass.webp)

## Setup keyboard shortcuts
Since it's too easy to hit the spacebar and accept a connection, ssh-askpass defaults to the cancel option, and we can use the keyboard shortcuts to press `OK` by following the below steps.

* Go to `System Preferences` and then `Keyboard`.

#### 10.15+
* Go to `Shortcuts` tab
* check the option ` Use keyboard navigation to move focus between controls`.
![keyboard shortscuts](/blog/2022/10/ssh-askpass-on-mac-os-for-agent-confirmation/keyboard_shortcuts.webp)

#### 13.0 Ventura
* Turn on the option ` Use keyboard navigation to move focus between controls `
![keyboard shortscuts](/blog/2022/10/ssh-askpass-on-mac-os-for-agent-confirmation/keyboard_shortcuts_on_ventura.webp)

Now you can press the tab ⇥ and then the spacebar to press `OK`.

Enjoy!

