---
author: Mike Farmer
gh_issue_number: 943
tags: devops, environment, tools
title: Provisioning a Development Environment with Packer, Part 1
---



I recently needed to reconstruct an old development environment for a project I worked on over a year ago. The code base had aged a little and I needed old versions of just about everything from the OS and database to Ruby and Rails. My preferred method for creating a development environment is to setup a small Virtual Machine (VM) that mimics the production environment as closely as possible.

### Introducing Packer

I have been hearing a lot of buzz lately about [Packer](https://www.packer.io/) and wanted to give it a shot for setting up my environment. Packer is a small command line tool written in the increasingly popular [Go](https://golang.org/) programming language. It serves three primary purposes:

1. Building a machine based on a set of configuration parameters
1. Running a provisioner to setup the machine with a desired set of software and settings
1. Performing any post processing instructions on that machine

Packer is really simple to install and I would refer you to their [great documentation](https://www.packer.io/docs/installation.html) to get it setup. Once setup, you will have the packer command at your disposal. To build a new machine, all you need to is call

packer build my_machine.json

The file my_machine.json can be the name of any json file and contains all the information packer needs to setup your machine. The configuration json has three major sections: variables, builders, and provisioners. Variables are simply key value pairs that you can reference later in the builders and provisioners sections.

### The Builder Configuration

[Builders](https://www.packer.io/docs/templates/builders.html) takes an array of json objects that specify different ways to build your machines. You can think of them as instructions on how to get your machine setup and running. For example, to get a machine up and running you need to create a machine, install an Operating System (OS) and create a user so that you can login to the machine. There are many different types of builders, but for the example here, I’ll just use the vmware-iso machine type. Here’s a working json configuration file:

```
{
  "variables": {
    "ssh_name": "mikefarmer",
    "ssh_pass": "mikefarmer",
    "hostname": "packer-test"
  },

  "builders": [
    {
      "type": "vmware-iso",
      "iso_url": "os/ubuntu-12.04.4-server-amd64.iso",
      "iso_checksum": "e83adb9af4ec0a039e6a5c6e145a34de",
      "iso_checksum_type": "md5",
      "ssh_username": "{{user `ssh_name`}}",
      "ssh_password": "{{user `ssh_pass`}}",
      "ssh_wait_timeout": "20m",
      "http_directory" : "preseeds",
      "http_port_min" : 9001,
      "http_port_max" : 9001,
      "shutdown_command": "echo {{user `ssh_pass`}} | sudo -S shutdown -P now",
      "boot_command": [
        "<esc><esc><enter><wait>",
        "/install/vmlinuz noapic ",
        "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/precise_preseed.cfg ",
        "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",
        "hostname={{user `hostname`}} ",
        "fb=false debconf/frontend=noninteractive ",
        "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",
        "keyboard-configuration/variant=USA console-setup/ask_detect=false ",
        "initrd=/install/initrd.gz -- <enter>"
      ]
    }
  ]
}
```

The [documentation](https://www.packer.io/docs/templates/builders.html) for these settings is really good but I want to point out a few things that weren’t immediately clear. Some of these pertain mostly to the vmware-iso builder type, but I believe they are worth pointing out because some of them apply to other builder types as well. 

First, the iso_url setting can be either an absolute path, a relative path, or a fully qualified url. The relative path is relative to the directory where you run the packer command. So here, when I run packer, I need to make sure that I do so from a directory that has an os subdirectory with the ubuntu iso located therein.

Next, once the ISO is downloaded, packer will automatically start up your VMWare client and boot the virtual machine. Immediately after that, packer will start up a [VNC client and server](https://en.wikipedia.org/wiki/Virtual_Network_Computing) along with a mini web server to provide information for your machine. The http_port_min and http_port_max specify which ports to use for the VNC clients. Setting them to the same will allocate just that port for it to use. The http_directory setting provides the name of a local directory to use for the mini web server as the document root. This is important for providing your VM with a preseed file, more about the preseed file will be discussed below.

Since we are using Ubuntu as our main machine, we will need to use sudo to send the shutdown command. The shutdown_command setting is used to gracefully shut down the machine at the conclusion of the run and provisioning of the machine.

### Installing your OS

The boot_command is a series of keystrokes that you can send to the machine via VNC. If you have setup a linux machine from scratch you know that you have to enter in a bunch of information to the machine about how to set it up for the first time such as time zone, keyboard layout, how to partition the hard drive, host name, etc. All these keystrokes needed to setup your machine can be used here. But if you think about it, that’s a ton of keystrokes and this command could get quite long. A better way to approach this is to use a preseed file. A [preseed.cfg](https://help.ubuntu.com/lts/installation-guide/s390x/apb.html) file contains the same information you enter when you setup a machine for the first time. This isn’t something provided by packer, but it is provided by the operating system to automatically provision machines. For Ubuntu, a preseed file is used like so:

- When you boot from the startup media (in this case an iso), you can choose the location of the preseed file via a url
- The preseed file is uploaded into memory and the configuration is read
- The installation process begins using information from the preseed file to enter the values where the user would normally enter them.

So how do we get the preseed file up to the machine? Remember that little web server that packer sets up? Well, the ip and port is made available to the virtual machine when it boots from the ISO. The following line tells the OS where to find the web server and the configuration file:

```
 "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/precise_preseed.cfg"
```

Strings in packer can be interpolated using a simple template format similar to [moustache](http://mustache.github.io/). The double curly braces tells packer to insert a variable here instead of text. The HTTPIP and HTTPPort variables are made available by packer to the template.

One more important note about the preseed file, you need to make sure that the settings for the username and password are the same as listed in your variables section so that you can login to the machine once it is built. Where do you get a preseed file? I found [one on a blog titled Packer in 10 Minutes](http://kappataumu.com/articles/creating-an-Ubuntu-VM-with-packer.html) by [@kappataumu](https://twitter.com/kappataumu). I only had to modify a few settings that were specific to my setup

Remember that http_directory mentioned above? Well, that directory needs to include your preseed file. I’ve named mine pricise_preseed.cfg for Ubuntu 12.04 Precise Pangolin.

Next up is provisioning but that is such a big topic by itself that I’ll move that into a separate blog post. The config file above will work as-is and once run it should setup a basic Ubuntu server for you. Go ahead and give it a try and let me know in the comments how it worked out for you.

### Super Powers

I said that packer has 3 primary purposes earlier. Well, I lied. Packer’s super power is that it can perform those 3 purposes over any number of machines, whether virtual, hosted, or otherwise in parallel. Supported machines are currently:

- Amazon EC2 (AMI)
- DigitalOcean
- Docker
- Google Compute Engine
- OpenStack
- QEMU
- VirtualBox
- VMware

Consider for a moment that you can now automatically setup and provision multiple machines with the same environment using a single command. Now you are seeing the power of Packer. 

