---
author: Muhammad Najmi bin Ahmad Zabidi
title: 'Endless OS: A Linux Distro for Kids'
github_issue_number: 1714
tags:
- linux
- kids
date: 2021-01-20
---

![Mom & daughter working at a computer](/blog/2021/01/linux-distro-for-kids/kid-at-computer.jpg)
[Photo](https://www.pexels.com/photo/mother-helping-her-daughter-with-her-homework-4260323/) by [August de Richelieu](https://www.pexels.com/@august-de-richelieu)

In 2020 some of us had to work from home while taking care of the kids ourselves, as most childcare services are temporarily closed due to the COVID-19 pandemic. In this post I won’t complain about the pandemic, but rather share my experience.

I have installed several different Linux distributions for my kids’ desktop computer in the past, but have found it quite difficult to find a balance between strict parental controls and no parental controls at all. Then I came across [Endless OS](https://endlessos.com/), a Linux distro based on Debian, but with heavy customizations to focus on school from home.

### Installation

The installation process was smooth and easy. The install image I chose was quite huge though, at around 16GB. But given we can just use a USB drive as the installation medium nowadays this should not be a big issue. The installer does not seem to give an option to encrypt my hard disk with LUKS during the installation phase.

Endless OS is powered by [OSTree](https://people.gnome.org/~walters/ostree/doc-onepage/) (which is defined as “a system for versioning updates of Linux-based operating systems”) and [Flatpak](https://flatpak.org/). According to the website, “Endless OS uses OSTree, a non-destructive and atomic technique to deploy operating system updates. That means updates can be installed without affecting the running state of the system, making the process safe and robust from environmental factors such as a sudden power loss.”

The default window manager is a customized Gnome.

According to its website, the operating system is free for individuals and non-commercial use up to 500 computers.

![](/blog/2021/01/linux-distro-for-kids/desktop.jpg)

### Package installation and package updates

We can choose from a couple of ways to install new packages (or update them). You can either use the Control Centre, or (if you want to install remotely) the command line. Although Endless OS is based on Debian, the `apt` command does not work here. Instead you can use Flatpak, with commands like `flatpak install <package name>`. Flatpak assists the user when installing a new package. For example, if you just typed the package name half correctly, it will suggest a similar name so that you can choose the correct package’s name.

It’s FOSS has [a guide to using Flatpak](https://itsfoss.com/flatpak-guide/).

![](/blog/2021/01/linux-distro-for-kids/installer.png)

![](/blog/2021/01/linux-distro-for-kids/app-centre.jpg)

![](/blog/2021/01/linux-distro-for-kids/flatpak-update.jpg)

### Package control

By default, the OpenSSH service for remote shell login is not enabled. The user needs to enable it through the GUI settings in `Sharing->Remote Login`.

![](/blog/2021/01/linux-distro-for-kids/sharing-ssh.png)

![](/blog/2021/01/linux-distro-for-kids/sharing-ssh2.png)

We can limit the type of applications enabled on Endless OS. For example, we could disable the web browser from the Control Centre, while maintaining use of the other apps. The default administrative level user in Endless OS is **administrator**, with sudo privileges. In other words, the “administrator” user is included in the “sudo” group. However, you could just drop your SSH key in the root account if you insist on using the root login to get into the shell account. I also had to remove the “shared” user account as it does not ask for any password. The kids in the house will have to use the account that I created and assigned to them.

![](/blog/2021/01/linux-distro-for-kids/parental-control.png)

We could disable the browser in the parental control settings, however we could not define where they could/​could not go from the settings.

![](/blog/2021/01/linux-distro-for-kids/parental-control2.png)

Although Endless OS is unlike other Linux distros, you can fortunately still do your work inside it if you need to using [Podman](https://support.endlessos.org/en/apps/podman).

### Browsing management

I tried to search for similar control for my network, but couldn’t find a good option. My colleague previously [wrote](/blog/2020/12/pihole-great-holiday-gift) about Pi-hole, so I decided to give a try. I found a [tutorial](https://codeopolis.com/posts/running-pi-hole-in-docker-is-remarkably-easy/) on using Pi-hole in a container, and made minor changes from that. As Endless OS ships with podman included, we can use the docker command or adapt it to podman. So I changed the --restart flag to --restart=always and used podman. The rest is similar to the original post.

```bash
podman run \
--name=pihole \
-e TZ=Asia/Kuala_Lumpur \
-e WEBPASSWORD=YOURPASS \
-e SERVERIP=YOUR.SERVER.IP \
-v pihole:/etc/pihole \
-v dnsmasq:/etc/dnsmasq.d \
-p 80:80 \
-p 53:53/tcp \
-p 53:53/udp \
--restart=always \
pihole/pihole
```

We can then browse Pi-hole’s admin page by going to `http://<server>/admin`.

![](/blog/2021/01/linux-distro-for-kids/pi-hole-eos.png)

### Conclusion

I like Endless OS for my kid’s usage, however I think the distro needs a lot of help from the community to make it appealing to working adults too. I previously found that I could not install the curl package with flatpak (and I could not use apt to install it). So I built curl with a manifest file from [here](https://community.endlessos.com/t/package-installer/9314/2).

![](/blog/2021/01/linux-distro-for-kids/curl-build.png)

The things I love about this distro are browser management and flatpak for installing the latest software/​games from flathub. There may be more points I like as I use it more and more. As for now, the current offerings are already enough. Maybe what I need is a screen time management and an internal URL blocking manager rather than installing an external application.

These are my main observations of Endless OS after a few weeks of usage on my kid’s computer. If you have also used it and have any useful information to add, please leave a comment below.
