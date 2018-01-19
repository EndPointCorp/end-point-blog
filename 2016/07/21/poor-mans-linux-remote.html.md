---
title: 
 - "Poor Man's Linux Remote Desktop Using VNC Server"
date: 2016-07-21 16:31:47 UTC
tags:
- Development
author: Ed Huott
image: 
 - '/images/blog-images/edblog.png'
published: true
description:
 - "How to DIY a Linux remote desktop"
keywords:
 - "development, linux, remote desktop, ed huott" 
---

Even the most hardcore Linux hackers want to run GUI applications sometimes. The problem is how do you do that with Linux when it's running on a remote server with no access to the console?

Remote Desktop is a built-in feature of Windows Server that lets you access a virtual remote desktop session that's not tied to a physical console. Many would be tempted to believe that most Linux distributions don't come with this kind of functionality out of the box. <em>Au contraire!</em> This article explains one method for accessing this feature using only packages included in most stock Linux installations. The examples given here are based on Debian/Ubuntu.

The core ingredient of our recipe is the <code>vnc4server</code> package, which includes Xvnc, the X VNC (Virtual Network Computing) server. A description of what that is comes right from the Xvnc(1) manual page itself:

<p class="indent">“Xvnc is the X VNC (Virtual Network Computing) server.  It is based on
a standard X server, but it has a "virtual" screen rather than a
physical one.  X applications display themselves on it as if it were
a normal X display, but they can only be accessed via a VNC viewer -
see vncviewer(1).</p>

<p class="indent">So Xvnc is really two servers in one. To the applications it is an X
server, and to the remote VNC users it is a VNC server.”</p>

The remaining ingredients are the packages needed to provide a window manager or desktop environment as well as the particular graphical programs you wish to run. Here, the best choice is probably a lightweight desktop environment such as <a href="http://www.xfce.org/" target="_blank">Xfce</a> or <a href="http://lxde.org/" target="_blank">LXDE</a>. Their lower demands on the graphics subsystem will make for snappier performance over a network connection.

Once all the necessary packages are installed, the <code>vncserver</code> command can be run on the remote server to start a virtual desktop session that can then be connected to by any VNC client. Multiple users on the remote system may run virtual desktop sessions at the same time. 

So, without further ado, here are some step by step instructions for making it all happen.

<h2 class="sub-head medium strong">Install and Configure Server Side Software</h2>

<p>1. Install the <code>vnc4server</code> package:</p>

<code class="indent">user@remote:~$ sudo apt-get install vnc4server</code>

<p>2. Install the packages needed to provide a graphical desktop environment. We use Xfce in this example:</p>

<code class="indent">user@remote:~$ sudo apt-get install xfce4</code>

<p>3. Use the vncpasswd command to set the password needed to access the remote session:</p>

<code class="indent">user@remote:~$ vncpasswd</code>

<p>4. Use the text below as the contents of the <code>vncserver</code> startup script in the file 
<code>$HOME/.vnc/xstartup</code>. If the file already exists, replace its contents with the text below. Otherwise, just create the file:</p>

<pre class="indent"><code>#!/bin/sh

# Enable normal desktop startup with cut and paste support to Xvnc session
unset SESSION_MANAGER
/usr/bin/vncconfig -nowin &amp;

# The standard X11 init script initializes the desktop running in the Xvnc server
sh /etc/X11/xinit/xinitrc

# Kill VNC server once session has ended
vncdisplay=`echo $DISPLAY | sed 's/^.*:/:/' | sed 's/\..*$//'`
vncserver -kill $vncdisplay</code></pre>

The astute reader will recognize that this file is the secret sauce of this recipe. You can customize it to control what programs are run in your virtual desktop session.

<h2 class="sub-head medium strong">Starting a Remote Virtual Desktop Session</h2>

Use the <code>vncserver</code> command to start a virtual desktop session on the remote server. The example below shows a typical command and its output:

<pre class="indent"><code>user@remote:~$ vncserver -geometry 1280x1024 -localhost

New 'remote:1 (user)' desktop is remote:1

Starting applications specified in /home/user/.vnc/xstartup
Log file is /home/user/.vnc/remote:1.log</code></pre>

The <code>-geometry</code> option sets the size of the virtual desktop. It cannot be changed once the session is started.

The <code>-localhost</code> option tells the server to only accept connections from the local machine. This is useful for ensuring that only encrypted connections tunneled through SSH can be used to access the desktop session. (This is necessary because Xvnc doesn't have any built-in support for encryption.)

<h2 class="sub-head medium strong">Accessing the Remote Desktop Session via a Secure SSH Connection</h2>

<p>1. Use ssh to set up a secure tunnel to the remote server:</p>

<code class="indent">user@local:~$ ssh -L 5901:localhost:5901 user@remote</code>

The remote Xvnc server listens on port 590x where x is the "display number" assigned to the desktop session. This is the number shown after the colon (:) in the output of the <code>vncserver</code> command (see above).

<p>2. Use the <code>vncviewer</code> command (or other VNC client program) to connect to the remote desktop session:</p>

<code class="indent">user@local:~$ vncviewer localhost:5901</code>

Once the password set by the <code>vncpasswd</code> command above is given, your remote desktop session should appear on the screen!

<h2 class="sub-head medium strong">So, What's This All Good For?</h2>

Say you have a remote network to which access is only possible via ssh through a single machine with a publicly accessible interface. Rather than going to the trouble of setting up a special VPN to this network, you can launch a secure, virtual desktop session on this machine and access the internal network as if you were logged into the machine's graphical console.

Another application would be for automated GUI testing. Instead of dedicating multiple physical machines to do <a href="http://seleniumhq.org/" target="_blank">Selenium</a> automated web testing, for example, multiple virtual desktops could simultaneously run scripted tests automatically. A VNC viewer application could be used to connect to any of the instances at any time to view progress or do debugging.

The possibilities are really endless.

