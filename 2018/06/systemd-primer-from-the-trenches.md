---
author: Ian Neilsen
title: 'systemd: a primer from the trenches'
github_issue_number: 1432
tags:
- hosting
- systemd
date: 2018-06-18
---

<img src="/blog/2018/06/systemd-primer-from-the-trenches/6095265888_a27b664798_o-crop.jpg" width="1540" alt="gears" /><br><a href="https://www.flickr.com/photos/guysie/6095265888/">Gears image by Guy Sie, CC BY-SA 2.0, cropped & scaled</a>

### systemctl: Let’s get back to basics

''Help me systemd, you are my only hope.''

Sometimes going back to day zero brings clarity to what seems like hopeless or frustrating situation for users from the Unix SysV init world. Caveat: I previously worked at Red Hat for many years before joining the excellent team at End Point and I have been using systemd for as long. I quite honestly have forgotten most of the SysV init days. Although at End Point we work daily on Debian, Ubuntu, CentOS, and BSD variants.

Here is a short and sweet primer to get your fingers wet, before we dive into some of the heavier subjects with systemd.

Did you know that systemd has many utilities you can run?

* systemctl
* timedatectl
* journalctl
* loginctl
* systemd-notify
* systemd-analyze - analyze system
* systemd-cgls - show cgroup tree
* systemd-cgtop
* systemd-nspawn

And systemd consists of several daemons:

* systemd
* journald
* networkd
* logind
* timedated
* udevd
* system-boot
* tmpfiles
* session

That’s a long way from the old SysV init days. But in all essence it’s not that different. The one thing that stands out to me is we have more information with less typing then previously. That can only be a good thing, right?

Well, let’s see! There are many many web pages out there that list systemd or systemctl switches/​flags. However in everyday use I want to speed up the work I do, I want information at my fingertips, and I find flags and switches which mean something sure do make it easier.

### Pro Tip 1: Tab completion

Before you begin playing with the commands, you should install `bash-completion`. Some distros don’t auto-complete with systemd until you install that, and without tab auto-completion you miss out on **a lot** of systemctl.

As an example when you tab for completion you will see many of the systemctl options:

```
# systemctl
add-requires           enable                 is-system-running      preset                 show
add-wants              exit                   kexec                  preset-all             show-environment
cancel                 force-reload           kill                   reboot                 start
cat                    get-default            link                   reenable               status
condreload             halt                   list-dependencies      reload                 stop
condrestart            help                   list-jobs              reload-or-restart      suspend
condstop               hibernate              list-machines          rescue                 switch-root
daemon-reexec          hybrid-sleep           list-sockets           reset-failed           try-reload-or-restart
daemon-reload          import-environment     list-timers            restart                try-restart
default                is-active              list-unit-files        revert                 unmask
disable                is-enabled             list-units             set-default            unset-environment
edit                   is-failed              mask                   set-environment
emergency              isolate                poweroff               set-property
```

### systemctl vs. old school commands

Here we will list out new systemctl commands and the corresponding old SysV command, followed by systemctl flags and explanation.

Go ahead and run each command to get a feel for what it displays. Remember each command usually has switches/​flags you can use.

Let’s start at the top and work down:

#### systemctl

Formerly: `service`

Used in conjunction with ABRT it can show you some great debug info and runtime metadata, categorized by their respective groupings of loaded, active, running and a description of the unit.

#### systemctl status

Formerly: `service --status-all` or `initctl list`.

Check all system services’ status. Normally during a server update I will run this and output it to a file. When the server reboots I can run it again and diff this file to ensure all things started.

The output is great. It shows me the PID path and potentially the arguments which were run for the process or service. Saves me `ps`ing the process.

Note that each distro deals differently with `service --status-all` output.

#### systemctl status serviceName -l

Formerly: `service serviceName status`

Good flags: `is-active`, `-a`, `-l`

As it suggests, show me the status and information related to the service unit file. Other good info included is whether the service is enabled or chkconfig is on, uptime, PID and cgroup info, and any other information associated with the service.

Tips:

* The `-l` flag will usually output enough information to diagnose a service start or reload problem without having to go into the logs.
* You can view more than one service by separating them with spaces, e.g.: `systemctl status httpd mysql postfix`.

#### systemctl enable|disable NameofService

Formerly: `chkconfig ServiceName on|off`

You might find on some distros that `chkconfig` is still present. It doesn’t do what you think it does with systemd systems.

#### systemctl start|stop|restart httpd

Formerly: `service httpd start|stop|restart`

Good unit commands: reload-or-restart

As it suggests, start, stop, or restart services/​processes/​units.

The `reload-or-restart` command tells the services to reload if it is able and if not then restart, similar to the old `service serviceName force-reload`. Some services don’t allow a reload. Nagios is one example where a `reload-or-restart` works because it doesn’t allow reloads.

#### systemctl reload httpd

Formerly: `service httpd reload`

Perform a graceful reload of a configuration you may have just changed. Example: I’ve just made some changes to httpd conf and need to gracefully reload them without restarting the web service.

#### systemctl daemon reload

Formerly: `chkconfig serviceName --add`

Graceful reloads configuration files on a running service/​process. See below for an explanation of “daemon reload”. Basically, if you have added in a new service and made many config changes, use `daemon-reload`.

#### systemctl list-unit-files

Good flags: `--type=service`

Formerly: `ls /etc/rc.d/init.d/ /etc/rc.d/rc.local`

Prints unit files from `/usr/lib/systemd/system/` and `/etc/systemd/system/`. Slightly different to `list-units`; rarely used but has any interesting output. You may want to use this in monitoring scripts you write.

#### systemctl list-units

Good flags: `-a (--all)`, `-t serviceName`

Formerly:

```bash
chkconfig --list
ntsysv
ls /etc/rc.d/init.d/ /etc/rc.d/rc.local
sysv-rc-conf
initctl list
```

I prefer to use `list-units` over `list-unit-files`. It shows more information and is shorter to type. Or you could install the `sysvinit-utils` package, which by default is not installed on systemd distros.

#### systemctl list-sockets

Formerly:

```bash
lsof
ss -s
cat /proc/net/*
```

Sockets of all types can be viewed from one command. Although time to time I will still use `lsof` or `ss` depending on the socket type I want to look at.

#### systemctl list-timers

Formerly: `crontab -e`

systemd offers a way to schedule tasks like crontab. I’m going to go out on a limb here and say they both do the same thing, except systemd timers may be more readable by human eyes, are logged to the journal, easier to debug and enable or disable.

My caveat is that I still use cron jobs in my daily work, because I’m familiar with them and emailing is still an issue from a timer.

Tip:

* set a systemd timer to a calendar day, month, year to trigger.

#### systemctl list-jobs

Requires further explanation in another blog post.

#### systemctl --failed

Show me failed services. `systemctl status` will highlight at the top if units have failed, especially useful after a reboot.

#### systemctl get-default

Formerly:

```bash
runlevel
chkconfig --list
```

To list targets run `systemctl list-units -t target`.

Gets the run level default for the system. Not often used, but good to know when you start having boot issues or need to change to a different run level to fix things.

Tips:

* There are many tables comparing the SysV runlevels to systemd. Get your Google on and search.
* `systemctl set-default graphical.target` will set a graphical user shell. For all those that like a good desktop.

#### systemctl set-default multi-user.target

Formerly: `telinit runlevel`

The systemd `multi-user.target` is equivalent to runlevels 2, 3, and 4.

#### systemctl shutdown or reboot

Formerly: `shutdown -r|-h now`

Reboot/shutdown and poweroff the system. Personally I still use `shutdown`.

#### systemctl cat serviceName

Formerly: `cat /etc/init.d/$init_file`

Shows me the system service (unit) file contents and options. We will go more into these commands later as we work through building and maintaining our own unit files.

Tips:

* `systemctl cat` shows all unit file information and snippets involved with the unit file.
* If you use Vim and Arch Linux, you can enable `vim-systemd` to help with syntax highlighting.

#### systemctl list-dependencies serviceName

What’s really depending on a given service. The `--all` flag will show everything from `--before`, `--after`, `--reverse`.

#### systemctl show serviceName

Flags: `-p` shows a single property of a service.

Shows more than using `systemctl cat servicename`. Don’t forget tab completion is your friend. Running the `-p` flag and using tab will help you.

#### systemctl mask serviceName

Formerly: `update-rc.d serviceName disable`

Never want someone starting a service **ever**? `mask` is your friend and a little sneaky. See if your system admins pick this one up. Good April Fool’s day trick on them. Use `unmask` to return it to its normal state.

#### systemctl edit serviceName

Formerly: edit `/etc/init.d/scriptName`

Good options: `--full`

Yes, that’s right! Edit the service file without having to go find it on disk. That has saved me a bit of time.

Tips:

* Careful with this. The plain edit creates an override file in /etc/systemd/system to complement the original unit file.
* If you need to edit the original unit file use the `--full` flag, which allows you to edit the unit file without creating a snippet.
* If you make a mistake in your unit file: `systemctl revert serviceName`

#### systemctl -o

Formerly: Edit Apache config to set log level to warn or debug, `/etc/init.d/httpd reload`, view logs

Good options: `--output=verbose`

Particularly good if you have a service acting up. Outputs a short standard message or a very verbose message using different flags.

Tip:

* `journalctl -u serviceName` can help you here, but I often find it easier to include `--output=verbose`

#### systemctl isolate

This deserves its own small blog post. Isolate can be used to rescue systems automagically following kernel reboot failures, but requires some special work.

#### systemd-delta

Check your unit files to see if someone has been changing things on you. Especially useful if you are writing your own unit files.

Tip:

* Used in conjunction with `systemctl cat` or `edit`, `delta` can help you see what was what.

### Gotchas

1. Sometimes you need to use the suffix such as ‘config_file@openvpn.service’. systemd will always think services are services unless you use the suffix like .target or .socket, so make sure you tell the system so.
1. If you want multiple services running use a prefix, such as; ssh1@sshd.service ssh2@sshd.service with different configs. Handy for multiple openvpn servers.
1. Mount points will always be determined as mount points.
1. If you have made a lot of configuration changes and want to gracefully load these without restarting everything try `systemctl daemon reload`. This is not the same as the above `reload` action. Daemon reload is for systemd and not the unit files it controls. This is a safe command to run since it keeps sockets open while it does its thing.
1. Reboots on newer systems only really need to be done when new kernels are presented. Systemd is gracious and good at processing new packages and enabling these changes during a yum update.
1. Autocomplete on CentOS is not present until you install `bash-completion`. systemctl takes on a life of its own when you install this utility. Tabbing out will list all systemctl options. Very handy!
1. Systemd does not use the /etc/inittab file even if you have it present.
1. Converting your init scripts to systemd is easier than you think. Create a systemd unit file and add in 10 basic lines to call the bin or init script. You have basically created a systemd managed init script. Don’t forget to go back and one day convert it completely.
1. Targets vs. runlevels: A target in systemd is a runlevel in sysV, names replace numbers; runlevel 3 = multi-user.target, runlevel 1 = rescue.target

### Who’s got the goods on speed?

Is systemd faster than SysV init? Parallel processing says it is? You be the judge!

One great test is to build a new machine which doesn’t have systemd installed. Reboot the machine and check your boot time. On an older SysV system you may have use “tuned”, “systemtap”, “numastat” etc. to gather performance information.

Then install systemd. Better still, upgrade from a old version of Linux to a new version of linux from ‘init’ to ‘systemd’ and then run ‘systemd-analyze’.

`systemd-analyze` will show you boot times. Notice that systemd starts fewer services at boot because it only starts what is necessary to get the server booting.

Not a bad way to collect a baseline on a newly-built server. Add it to your Ansible facts for the server so you have a historical view and collection of boot times. In fact add it to your monitoring system and be proactive in your monitoring of server boot times while performing your maintenance cycles.

How do you see what is taking its sweet time during boot or what is borking your beautiful server following an update/​upgrade? Wonder no more!

```
# systemd-analyze blame
# systemd-analyze time
```

For example on my system, I can see that my top 10 culprits for a potentially slow boot are:

```
# systemd-analyze blame
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

I might disable the Docker service by `systemctl disable docker` and start it when I need it.

What else can `systemd-analyze` show me?

```
# systemd-analyze critical-chain
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

Let’s look at how long our network targets take to start:

```
# systemd-analyze critical-chain network.target
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

Let’s go one step further and output the entire system hierarchy. With this one you get a nice image:


```bash
# systemd-analyze dot | dot -Tpng -o system-stuff.png
```

### Pro Tip 2: Remote commands

I have a server which needs a service restarted or checked constantly. Running systemctl remotely will show me or allow me to do this:

```bash
# systemctl status sshd -H root@server.domain.tld
```

Or:

```bash
# systemctl -H root@server.domain.tld status httpd
```

I might make an alias for it. Obviously this is a pretty useless example, if you’re having to manually do this for a service/​process you should fix the problem on the server. However for edge cases it can be quite handy. Use your imagination: We could use this for monitoring which takes a local ssh user found on all machines and pass this for some returned output to a monitoring server.

### Pro Tip 3: What relies on my service

Figure out what targets/​runlevel a target runs at:

```bash
# systemctl show httpd -p wants multi-user.target
```

#### Pro Tip 4: Monitoring

Check processes, service association, and busiest processes. You can still grep/​awk the output if you wish.

Instead of using `top` or something like this:

```bash
ps xawf -eo pid,user,cgroup,args
```

use the following:

```bash
# systemd-cgls
# systemd-cgtop
```

### Summing up

I know this is only touching the surface of systemctl or systemd as whole but from a day-to-day context this should help you play in the systemd world. I think the biggest part that people struggle with is workable, usable examples.

Stay tuned for future posts on unit files, unit targets, systemctl isolate and slices, journalctl, timedatectl, and loginctl.
