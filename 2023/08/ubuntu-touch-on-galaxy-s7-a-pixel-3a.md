---
title: "Ubuntu Touch on a Galaxy S7 & a Pixel 3a"
author: Seth Jensen
featured:
  image_url: /blog/2023/08/ubuntu-touch-on-galaxy-s7-a-pixel-3a/arabesque_with_knight-crop.webp
tags:
- linux
- mobile
- ubuntu
date: 2023-08-29
---

![A dark print on very old paper shows an armored knight on a horse, surrounded completely by swirling floral patterns. In a few places the pattern evolves into a flower or what appears to be a curved, long bird head.](/blog/2023/08/ubuntu-touch-on-galaxy-s7-a-pixel-3a/arabesque_with_knight-crop.webp)

<!-- Image: Arabesque with Knight, Italian, niello print, unknown date. Retrieved from https://www.nga.gov/collection/art-object-page.4541.html -->

I have a shoebox in my closet I call my "phone graveyard." At times I've had five or more old phones in there, in various states of decay — some have fully shattered screens, some broken USB ports, etc. But some still have quite usable hardware, their main drawback being how slow they run on modern versions of Android or iOS, and the lack of support for modern features.

It's always troubled me to have such incredible devices, with way more computing power than, say, a Raspberry Pi, gather dust because of software limitations. Even if I don't use an old phone for daily use any more, what if I could use it as a DNS server (like a Pi-Hole), or as a camera or media player?

When I heard about Ubuntu Touch, it seemed like the perfect OS to bring back some long-term functionality to these old devices. Originally created by Canonical, it was soon abandoned but revived by UBports, who started community development in 2015. They actively maintain the OS for around 80 devices, including two I have in my phone graveyard: a Samsung Galaxy S7 and a Google Pixel 3a.

### Installation

Installing Ubuntu Touch is quite straightforward; the UBports installer does most of the heavy lifting. See the [UBports website](https://devices.ubuntu-touch.io/installer/) for instructions.

For the Pixel 3a, I had to flash an older version of the stock OS before running the UBports installer. The Ubuntu Touch [device page](https://devices.ubuntu-touch.io/device/sargo) for the Pixel 3a specifies which version to flash under "Preparatory Step," but this seems to be in a different place for each device. Read the device-specific instructions carefully before installing.

See also:

* This useful [guide](https://android.gadgethacks.com/how-to/complete-guide-flashing-factory-images-android-using-fastboot-0175277/) from Gadget Hacks on flashing a factory image
* Android's [SDK platform tools](https://developer.android.com/studio/releases/platform-tools), including fastboot
* Android's docs for [locking/unlocking the bootloader](https://source.android.com/docs/core/architecture/bootloader/locking_unlocking)

### Usability

The native app landscape for Ubuntu Touch is, as you would expect, pretty limited. You won't be able to play most DRM content, and while there are web apps for Uber, Discord, and others, they tend to be various levels of buggy. You can see the apps, including helpful usability reports, at [open-store.io](https://open-store.io/).

There are plenty of bugs I encountered while briefly testing, like having no volume indicator when using volume keys and not seeing the Libertine installation which should've been there, making it hard to install programs with the terminal emulator.

Audio playback had fairly frequent interruptions, at least on my Pixel 3a, making it not viable as a music player. However, for audiobooks or podcasts this probably wouldn't be a big deal.

However, most of the base functionality for web browsing, photos, and media playback seemed to work well.

The inclusion of a fully-featured terminal emulator expands the possibilities greatly, allowing your old phone to act in place of a Raspberry pi for projects like a [Pi-Hole](/blog/2020/12/pihole-great-holiday-gift/).

> The system is, by default, in read-only mode, requiring containers (the intent is to run the custom container system, [Libertine](https://docs.ubports.com/en/latest/userguide/dailyuse/libertine.html)) to run most apps. However, you can change it to read-write for a more traditional Linux system.
> For more info on terminal capability, see [the UBports blog](https://ubports.com/en/blog/ubports-news-1/post/terminal-chapter-1-3082).

While I wouldn't want to run Ubuntu Touch as my only smartphone OS, it is an exciting option for secondary or old devices, especially if you want to contribute to open-source projects and help out the community!
