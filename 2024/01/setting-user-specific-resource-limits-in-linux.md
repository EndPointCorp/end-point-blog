---
title: Setting User-Specific Resource Limits with systemd
date: 2024-02-03
author: Seth Jensen
featured:
  image_url: /blog/2024/01/setting-user-specific-resource-limits-in-linux/sun-through-trees.webp
github_issue_number: 2029
tags:
- linux
- sysadmin
- systemd
- vscode
---

![In the center of a dim American street lined with houses and cars, the sun illuminates and sillhouettes green foliage. It projects a triangle of light on the ground, first the street and then the grass, centered in the frame. On either side of the light, centered verticaly, a white car catches the light.](/blog/2024/01/setting-user-specific-resource-limits-in-linux/sun-through-trees.webp)

We recently encountered an issue on one of our servers where the VS Code extension "Remote - SSH" was spinning out of control and using all the resources on the system. This was a particularly pressing problem, because this server was shared between production websites and development environments.

TL;DR: We set per-user limits using `cgroups`, which is available since our server uses systemd. You can do this by adding the following to `/etc/systemd/system/user-1000.slice.d/50-limits.conf`, then stopping all of that user's processes before logging in again.

```plain
[Slice]
CPUQuota=50%
MemoryLimit=1G
TasksMax=40
```

In many cases, you could use [ulimit](https://linuxcommand.org/lc3_man_pages/ulimith.html) to control a user's resource limits. But ulimit only controls resources for the shell it's running in, and since VS Code was connecting through SSH and spawning a bunch of processes, we didn't have a reasonable way to do this.

Using systemd, you can instead control overall user limits, not just the limits on a specific process or in a specific shell. This seems like a good practice for any mixed develpoment/production server so that messing with the development environment won't ever slow down or crash the live website.

> On PAM systems, you can also use the `pam_limits` module to set user-wide resource limits. O'Reilly has a good [guide on configuring limits](https://www.oreilly.com/library/view/network-security-hacks/0596006438/ch01s20.html) this module.

### A closer look at setting limits with cgroups

You can add systemd controllers—including resource limits—via drop-in files in `/etc/systemd/system/`.

To set limits for a specific user, we need the user's UID. You can find this in the third column of `/etc/passwd`:

```plain
seth:x:1000:1000:Seth Jensen:/home/seth:/bin/bash
testy:x:1001:1001:Testy Tester:/home/testy:/bin/bash
```

For the `seth` user, the UID is 1000, so we will create a file called `50-limits.conf` in the `/etc/systemd/system/user-1000.slice.d/` directory to limit that user's resources.

The `50-` in the filename just determines the order in which the config files will be applied, so it shouldn't matter if this is the only file you're adding.

Now, in our `50-limits.conf` file we can add limits:

```plain
[Slice]
CPUQuota=50%
MemoryLimit=1G
TasksMax=40
```

Here we're just limiting CPU time, memory, and the number of tasks run by the `seth` user. You can see a full list of what's available with [man systemd.resource-control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html).

It's worth noting that `CPUQuota=50%` will limit `seth` to 50% of a *single* CPU, which would be 25% of total CPU on a dual-core system, etc.
