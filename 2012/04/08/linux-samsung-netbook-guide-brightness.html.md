---
author: Brian Buchalter
gh_issue_number: 585
tags: linux, tips
title: Guide to Ubuntu 11.10 on a Samsung Netbook
---



**12.04 UPDATE**: Unsurprisingly, after installing 12.04 which includes the 3.2.x kernel, brightness controls work perfectly out of the box. Sadly, it’s still necessary to tweak modprobe to get wireless working after a suspend/resume. Also, don’t forget to reboot after making the changes!

-----------

After reading a few too many reviews about netbook hardware and its compatibility with Linux, I settled on a Samsung NF310 netbook. However, like all things worth doing, it wasn’t nearly as easy as I’d hoped. This post highlights some of the lessons learned from my first days with Linux on my Samsung netbook.

### Pre-Installation

I had been eagerly awaiting the arrival of my new hardware and had already gotten a fresh copy of Fedora 16 ready. The crippled Windows 7 Starter Edition was going to be off that netbook as a first order of business, as a matter of principle. If I had it to do over again, I would have installed the Windows-only BIOS update for the Netbook first. I’m working through using BartPE, but the installation onto the USB drive hasn’t gone well. Best to do these kinds of Windows-only activities while Windows is still easily available.

Additionally, I would have used [YUMI multiboot USB creator](http://www.pendrivelinux.com/yumi-multiboot-usb-creator/) to put on a copy of [Ultimate Boot CD](http://www.ultimatebootcd.com/) as well as a handful of live Linux distros for testing. When I later had issues installing, I found myself wondering, is it the hardware? I ended up going back and running the tests (which passed), but had I done this first, I would not have been distracted from the real problem.

### Installation

Aside from choosing a distro, I found getting the installation to complete successfully to be a chore. It seems the disk’s partition table was GPT and so both Ubuntu and Fedora’s installation processes failed.

> ext4 Filesystem check failure on/dev/mapper/vgsamsungnetbook-lvroot:
> 
> 
> 
> Operational error.
> 
> 
> 
> Errors like this usually mean there is a problem with the filesystem that will require user interaction to repair. Before restarting installation reboot to rescue mode or another system that allows you to repair the filesystem interactively. Restart installation after you have corrected the problems on the filesystem.
> 
> 

You can see how an error like this might prompt you to run hardware checks. To work around this, simply fire up one of the Live CD installations on your YUMI stick and offer Linux the following incantation:

```bash
parted
mklabel msdos
quit
```

### Test Driving Fedora 16

After getting past installation issues, I loaded Fedora 16’s XCFE spin. Despite the dual core Atom processors and the 2GB RAM, I was looking for a lightweight distro; snappy UI and battery life were my first concerns and I knew less demands from the OS would leave more resources for the work I wanted to do.

The sparse XCFE desktop experience offered few bells and whistles but exactly what (I thought) I wanted. It was responsive and stayed out of the way. However, I quickly discovered that after resuming from suspend, my wireless connection would not work. Was this Fedora? Was this the kernel? Was this hardware failure? Only trial and error would help me figure it out...

### Troubleshooting wireless connectivity after resume

The Samsung came with a Broadcom chip, which was recognized by Fedora, but I have a low opinion of Broadcom hardware and know that its driver support is relatively new in the kernel mainline. I noticed kernel errors related to the driver and decided to swap out my other laptop’s Intel Ultimate N Wifi Link 5300 card and see what happened. To Linux’s credit, it detected the new hardware without a hitch and connected right away after booting. However, upon another round of suspend/resume, wireless connectivity couldn’t be established.

Next, I decided to see if this could be a distro issue. I tried Ubuntu 11.10 to find this was not an issue with a particular distro. Of course with both attempts I fully patched all the software, so I didn’t think it a kernel issue; Fedora was running the 3.3 kernel!

Sadly, it’s 2012 and Linux still can’t handle simple power management issues out the box. Fortunately for you, lucky reader, I have the magic incantations you need to have wireless network connectivity after suspend/resume. I knew I couldn’t be the only one experiencing the issue but was simply blown away this wasn’t better documented. As always, log files tend to be the best source for searching Google; results seem more accurate and from more authoritative sources. Here’s what I was seeing from /var/log/kern.log after resuming:

```bash
kernel: [  326.394858] wlan0: direct probe to 00:13:10:9e:88:5f (try 1/3)
kernel: [  326.592242] wlan0: direct probe to 00:13:10:9e:88:5f (try 2/3)
kernel: [  326.792214] wlan0: direct probe to 00:13:10:9e:88:5f (try 3/3)
kernel: [  326.992198] wlan0: direct probe to 00:13:10:9e:88:5f timed out
```

### Fixing Wireless Connectivity after suspend/resume

After a long and winding hunt through Launchpad bug reports and unhelpful forum threads, the first step is to identify which kernel module is providing your wifi driver.

```bash
lspci -k | grep -i -E "network|wireless|wifi|wlan|802.11" -A3

#my output...
05:00.0 Network controller: Intel Corporation Ultimate N WiFi Link 5300
 Subsystem: Intel Corporation Device 1101
 Kernel driver in use: iwlwifi
 Kernel modules: iwlwifi
```

On my machine, it was the **iwlwifi** module responsible for wireless. Armed with the module name, we now need just one simple line, in one simple file:

```bash
# /etc/modprobe.d/iwl.conf
options iwlwifi bt_coex_active=0
```

With that simple modification AND A REBOOT—​Linux sanity is restored. The wireless works perfectly (and quite quickly) after resume.

For those who don’t happen to be using the iwlwifi module, it’s not obvious what the modprobe.d config file naming conventions are, but in general, Googling for your kernel module name plus bt_coex_active=0 should yield something useful.

### Samsung screen brightness control, out of control

After having made the switch to Ubuntu to help troubleshoot my wireless issues, I found that the screen brightness would occasionally start randomly cycling through various levels repeatedly and rapidly. To stop this behavior temporarily, I found I could jump to a tty session by pressing ALT+F2 and return to X with ALT+F7.

For a more permanent fix, a kernel upgrade was required. While, Ubuntu 11.10’s stock 3.0.x kernel did not include the fixed “samsung_laptop” modules, the 3.2.x kernel did. Fortunately, with the upcoming 12.04 release, the 3.2.x kernel is actively being packaged for Ubuntu and can be downloaded from kernel.ubuntu.com. More specifically, you can [browse the available kernel packages](http://kernel.ubuntu.com/~kernel-ppa/mainline/) and choose your release of choice. Because I knew 3.2.x was going to be supported for the 12.04 release and I was looking for stability and didn’t see any must-have features in the 3.3.x kernel, I went with these downloads and installations:

```bash
# 64 bit installation
su
cd ~
mkdir src
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.14-precise/linux-headers-3.2.14-030214_3.2.14-030214.201204021356_all.deb http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.14-precise/linux-headers-3.2.14-030214-generic_3.2.14-030214.201204021356_amd64.deb http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.14-precise/linux-image-3.2.14-030214-generic_3.2.14-030214.201204021356_amd64.deb
dpkg -i linux-headers-3.2.14-030214_3.2.14-030214.201204021356_all.deb linux-headers-3.2.14-030214-generic_3.2.14-030214.201204021356_amd64.deb linux-image-3.2.14-030214-generic_3.2.14-030214.201204021356_amd64.deb

reboot
```

After updating the kernel the screen brightness worked flawlessly and updating the kernel this way seemed more reasonable than compiling. However, I did notice that Update Manager wanted to reinstall the stock kernel. Running these lines as root will prevent that:

```bash
echo linux-generic hold | dpkg --set-selections
echo linux-headers-generic hold | dpkg --set-selections
echo linux-image-generic hold | dpkg --set-selections
```

### Choosing a Distro and Desktop Shell

While I had originally planned to use Fedora 16 XCFE spin, I find myself wanting to stay with Ubuntu and Unity. The polish in the interface may be worth a bit of lag, and it seems it’s easy enough to switch shells at login with the little gear icon next to your username. You can easily [add additional shells](http://www.techdrivein.com/2011/05/top-4-lightweight-official-ubuntu-based.html) and experiment with what works for you.

Unity2D works reasonably well, despite a bit of delay. Moreover, [adding lenses to Dash](https://askubuntu.com/questions/38772/what-lenses-for-unity-are-available) seems like it will make the interface even more usable. I guess I did want some of the bells and whistles, but not always, especially when I need to save battery life. But isn’t this kind of flexibility the point of Linux and Free software in general?

### Closing thoughts: MacBook Air alternative?

Several times over the last few days of banging my head against the wall, I found myself thinking about Apple’s MacBook Air. It’s hard to argue the hardware is world class and OS X can be made to do most things a Linux distro can, while providing rock-solid power and device management with a slick UI. However, I just couldn’t bring myself to shell out $999 upfront, with the obligatory because-you’re-on-your-own-without AppleCare ($249), plus all the little Apple lock-in-gotchas that I knew were down the road.

Instead, I paid $315 for hardware that I can actually modify with additional batteries ($75/each/4hrs life) and a [SSD upgrade ($85 for 40 GB)](https://www.newegg.com/Product/Product.aspx?Item=N82E16820167046). I guess the bottom line is, if you’re a developer, or a system administrator, it may seem like the Apple product is a way to avoid the pain of running Linux on something other than a server. However, by deciding to fight the good fight, I’ve saved $773 (after planned upgrades!) but spent 20 hours of time, which means I paid myself about $40/hr to learn a few things. That’s a great rate of return and now that the pain is over, it all seems worth it.


