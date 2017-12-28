---
author: Jon Jensen
gh_issue_number: 685
tags: hosting, linux, perl
title: Automatically kill process using too much memory on Linux
---

Sometimes on Linux (and other Unix variants) a process will consume way too much memory. This is more likely if you have a fair amount swap space configured -- but within the range of normal, for example, as much swap as you have RAM.

There are various methods to try to limit trouble from such situations. You can use the shell’s ulimit setting to put a hard cap on the amount of RAM allowed to the process. You can adjust settings in /etc/security/limits.conf on both Red Hat- and Debian-based distros. You can wait for the OOM (out of memory) killer to notice the process and kill it.

But all those remedies don’t help in situations where you want a process to be able to use a lot of RAM, sometimes, when there’s a point to it and it’s not just in an infinite loop that will eventually use all memory.

Sometimes such a bad process will bog the machine down horribly before the OOM killer notices it.

We put together the following script about a year ago to handle such cases:

<script src="https://gist.github.com/3540671.js"></script>

It uses the [Proc::ProcessTable](http://search.cpan.org/perldoc?Proc%3A%3AProcessTable) module from Perl’s CPAN to do the heavy lifting. We invoke it once per minute in cron. If you have processes eating up memory so quickly that they bring down the machine in less than a minute, you could run it in a loop every few seconds instead.

It’s easy to customize based on various attributes of a process. In our example here we have it ignore root processes which are assumed to be better vetted. We have commented out a restriction to watch only for Ruby on Rails processes in Passenger. And we kill only processes using 1 GiB or more RAM.

If a process makes it past these tests and is considered bad, we print out a report that crond emails to us, so we can investigate and ideally fix the problem. Then we try to kill the process gracefully, and after 5 seconds forcibly terminate it.

It’s simple, easily customizable, and has come in handy for us.
