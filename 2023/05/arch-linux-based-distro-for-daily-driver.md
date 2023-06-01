---
author: "Muhammad Najmi bin Ahmad Zabidi"
title: "Arch Linux based distro for daily driver"
github_issue_number: 
date: 2023-05-31
tags:
- Linux
- Arch Linux
---

I have been using Manjaro Linux (Arch Linux-based) for my work desktop and PopOS (Ubuntu-based) for my laptop for quite some time now and feel that I want to search for another Arch Linux-based distro for my daily driver. Rather than endlessly searching for hundreds (or maybe even thousands) of Linux distros out there, I put my several objectives that the distro that will be chosen should be:
- Easy to maintain 
- Has a strong community support and stable development, otherwise I will need to search for another distro again
- Has Linux Unified Key Setup (LUKS) option in the installation
- If possible, the distro of choice should be able to trim down the number of default packages (for example, I am a Gnome desktop user, so maybe I don’t have to install the games packages which I rarely used). 

I then decided to use [EndevourOS](https://endeavouros.com). It has a strong community and most of Arch Linux's documentations/references still applicable on this distro.

### Installation
EndevourOS is quite easy to install. It supports the features that I need. Linux Unified Key Setup (LUKS) encryption option is available during the installation process (however, distros that use [Calamares](https://calamares.io) installer tool also have this feature available too). Arch Linux’s documentation mostly still applies to Manjaro, EndevourOS and probably most Arch Linux variants out there, as long as they are using systemd. After the basic installation, I usually need to do some other customizations before I am able to use it for my daily usage.

### Printing
The printing support is quite easy to set up
It has some application helper (most likely useful for the newbie, but could be useful for the seasoned Linux users who might have missed the boat for the new applications). I remember that when I installed Manjaro, there is an application called as “manjaro-application-utility” in Manjaro Linux. Since Archlinux-based distro could use AUR - many packages which are provided independently and do not have an official repository could be updated with the “yay” command. The AUR and yay tool will be explained later. 

I am using Canon E410 printer, and in the event that the printer is not detected right away by the OS, we can use either CUPS configuration tool (accessible at https:localhost:631) or if you are using Gnome, you can try to add the printer through Gnome's printer selection in its settings. 

### Starting services
If you want Bluetooth and cronjob to start automatically, check with
systemctl <service name> status

One thing that I noticed is that, by default the cron service is not enabled.I  have set up my cron job in the normal userland, however I noticed that the cron is not running. So after I checked online, seems that I have to enable the “cronie” service first.

## Cronie
```plain
# systemctl status cronie
# systemctl enable cronie
# systemctl status cronie
```

##  Bluetooth
```plain
# systemctl status bluetooth
# systemctl enable bluetooth
# systemctl status bluetooth
```

### Desktop Environment - Gnome
  
Gnome user - assign desktop switching hotkey for the workspace navigation (the other desktop environments may have different ways to assign the keys). 

I usually use Alt 1, Alt 2, Alt 3 and Alt 4 to switch to the Workspace 1,2,3 and 4, respectively.

This can be done with:
Open the Settings app
Go to Keyboard -> Keyboard Shortcuts -> View and Customize Shortcuts -> Navigation -> Switch to Workspace 1 (until 4)

Apart from the GUI goodness, I also use “Oh My Zsh” for my ZSH shell and also “Oh My Posh” or Bash. You can refer to the installation method from their respective sites.

Diving a bit on AUR

In the modern Archlinux’s variants - sometimes they already came with [“yay”](https://aur.archlinux.org/packages/yay-git) - an AUR (Arch Linux User Repository) helper which is written in the go language. For work related tool, we could consider installing the following packages
zoom
skype
Microsoft Edge browser (Bing with chatGPT - conversational method, seems to only work with Microsoft Edge, just in case you want to try it).
WPS Office (if you are using it).

On my Bash config

I have my own shell configurations but I just want to highlight on this:
```plain
POSHTHEME="easy-term"
eval "$(oh-my-posh --init --shell bash --config ~/.poshthemes/$POSHTHEME.omp.json)"

export SSH_ASKPASS=/usr/bin/ksshaskpass
export EDITOR=/usr/bin/vim
```
  
[ksshaskpass](https://invent.kde.org/plasma/ksshaskpass) is a KDE based sshaskpass client. We can install it with “yay”

Check the availability first:
```plain
yay -Ss ksshaskpass

aur/ksshaskpass-git 5.22.80_r196.gdaa2679-1 (+6 0.00) 
    ssh-add helper that uses kwallet-git and kpassworddialog
extra/ksshaskpass 5.27.3-1 (29.7 KiB 101.9 KiB) [plasma] (Installed)
    ssh-add helper that uses kwallet and kpassworddialog
```
Since I already installed ksshaskpass, we can see that the status indicated as “Installed”. If we want to install it for the first time, just type ```“yay -S ksshaskpass”```.

In conclusion, Arch Linux-based distros mostly have to same base and tool, except a few and have their own community. Arch Linux itself  is quite stable and able to ease up the users’ time to maintain their daily computer. 
