---
author: Jon Jensen
gh_issue_number: 83
tags: hardware, linux
title: Sometimes it's a silly hardware problem
---

I've been using [Twinkle](http://www.xs4all.nl/~mfnboer/twinkle/index.html) and [Ekiga](http://ekiga.org/) for SIP VoIP on Ubuntu 8.10 x86_64. That's been working pretty well.

However, I finally had to take some time to hunt down the source of a very annoying high-pitched noise coming from my laptop's sound system (external speaker and headset both). I have an Asus M50SA laptop with Intel 82801H (ICH8 Family) audio on Realtek ALC883. I first thought perhaps it was the HDMI cable going to an external monitor, or some other RF interference from a cable, but turning things off or unplugging them didn't make any difference.

Then I suspected there was some audio driver problem because the whine only started once the sound driver loaded at boot time. After trying all sorts of variations in the ALSA configuration, changing the options to the snd-hda-intel kernel module, I was at a loss and unplugged my USB keyboard and mouse.

It was the USB mouse! It's a laser-tracked mouse with little shielding on the short cable. Plugging it into either of the USB ports near the front of the computer caused the noise. The keyboard didn't matter.

At first I thought my other USB non-laser ball mouse didn't add any noise, but it did, just a quieter and lower-pitch noise.

Then ... I discovered a third USB port near the back of the computer that I hadn't ever noticed. Plugging mice in there doesn't interfere with the audio. Sigh. Maybe this tale will save someone else some trouble.

In the process I also fixed a problem that *was* in software: The external speakers didn't mute when headphones are plugged in, as [others have described](https://bugs.launchpad.net/ubuntu/+source/alsa-driver/+bug/253422) as well. One of their solutions worked.

In /etc/modprobe.d/alsa-base add: "options snd-hda-intel model=targa-2ch-dig" and reboot. Or, if you dread rebooting as I do, exit all applications using audio, modprobe -r snd-hda-intel then modprobe snd-hda-intel. Finally, uncheck the "Headphones" checkbox in the sound control panel.
