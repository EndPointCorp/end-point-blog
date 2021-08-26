---
author: Jon Jensen
title: GNU Screen logtstamp string
github_issue_number: 838
tags:
- hosting
- terminal
date: 2013-07-24
---

A short note on [GNU Screen](https://www.gnu.org/software/screen/) configuration:

You can add configuration to `~/.screenrc` or another configuration file named by `-c $filename` upon invocation, and among the many options are some to enable logging what happens in the screen windows. This is useful when using screen as a reattachable daemonizer.

Consider this configuration:

```nohighlight
logfile path/to/screen-output.%Y%m%d.log
logfile flush 1
logtstamp on
logtstamp after 5
log on
```

That works nicely. With `logfile` we specify the name of the log file, using some `%` escapes as per “STRING ESCAPES” in the manpage to put the date in the logfile name.

With `logfile flush 1` we request that every 1 second the output be flushed to the log, making it easier to follow with `tail -f`.

The `logtstamp on` option writes a timestamp to the log after a default 2 minutes of inactivity. We shorten that to 5 seconds with `logtstamp after 5`.

Finally, `log on` turns on the logging.

Now, what if we want to customize the timestamp? The default looks like this:

```nohighlight
-- 0:process-name -- time-stamp -- Jul/24/13  9:09:56 --
```

The manpage says that can be customized with `logtstampt string ...`, where the default is:

```nohighlight
-- %n:%t -- time-stamp -- %M/%d/%y %c:%s --\n
```

The manpage earlier says that arguments may be separated by single or double quotes. Doing so with the default shown doesn’t work, because a literal \n shows up in the logfile.

The solution I worked out by trial and error is that you must double-quote the string and use octal escape value `\012`. Single-quoting that will output a literal backslash 0 1 2, and `\n` simply is not a recognized escape. Thus our final configuration directive is:

```nohighlight
logtstamp string "-- time-stamp -- %Y-%m-%d %0c:%s --\012"
```

which results in output like:

```nohighlight
-- time-stamp -- 2013-07-24 09:59:35 --
```

If you use more than one screen window with this configuration, all windows’ output will go into the same logfile. Use the `%n` escape string to include a window number in the logfile name if you’d like them kept separate.
