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

ssh-askpass for OS X/macOS. Works in (at least) 10.7+ (including Monterey), this also works on the latest M1 pro chip.

Used to accept (or deny) the use of the private key(s) added to the SSH authentication agent with `ssh-add -c`.

At End Point Dev we mostly use the SSH keys for authentication when connecting to remote servers and Git services. The majority of the time, the servers we are trying to visit are barred from direct access and require a middle "jump server" instead.

We use SSH key forwarding, which enables us to use the private key kept on our local machine to authenticate with each server in the chain without entering a password.

Using ssh-askpass as the agent confirmation is one of the recommended way when using SSH key forwarding. When utilizing the ssh-askpass, a prompt will show on your local computer to confirm the usage of the key each time a request is made to use the private key loaded in the SSH agent. Doing this makes it harder for an attacker to utilize the private key without permission.

If case if you don’t want to using agent confirmation, then it’s best to use ProxyJump instead of agent forwarding.

![agent confirmation dialog](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/ssh-askpass.png)

## Installation

### [Homebrew](https://brew.sh/)
You can install ssh-askpass using Homebrew, this method works on the Apple M1 Pro chip as well.

* Install:

```
    $ brew tap theseal/ssh-askpass
    $ brew install ssh-askpass

```
* Follow caveats

### [MacPorts](https://www.macports.org)
* Install:

```
    $ sudo port install ssh-askpass
```

### Without Homebrew/MacPorts

* Run:

```
$ cp ssh-askpass /usr/local/bin/
$ cp ssh-askpass.plist ~/Library/LaunchAgents/
$ launchctl load -w ~/Library/LaunchAgents/ssh-askpass.plist
```

## To start the ssh-askpass now and restart at login

```
$ brew services start theseal/ssh-askpass/ssh-askpass

```

## Enabling keyboard navigation
For security reasons ssh-askpass defaults to cancel since it's too easy to
press the spacebar and accept a connection or other actions which might use
ssh-keys. To make it easier to press `OK`:

* Go to `System Preferences` and then `Keyboard`.

#### Pre 10.11
* Under the `Keyboard` tab, click on `All controls`.

#### 10.11-10.14
* Under the `Shortcuts` tab, click on `All controls`.

#### 10.15+
* At the bottom of the `Shortcuts` tab, check the option ` Use keyboard navigation to move focus between controls `.

![keyboard shortscuts](/blog/2022/10/ssh-askpass-on-Mac-OS-for-agent-confirmation/keyboard_shortscuts.png)

Now you can press the tab ⇥ and then the spacebar to press `OK`.


* Now no need to log out; you can add keys to the agent with `ssh-add -c`.
* When you ssh, it prompts for confirmation.

Enjoy!

