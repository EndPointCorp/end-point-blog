---
author: Jon Jensen
title: Login shells in scripts called from cron
github_issue_number: 809
tags:
- devops
- linux
- perl
- python
- ruby
date: 2013-05-28
---

### The problem

I would guess that almost anyone who has set up a cron job has also had a cron job not work for initially mysterious reasons that often stem from cron running in a minimal environment very different from the same user’s normal login shell. For example, cron typically runs with:

```
SHELL=/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin
```

Whereas a common login shell has this in its environment, often with much more in the PATH:

```
SHELL=/bin/bash
PATH=/usr/local/bin:/bin:/usr/bin:$HOME/bin
```

`/bin/sh` may be bash, but bash behaves differently when invoked as sh. It may also be another shell such as [dash](https://en.wikipedia.org/wiki/Debian_Almquist_shell). And the impact of PATH differences is obvious, not just on the commands in the crontab but also in scripts they invoke.

I’ve been dealing with this for many years but it reached a new level of frequency with new systems like [rvm](https://rvm.io/), [rbenv](https://github.com/sstephenson/rbenv), [Perlbrew](https://perlbrew.pl/), and [pyenv](https://github.com/yyuu/pyenv), among others, which depend on the environment or shell aliases being modified.

The benefits of such multi-version local user-installed software are obvious, but the downside is that you have users installing various software that ends up being used in production, without sufficient wariness of production gotchas such as:

- the vagaries of things not running the same in cron
- starting services automatically at boot time
- service monitoring
- routing automated and bounced email
- logfile rotation
- and most of all, verifying all of the above things are not only set up, but actually work as expected in the days to follow when you’re not watching closely.

This is not to say that system administrators, or their brutal new DevOps 2.0 overlords, get this all right all the time. But usually they have more experience with it and know more what to watch out for.

### The scenario

Now to my point: When writing e.g. a start-app script that runs a Rails or Dancer site running in rbenv or perlbrew, developers often get it working nicely from their shell, then put it in a `@reboot` cron job, and leave. And that almost never works at reboot. At the next maintenance reboot, sysadmins discover via monitoring or manual testing that the daemon didn’t start. If sysadmins are in a hurry or being a little lazy, they’ll go make a “fix” to the crontab to change something or other, but also not test it, and it still won’t work after the next reboot. We get it right fairly often, but we also get it wrong more often than we’d like.

### The solution

This has a complicated and supposedly correct fix that makes the tinker/test loop take a long time.

It also has a simple, always-consistent, and supposedly incorrect fix that works very well in our environment.

1. Make sure your start-app script is marked executable: chmod +x
1. Give it the proper shebang line: `#!/bin/bash`, most often, unless you really know how to keep with the classic Bourne shell subset and use `#!/bin/sh`
1. Invoke the script directly in your crontab, e.g. `bin/start-app`, not with a manually-specified shell such as `bash bin/start-app`, etc. The goal is to always run the script the same way, and have that way encapsulated in the script itself.
1. Finally, since the problem is that cron is using a different environment, and you always have your login environment working with rbenv, perlbrew, etc., fix that by making your script’s shebang line invoke a full login shell: `#!/bin/bash -l`

Yes, it’s that simple: `#!/bin/bash -l` and a direct invocation are all it takes.

It’s true that this is abusing the idea of a “login shell”, since it’s not interactive. That has never mattered for us in our fairly plain-vanilla bash setups we use in production server accounts. It has the virtue of being exactly what a developer expects. It avoids repetition of environment setups or version-specific invocations in the crontab, which can become out of date quickly since it is easily forgotten. It follows the wise dicta “different makes a difference” (#21 in [Practices of an Agile Developer](http://media.pragprog.com/titles/pad/PAD-pulloutcard.pdf)) and “don’t repeat yourself” (from the book [The Pragmatic Programmer](https://ptgmedia.pearsoncmg.com/images/9780201616224/samplepages/020161622X.pdf)).

None of this is as clean as having RHEL/CentOS RPM or Debian/Ubuntu .deb system packages for the language and its modules, but I don’t know of anything like the essential Ruby [Bundler](http://gembundler.com/) that works with system packages, and coexisting multiple system-wide versions of Ruby, Perl, Python, etc. are rare. So we have to work with this for now.

Out in the wilds of the web, several projects and individuals adopt this same approach. Their rationales can be summed up as: it works, and I don’t see any actual downsides.

### Impure!

The dissenting voices such as [Daniel Szmulewicz on cron jobs using rvm](http://danielsz.github.io/how-to-run-rvm-scripts-as-cron-jobs/index.html/) are eloquent, but all seem to focus on the “ickiness” of starting a noninteractive shell session as a login session. The main actual problem reported is an rvm corner case where [rvm goes into an infinite loop](https://github.com/rvm/rvm/issues/791). But this appears to me to have been a bug in rvm, and one of several rvm infinite loop bugs that led us to move to rbenv and away from rvm’s tightly-coupled shell trickery in the first place.

Further study is worthwhile to understand how all these pieces fit together. I recommend your own shell’s manpage, [rbenv’s Unix shell initialization overview](https://github.com/rbenv/rbenv/wiki/Unix-shell-initialization), and this StackOverflow answer on [exposing cron’s run environment](https://stackoverflow.com/questions/2135478/how-to-simulate-the-environment-cron-executes-a-script-with/2546509#2546509).
