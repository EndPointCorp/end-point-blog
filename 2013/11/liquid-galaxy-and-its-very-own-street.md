---
author: Matt Vollrath
title: Liquid Galaxy and its Very Own Street View App
github_issue_number: 881
tags:
- javascript
- visionport
- nodejs
date: 2013-11-09
---



### Liquid Galaxy does Street View!

Peruse-a-Rue is the combination of a Node.js server with a Maps API browser client, all wrapped up in one neat bundle. The result of this marriage is a highly compelling immersive Street View experience.

Everything from a single screen kiosk to a cylindrical Liquid Galaxy to an endless display wall can be configured, with bezel offsets, portrait or landscape. A touchscreen control interface is optional, and a Space Navigator can drive the display.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/11/liquid-galaxy-and-its-very-own-street/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img alt="Testing Peruse-a-Rue" border="0" height="295" src="/blog/2013/11/liquid-galaxy-and-its-very-own-street/image-0.png" width="480"/></a><p style="text-align: center; font-size: 0.8em;">Testing Peruse-a-Rue on the desktop</p></div>

By leveraging the Connect framework for Node, the entire application is served on a single port. Any number of browser windows can be synchronized, thanks to the scalability of websockets. When integrated with the Squid caching of the Liquid Galaxy project, redundant downloading is eliminated; each screen shares retrieved tile data with its peers.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/11/liquid-galaxy-and-its-very-own-street/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img alt="Peruse-a-Rue Touchscreen" border="0" height="281" src="/blog/2013/11/liquid-galaxy-and-its-very-own-street/image-1.png" width="480"/></a><p style="text-align: center; font-size: 0.8em;">The Peruse-a-Rue touchscreen interface</p></div>

Since NPM installs dependencies automatically, deployment is a breeze. Every Liquid Galaxy is a git checkout and an `npm install` away from running the server. Peruse-a-Rue supports any operating system that can run Node.js (as a server) or Google Chrome (as a client). I’ve even tested the server on a Raspberry Pi and BeagleBone Black, and it runs perfectly!

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/11/liquid-galaxy-and-its-very-own-street/image-2.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img alt="Raspberry Pi" border="0" height="247" src="/blog/2013/11/liquid-galaxy-and-its-very-own-street/image-2.png" width="480"/></a><p style="text-align: center; font-size: 0.8em;">It runs on this thing, too</p></div>

Peruse-a-Rue is hosted [here](https://github.com/EndPointCorp/lg-peruse-a-rue). If you’re interested in the project or want to contribute, drop us a line.

Happy Perusing!


