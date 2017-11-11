---
author: Jon Jensen
gh_issue_number: 168
tags: browsers, environment, networking
title: 'MTU tweak: a fix for upload pain'
---

While traveling and staying at [Hostel Tyn](http://tyn.prague-hostels.cz/) in Prague's city center, I ran into a strange problem with my laptop on their wireless network.

When many people were using the network (either on the hostel's public computers or on the wireless network), sometimes things bogged down a bit. That wasn't a big deal and required merely a little patience.

But after a while I noticed that absolutely no "uploads" worked. Not via ssh, not via browser POST, nothing. They always hung. Even when only a file upload of 10 KB or so was involved. So I started to wonder what was going on.

As I considered trying some kind of rate limiting via iptables, I remembered somewhere hearing that occasionally you can run into mismatched MTU settings between the Ethernet LAN you're on and your operating system's network settings.

I checked my setup and saw something like this:

```
ifconfig wlan0
wlan0     Link encap:Ethernet  HWaddr xx:xx:xx:xx:xx:xx
          inet addr:10.x.x.x  Bcast:10.x.x.x  Mask:255.255.255.0
          inet6 addr: fe80::xxx:xxxx:xxxx:xxxx/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1239 errors:0 dropped:0 overruns:0 frame:0
          TX packets:20 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:191529 (191.5 KB)  TX bytes:4543 (4.5 KB)
```

The MTU 1500 stood out as being worthy of tweaking. So I tried a completely unscientific change:

```bash
sudo ifconfig wlan0 mtu 1400
```

Then tried the same HTTP POST that had been consistently failing, and poof! It worked fine. Every time.

I think mostly likely something more than 1400 bytes would've been possible, perhaps just a few short of 1500. The number 1492 rings familiar. I'll be old-fashioned and *not* look it up on the web. But this 1400-byte MTU worked fine and solved the problem. To my delight.

As an interesting aside, before making the change, I found one web application where uploads did work fine anyway: Google's Picasa. I'm not sure why, but maybe it sliced &amp; diced the upload stream into smaller chunks on its own? A mystery for another day.
