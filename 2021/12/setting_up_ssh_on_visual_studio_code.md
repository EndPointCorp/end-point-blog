---
title: "Setting up SSH on Visual Studio Code"
author: Couragyn Chretien
tags:
- ssh
- visual studio code
- configuration
- tunneling
- multiple jumps
- ForwardAgent
- ProxyJump
date: 2021-12-31
---

Visual Studio Code is a powerful code editor that can create a localized IDE for your code. VSCs default configuration is great for working locally but lacks the functionality to give the same experience for remote SSH development. Enter the extension Remote SSH.

### Installation

![Remote SSH in Marketplace](/blog/2021/12/setting_up_ssh_on_visual_studio_code/marketplace.png)

- Access the Extension Marketplace with `Ctrl+Shift+X`, or nav to `View > Extensions`
- Select `Remote - SSH`
- Install the latest version

### Setting up SSH Config File

- Click the green `Open a Remote Window` icon on the bottom left corner
![Open Remote Window](/blog/2021/12/setting_up_ssh_on_visual_studio_code/open_remote_window.png)
- Select `Open SSH Configuration File...`
- Select the file to use, I use the default `/home/$User/.ssh/config` file
- Add the Host, HostName, and User as required to the file and save
```
Host MySite
  HostName site.endpointdev.com
  User couragyn
```

### Connecting

- Click the green `Open a Remote Window` icon on the bottom left corner
- Select `Connect to Host...`
- Select your Host, in this case `MySite`
  - If your Public SSH Key isn't on the remote server, you will be promted to enter a password
  - If your Key is on the server, it will state it has your fingerprint and prompt you to continue

You're now connected and can use the Terminal, Debug Console, and other features as you would locally.


### Opening Working Directory

Wouldn't it be nice to have VSC automatically open to the correct folder when the SSH connection is established? It sure would, but unfortunatley there isn't a way to pass in a folder location at this time. You need to Click Open Folder and nav to the project root every time you connect.

There is a workaround to make this a bit less tedious. 

- Click `Open Folder`
- Nav to project root
- Nav `File > Save Workplace As...`
- Save `.code-workspace` file somewhere it won't be picked up by git
- Open workspace with new connection
  - If the workspace was recently used, nav `File > Open Recent > $Workspace.code-workspace`
  - If it hasn't been used in a while, nav `File > Open Workspace..` and select `.code-workspace` file 


### SSH with Multiple Hops

Sometimes you will need to SSH into one location before tunneling into another. To connect to a remote host through another intermediate jump host, you will need to add `ForwardAgent` and `ProxyJump` to the config file.

```
Host MySite
  HostName site.endpointdev.com
  User couragyn
  ForwardAgent yes

Host SiteThatNeedsToGoThroughMySite
  HostName completely.different.com
  User couragyn
  ProxyJump MySite
```