---
author: Brian Buchalter
gh_issue_number: 759
tags: networking
title: Detecting Bufferbloat
---



Bufferbloat is topic which has been gaining broader attention, but is still not widely understood. This post will walk you through the basics of bufferbloat and how to determine if you are the victim of bufferbloat.

### A Brief Synopsis of the Bufferbloat Problem

The topic of bufferbloat has been explained wide and far, but I’ll add to the conversation too, focusing on brevity. This summary is based on the highly informative and technical talk [Bufferbloat: Dark Buffers in the Internet](https://www.youtube.com/watch?v=qbIozKVz73g), a Google Tech Talk by Jim Gettys. There is an assumption in the design of TCP that if there is network congestion, there will be **timely** packet loss. This packet loss triggers well designed TCP flow control mechanisms which can manage the congestion. Unfortunately, engineers designing consumer grade routers and modems (as well as all sorts of other equipment) misunderstood or ignored this assumption and in an effort to **prevent** packet loss added large FIFO (first-in-first-out) buffers. If users congest a network chokepoint, typically an outgoing WAN link, the device’s large buffers are filled with packets by TCP and held instead of being dropped. This “bufferbloat” prevents TCP from controlling flow and instead results in significant latency.

### Detecting Bufferbloat

All that’s required to experience bufferbloat is to saturate a segment of your network which has one of these large FIFO buffers. Again, the outgoing WAN link is usually the easiest to do, but can also happen on low-speed WiFi links. I experienced this myself when installing Google’s Music Manager, which proceed to upload my entire iTunes library in the background, at startup, using all available bandwidth. (Thanks Google!) I detected the latency using [mtr](https://linux.die.net/man/8/mtr). Windows and OS X does not offer such a fancy tool, so you can simply just ping your WAN gateway and see the lag.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2013/02/11/detecting-blufferbloat/image-0-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" height="208" src="/blog/2013/02/11/detecting-blufferbloat/image-0.png" width="400"/></a><br/>
<b>Music Manager enabled, bufferbloat, slow ping to WAN gateway</b></div>

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2013/02/11/detecting-blufferbloat/image-1-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" height="207" src="/blog/2013/02/11/detecting-blufferbloat/image-1.png" width="400"/></a><br/>
<b>Music Manager paused, no bufferbloat, fast ping to WAN gateway</b></div>

### Managing Bufferbloat

Unfortunately, there are no easy answers out there right now for many users. Often we cannot control the amount of bandwidth a piece of software will try to use or the equipment given to us by an ISP. If you are looking for a partial solution to the problem, checkout [Cerowrt](https://www.bufferbloat.net/projects/cerowrt), a fork of the OpenWrt firmware for routers. It makes use of the best available technologies used to combat bufferbloat. Additionally, be on the look out for any software that might saturate a network segment, such as Bittorrent, Netflix streaming, or large file transfers over weak WiFi links.


