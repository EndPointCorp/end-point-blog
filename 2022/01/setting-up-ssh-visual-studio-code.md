---
title: "Setting up SSH in Visual Studio Code"
author: Couragyn Chretien
tags:
- ssh
- tips
- vscode
date: 2022-01-06
github_issue_number: 1817
---

![View of Grand Canyon](/blog/2022/01/setting-up-ssh-visual-studio-code/banner.jpg)
<!-- Photo by Zed Jensen, 2021 -->

Visual Studio Code is a powerful code editor that can create a customized IDE for your development. VS Code's default configuration is great for working locally but lacks the functionality to give the same experience for remote SSH development. Enter the extension [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh).

### Installation

![Remote SSH in Visual Studio Code Marketplace](/blog/2022/01/setting-up-ssh-visual-studio-code/marketplace.png)

Installing the Remote SSH extension is really easy! First you access the Extension Marketplace with `Ctrl+Shift+X` or by clicking `View > Extensions` in the menu, then you just search for and select `Remote - SSH`.

### Setting up your SSH config file

To configure your connection, you'll need to add a few lines to your SSH config. Click the green `Open a Remote Window` icon on the bottom left corner:

![Open Remote Window](/blog/2022/01/setting-up-ssh-visual-studio-code/open_remote_window.png)

Select `Open SSH Configuration File...` and select the config file you want to use. I use the Linux default, `/home/$USER/.ssh/config`. Add the Host, HostName, and User as required and save:

```plain
Host MySite
  HostName site.endpointdev.com
  User couragyn
```

### Connecting

Click the green `Open a Remote Window` icon on the bottom left corner, select `Connect to Host...`, and pick your desired host, in this case `MySite`. If your public SSH key isn't on the remote server, you will be prompted to enter a password. If your key is on the server, it will state it has your fingerprint and prompt you to continue.

You're now connected and can use VS Code's features like Terminal and Debug Console just like you would locally.

### Opening the working directory

Wouldn't it be nice to have VS Code automatically open to the correct folder once your SSH connection is established? Unfortunately there isn't a way to set a folder location in the settings yet; you'd need to click Open Folder and navigate to the project root every time you connect.

There is, however, a workaround to make this a bit less tedious:

- Click `Open Folder`
- Navigate to the project root
- Click `File > Save Workplace As...`
- Save your `.code-workspace` file somewhere it won't be picked up by Git

Now open your workspace again with a new connection. If the workspace was recently used, you can use `File > Open Recent > $Workspace.code-workspace`; otherwise go to `File > Open Workspace...` and select your `.code-workspace` file. This should get you set up right in the correct directory after you've connected.

### SSH with multiple hops

Sometimes you will need to SSH into one location before tunneling into another. To connect to a remote host through an intermediate jump host, you will need to add `ForwardAgent` and `ProxyJump` to the config file, like this:

```plain
Host MySite
  HostName site.endpointdev.com
  User couragyn
  ForwardAgent yes

Host SiteThatNeedsToGoThroughMySite
  HostName completely.different.com
  User couragyn
  ProxyJump MySite
```

Happy remote development!
