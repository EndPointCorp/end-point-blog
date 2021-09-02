---
author: Greg Davidson
title: Test Web Sites with Internet Explorer for Free
github_issue_number: 697
tags:
- browsers
- environment
- testing
- tips
- tools
- virtualization
date: 2012-09-26
---



## Browser Testing

While many Web Developers prefer to build sites and web applications with browsers like [Chrome](https://www.google.com/intl/en/chrome/browser/) or [Firefox](http://getfirefox.com) it's important for us to keep an eye on the [browser market share](http://marketshare.hitslink.com/browser-market-share.aspx?qprid=0&qpcustomd=0&qpcustomc=) for **all** web users. [Internet Explorer](http://windows.microsoft.com/en-US/internet-explorer/products/ie/home) (IE) still owns a large piece of this pie and because of this, it is important to test sites and applications to ensure they work properly when viewed in IE. This poses a potential problem for developers who do not use Windows.

Although I use OS X on my desktop, I have Windows virtual machines with IE 6,7,8,9 and 10 installed. I also have a Linux virtual machine running Ubuntu so I can check out Chrome/Chromium and Firefox on that platform. In the past I had tried solutions like [MultipleIEs](http://tredosoft.com/Multiple_IE) but wasn't satisfied with them. In my experience I've found that the best way to see what users are seeing is to have a virtual machine running the same software they are.

I did some IE8 testing for a colleague a short time ago and suggested she should give VirtualBox a shot. Her response was "You should write a blog post about that!". So here we are.

## Free Tools

[VirtualBox](https://www.virtualbox.org/) is a free virtualization application similar to [Parallels](http://www.parallels.com/) or [VMWare](http://www.vmware.com/). These applications aim to solve this problem by allowing us to run different "guest" operating systems on the "host" operating system of our choice. For example, I run several versions of IE and Windows on my computer which is running OS X.

Microsoft have begun in recent years to release Virtual PC (VPC) images for free to enable Web Developers to test their sites and applications with various versions of Internet Explorer. The most recent images were released on July 30, 2012 and you can check them out [here](http://www.microsoft.com/en-us/download/details.aspx?id=11575). Although these images are created to run on Microsoft's [Virtual PC](http://www.microsoft.com/windows/virtual-pc/) application, with a little bit of effort we can also use them on Linux, OS X or Windows via VirtualBox.

For our purposes, we will be building a Windows 7 virtual machine running Internet Explorer 8. However, there are several images available with various Windows OS and Internet Explorer version combinations:

- Windows 7 / IE8
- Windows 7 / IE9
- Windows Vista / IE7
- Windows XP / IE6

There will likely be some differences creating virtual machines for the various images but the process will be similar to what we'll document here for Windows 7 / IE.

## Linux and OS X Users

In researching this article I came across a very helpful project on GitHub. The [ievms project](https://github.com/xdissent/ievms#readme) by [xdissent](https://github.com/xdissent) is a bash script that automates this process. I was able to run the script and run my newly created Windows 7 / IE virtual machine shortly afterward.

## Requirements

To start we'll need to download and install VirtualBox. Be sure you have the most recent version available as it gets updated quite often. We'll also need to install the VirtualBox Extension Pack. Both are available on the [VirtualBox Downloads page](https://www.virtualbox.org/wiki/Downloads).

Because the [VPC images](http://www.microsoft.com/en-us/download/details.aspx?id=11575) are quite large (~2.6GB in our case) they have been split up into several files. For the Windows 7 / IE8 image we'll download the following files: 

- [Windows 7 / IE8 - Part 1](http://download.microsoft.com/download/B/7/2/B72085AE-0F04-4C6F-9182-BF1EE90F5273/Windows_7_IE8.part01.exe)
- [Windows 7 / IE8 - Part 2](http://download.microsoft.com/download/B/7/2/B72085AE-0F04-4C6F-9182-BF1EE90F5273/Windows_7_IE8.part02.rar)
- [Windows 7 / IE8 - Part 3](http://download.microsoft.com/download/B/7/2/B72085AE-0F04-4C6F-9182-BF1EE90F5273/Windows_7_IE8.part03.rar)
- [Windows 7 / IE8 - Part 4](http://download.microsoft.com/download/B/7/2/B72085AE-0F04-4C6F-9182-BF1EE90F5273/Windows_7_IE8.part04.rar)

Once the files have been extracted we have created our virtual machine the disk will take up close to 10 GB. Make sure you have enough disk space available. I run my virtual machines on an external USB hard drive which works well if your local hard drive is starved for space.

## Extract the VPC Files

Once you have all of the the VPC image files downloaded you'll need to extract them:

**Windows users**: double-click the Windows_7_IE8.part01.exe file

**Linux / OS X users**: You will need to install unrar. I did so on OS X with Homebrew and there are packages available for Ubuntu as well.

Once you have unrar installed, issue the following command in the directory containing all of the VPC image files:

```
`unrar e -y Windows_7_IE8.part01.exe`
```

This will extract the files and combine them into a single .vhd file. The -y flag tells unrar to say "yes" to the EULA from Microsoft so be aware of that.

## Create a new Machine

Once the .vhd file is ready we can create a new machine in VirtualBox. Start up VirtualBox and click the "New" button:

<img alt="Vbox new" border="0" height="198" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-0.png" title="vbox-new.png" width="518"/> 

Click "Continue" to proceed. 

## VM Name and OS Type

We'll enter a name (IE8 / Windows 7) and select "Microsoft" and "Windows 7" in the Operating System and Version drop-downs:

<img alt="Vbox name and type" border="0" height="345" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-1.png" title="vbox-name-and-type.png" width="600"/>

Click "Continue" to proceed. 

## Memory

Specify how much memory (RAM) you'd like to allocate to the virtual machine. This really depends on how much you have available but it is best to go with the minimum at the very least: <img alt="Vbox mem config" border="0" height="345" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-2.png" title="vbox-mem-config.png" width="600"/>

Click "Continue" to proceed. 

## Disk

Select the "Do not add a virtual hard drive" option.: <img alt="Vbox do not add hdd 1" border="0" height="394" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-3.png" title="vbox-do-not-add-hdd-1.png" width="600"/>

The reason we skip this for now is because we want to add the hard disk as an IDE drive. For some reason VirtualBox adds the disk as a SATA drive which causes the blue screen of death (BSOD) to appear when the virtual machine is booted up.

Click "Continue" to proceed **and** click "Continue" again when presented with the warning about not attaching a hard disk. 

## Review Settings and Create the VM

At this point you can review the settings you've made and click "Create" to complete the process:

<img alt="Vbox review and create" border="0" height="369" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-4.png" title="vbox-review-and-create.png" width="600"/>

## Configure Storage Settings

Highlight your newly created virtual machine and click the "Settings" button. From there, click the "Storage" tab and add a hard disk to the IDE controller: <img alt="Vbox storage add hd" border="0" height="509" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-5.png" title="vbox-storage-add-hd.png" width="600"/>

## Absolute Pointing Device

In the Settings, click on the "System" tab and uncheck "Enable absolute pointing device". I had to do this in order to to get the mouse working properly.

## Start it Up

We're almost there: next we need to start up the VM by clicking the "Start" button. You'll see Administrator and IEUser accounts and the password for both is "Password1". Log in as Administrator and check it out! It's important to note when the virtual machine has the keyboard and mouse focus. When you click inside the virtual machine window, it will capture the input from your mouse and keyboard. To return focus back to your computer you will need to press the "host key" sequence on your computer:

<img alt="Vbox host key" border="0" height="123" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-6.png" title="vbox-host-key.png" width="343"/>

The "host-key" sequence can be configured in the VirtualBox preferences. On my computer, the host-key sequence is the left CTRL key (displayed as Left ^). When the arrow icon is illuminated, the guest computer – Windows 7 in this case, has the focus. When I press the left CTRL key on my computer the arrow icon goes tray to indicate focus has been returned to my computer. 

## Activation

As soon as you log in you will be presented with the Windows Activation wizard. Follow the steps to activate this copy of Windows. Once that is complete you will be prompted to restart your computer. Go ahead and do that.

<img alt="Vbox activate now" border="0" height="487" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-7.png" title="vbox-activate-now.png" width="600"/>

The screen resolution in the virtual machine will be quite low at first — I believe 800x600 is the default. Don't worry about this as it will be addressed in the next step. 

## Guest Additions

Log in as Administrator (Password1) and Install the VirtualBox Guest Additions. To do this,  navigate to Devices in the VirtualBox menu on your computer (the "host" machine"). Choose the menu option to "Install Guest Additions". Each time you are prompted with the "Would you like to install..." dialog, choose "Install":

<img alt="Vbox install guest additions" border="0" height="487" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-8.png" title="vbox-install-guest-additions.png" width="600"/>

This will install some drivers optimized by VirtualBox which allow you to change the screen resolution, improve the interaction between your host computer and the Windows guest operating system. Once the install process is complete you will be prompted to restart your virtual machine once more.

## Finished Product

With Windows activated and the Guest Additions installed you should be able to log in to your very own Windows 7 / IE8 testing machine!

<img alt="Vbox ie8 mr" border="0" height="476" src="/blog/2012/09/test-web-sites-with-internet-explorer/image-9.png" title="vbox-ie8-mr.png" width="600"/>

This free copy of Windows will operate for 30 days and the trial period can be extended twice by running the following at the command prompt:

```
slmgr –rearm
```

Check out [the documentation](http://www.microsoft.com/en-us/download/details.aspx?id=11575#overview) at Microsoft for more details.


