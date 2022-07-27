---
title: "Windows SSH key agent forwarding confirmation"
author: Ron Phipps
date: 2022-07-26
github_issue_number: 1882
tags:
- windows
- ssh
---

![A sunset with silhouetted construction equipment](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/sunset.webp)

<!-- Photo by Seth Jensen -->

At End Point we use SSH keys extensively, primarily for authentication with servers for remote shell access as well as with Git services including GitHub, GitLab, and Bitbucket. Most of the time the servers we are attempting to reach are blocked from direct access and require that we go through an intermediate “jump server”.

Because of this need to jump from server to server we utilize SSH key forwarding that allows us to use the private key stored on our local system to authenticate with each of the servers in the chain. When we reach our destination server we can use the same private key to authenticate with the Git hosting service and perform git commands without having to enter a password.

One of the best practices when using SSH key forwarding is to use an option called key confirmation. When key confirmation is turned on, each time a request is made to use the private key that is loaded in the SSH agent a prompt will appear on your local machine to approve the use of the key. This reduces the ability for an attacker to use your private key without approval.

For the longest time SSH key confirmation was not available on Windows. One of the most popular SSH clients on Windows is PuTTY and its agent (pageant) does not support the option. Many other SSH key compatible Windows applications use PuTTY’s agent for SSH key caching and as a result these applications also lack the ability for key confirmation.

### KeePass and KeeAgent

To use key confirmation on Windows we need to utilize two programs, KeePass and KeeAgent. KeePass is an open source password manager and KeeAgent is a plugin for KeePass that provides a PuTTY-compatible SSH key agent. It also appears that KeeAgent has support for integration with the Windows shell, Cygwin/MSYS, and Git Bash.

The instructions below will assume that you already have a SSH key in PuTTY that you’d like to use with key confirmation and that you have previously used PuTTY with key forwarding.

You should start by [installing KeePass](https://keepass.info/). Then [install KeeAgent](https://lechnology.com/software/keeagent/).

Once both are installed create a new KeePass database, or use your existing database if you are already a KeePass user.

Add a new entry to the database and name it SSH key. Enter your SSH key password into the Password and Repeat fields.

![KeePass’s Add Entry screen](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/1-add-entry.webp)

Then click on the KeeAgent tab and check ‘Allow KeeAgent to use this entry’.

In the Private Key section select External File and point it at your PuTTY private key. If you have entered the correct password on the first tab you should see your key comment and fingerprint listed. Then press OK.

![The KeeAgent tab in Add Entry](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/2-add-entry.webp)

Verify that confirmation is enabled by clicking on Tools -> Options and selecting the KeeAgent tab.

![A checked box reading "Always require user confirmation when a client program requests to use a key"](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/3-options.webp)

Press OK.

Then go to File -> Save. Close KeePass and re-open it. You’ll be asked to enter your KeePass password and then you can verify that the agent is loaded with your key by clicking Tools -> KeeAgent.

![KeeAgent in Agent Mode](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/4-agent.webp)

Now when we use PuTTY or another PuTTY agent-compatible program we’ll be presented with a confirmation dialog. Clicking Yes will allow the key to be used.

![KeeAgent’s confirmation dialog](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/5-confirmation.webp)

Notice that the default selected option is No. This is different than the standard openssh-askpass on Linux, which defaults to Yes. If you’re typing along in a fury and the confirmation window pops up and you hit Enter or space, it will decline the use of your SSH key, rather than accepting it.

If you have enabled SSH key forwarding in the PuTTY options for the connection you’ll be using you can then SSH to other servers using the same key and each time you do so the confirmation will be presented to you.

If you close KeePass the key agent will be closed and unavailable for future connections. Re-opening KeePass will allow the key to be used again.

If you use Windows and SSH agent forwarding but have never tried agent confirmation to protect against malicious use of your secret key, give KeePass and KeeAgent a try!
