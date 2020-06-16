---
author: "Kevin Campusano"
title: "Developing in Linux via Docker in Windows 10 WSL2"
tags: windows, wsl, linux, docker, vscode, php
---

![Banner](/blog/2020/06/16/developing-in-linux-via-docker-in-windows-10-wsl2/banner.png)

I'm first and foremost a Windows guy. For a few years now though, moving away from working mainly with [.NET](https://dotnet.microsoft.com/) technologies and into a plethora of open source technologies has given me the opportunity to change platforms and run a Linux based system as my daily driver. Ubuntu, which I honestly love for work, has been serving me well by supporting my development workflow with languages like [PHP](https://www.php.net/), [JavaScript](https://www.javascript.com/) and [Ruby](https://www.ruby-lang.org/en/). And with the help of the excellent [Visual Studio Code](https://code.visualstudio.com/) editor, I've never looked back. There's always been an inclination in the back of my mind though, to take some time and try giving Windows another shot...

With the latest improvements coming to the [Windows Subsystem for Linux with its second version](https://docs.microsoft.com/en-us/windows/wsl/wsl2-index), the new and exciting [Windows Terminal](https://github.com/microsoft/terminal) and [Docker support for running containers inside WSL2](https://docs.docker.com/docker-for-windows/wsl/); I think the time is now.

In this post, we'll walk through the steps that I had to take to set up a PHP development environment in Windows, running in a Ubuntu Docker container running on WSL2, and VS Code. Let's go.

## What's new with WSL 2.

Many have written about this so I won't be redundant and just point you right to the source: https://docs.microsoft.com/en-us/windows/wsl/wsl2-index

Being a WSL 1 veteran, what I can mention are the main improvements that have been made since the last time I used it which have sparked my interested in trying it again.

### 1. It's faster and more compatible.

WSL 2 introduces a complete architectural overhaul. Now, Windows ships with a full Linux Kernel which is what WSL 2 distributions use to run. This results in greatly improved file system performance and much better compatibility with Linux programs. It's no longer running a Linux look-alike, but rather, actual Linux.

### 2. It's better integrated with Windows.

This is a small one: we can now use the Windows explorer to browse files within a WSL distribution. This is not a WSL 2 exclusive feature, it has been there for a while now. I think it's worth mentioning though because it truly is a great convenience and a far cry from WSL's first release, where Microsoft specifically advised against browsing WSL distribution file systems from Windows. If anything else, this makes WSL feel like a first class citizen in the Windows ecosystem and shows that Microsoft actually cares about making it a good experience. 

### 3. It can run Docker.

I've recently been learning more and more about Docker and it's quickly becoming my preferred way of setting up development environments. Due to its lightweightness, ease of use, and VM-like compartmentalization, I find it really convenient to develop against a purpose-built Docker container, rather than directly in my local machine. And with VS Code's Remote development extension, the whole thing is very easy to set up. Docker for windows now supports running containers within WSL, so I'm eager to try that out and see how it all works.

### 4. A newer version means several bugfixes.

Performance not whistanding, WSL's first release was pretty stable. I did however, encounter some weird bugs and gotchas when working with the likes of SSH and Ruby during certain specific tasks. It was nothing major as workwrounds were readily available, so I won't bother mentioning them here again. I've already discussed some of them [here](https://www.endpoint.com/blog/2019/04/04/rails-development-in-windows-10-pro-with-visual-studio-code-and-wsl). But the fact that the technology has matured since last time I saw it, and considering the architectural direction it is going in, I'm excited to not have to deal with any number of quirks. Developing software is hard enough as it is, I don't need to also be fighting my OS.

## The development environment

Ok, now with some of the motivation out of the way, let's try and build a quick PHP hello world app, run it in a Docker container inside WSL 2, which we can edit with VS Code and browse from a browser from Windows.


[AMD](https://github.com/amdjs/amdjs-api/blob/master/AMD.md)
