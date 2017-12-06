---
author: Ian Neilsen
title: "systemd: A primer from the trench's"
tags: hosting, systemd, systemctl 
---

# systemctl - lets get back to basics

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
Lets start with a good daily list of systemctl commands versus their SysV counterpart. Go ahead and run each command 
to get a feel for what it displays.

Remember each command usually has switches/flags you can use.
 
A good example is using the ```-l``` flag when checking a failing service such as; ```systemctl status httpd -l```. 
The -l flag will usually output enough information to diagnose a service start or reload problem without having to go into the logs. 


##### systemctl versus old school explanation. The next few lines will list out the command followed by flags and explanation.

example:

```systemd command/s```

```sysv command/s``` 


**Pro Tip 1**

Before you begin playing with the commands, you should install ```bash-completion.noarch```. Some distro's don't auto complete with systemd until you
install bash auto completion. Without tab auto-completion you miss out on a ALOT of systemctl.

As an example when you `TAB` for completion you will see many of the systemctl options;

```bash
local-ian ~]# systemctl 
add-requires           condstop               edit                   halt                   is-failed              list-dependencies      mask                   reload-or-restart      set-environment        status                 unset-environment
add-wants              daemon-reexec          emergency              help                   isolate                list-jobs              poweroff               reload-or-try-restart  set-property           stop                   
cancel                 daemon-reload          enable                 hibernate              is-system-running      list-sockets           preset                 rescue                 show                   suspend                
cat                    default                exit                   hybrid-sleep           kexec                  list-timers            reboot                 reset-failed           show-environment       switch-root            
condreload             delete                 force-reload           is-active              kill                   list-unit-files        reenable               restart                snapshot               try-restart            
condrestart            disable                get-default            is-enabled             link                   list-units             reload                 set-default            start                  unmask 
```

Lets start at the top and work down;

1.

```systemctl``` 

```service```

Used in conjunction with ABRT can show you some great debug info and runtime metadata, categorised in their respective groupings of loaded, 
active, running and a description of the unit.

2.
```systemctl status```

```service --status-all```
or
```initctl list```. If jobs are started in upstart on Ubuntu systems you will need to run this as well as `service --status-all`

Check all system services status. Normally during a server update I will run this and output it to a file. 
When the server reboots I can run it again and diff this file to ensure all things started. The output is great. It shows me the 
PID path and potentially the arguments which were run for the process or service. Saves me `ps`'ing the process.

Note, each distro deals differently with `service --status-all` output. 

3.
```systemctl status serviceName -l```

Good flags: is-active or -a 

```service serviceName status```

As it suggests, show me the status and information related to the service Unit file. Other good info includes is the service enabled or
is chkconfig on, uptime, PID and CGroup info, plus any other information associated with the service. 

Tip: 
* use the -l flag
* To view more than one service group services in {} braces, i.e.  {httpd,mysql,postfix}

4.
```systemctl enable NameofService```

Flags: disable

```chkconfig on ServiceName```

Flags: on or off

You might find on some distro's that chkconfig is still present. It doesn't do what you think it does with systemd systems.

Tip:
* No tip on this, just remember, `enable` vs `chckconfig` and you will be swell.

5.
```systemctl start/stop/restart httpd```

Good flags: reload-or-restart

```service httpd start/stop/restart```

As it suggests, start,stop,restart services/processes. The `reload-or-restart` pattern tells the services to reload if it is able and if
not then restart. SOme services doent allow a reload, often you will find this when you go to systemctl reload service. Nagios was one
example where a reload-or-restart would work, because it didn't allow reloads.

Tip:
* reload or restart is similar to `force-reload`. 

6.
```systemctl reload httpd```

```service httpd reload```

Perform a graceful reload of a configuration you may have just changed. Example, I've just made some changes to httpd conf and need to gracefully
reload them without restarting the web service. 

7.
```systemctl daemon reload```

```chkconfig serviceName --add```

Graceful reloads configuration files on a running service/process. See below for an explanation of “daemon reload”.
Basically, if you have added in a new service and made many config changes, use daemon-reload.

8.
```systemctl list-unit-files```

Good flags: --type=service

```ls /etc/rc.d/init.d/```
```ls /etc/rc.d/rc.local```

Prints from  /usr/lib/systemd/system/ and /etc/systemd/system/
Slightly different to list-units, rarely used but has any interesting output. You may want to use this in any 
monitoring scripts you write.


9.
```systemctl list-units```

Good flags -a (--all), -t serviecName, --all

```chkconfig --list``` or ```ntsysv```
```ls /etc/rc.d/init.d/```
```ls /etc/rc.d/rc.local```
```sysv-rc-conf```
```Initctl list```

Anyone see the problem between the two cmd passes? I prefer to use ‘list-units’ over ‘list-unit-files’. 
It shows more information and is shorter to type. List all active services using systemctl. 
Or you could install the sysvinit-utils, which by default are not installed on SysV distro's.

10.
```systemctl list-sockets```

```lsof```
```ss -s```
```cat /proc/net/*```

Sockets of all types can be viewed from one command. Although time to time I will ise lsof or ss depending on the socket
type I am wanting to look at.

11.
```systemctl list-timers```

```crontab -e```

systemd offers a way to schedule tasks aka crontab. Im going to go out on a limb here and say they both do the same thing, except
systemd timers may be more readable by human eyes, are logged to the journal, easier to debug and enable or disable.

Although my caveat; I still use cron jobs in my daily work, because Im familiar with them and emailing is still an issue from a timer.

Tip:
* set a systemd timer to a calendar, day, month, year to trigger.


12.
```systemctl list-jobs```

Requires further explanation in another blog post.


13.
```systemctl --failed```

Show me failed services. systemctl status will highlight at the top if units have failed, especially after a reboot.

14.
```systemctl get-default```

```systemctl set-default multi-user.target``` - equivalent to runlevels 2,3 and 4

to list targets run ```systemctl list-units -t target```

```Runlevel```
```Chkconfig --list```
```telinit runlevel```

Gets the run level default for the system. Not often used, if rarely, but good know when you start having boot issues or need
to swap out to a different run level to fix things.

Tip:
* There are many tables comparing the SysV runlevels to systemd. Get your google on and search.
* `systemctl set-default graphical.target` will set a graphical user shell. For all those that like a good desktop.

15.
```systemctl shutdown or reboot```

```shutdown -r now```

Reboot/shutdown the system. Personally I use ‘shutdown -r now’ still.

16.
```systemctl cat serviceName```

```cd to dir, cat init file```

Shows me the system service(unit) file contents and options. We will go more into these commands as we work through next week
building and maintaining our own UNIT files.

Tip:
* systemctl cat shows all unti file information and snippets involved with unit file.
* If you use VIM as I do, you can enable vim-systemd to help wotj syntax highlighting.

17.
```systemctl list-dependencies serviceName```

What’s really depending on my process. The --all flag will show everything --before, --after, --reverse.

Tip:
* Pretty handy little dependency checker for processes.

18.
```systemctl show serviceName```

Flags: -p - shows a single property of a service. 

Shows more than using ‘systemctl cat servicename’. Dont forget TAB is your friend. 
Running the ``-p`` flag and using TAB will help you.

19.
```systemctl mask serviceName```

```Update-rc.d serviceName disable```

Never want someone starting a service EVER!! 'Mask' is your friend and a little sneaky. See if your system admins 
pick this one up. Good April fools day. ‘’unmask’’ to return it to its user

20.
```systemctl edit serviceName```

Good flags --full

```vim /etc/inittab```

Yes that’s right! Edit the service file without having to cd into the directory. Now that saved me a bit of time.

Tip:
* Careful with this. The plain edit creates an override file in /etc/systemd/system to complement the original unit file. 
* If you need to edit the original unit file use the ```--full``` flag.
* I made mistake in my unit file or I messed up a system unti file; use `systemctl revert unit`

21.
```systemctl --output=```

Good Flags verbose, --full

```/etc/init.d/httpd start >httpd-output 2>&1```

Particular good if you have a bad service which is playing up. Outputs a short standard message or a very verbose message
using different flags.

Tip:
* `Journalctl -u serviceName` can help you here, but I often find it easier to reply the command and include `--output=verbose`

22.
```systemctl isolate```

This deserves its own small blog post. Isolate can be used to rescue systems automagically following kernel reboot 
failures, but requires some special work.

Tip:
We will cover this next week.

23.
```systemd-delta```

Check your unit files to see if someone has been changing things on you. Especially useful if you are writting your own Unit files.

Tip:
* Used in conjunction with `systemctl cat` or `edit`, `delta` can help you see what was what.

## Gotchas

1. Sometimes you need to use the suffix such as ‘config_file@openvpn.service’.  Keep this back of mind.
2. systemd will always think services are services unless you use the suffix like .target or .socket, make sure you tell the system so.
3. If you want multiple services running use a prefix, such as; ssh1@sshd.service ssh2@sshd.service with different configs. Handy for multiple openvpn servers.
4. Mount points will always be determined as mount points.
6. If you have made a lot of configuration changes and want to gracefully load these without restarting everything try  
`systemctl daemon reload`
7. This is not the same as the above “reload” action. Daemon reload is for systemd and not the unit files it controls. This is a safe 
command to run since it keeps sockets open while it does its thing.
8. Reboots on newer systems only really need to be done when new kernels are presented. Systemd is gracious and good at 
processing new packages and enabling these changes during a yum update.
9. Autocomplete on Centos is not present until you install `bash-completion`. systemctl takes on a life of it’s own, 
when you install this utility. Tabbing out will list all systemctl options. Very handy!!
10. Systemd does not use the /etc/inittab file even if you have them present.
11. Converting your init’s to systemd is easier than you think. Create a systemd unit file and add in 10 basic lines to 
call the bin or init script. You have basically created a systemd managed init script. Don’t forget to go back and one day convert it completely. For the basic lines you need, see next week's blog post on unti files.
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

OK ok... but how do I see what is taking its sweet time during boot or what is borking your beautiful server following an 
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
I might disable the docker service by `systemctl disable docker` and start it when I need it.

What else can `systemd-analyze` show me, that's all a bit boring!!!

```# systemd-analyze critical-chain```

Don't forget your TAB. There are options hiding that you will miss unless you know them.

```bash
@local-ian ~]$ systemd-analyze critical-chain 
The time after the unit is active or started is printed after the "@" character.
The time the unit takes to start is printed after the "+" character.

graphical.target @5.209s
└─multi-user.target @5.209s
  └─abrt-journal-core.service @5.209s
    └─abrtd.service @2.897s +2.308s
      └─livesys.service @2.881s +13ms
        └─basic.target @2.804s
          └─sockets.target @2.804s
            └─dbus.socket @2.804s
              └─sysinit.target @2.797s
                └─systemd-update-utmp.service @2.782s +14ms
                  └─auditd.service @2.634s +145ms
                    └─systemd-tmpfiles-setup.service @2.590s +41ms
                      └─fedora-import-state.service @2.566s +22ms
                        └─local-fs.target @2.562s
                          └─run-user-42.mount @4.614s
                            └─local-fs-pre.target @964ms
                              └─lvm2-monitor.service @321ms +442ms
                                └─dm-event.socket @320ms
                                  └─-.slice
```

Lets look at how long our network targets take to start:

```# systemd-analyze critical-chain network.target```

```bash
icinga-ian ~]# systemd-analyze critical-chain network.target
The time after the unit is active or started is printed after the "@" character.
The time the unit takes to start is printed after the "+" character.

network.target @2.618s
└─network.service @2.403s +214ms
  └─NetworkManager-wait-online.service @1.458s +941ms
    └─NetworkManager.service @1.417s +40ms
      └─network-pre.target @1.415s
        └─firewalld.service @976ms +438ms
          └─polkit.service @891ms +83ms
            └─basic.target @885ms
              └─paths.target @885ms
                └─brandbot.path @885ms
                  └─sysinit.target @881ms
                    └─systemd-update-utmp.service @872ms +7ms
                      └─auditd.service @702ms +168ms
                        └─systemd-tmpfiles-setup.service @676ms +24ms
                          └─rhel-import-state.service @653ms +22ms
                            └─local-fs.target @652ms
                              └─boot.mount @523ms +128ms
                                └─local-fs-pre.target @522ms
                                  └─lvm2-monitor.service @369ms +152ms
                                    └─lvm2-lvmetad.service @397ms
                                      └─lvm2-lvmetad.socket @368ms
                                        └─-.slice
```

Lets go one step further and output the entire system heirachy. 

``systemd-analyze dot``

Now with this one you should output to nice res picture

```systemd-analyze dot | dot -Tpng -o system-stuff.png```

 
## Too many typings - I type enough everyday and a have bzillion servers

*Pro Tip 2*

I have a server which needs a service restarted or checked constantly. Running systemctl remotely will show me or 
allow me to do this.

```systemctl status sshd -H root@server.address.com```

or

```systemctl -H root@server.address status httpd```

I might make an alias for it. Obviously this is a pretty useless example, if you’re having to manually do this for a 
service/process you should fix the problem on the server. However for edge cases it can be quite handy. Use your imagination,
we could use this for monitoring which takes a local ssh user found on all machines and pass this for some returned
output to a monitoring server.

## What relies on my service
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


I think the biggest part that people struggle with is workable, usable examples. 

## Next week
I know this is only touching the surface of systemctl or systemd as whole, however from a day-to-day context this should help
play in the systemd world. We will come back to systemctl more next week when we start working with units and targets.
  
Each week I will try and delve deeper into unit files, unit targets, systemctl isolate and slices, followed by a small primer 
on journalctl, timedatectl, loginctl. providing working examples where I can.

Stay tuned next week for hero to zero on unit files.



