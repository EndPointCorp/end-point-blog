---
author: Ethan Rowe
gh_issue_number: 248
tags: hosting, security, tips
title: SSHFS and ServerAliveInterval
---



If you’re using SSHFS (as I do recently since OpenVPN started crashing frequently on my OpenBSD firewall), note that the ServerAliveInterval option for SSH can have significant impact on the stability of your mounts.

I set it to 10 seconds on my system and have been happy with the results so far. It could probably safely go considerably higher than that.

It’s not on by default, which leaves the stability of your SSH tunnels up to the success of TCP keepalive (which *is* on by default). On my wireless network, that alone has not been sufficient.


