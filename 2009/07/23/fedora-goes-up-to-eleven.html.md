---
author: Daniel Browning
gh_issue_number: 175
tags: redhat, linux
title: Fedora goes up to eleven
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2009/07/23/fedora-goes-up-to-eleven/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2009/07/23/fedora-goes-up-to-eleven/image-0.png"/></a></div>

I upgraded to Fedora Core 11 this week, up from 9. What really surprised me is how fast it is. I don't recall ever having such a noticably faster and responsive desktop after a distro upgrade. Everything is more responsive and instantaneous. Even though FC9 didn't seem particularly slow, I realize now that I had been spending time just waiting for the software to catch up. I don't know where the credit is due. Could be anything from the kernel to XFCE to the apps. But I like it.

Normally, most SELinux issues occur when it is enabled. But after the upgrade I ran into one of the opposite variety: the gedit program threw an error on every file save. The [244605](https://bugzilla.redhat.com/show_bug.cgi?id=244605) and [477070](http://bugzilla.gnome.org/show_bug.cgi?id=477070) tickets might be the same issue I ran into. I worked around the problem by switching to 'kate -u'.

I need at least four different text editors in order to enjoy using the computer. How could anyone stand the monotony of a single text editor all day? Right now I'm doing:

- gvim for detailed things
- vanilla vim for when gvim is too awesome.
- kate for vogon poetry
- jedit for when I get that certain IDE feeling (you know the one)
- emacs for inducing carpal tunnel syndrome

It's also important to switch out text editors at regular intervals, such as when one of them breaks in a distro upgrade.

The first few minutes after booting up a fresh distro install are disorienting. Keyboard shortcuts and other customizations are so much a part of me that I can hardly function at all without them. Thank goodness that it's only a matter of minutes before /home gets restored and everything is back to normal.

The policy I follow is to upgrade to every odd-numbered Fedora release. I don't actually know if the even-numbered releases are worse or better, but based on my experience with Star Trek movies, I'm not going to take any chances. The majority of my coworkers run non-Fedora distros, even the ones that used to work at Red Hat. Some of them do RHEL, which I did a few times when I was waiting for an odd-numbered Fedora release.

<img src="/blog/2009/07/23/fedora-goes-up-to-eleven/image-1.jpeg"/>

Although I considered the B-tree FS with its "i-can't-believe-it's-not-btr" kernel option, ext4 won in the end. With the new policy of updating atime only once per day, I'm leaving it enabled. I couldn't get the nvidia driver to load until I [removed nouveau from initrd](http://rpmfusion.org/Howto/nVidia) and downgraded to 173xx.

Overall, FC11 has been a great upgrade. Thanks to Free Software developers the world over.
