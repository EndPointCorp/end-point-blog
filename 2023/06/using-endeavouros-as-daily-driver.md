---
author: "Muhammad Najmi bin Ahmad Zabidi"
title: "Using EndeavourOS as a daily driver"
github_issue_number: 1983
date: 2023-06-16
tags:
- linux
---

![A nearby mountain skyline lies against an overcast sky. The lower hills are obscured on the edges by close green trees in the foreground, which lead toward US freeway signs in storage.](/blog/2023/06/using-endeavouros-as-daily-driver/freeway-signs.webp)

<!-- Photo by Seth Jensen, 2023 -->

### Choosing a new distro

I have been using Manjaro Linux (based on Arch Linux) for my work desktop and Pop!\_OS (based on Ubuntu) for my laptop for quite some time now, and wanted to find another Arch Linux-based distro for my daily driver. Rather than aimlessly searching through the hundreds of Linux distros out there, I made several requirements the chosen distro should meet:

- Easy to maintain.
- Has strong community support and stable development.
- Has a Linux Unified Key Setup (LUKS) full-disk encryption option in the installation.
- If possible, the distro of choice should be able to trim down the number of default packages. For example, I am a Gnome desktop user, so I don’t want to install the game packages I won't use.

I decided to use [EndeavourOS](https://endeavouros.com). It supports the features that I need: It has a strong community and most of Arch Linux's documentation/​references are still applicable to it, like they are to most Arch Linux-based distros using `systemd`.

The most notable differences between EndeavourOS and Arch Linux are EndeavourOS's GUI-based installer—we can select between installing XFCE, Plasma KDE, Gnome, and several others desktop environments—as well as wallpapers and some other tools, for instance, EndeavourOS QuickStart Installer and EndeavourOS log tools.

Also, EndeavourOS notifies the user when there are pending OS updates, making it easy to keep my box up to date, especially when I am busy during the week and forget to apply important OS updates!

### Installation

EndeavourOS is quite easy to install. The Linux Unified Key Setup (LUKS) encryption option is available during the installation process. (Any distro using the [Calamares](https://calamares.io) installer tool will also have this feature.)

After the basic installation, I usually need to do some other customizations before it's suitable for daily usage.

### Starting services

One thing that I noticed is that by default the cron service is not enabled. After checking online, I found that I have to enable the `cronie` service first.

Bluetooth is another service that isn't running by default. If you want Bluetooth and cron jobs to start automatically, first check whether they are running with:

```plain
systemctl status cronie bluetooth
```

Enable them with:

```plain
systemctl enable --now cronie bluetooth
```

Check the service status again:

```plain
systemctl status cronie bluetooth
```

### Diving a bit into AUR

Some modern Arch Linux variants come preloaded with [yay](https://aur.archlinux.org/packages/yay-git), an AUR (Arch Linux User Repository) helper written in the Go language.

[ksshaskpass](https://invent.kde.org/plasma/ksshaskpass) is a KDE-based ssh-askpass client. We can install it with `yay`. Check the package's availability first:

```plain
$ yay -Ss ksshaskpass

aur/ksshaskpass-git 5.22.80_r196.gdaa2679-1 (+6 0.00)
    ssh-add helper that uses kwallet-git and kpassworddialog
extra/ksshaskpass 5.27.3-1 (29.7 KiB 101.9 KiB) [plasma] (Installed)
    ssh-add helper that uses kwallet and kpassworddialog
```

Since I already installed ksshaskpass, we can see that the status is indicated as “Installed”. If you want to install it for the first time, just type `yay -S ksshaskpass`.

### Printing

Support for printing is quite easy to set up. It has an application helper which is most useful for newbies, but could also be useful for seasoned Linux users who might have missed the boat for new applications. Since Arch Linux-based distros can use AUR, many packages which are provided independently and do not have an official repository can be updated with the `yay` command.

I am using a Canon E410 printer, and in the event that the printer is not detected right away by the OS, we can use the CUPS configuration tool (accessible at `localhost:631`) to configure the printing server. If you are using Gnome, you can also try to add the printer through Gnome's printer selection in its settings.

### Desktop environment: Gnome

I like to assign hotkeys for workspace navigation. I usually use Alt+1, Alt+2, Alt+3, and Alt+4 to switch to the Workspace 1, 2, 3, and 4, respectively.

In Gnome, this can be done by opening the settings app and doing the following:

Go to Keyboard → Keyboard Shortcuts → View and Customize Shortcuts → Navigation → Switch to Workspace #

Apart from the GUI goodness, I also use [Oh My Zsh](https://ohmyz.sh/) for my Zsh shell and [Oh My Posh](https://ohmyposh.dev/) for Bash. You can see how to install them on their respective sites.

### Bash config

I have my own shell configurations but I want to highlight my setup for Oh My Posh, ksshaskpass, and Vim:

```plain
POSHTHEME="easy-term"
eval "$(oh-my-posh --init --shell bash --config ~/.poshthemes/$POSHTHEME.omp.json)"

export SSH_ASKPASS=/usr/bin/ksshaskpass
export EDITOR=/usr/bin/vim
```
