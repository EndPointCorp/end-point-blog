---
author: Jon Jensen
gh_issue_number: 283
tags: hosting, redhat, tips, virtualization
title: Xen MAC mismatch VNC mouse escape HOWTO
---



This is a story that probably shouldn't need to be told if everything is in documentation somewhere. I'm not using any fancy virtualization management tools and didn't have an easy time piecing everything together, so I thought it'd be worth writing down the steps of the manual approach I took.

Dramatis personæ:

- Server: Red Hat Enterprise Linux 5.4 with Xen kernel
- Guest virtual server: CentOS 5.4 running paravirtualized under Xen
- Workstation: Ubuntu 9.10

The situation: I updated the CentOS 5 Xen virtual guest via yum and rebooted to load the new Linux kernel and other libraries such as glibc. According to Xen as reported by xm list, the guest had started back up fine, but the host wasn't reachable over the network via ping, http, or ssh, including from the host network.

The guest wasn't using much CPU (as shown by xm top), so I figured it wasn't just a slow-running fsck during startup. And I was familiar with the iptables firewall rules on this guest, so I was fairly sure I wasn't being blocked there. I needed to get to the console to see what was wrong.

The way I've done this before is using VNC to access the virtual console remotely. The Xen host was configured to accept VNC connections on localhost, which I could see by looking in /etc/xen/xend-config.sxp:

```nohighlight
(vnc-listen '127.0.0.1')
```

There are 11 Xen guests, with consoles listening on TCP ports 5900-5910. Which one was the one? I don't know any simple way to get a list that maps ports to Xen guests, but I did it this way:

```nohighlight
ps auxww | grep qemu-dm
```

I noted the PID of the process that was running for my guest as revealed in its command line. Then I looked for the listener running under that PID:

```nohighlight
netstat -nlp
```

I looked for $pid/qemu-dm in the PID/Program Name column and could then see the TCP port in the Local Address column. In my case it was 127.0.0.1:5903.

So I set up an ssh tunnel to the server for my VNC traffic:

```nohighlight
ssh -f -N -L 5903:localhost:5903 root@$remote_host &
```

Then I opened the default Ubuntu/GNOME VNC viewer, labeled "Remote Desktop Viewer" under the Internet menu. This program is actually called Vinagre, and is basic but works. I connected to localhost:5903, since I'd forwarded my own local TCP port 5903 to the remote port 5903.

The remote console came up, and I was presented with the login banner and prompt. If I hadn't had the root password, I would have needed to reboot the guest and start it in runlevel 0 to get a root shell without a password and change the password. But I did have the password, so that wasn't necessary.

Then when trying to change to another window on my desktop, I ran into the biggest snag of the whole exercise: Getting control of the mouse out of the VNC remote desktop window and back in my own desktop! I couldn't find anything accurate on this in any documentation, forums, etc. Finally I stumbled across the trick: Press F10, which pulls down the Machine menu in Vinagre and as a side-effect takes control of the mouse away from the remote desktop. It was nice not to have to ssh in from another machine to kill Vinagre. But it makes me wonder how I'd send an F10 through to the remote console ...

Armed with the root password I was able to log into the guest and discover that only the lo (loopback) interface started on boot. The eth0 and eth1 interfaces failed because there was no virtual NIC available with the MAC addresses specified in /etc/sysconfig/network-scripts/ifcfg-eth0 and eth1.

That was because the virtual machine image had been cloned from another one and hadn't been given new unique MAC addresses. The problem was easily fixed by updating the ifcfg-eth0 and ifcfg-eth1 files with the MAC addresses actually given to the interfaces, as seen by ifconfig, which were ultimately assigned by the Xen host in /etc/xen/$host in the vif parameter. (You can also specify no MAC addresses in the guest at all and it will use whatever it gets.)

Then after running service network restart the networking was back, and I rebooted to make sure it started correctly on its own.


