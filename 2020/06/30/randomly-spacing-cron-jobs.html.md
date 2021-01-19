---
author: Jon Jensen
title: Randomly spacing cron jobs
tags: sysadmin, automation
gh_issue_number: 1646
---

<img src="/blog/2020/06/30/randomly-spacing-cron-jobs/20200127-160558-sm.jpg" alt="bird footprints in snow" />

<!-- Photo by Jon Jensen -->

Cron is the default job scheduler for the Unix operating system family. It is old and well-used infrastructure — it was first released 45 years ago, in May 1975!

On Linux, macOS, and other Unix-like systems, you can see any cron jobs defined for your current user with:

```bash
crontab -l
```

If nothing is printed out, your user doesn’t have any cron jobs defined.

You can see the syntax for defining the recurring times that jobs should run with:

```bash
man 5 crontab
```

Important in that document is the explanation of the space-separated time and date fields:

```nohighlight
field          allowed values
-----          --------------
minute         0-59
hour           0-23
day of month   1-31
month          1-12 (or names, see below)
day of week    0-7 (0 or 7 is Sunday, or use names)

A field may contain an asterisk (*), which always stands for "first-last".
```

For example, to make a job run every Monday at 3:33 am in the server’s defined time zone:

```nohighlight
33 3 * * 1 /path/to/executable
```

### Random interval scheduling

Sometimes it may be good to schedule a cron job to run at a somewhat random time: generally not truly random, but maybe at an arbitrary time within a specified time range rather than at a specific recurring interval.

This can be useful to keep simultaneous cron jobs for different users from causing predictable spikes in resource usage, or to run at a time other than the start of a new minute, since cron’s interval resolution doesn’t go smaller than one minute.

There isn’t any simple built-in way to randomize the scheduling in classic cron, but there are several ways to get it done:

#### cronie RANDOM_DELAY

The version of cron included with Red Hat Enterprise Linux (RHEL), CentOS, and Fedora Linux is cronie. It allows us to set the variable `RANDOM_DELAY` for this purpose. From its manual:

> The RANDOM_DELAY variable allows delaying job startups by random amount of minutes with upper limit specified by the variable. The random scaling factor is determined during the cron daemon startup so it remains constant for the whole run time of the daemon.

To use that we set the variable in a crontab before the jobs it should apply to. For example, to delay every job defined after that variable by a random time up to 10 minutes:

```bash
RANDOM_DELAY=10
```

When it starts, cronie logs its random scaling factor so you can tell how long each `RANDOM_DELAY` will work out to be during the lifetime of this cron daemon. It looks like this:

```nohighlight
# systemctl status crond
● crond.service - Command Scheduler
     Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2020-06-29 19:05:50 MDT; 2min 29s ago
   Main PID: 60630 (crond)
      Tasks: 1 (limit: 19011)
     Memory: 3.4M
        CPU: 218ms
     CGroup: /system.slice/crond.service
             └─60630 /usr/sbin/crond -n

Jun 29 19:05:50 myhost systemd[1]: Started Command Scheduler.
Jun 29 19:05:50 myhost crond[60630]: (CRON) STARTUP (1.5.5)
Jun 29 19:05:50 myhost crond[60630]: (CRON) INFO (RANDOM_DELAY will be scaled with factor 66% if used.)
Jun 29 19:05:50 myhost crond[60630]: (CRON) INFO (running with inotify support)
Jun 29 19:05:50 myhost crond[60630]: (CRON) INFO (@reboot jobs will be run at computer's startup.)
```

If we restart cronie with `systemctl restart crond`, we will (probably) see a different scaling factor:

```nohighlight
Jun 29 22:42:02 myhost crond[75200]: (CRON) INFO (RANDOM_DELAY will be scaled with factor 29% if used.)
```

Note that this feature is not available on Debian &amp; Ubuntu because they use the parent project vixie-cron, aka ISC Cron, that cronie descended from.

#### bash sleep RANDOM

If your cron uses bash as its default shell for executing jobs, or if you set it to bash with `SHELL=/bin/bash` before the cron job in question, you will have available the variable `RANDOM` which returns numbers between 0 and 32767.

To scale that number to the range of seconds you want to delay starting your cron job, do some modulo arithmetic. For example, to wait for a random time between 0 and 600 seconds (= 10 minutes) before running your job, do:

```bash
sleep $(( RANDOM % 600 )); /path/to/executable
```

That works when run directly from the shell, but watch out! Both cronie and vixie-cron terminate any line at the first unescaped `%` character, so you must write `\%` in the cron job. Why do they do that? It’s an old feature: The rest of the line after `%` is sent as stdin (standard input) to the command.

So that same example in a cron job would look like:

```bash
@reboot sleep $(( RANDOM \% 600 )); /path/to/executable
```

#### Wrapper script

If you want to avoid the pitfall of forgetting to escape `%` in cron jobs, you can write a wrapper script that waits a configurable random duration and then exits, and run that before running your program.

#### Perl sleep random

Another way is to use Perl instead of bash:

```bash
@reboot perl -e 'sleep(rand(3000))'; /path/to/executable
```

Or similarly in another scripting language of your choice.

#### at

If you want to have your job possibly wait quite a long while and not have the cron job sitting there sleeping the whole time, you can create a cron job that runs at the start of every period during which you want things to run randomly, and it can schedule an `at` job to run at later random time. For example:

```bash
@reboot echo /path/to/executable | at now + $(( RANDOM \% 60 )) minutes
```

#### Program delay feature

If your program has some inherent reason to delay before starting its actual work, you could add an option to your program to do the initial wait within a certain number of seconds.

But generally this seems better done by a separate program since it is unlikely that startup delay is a function closely related to your program and it will just bloat it. Why not keep it simple(r)?

#### OpenBSD cron

In OpenBSD 6.7 cron a new feature was introduced using the symbol `~`. The [OpenBSD crontab manual](https://man.openbsd.org/crontab.5) explains:

> A random value (within the legal range) may be obtained by using the ‘~’ character in a field. The interval of the random value may be specified explicitly, for example “0~30” will result in a random value between 0 and 30 inclusive. If either (or both) of the numbers on either side of the ‘~’ are omitted, the appropriate limit (low or high) for the field will be used.

There is an important caveat not mentioned in the manual, [explained on StackOverflow](https://unix.stackexchange.com/questions/179598/cron-job-random-start-but-within-timeframe/580493#580493) by [user Kusalananda](https://unix.stackexchange.com/users/116858/kusalananda):

> The random times are picked randomly, but they are fixed until the crontab is reloaded, i.e. until the cron daemon restarts or when the crontab is edited with crontab -e. This would therefore not provide you with a new random value for each run of the job, like using sleep with $RANDOM would do.

#### Jenkins scheduling

It is not standard Unix cron, but also consider the cron-inspired scheduling functionality in the Jenkins continuous integration system.

There a special symbol `H` is used to indicate that a “hashed” value is used, similarly to OpenBSD cron’s `~` when no range endpoints are specified. As the [Wikipedia cron article](https://en.wikipedia.org/wiki/Cron) describes it:

> Thus instead of a fixed number such as `20 * * * *` which means at 20 minutes after the hour every hour, `H * * * *` indicates that the task is performed every hour at an unspecified but invariant time for each task. This allows spreading out tasks over time, rather than having all of them start at the same time and compete for resources.

Though this seems effectively random, it is actually stable based on the job name, as the [Jenkins Pipeline Syntax cron syntax](https://www.jenkins.io/doc/book/pipeline/syntax/#cron-syntax) documentation notes:

> The `H` symbol can be thought of as a random value over a range, but it actually is a hash of the job name, not a random function, so that the value remains stable for any given project.

### Limiting concurrent runs

Finally, a separate but important consideration: If you have a job that takes a long time to run, and if this isn’t just a job to run once with `@reboot` each time the server starts, you may want to make sure a new instance of the job will not start running before the previous one has finished.

You can do that by using a shared lock file that tells when another instance of the job is running, for example:

```bash
flock -n /tmp/describe-your.lock -c /path/to/executable
```

See `man 1 flock` for more details on what it can do.

### ⏲ 

Happy scheduling!
