---
author: Ian Neilsen
title: "systemd: A primer from the trench's"
tags: hosting, systemd, systemctl 
---

#systemctl - lets get back to basics

''help me systemd you are my only hope''. If we start back at the beginning, sometimes going back to day dot
often brings clarity to what seems like hopeless or frustrating situation for users from SysV world. Caveat, 
I previously worked at Red Hat for many years before joining the excellent team at End Point and have been using systemd for as long. 
I quite honestly have forgotten most of the SysV or init days. Although at End Point we work daily on Debian, Ubuntu, Centos and BSD variants.

So here is a short and sweet primer to get your fingers wet, before we dive into some of the heavier subjects with systemd.

Did you know that systemd has many utilities it can run:

* systemctl
* timedatectl
* journalctl
* loginctl
* notify
* Analyze - analyze system
* Cgls - show cgroup tree
* cgtop
* N spawn

systemd for want of keeping thinigs simple in unix terms also runs several daemons
 - systemd, journald, networkd, loginduser, timedated, udevd, system-boot, tmpfiles and session 
 
That’s a long way from the old init days. But in all essence it’s not that far from SysV. The one thing that stands out to me
 is we have more information with less typing then previously. That can only be a good thing right??
 
Well lets see! There are many many web pages out there that list systemd or systemctl switches/flags. 
However in everyday use I want to speed up the work I do, I want information at my fingertips and quite honestly in the
day and age of being human friendly, having flags and switches which mean something sure does make it easier.

### Daily List of systemctl
Below is a good daily list of systemctl commands versus their SysV counterpart. Go ahead and run each command 
to get a feel for what it displays.

Remember each command usually has switches/flags you can use. 
A good example is using the ```-l``` flag when checking a failing service such as; ```systemctl status httpd -l```. 
Usually will output enough information to diagnose the problem without going to the logs and or journalctl. 


##### systemctl versus old school explanation. The terminal command followed by flags and explanation. 


*Pro Tip 1*

Before you begin playing with the commands, you should install ```bash-completion.noarch```. Some distro's don't auto complete with systemd until you
install bash auto completion and you miss out on a ALOT of systemctl. Just having auto-completion really helps alot.

Lets start at the top and work down;

```systemctl``` 

```service```

Used in conjunction with ABRT can show you some great debug info and runtime metadata, categorised groupings.
tab out when you type in systemctl and you will see many optional arguments. Choose one and then tab again to see its options/args.


```systemctl status```

```service --status-all```

Check all system services status. Normally during a server update I will run this and output it to a file. 
When the server reboots I can run it again and diff this file to ensure all things started. The output is great. It shows me the 
PID path and potentially the arguments which were run for the process or service. Saves me ps'ing the process.

```systemctl status serviceName -l```


```service serviceName status```

Check the service/process status. The ```-l``` switch will output more for that service. A similar command might be ```
journalctl -xe```

```systemctl enable NameofService```

```chkconfig on ServiceName```

You might find on some distro's that chkconfig is still present. It doesn't do what you think it does!

```systemctl start/stop/restart httpd```

```service httpd start/stop/restart```

As it suggests, start,stop,restart services/processes.

```systemctl reload httpd```

```service httpd reload```

Perform a graceful reload of a configuration you may have just changed. 


```systemctl daemon reload```

Graceful reloads of configuration files on a running service/process. See below for an explanation of “daemon reload”.

```systemctl list-unit-files```

Good flags: --type=service

```ls /etc/rc.d/init.d/```
```ls /etc/rc.d/rc.local```

Prints from  /usr/lib/systemd/system/ and /etc/systemd/system/
Slightly different to list-units, rarely used but has any interesting output. You may want to use this in any 
monitoring scripts you write.

```systemctl list-units```
Good flags -a (--all)

```chkconfig --list``` or ```ntsysv```
```ls /etc/rc.d/init.d/```
```ls /etc/rc.d/rc.local```
```sysv-rc-conf```
```Initctl list```

Anyone see the problem between the two cmd passes? I prefer to use ‘list-units’ over ‘list-unit-files’. 
It shows more information and is shorter to type. List all active services using systemctl. 
Or you could install the sysvinit-utils, which by default are not installed.

```systemctl list-sockets```

```systemctl list-timers```


```systemctl list-jobs```
Requires further explanation in another blog post.

```systemctl --failed```
Show me failed services. Systemctl status will highlight at the top if units have failed, especially after a reboot.

```systemctl get-default```

```Runlevel```
```Chkconfig --list```
```sysv-rc-conf```
```ntsysv```
```ls /etc/rc.d/rc.local```
```ls /etc/rc.d/init.d```

Gets the run level which i sdefault for the system. NOt often used if rarely but good know when you start having boot issues or need
to swap out to a different run level to fix things.

```systemctl shutdown or reboot```

```shutdown -r now```

Reboot/shutdown the system. Personally I use ‘shutdown -r now’ still.


```systemctl cat serviceName```

```cd to dir, cat init file```

Shows me the system service(unit) file contents and options.

```systemctl list-dependencies serviceName```

What’s really depending on my process. The --all flag will show everything --before, --after, --reverse
Pretty handy little dependency checker for processes.

```systemctl show serviceName```
-p - shows a single property of a service. Shows more than using ‘systemctl cat servicename’.
Dont forget TAB is your friend. running the ``-p`` flag and using TAB will help you.


```systemctl mask serviceName```

```Update-rc.d serviceName disable```

Never want someone starting a service EVER!! 'Mask' is your friend and a little sneaky. See if your system admins 
pick this one up. Good April fools day. ‘’unmask’’ to return it to its user

```systemctl edit serviceName```
Good flags --full

```vim /etc/inittab```

Yes that’s right, edit the service file without having to cd into the directory. Now that saved me a bit of time.
Careful with this. The plain edit creates an override file in /etc/systemd/system to complement the original unit file. 
If you need to edit the original unit file use the ```--full``` flag.

```Systemctl --output=```
Good Flags =verbose

Particular good if you have a bad service which is playing up. Outputs a short standard message or a very terse verbose message
using different flags.

```systemctl isolate```

This deserves its own small blog post. Isolate can be used to rescue systems automagically following kernel reboot 
failures, but requires some special work.


## Gotchas

1. Sometimes you need to use the suffix such as ‘config_file@openvpn.service’. 
2. Usually if you don't use the suffix, systemd will think it is a .service
3. If you want multiple services running use the suffix, such as two sshd services or distinct openvpn servers.
4. Mount points will always be determined as mount points.
5. Gracefully reloading configs can be done using “reload”  
systemctl reload httpd
6. If you have made a lot of configuration changes and want to gracefully load these without restarting everything try  
systemctl daemon reload
7. This is not the same as the above “reload” action. Daemon reload is for systemd and not the unit files it controls. This is a safe command to run since it keeps sockets open while it does its thing.
8. Reboots on newer systems only really need to be done when new kernels are presented. Systemd is gracious and good at processing new packages and enabling these changes during a yum update.
9. Autocomplete on Centos is not present until you install “bash-completion and “bash-completion-extras”. Systemctl takes on a life of it’s own, when you install these two utilities. Tabbing out will list all systemctl options. Very handy!!
yum install bash-completion bash-completion-extras
10. Systemd does not use the /etc/inittab file even if you have them present.
11. Converting your init’s to systemd is easy than you think. Create a systemd unit file and add in 10 basic lines to call the bin or init script. YOU have basically created a systemd managed init script. Don’t forget to go back and one day convert it completely. For the basic lines you need, see next week's blog post on unti files.
12. Targets vs runlevels - A target in systemd is a runlevel in sysV, Names replace numbers; runlevel3 = multi-user.target, runlevel1 = rescue.target


## Who's got the goods on speed - ```systemd-analyze```

Is systemd faster than sysv-init? Parallel processing says it is? You be the judge! 

One great test is to build a new machine which doesn't have systemd installed. Reboot the machine and check your boot time. 
On an older SysV system you may have use “tuned”, “systemtap”, “numastat” etc to gather performance information.

Then install systemd. Better still, upgrade from a old version of linux to a new version of linux from ‘init’ to ‘systemd’ 
then run ‘systemd-analyze’

‘systemd-analyze’ will show you boot times. Notice that systemd starts less services at boot because systemd only starts 
what is necessary to get the server booting.

Not a bad way to collect a baseline on a newly built server. Add it to your ansible facts for the server so you have a 
historical view and collection of boot times. In fact add it to your monitoring system and be proactive in your monitoring 
of client server boot times, while performing your maintenance cycles.

OK ok but how do I see what is taking its sweet time during boot or what is borking your beautiful server following an 
update/upgrade... Wonder no more!!

```bash 
$ systemd-analyze blame
$ systemd-analyze time
```

For example on my system, I can see that my top 10 culprits to a potentially slow boot are;

```bash
@local-ian ~]$ systemd-analyze blame
          7.346s dracut-initqueue.service
          6.787s systemd-cryptsetup@luks.service
          5.378s NetworkManager-wait-online.service
          2.308s abrtd.service
          1.444s docker.service
          1.395s plymouth-quit-wait.service
          1.358s lvm2-pvscan@8:1.service
          1.145s lvm2-pvscan@253:0.service
          1.072s fwupd.service
           609ms docker-storage-setup.service
```
I might disable the docker service by ```systemctl disable docker``` and start it when I need it.

## Too many typing - I type enough everyday and a have bzillion servers

*Pro Tip 2*

I have a server which needs a service restarted or checked constantly. Running systemctl remotely will show me or 
allow me to do this.

```systemctl status sshd -H root@server.address.com```

I might make an alias for it. Obviously this is a pretty useless example, if you’re having to manually do this for a 
service/process you should fix the problem on the server. However for edge cases it can be quite handy.

*Pro Tip 3*

Figure out what targets/runlevel a target runs at. We will touch on 'WANTS' in next weeks 'UNIT' files journey.

```systemctl show httpd -p “wants” multi-user.target```

Vs

```insert sysv option```

*Pro Tip 4*

Check processes, service association and top. You can still grep/awk the output if you wish.
Instead of using ps or top use the following;

```$ systemd-cgls``` 
```$ systemd-cgtop```

Vs 

```ps xawf -eo pid,user,cgroup,args```



I know this is only touching the surface of systemctl or systemd as whole, however from a day-to-day context this should help
 newbies to the systemctl world.
 
Each week I will try and delve deeper into unit files, unit targets, systemctl isolate and slices, followed by a small primer 
on journalctl, timedatectl, loginctl.

Stay tuned next week for hero to zero on unit files.



