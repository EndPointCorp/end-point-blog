---
author: "Kevin Campusano"
title: "Developing in Linux via Docker in Windows 10 WSL2"
tags: development, javascript, webpack, babel
---

![Banner](/blog/2020/06/16/developing-in-linux-via-docker-in-windows-10-wsl2/banner.png)

I'm first and foremost a Windows guy. For a few years now though, moving away from working mainly with [.NET](https://dotnet.microsoft.com/) technologies and into a plethora of open source technologies has given me the opportunity to change platforms and run a Linux based system as my daily driver. Ubuntu, which I honestly love for work, has been serving me well by supporting my development workflow with languages like [PHP](https://www.php.net/), [JavaScript](https://www.javascript.com/) and [Ruby](https://www.ruby-lang.org/en/). And with the help of the excellent [Visual Studio Code](https://code.visualstudio.com/) editor, I've never looked back. There's always been an inclination in the back of my mind though, to take some time and try giving Windows another shot...

With the latest improvements coming to the [Windows Subsystem for Linux with its second version](https://docs.microsoft.com/en-us/windows/wsl/wsl2-index), the new and exciting [Windows Terminal](https://github.com/microsoft/terminal) and [Docker support for running containers inside WSL2](https://docs.docker.com/docker-for-windows/wsl/); I think the time is now.

In this post, we'll walk through the steps that I had to take to set up a PHP development environment in Windows, running in a Ubuntu Docker container running on WSL2, and VS Code. Let's go.

### What's new with WSL 2.

Many have written about this so I won't be redundant and just point you right to the source: https://docs.microsoft.com/en-us/windows/wsl/wsl2-index

Me being a WSL 1 veteran, what I can say is the few main features/aspects that made me interested in trying this latest WSL release.

1. It's faster and more compatible.
3. It's better integrated with Windows.
2. It can now run Docker.
3. A newer version means several bugfixes.

### subtitle
[AMD](https://github.com/amdjs/amdjs-api/blob/master/AMD.md)
