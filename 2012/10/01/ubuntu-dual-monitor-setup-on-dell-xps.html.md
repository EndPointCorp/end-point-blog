---
author: Steph Skardal
gh_issue_number: 699
tags: ubuntu
title: Ubuntu Dual Monitor Setup on Dell XPS
---



Over the weekend, I received a new desktop (Dell XPS 8500 with NVIDIA graphics card) and troubleshot dual monitor setup on Ubuntu. Because I spent quite a while googling for results, I thought I'd write up a quick summary of what did and didn't work.

One monitor was connected via HDMI and the other through DVI (with a VGA to DVI adaptor provided with the computer). When I started up the computer in Windows, both monitors were recognized immediately. Besides configuring the positioning of the monitors, Windows was good to go. But when I installed Ubuntu, the DVI/VGA monitor was recognized with incorrect resolution and the monitor connected via HDMI was not recognized at all. I tried switching the unrecognized monitor to a VGA/DVI connection, and it worked great by itself, so I concluded that it wasn't an issue with a driver for the HDMI-connected monitor.

Many of the Google results I came across pointed to troubleshooting with xrandr, but any xrandr commands produced a "Failed to get size of gamma for output default." error and any progress beyond that was shut down. Another set of Google results pointed to using "nvidia-detector", but there weren't any follow-up tips or pointers on that when it returned nothing. And many Google results were all over the place or were on forums and were unanswered.

Finally, I came across a couple of articles that suggested that Ubuntu didn't have the proprietary nvidia driver and to install it with the command nvidia-current. After installing this, and restarting my X session, both monitors were working with correct resolution. I finished up by resetting the positioning of the monitors, adjusting the primary display, and saving to the xorg (X Configuration) file. This was probably the fastest I've figured out dual monitor setup (it's always an *adventure*), most likely because of improved Linux/Ubuntu support on various machines over time.

<div class="separator" style="clear: both; text-align: center;"><img border="0" height="639" src="/blog/2012/10/01/ubuntu-dual-monitor-setup-on-dell-xps/image-0.png" width="715"/><br/>
nvidia-settings display settings.</div>


