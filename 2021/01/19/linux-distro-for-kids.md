---
author: Muhammad Najmi Ahmad Zabidi 
title: 'Linux Distro for Kids'
tags: linux, kids, distro
gh_issue_number: 1656
---
We were done with the year 2020, with some of us needing to work at home taking care of the kids themselves as the childcare are probably not allowed to operate (temporarily) due to the Covid-19 pandemic. This writing will not complain about the pandemic, rather sharing the author's experience.

I previously installed several Linux distros for my kids' desktop computer but then I find it quite difficult to get a fair control between a strict no-no or no control at all. Then I came across with [Endless OS](https://endlessos.com/) - a Linux distro which was built based from Debian but with heavy customizations.

###Installation
The installation process was smooth and easy. The installer's image that I chose was quite huge though - it was around 16GB. But then given we could just use USB disk as the installation medium nowadays then this should not be a big issue.  Endless OS' installer does not seems to give option to encrypt my hard disk with LUKS during the installation phase.

Endless OS is powered by [OSTree](https://people.gnome.org/~walters/ostree/doc-onepage/) (which is defined as "a system for versioning updates of Linux-based operating systems") and [Flatpak](https://flatpak.org/). The default environment is a customized Gnome.
The website says "Endless OS uses OSTree, a non-destructive and atomic technique to deploy operating system updates. That means updates can be installed without affecting the running state of the system, making the process safe and robust from environmental factors such as a sudden power loss."

According to its website, the operating system is free for individuals and non-commercial use up to 500 computers. 

![](end-point-blog/2021/01/19/linux-for-kids/desktop.png)

###Package installation and packge updates
We could use several ways to install new packages (or to update them). One way of doing it is by using the Control Centre and the other one (if we want to install remotely) is by using the command line. Although Endless OS is based on Debian, the apt-get command does not work here. You could use Flatpak's command for e.g `flatpak install <package name>`. Flatpak is quite helpful in assisting the user to install a new package - in a way that if you just typed the package name half correctly then it will suggest the approximately similar name so that you would be able to choose the correct package's name.  
For Flatpak related introduction and commands, you can refer them [here](https://itsfoss.com/flatpak-guide/)

![](/2021/01/19/linux-for-kids/installer-reduced.png)

![](/2021/01/19/linux-for-kids/app-centre-reduced.png)

![](/2021/01/19/linux-for-kids/flatpak-update.png)

###Package control
By default, the OpenSSH service is not enabled. The user need to enable the connection through the GUI based `Settings->Sharing->Remote Login`.

![](/2021/01/19/linux-for-kids/sharing-ssh.png)

![](/2021/01/19/linux-for-kids/sharing-ssh2.png)
 
We could limit the type of applications that the user could use on Endless OS. For example, we could disable the browser from being used from the Control Centre, and the user could use the other applications but not the browser. Also, the default administrative level user in Endless OS is ***administrator*** - and then you can run the sudo command ever here (in the other words, the “administrator” user is included in the “sudo” group. However you could just drop your SSH key in the root account if you insist on using the root login to get into the shell account. In my experience, I also need to remove the "shared" user account as it does not ask for any password. The kids in the house will have to use the account that I created and assigned for them.  


![](/2021/01/19/linux-for-kids/parental-control-reduced.png)

We could disable browser in the parental control settings, however we could not define where they could/could not go from the settings.

![](/2021/01/19/linux-for-kids/parental-control2.png)


As Endless OS is running unlike the other Linux distros - fortunately you can still do your work inside it if you need to - by using [Podman](https://support.endlessos.org/en/apps/podman) inside it. 

###Browsing management
I tried to search for the related contents for the Internet management however I could not find one. My office colleague's previously [wrote](https://www.endpoint.com/blog/2020/12/03/pihole-great-holiday-gift) about Pi-hole, so I decided to give a try. I found a tutorial on using Pi-hole in a container, for example [this note](https://codeopolis.com/posts/running-pi-hole-in-docker-is-remarkably-easy/). I did a minor modifications from the docker's note that I previously referred. As Endless OS has already podman shipped within, we can just use the docker's command or adapt it to podman . So this is what I did (changed the --restart flag to --restart=always and use podman). The rests are similar as in the original note

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

We could then later browse Pi-hole’s admin page by going to  `http://<server>/admin`

![](/2021/01/19/linux-for-kids/pi-hole-eos2-reduced.png)

### Conclusion
I like Endless OS for my kid’s usage, however I think the distro needs a lot of help from the community to make it appealing to the working adults too. I previously found that I could not get the curl package to be installed from the flatpak command (and I could not use the apt-get command too to install it). So what I did what I build curl with the manifest file that Ireferred from [here](https://community.endlessos.com/t/package-installer/9314/2)

![](/2021/01/19/linux-for-kids/curl-build.png)

The points that I love about this distro: browser management, flatpak to install latest software/games from flathub. I might be seeing other points too later once I use it more and more. As for now, whatever they are offering to me is already enough. Maybe what I need is a screen time management and an internal URL blocking manager rather than installing an external application. 

That is all that I could write about the Endless OS after a few weeks of usage on my kid’s computer. If you have been using it too and want to add useful information, please let me know.



