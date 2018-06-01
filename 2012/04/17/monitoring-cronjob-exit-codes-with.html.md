---
author: Brian Buchalter
gh_issue_number: 592
tags: monitoring
title: Monitoring cronjob exit codes with Nagios
---



If you’re like me, you’ve got cronjobs that make email noise if there is an error. While email based alerts are better than nothing, it’d be best to integrate this kind of monitoring into Nagios. This article will break down how to monitor the exit codes from cronjobs with Nagios.

### Tweaking our cronjob

The monitoring plugin depends on being able to read some sort of log output file which includes an exit code. The plugin also assumes that the log will be truncated with every run. Here’s an example of a cronjob entry which meets those requirements:

```bash
rsync source dest 2>&1 > /var/log/important_rsync_job.log; echo "Exit code: $?" >> /var/log/important_rsync_job.log
```

So let’s break down a couple of the more interesting points in this command:

- 2>&1 sends the stderr output to stdout so it can be captured in our log file
- Notice the single > which will truncate the log every time it is run
- $? returns the exit code of the last run command
- Notice the double >> which will append to the log file our exit code

### Setting up the Nagios plugin

The [check_exit_code](https://github.com/bbuchalter/check_exit_code/blob/master/check_exit_code.pl) plugin is available on GitHub, and couldn’t be easier to setup. Simply specify the log file to monitor and the frequency with which it should be updated. Here’s the usage statement:

```bash
Check log output has been modified with t minutes and contains "Exit code: 0".
        If "Exit code" is not found, assume command is running.
        Check assumes the log is truncated after each command is run.
        
        --help      shows this message
        --version   shows version information

        -f          path to log file
        -t          Time in minutes which a log file can be unmodified before raising CRITICAL alert
```

The check makes sure the log file has been updated within t minutes because we want to check that our cronjob is not only running successfully, but running regularly. Perhaps this should be an optional parameter, or this should be called check_cronjob_exit_code, but for right now, it’s getting the job done and cutting back on email noise.


