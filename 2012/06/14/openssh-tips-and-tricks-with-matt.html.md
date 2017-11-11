---
author: Brian Buchalter
gh_issue_number: 640
tags: liquid-galaxy, ssh, tips
title: OpenSSH Tips and Tricks with Matt Vollrath
---



Matt Vollrath's presentation focused on unique solutions Liquid Galaxy administration requires.

Specifically, Liquid Galaxy requires secure access to many public sites, which we don't have physical access to. OpenSSH helps handle these remote challenges securely and quickly.

<a href="http://www.flickr.com/photos/80083124@N08/7372338082/" title="IMG_0803.JPG by endpoint920, on Flickr"><img alt="IMG_0803.JPG" height="375" src="/blog/2012/06/14/openssh-tips-and-tricks-with-matt/image-0.jpeg" width="500"/></a>

### Multiplexing for Speed

The LG master node can send commands to all the slave nodes at the same time. This can be helpful to examine all display nodes' current states without manual work. The multiplexed connection uses options -f (background), -M (control socket), -N (no command), and -T (prevents pseudo-terminal from being allocated), and any further connections to the host do not need to authenticate, for speed.:

ssh -fMNT hostname &

Include the ampersand to be able to track the PID of the background ssh connection.  This connection will be maintained until it fails or is killed.

Additionally -O allows us to examine the state of the control connection as well as exit. As of OpenSSH 5.9, you can also use -O with the "stop" command to not accept any more multiplexers.

When combined with a simple bash script to inspect the host connection first, the script can create that multiplexed connection first. This allows for **very** fast work. Without control connection it takes 700ms to run a command; with sockets, 85ms.

For Liquid Galaxy, everything is done over SSH so this speed is critical for a responsive experience while maintaining security. This responsive experience is multiplied for each node in the setup, which in LG's case, may be up to 8 nodes.

### Reverse SSH for Security

In order to allow access behind deployments' firewalls, the LG head node connects to a proxy server and then forwards its own SSH port to that proxy server, allowing secure remote connectivity from any network which will allow output SSH.


