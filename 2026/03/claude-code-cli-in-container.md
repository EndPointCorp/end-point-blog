---
title: "Containerizing Claude Code with Podman"
author: Seth Jensen
date: 2026-03-31
description: "How to (relatively) safely bypass permissions in Claude Code using Podman or Docker containers"
featured:
  image_url: /blog/2026/03/claude-code-cli-in-container/train-winter.webp
github_issue_number: 2175
tags:
- artificial-intelligence
- podman
- containers
---

![A long freight train points to the right, slightly toward the camera. The train cars extend off the image to the left. Above the tracks is a white snow-capped mountain and a deep blue sky.](/blog/2026/03/claude-code-cli-in-container/train-winter.webp)<br>
Photo by Seth Jensen, 2026.

I've been experimenting with many different AI tools, and my favorite is Claude Code. It provides the impressive performance of the Opus models without forcing me to use Visual Studio Code (or a fork of it).

IDEs and fancy editors like IntelliJ and VS Code are great, but I often prefer the simplicity and low memory footprint of working directly in the terminal. Claude Code works well with my tmux-centered work environment.

However, I don't like giving AI agents access to all of my files, and I *really* don't like letting them run arbitrary commands in my shell. I'm already pretty cautious about running unvetted code on my machine (I'm looking at you, install.sh files I'm supposed to blindly `curl | bash`), and the nondeterministic nature of LLMs takes this to the next level. It's not just data-sniffing closed-source code or malware you need to worry about, it's the product itself running commands and editing files in ways that, by design, are unique and untested.

Claude Code has a [sandbox mode](https://code.claude.com/docs/en/sandboxing) which is supposed to limit filesystem access to the folder it's run from, but since it's closed-source ([in theory](https://arstechnica.com/ai/2026/03/entire-claude-code-cli-source-code-leaks-thanks-to-exposed-map-file/)), you can't verify this isolation. Even in this mode, it can run commands outside the sandboxed folder (in my experience, it asks first, but I wouldn't count on this).

So, I wrote a little wrapper script to run Claude Code in a Podman container with access only to Claude's config directory and the working directory you pass to the script. I also let it run with the `--dangerously-skip-permissions` flag, which I would never do on my host machine (it didn't take long to find a horror story of a typo in an `rm -rf` command deleting half of the programs in `/Applications` on one Redditor's Mac).

### Important security notes

Claude has full access to the folder you pass to this script. That means it can run `rm -rf` as much as it wants, and you won't be prompted before it does so, especially when using the `--dangerously-skip-permissions` flag.

You should only run this script if you don't mind everything in that folder getting deleted — for example, in a Git repository where everything has been pushed to a remote, or in a sandbox folder — it's easy to create a copy of your working directory for Claude to play in!

There is no constraint on outward network traffic, so Claude can send data anywhere it wants. If you're working with sensitive data, you should set up a firewall so it only has access to the necessary Anthropic servers (and perhaps an allowlist you provide). **Think carefully about what data you give to powerful AI agents.**

### Using my claude-container script

* Make sure you have Podman and Podman Compose installed (this would also work with Docker & Docker Compose, just replace `podman compose` with `docker compose` in the `claude-container` script)
* Clone the repo from [my GitHub](https://github.com/sethjensen1/claude-container).
* From the cloned folder, run `./claude-container /path/to/working/directory`
* Optionally, add the script to your PATH. This is what I ran on macOS:

  ```
  ln -s /Users/myuser/repos/claude-container/claude-container /Users/myuser/bin/claude-container
  ```

  You can then run the script from anywhere: `claude-container /my/favorite/sandbox`

That's all you need to run it! Keep reading if you're interested in the technical details.

### What the script is doing

The `claude-container` script is a lightweight wrapper around `podman compose`, setting a couple of environment variables so the process is as simple as running Claude in the first place.

The compose setup uses [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/) to give Claude access to the folder you pass, along with your Claude config directory. This means you don't have to reauthenticate every time, and that session history is shared between containers/​your local Claude install.

Podman compose will automatically build the image if it doesn't exist. If you want to trigger a rebuild, you can run it with the `-b` flag: `claude-container -b /path/to/working/directory`.

The first time you run the script, it will ask you if you're okay bypassing permissions. Because we're only mounting two directories, this should be much safer than it normally would be (provided you're smart about which folders you pass).

### The Dockerfile

The Dockerfile is based on the one from Claude's devcontainer [docs](https://code.claude.com/docs/en/devcontainer). I've stripped out some development helpers since I'm running Claude directly in the `CMD`, not using the shell.

I previously copied the working directory into the image, but have since moved to using bind mounts only. If I want to make sure that Claude doesn't touch any files on my machine, I just create a copy of the working directory to bind mount to the container.

Another important thing I removed from Claude's devcontainer Dockerfile is the firewall setup with init-firewall.sh. Limiting outgoing traffic is a good idea, but the repos I was working with weren't sensitive enough for me to spend the time getting this working (especially since it seems you need to run the container with the NET_ADMIN capability, which I don't understand well enough to be using).

Running this with no firewall is dangerous, but less so than running the agent outside of a container.

### No container-ception, unfortunately

At some point, I wanted to give Claude access to a backend dev server (it was running a frontend dev server in the container). But the backend dev server runs in a container itself, so I couldn't just have Claude spin up the backend dev server in its container.

After trying a few things, my workaround was to connect Claude's container to the backend container's Podman network. Once all your containers have been started, find the relevant container network with:

```
podman network ls
```

If you're not sure which is the right network, you can check which containers are connected to a network using `podman network inspect <network_name>`. To connect Claude to the desired network, run:

```
podman network connect <relevant container's network> <claude container>
```

And of course, if this container is connected to something important (like a database), this will allow Claude access to it. **Always be careful before letting an LLM have access to data**. In my case, this was an empty database for development, so in terms of exposing data to Claude, it was similar to running the backend dev server within the container.

### A few notes

Claude won't have access to some important developer tools in the container (e.g., Playwright). If you want to give it more tools, you could modify the Dockerfile to install them at build time. I tried installing Playwright at first, but found I actually prefer manually testing outside of the container & copying output back to Claude. I appreciate the extra time to slow down, check Claude's decisions, and catch bugs.

This setup intentionally doesn't give your container SSH access — I don't ever want an LLM to have access to my SSH key, and I would suggest thinking *very* hard before giving it access to any servers. That's one of the big reasons I don't want to run Claude on my own machine, especially when using an SSH agent.

I've enjoyed developing using Claude Code from within the confines of a single folder. I get the solid code analysis and generation without giving away an excessive amount of data.

