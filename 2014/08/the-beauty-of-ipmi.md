---
author: Josh Ausborne
title: The Beauty of IPMI
github_issue_number: 1021
tags:
- hosting
- linux
- visionport
date: 2014-08-01
---

For our [Liquid Galaxy](https://www.visionport.com/) installations, we use a master computer known as a “head node” and a set of slave computers known as “display nodes.” The slave computers all PXE-boot from the head node, which directs them to boot from a specific ISO disk image.

In general, this system works great. We connect to the head node and from there can communicate with the display nodes. We can boot them, change their ISO, and do all sorts of other maintenance tasks.

There are two main settings that we change in the BIOS to make things run smoothly. First is that we set the machine to power on when AC power is restored. Second, we set the machine’s boot priority to use the network.

Occasionally, though, the CMOS battery has an issue, and the BIOS settings get lost.  How do we get in and boot the machine up? This is where ipmitool has really become quite handy.

Today we had a problem with one display node at one of our sites. It seems that all of the machines in the Liquid Galaxy were rebooted, or otherwise powered off and then back on. One of them just didn’t come up, and it was causing me much grief.  We have used [ipmitool](https://sourceforge.net/projects/ipmitool/) in the past to be able to help us administer the machines.

IPMI stands for [Intelligent Platform Media Interface](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface), and it gives the administrator some non-operating system level access to the machine.  Most vendors have some sort of management interface ([HP’s iLO](https://en.wikipedia.org/wiki/HP_Integrated_Lights-Out), [Dell’s DRAC](https://en.wikipedia.org/wiki/Dell_DRAC)), including our Asus motherboards.  The open source ipmitool is the tool we use on our Linux systems to be able to interface with the [IPMI module on the motherboard](https://www.asus.com/Commercial_Servers_Workstations/ASMB5iKVM/).

I connected to the head node and ran the following command and got the following output:

```plain
admin@headnode:~ ipmitool -H 10.42.41.33 -I lanplus -P 'xxxxxx' chassis status
System Power         : off
Power Overload       : false
Power Interlock      : inactive
Main Power Fault     : false
Power Control Fault  : false
Power Restore Policy : always-off
Last Power Event     : ac-failed
Chassis Intrusion    : inactive
Front-Panel Lockout  : inactive
Drive Fault          : false
Cooling/Fan Fault    : true
```

While Asus’s Linux support is pretty lacking, and most of the options we find here don’t work with with the open source ipmitool, we did find “System Power : off” in the output, which is a pretty good indicator of our problem.  This tells me that the BIOS settings have been lost for some reason, as we had previously set the system to power on when AC power was restored.  I ran the following to tell it to boot into the BIOS, then powered on the machine:

```plain
admin@headnode:~ ipmitool -H 10.42.41.33 -I lanplus -P 'xxxxxx' chassis bootdev bios
admin@headnode:~ ipmitool -H 10.42.41.33 -I lanplus -P 'xxxxxx' chassis power on
```

At this point, the machine is ready for me to be able to access the BIOS through a terminal window. I opened a new terminal window and typed the following:

```plain
admin@headnode:~ ipmitool -H ipmi-lg2-3 -U admin -I lanplus sol activate
Password:
```

After typing in the password, I get the ever-helpful dialog below:

```plain
[SOL Session operational.  Use ~? for help]
```

I didn’t bother with the ~? because I knew that the BIOS would eventually just show up in my terminal. There are, however, other commands that pressing ~? would show.

See, look at this terminal version of the BIOS that we all know and love!

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2014/08/the-beauty-of-ipmi/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="433" src="/blog/2014/08/the-beauty-of-ipmi/image-0.png" width="640"/></a></div>

Now that the BIOS was up, it’s as if I was really right in front of the computer typing on a keyboard attached to it. I was able to get in and change the settings for the APM, so that the system will power on upon restoration of AC power. I also verified that the machine is set to boot from the network port before saving changes and exiting. The next thing I knew, the system was booting up PXE, which then pointed it to the proper ISO, and then it was all the way up and running.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2014/08/the-beauty-of-ipmi/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="449" src="/blog/2014/08/the-beauty-of-ipmi/image-1.png" width="640"/></a></div>

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2014/08/the-beauty-of-ipmi/image-2.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="450" src="/blog/2014/08/the-beauty-of-ipmi/image-2.png" width="640"/></a></div>

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2014/08/the-beauty-of-ipmi/image-3.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="450" src="/blog/2014/08/the-beauty-of-ipmi/image-3.png" width="640"/></a></div>

And this, my friends, is why systems should have IPMI. I state the obvious here when I say that life as a system administrator is so much easier when one can get into the BIOS on a remote system.
