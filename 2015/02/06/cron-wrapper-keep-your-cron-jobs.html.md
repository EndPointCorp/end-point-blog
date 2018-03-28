---
author: Richard Templet
gh_issue_number: 1088
tags: devops, hosting
title: 'Cron Wrapper: Keep your cron jobs environment sane'
---

It is becoming more common for developers to not use the operating system packages for programming languages. Perl, Python, Ruby, and PHP are all making releases of new versions faster than the operating systems can keep up (at least without causing compatibility problems).
There are now plenty of tools to help with this problem. For Perl we have [Perlbrew](https://perlbrew.pl/) and [plenv](https://github.com/tokuhirom/plenv). For Ruby there is [rbenv](https://github.com/sstephenson/rbenv) and [RVM](https://rvm.io/). For Python there is [Virtualenv](https://virtualenv.pypa.io/en/latest/). For PHP there is [PHP version](https://github.com/wilmoore/php-version).
These tools are all great for many different reasons but they all have issues when being used with cron jobs. The cron environment is very minimal on purpose. It has a very restrictive path, very few environment variables and other issues. As far as I know, all of these tools would prefer using the env command to get the right version of the language you are using. This works great while you are logged in but tends to fail bad as a cron job. The cron wrapper script is a super simple script that you put before whatever you want to run in your crontab which will ensure you have the right environment variables set.

```bash
#!/bin/bash -l

exec "$@"
```

The crontab entry would look something like this:
```bash
34 12 * * * bin/cron-wrapper bin/blog-update.pl
```

The -l on the executing of bash makes it act like it is logging in. Therefore it picks up anything in the ~/.bash_profile and has that available to the env command. This means the cron job runs in the same environment that is setup when you run it from the command line, helping to stop those annoying times where it works fine from the command line but breaks in cron. Jon Jensen went into much greater detail on the benefits of using the -l [here](/blog/2013/05/28/login-shells-in-scripts-called-from-cron).
Hope this helps!
