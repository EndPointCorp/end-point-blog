---
author: Jon Jensen
title: TrueCrypt whole-disk encryption for Windows
github_issue_number: 82
tags:
- windows
- security
date: 2008-12-13
---

A few months ago I had a chance to use a new computer with Windows Vista on it. This was actually kind of a fun experience, because Windows 98 was the last version I regularly used myself, though I was at least mildly familiar with Windows 2000 and XP on others’ desktops.

Since I’ve been using encrypted filesystems on Linux since around 2003, I’ve gotten used to the comfort of knowing a lost or stolen computer would mean only lost hardware, not worries about what may happen with the data on the disk. Linux-Mandrake was the first Linux distribution I recall offering an easy encrypted filesystem option during setup. Now Ubuntu and Fedora have it too.

I wanted to try the same thing on Windows, but found only folder-level encryption was commonly used out of the box. Happily, the open source [TrueCrypt](http://www.truecrypt.org/) software introduced whole-disk [system encryption](https://www.truecrypt71a.com/documentation/system-encryption/) for Windows with version 5. I’ve now used it with versions 6.0, 6.1, and 6.1a on three machines under Windows Vista and XP, and it really works well, with a few caveats.

The installation is smooth, and system encryption is really easy to set up **if** you don’t have any other operating systems on the machine. It will even encrypt on the fly while you’re still using the computer! It’s faster if you exit any programs that would use the disk, but it still works under active use. Very impressive.

Some people have reported problems with logical (extended) partitions. Others have workarounds for dual-booting. I tried dual-booting GRUB with Windows Vista as per [this blog post](https://web.archive.org/web/20080803080614/http://blog.redinnovation.com/2008/07/15/perfect-dual-boot-crypted-hard-disk-setup-with-truecrypt-and-luks/).

That seemed to work well, and Linux booted. Vista also started but then partway through the boot process, after the GUI started up, it noticed something had changed and it died with the largest red “ERROR” message I’ve ever seen. Microsoft makes impressive error messages!

I battled with dual-booting for a while but eventually gave up, as I was just playing around with it anyway. Sticking with TrueCrypt’s recommended Windows-only configuration, everything’s worked great. The additional CPU for encryption and decryption is negligible, and becomes increasingly so with multi-core CPUs.

Everyone with a laptop should really be using encrypted filesystems. The peace of mind is well worth the minor initial work and the one extra passphrase to enter at boot time.

As a footnote to my catch-up on the state of Windows, it’s really much easier to bear as a Unix and X Window System user with the now wide availability of open source software for Windows. I used 7zip, Audacity, Coolplayer, Cygwin, Firefox, Gimp, Git, Gnucash, Google Chrome, OpenOffice.org, Pidgin, Putty, Strawberry Perl, Vim, VirtualBox, VLC, WinMTR, WinPT (including GnuPG), WinSCP, Wireshark, and Xchat (from Silverex).

Oh, and also helpful was somebody’s nice registry edit to remap the Caps Lock key as another Control key, so I don’t go crazy. The somewhat abandoned WinPT takes some prodding to get working on a few customer machines I’ve set it up on, but otherwise all the open source software I tried worked well on Windows. I’m sure there’s much more out there too. [This UTOSC presentation](https://web.archive.org/web/20080803082335/http://2008.utosc.com/presentation/54/)’s slides mentions more.

However, it’s still no replacement for a fully free system. So despite the brief investigation, I’ll be sticking with Linux. :)
