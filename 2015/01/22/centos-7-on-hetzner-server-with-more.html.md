---
author: Spencer Christensen
gh_issue_number: 1075
tags: redhat, devops, hosting
title: CentOS 7 on Hetzner server with more than 2 TB disk
---

We use a variety of hosting providers for ourselves and our clients, including [Hetzner](http://www.hetzner.de/).  They provide good servers for a great price, have decent support, and we've been happy with them for our needs.

Recently I was given the task of building out a new development server for one of our clients, and we wanted it to be set up identically to another one of their servers but with CentOS 7. I placed the order for the hardware with Hetzner and then began the procedure for installing the OS.

Hetzner provides a scripted install process that you can kick off after booting the machine into rescue mode. I followed this process and selected CentOS 7 and proceeded through the whole process without a problem. After rebooting the server and logging in to verify everything, I noticed that the disk space was capped at 2 TB, even though the machine had two 3 TB drives in it (in hardware RAID 1). I looked at the partitions and found the partition table was "msdos". Ah ha!

At this point [painful memories of running into this problem before](/blog/2013/11/06/installing-centos-5-on-3tb-drive) hit me. I reviewed our notes of what we had done last time, and felt like it was worth a shot even though this time I'm dealing with CentOS 7. I went through the steps up to patching anaconda and then found that anaconda for CentOS 7 is newer and the files are different. I couldn't find any files that care about the partition table type, so I didn't patch anything.

I then tried to run the CentOS 7 install as-is. This only got me so far because I then ran into trouble with NetworkManager timing out and not starting.

<a href="http://www.bsd-unix.net/seitz/jing/2015-01-07_1543.png"><img alt="screen shot of CentOS 7 installer failing" height="300" src="http://www.bsd-unix.net/seitz/jing/2015-01-07_1543.png" width="400"/>
<div style="font-size:11px; font-style:italic; clear: both; margin-bottom:15px;">A screenshot of the CentOS 7 installer failing (anaconda) similar to what I was seeing.</div></a>

Baffled, I looked into what may have been causing the trouble and discovered that the network was not set up at all and it looked as if no network interfaces existed. WHAT?? At this point I dug through dmesg and found that the network interfaces did indeed exist but udevd had renamed them. Ugh!

Many new Linux distributions are naming network interfaces based on their physical connection to the system: those embedded on the motherboard get named em1, em2, etc. Apparently I missed the memo on this one, as I was still expecting eth0, eth1, etc. And from all indications, so was NetworkManager because it could not find the network interfaces!

Rather than spend more time going down this route, I decided to change gears and look to see if there was any way to patch the Hetzner install scripts to use a GPT partition table with my install instead of msdos. I found and read through the source code for their scripts and soon stumbled on something that just might solve my problem. In the file /root/.oldroot/nfs/install/functions.sh I found mention of a config variable **FORCE_GPT**.  If this is set to "1" then it will try to use a GPT partition table unless it thinks the OS won't like it, and it thinks that CentOS won't like it (no matter the version). But if you set **FORCE_GPT** to "2" it will use a GPT partition table no matter what. This config setting just needs to be added to the file you edit where you list out your partitions and LVM volumes.

```nohighlight
FORCE_GPT 2

PART /boot ext3 512M
PART lvm   vg0  all

LV  vg0  swap swap   swap  32G
LV  vg0  root  /     ext4 100G
LV  vg0  home  /home ext4 400G
```

I then ran the installer script and added the secret config option and... Bingo! It worked perfectly! No need to manually patch anything or install manually. And now we have a CentOS 7 server with full 3 TB of disk space usable.

```nohighlight
(parted) print
Model: DELL PERC H710 (scsi)
Disk /dev/sda: 3000GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: pmbr_boot

Number  Start   End     Size    File system  Name  Flags
 3      1049kB  2097kB  1049kB                     bios_grub
 1      2097kB  539MB   537MB   ext3
 2      539MB   3000GB  2999GB                     lvm
```
