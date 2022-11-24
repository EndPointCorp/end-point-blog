---
author: "Bharathi Ponnusamy"
date: 2022-11-23
title: "ssh-askpass on macOS for SSH agent confirmation"
github_issue_number: 1915
tags:
- ssh
- mac
- security
---

![A city street at night. A man sits on a bench, looking at his laptop as cyclists pass by.](/blog/2022/11/ssh-askpass-on-mac-os-for-agent-confirmation/night-street.webp)<br>
[Photo](https://flic.kr/p/2nUPsJQ) by [Kristoffer Trolle](https://www.flickr.com/people/kristoffer-trolle/), [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

At End Point Dev we mostly use SSH keys for authentication when connecting to remote servers and Git services. The majority of the time, the servers we are trying to visit are barred from direct access and require a middle "jump server" instead.

Enabling SSH agent forwarding makes it easier to reuse SSH private keys. It keeps the private keys on our local machine and uses them to authenticate with each server in the chain without entering a password.

However, this approach comes with an inherent risk of the agent being hijacked if one of the servers is compromised. This means a bad guy could use the SSH keys to compromise downstream servers.

In this post, we’ll cover a simple way to protect against SSH agent hijacking. We will see in detail on macOS how to configure a system-wide agent using ssh-askpass to pop up a graphical window to ask for confirmation before using the agent.

### How it works

![Agent confirmation dialog reading "Allow us of key /Users/(blank)/.ssh/id_rsa? Key fingerprint (blank) (blank). The cancel button is highlighted.](/blog/2022/11/ssh-askpass-on-mac-os-for-agent-confirmation/ssh-askpass.webp)

It is strongly recommended to use the `-c` option on the `ssh-add` command when adding your SSH keys to the agent in order to protect yourself against SSH agent hijacking.

With this, every time a request is made to utilize the private key stored in the SSH agent, ssh-askpass will display a prompt on your local computer asking you to approve the usage of the key. By doing this,  it becomes more difficult for a remote attacker to use the private key without authorization.

If you don't want to use the ssh-askpass agent confirmation, I recommend using the OpenSSH feature ProxyJump rather than agent forwarding to get an equivalent level of security.

### Installing ssh-askpass on macOS

So let's set this up. The recommended way is with Homebrew:

#### Install ssh-askpass with Homebrew

```plain
$ brew tap theseal/ssh-askpass
$ brew install ssh-askpass
```

You might see some warnings. Go ahead and proceed with them.

Now we need to start the Homebrew services. Note that this is a brew service, not a regular macOS daemon service.

```plain
$ brew services start theseal/ssh-askpass/ssh-askpass
=> Successfully started `ssh-askpass` (label: homebrew.mxcl.ssh-askpass)
```

Behind the scenes, it just sets the `SSH_ASKPASS` and `SUDO_ASKPASS` environment variables and stops `ssh-agent`, so that the SSH agent can pick up these environment variables when it restarts.

To list the services and make sure it’s started:

```plain
$ brew services list | grep ssh-askpass
ssh-askpass started ~/Library/LaunchAgents/homebrew.mxcl.ssh-askpass.plist
```

#### Install ssh-askpass with MacPorts

If you prefer MacPorts, do:

```plain
$ sudo port install ssh-askpass
```

#### Install ssh-askpass from source code

And of course you can install from source if you wish:

```plain
$ cp ssh-askpass /usr/local/bin/
$ cp ssh-askpass.plist ~/Library/LaunchAgents/
$ launchctl load -w ~/Library/LaunchAgents/ssh-askpass.plist
```

### Configure the SSH agent with the `ssh-add -c` option

* Let's first verify that the agent is running, then add the private key with the confirmation option:

    ```plain
    $ ssh-add -l
    The agent has no identities.
    $ ssh-add -c .ssh/id_rsa
    Enter passphrase for .ssh/id_rsa (will confirm after each use):
    Identity added: .ssh/id_rsa (.ssh/id_rsa)
    The user must confirm each use of the key
    ```

* The Identity will get added if you provide the correct passphrase for the key. This can be confirmed by listing the keys again with `ssh-add -l`.

### ssh-askpass agent confirmation

Now let's log into a remote server.

You will be prompted to confirm the private key’s usage with the pop-up window:

![Agent confirmation dialog. Identical to the previous dialog.](/blog/2022/11/ssh-askpass-on-mac-os-for-agent-confirmation/ssh-askpass.webp)

### Set up keyboard shortcuts

Since it's too easy to hit the spacebar and accept a connection, ssh-askpass defaults to the cancel option. We can use keyboard shortcuts to press "OK" by following the below steps.

* Go to "System Preferences" and then "Keyboard".

#### 10.15–12

* Go to "Shortcuts" tab
* check the option "Use keyboard navigation to move focus between controls".

    ![macOS 10.15+ settings open to the Keyboard section. First highlighted is the "Shortcuts" tab, and second is a checkbox at the bottom of the window reading "Use keyboard navigation to move focus between controls."](/blog/2022/11/ssh-askpass-on-mac-os-for-agent-confirmation/keyboard_shortcuts.webp)

#### 13.0 Ventura

* Turn on the "Keyboard navigation" option.

    ![macOS 13.0 settings open to the keyboard tab, with a slider button reading "Keyboard navigation" highlighted.](/blog/2022/11/ssh-askpass-on-mac-os-for-agent-confirmation/keyboard_shortcuts_on_ventura.webp)

Now you can press tab ⇥ and then the spacebar to select "OK".

Enjoy!
