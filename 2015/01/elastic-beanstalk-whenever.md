---
author: Kent Krenrich
title: Elastic Beanstalk Whenever
github_issue_number: 1076
tags:
- rails
- sysadmin
- aws
date: 2015-01-27
---

I recently got the opportunity to pick up development on a Ruby on Rails application that was originally set up to run on [AWS](https://aws.amazon.com) using their [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) deployment tools. One of our first tasks was to move some notification hooks out of the normal workflow into scripts and schedule those batch scripts using cron.

Historically, I’ve had extremely good luck with [Whenever](https://github.com/javan/whenever). In my previous endeavors I’ve utilized Capistrano which Whenever merged with seamlessly. With how simple it was to integrate Whenever with Capistrano, I anticipated a similar experience dealing with Elastic Beanstalk. While the integration was not as seamless as Capistrano, I did manage to make it work.

My first stumbling block was finding documentation on how to do after or post hooks. I managed to find [this forum post](https://forums.aws.amazon.com/thread.jspa?messageID=493887) and [this blog post](http://junkheap.net/blog/2013/05/20/elastic-beanstalk-post-deployment-scripts/) which helped me out a lot. The important detail is that there is a “post” directory to go along with “pre” and “enact”, but it’s not present by default, so it can be easy to miss.

I used [Marcin’s delayed_job config](http://junkheap.net/blog/2013/05/20/elastic-beanstalk-post-deployment-scripts/) as a base. The first thing I had to address was an apparent change in Elastic Beanstalk’s configuration structure. Marcin’s config has

```bash
  . /opt/elasticbeanstalk/support/envvars
```

but that file doesn’t exist on the system I was working on. With a small amount of digging, I found:
```bash
  . /opt/elasticbeanstalk/containerfiles/envvars
```

in one of the other ebextensions. Inspecting that file showed a definition for and exportation of $EB_CONFIG_APP_CURRENT suggesting this is a similar file just stored in a different location now.

Another change that appears to have occurred since Marcin developed his config is that directories will be created automatically if they don’t already exist when adding a file in the files section of the config. That allows us to remove the entire commands section to simplify things.

That left me with a config that looked like:

```bash
files:
  "/opt/elasticbeanstalk/hooks/appdeploy/post/99_update_cron.sh"
  mode: "000755"
  owner: root
  group: root
  content: |
    #! /usr/bin/env bash
    . /opt/elasticbeanstalk/containerfiles/envvars
    su -c "cd $EB_CONFIG_APP_CURRENT; bundle exec whenever --update-cron" - $EB_CONFIG_APP_USER
```

This command completed successfully but on staging the cron jobs failed to run. The reason for that was an environment mismatch. The runner entries inside the cron commands weren’t receiving a RAILS_ENV or other type of environment directive so they were defaulting to production and failing when no database was found.

After some greping I was able to find a definition for RACK_ENV in:

```bash
/opt/elasticbeanstalk/containerfiles/envvars.d/sysenv
```

Making use of it, I came up with this final version:
```bash
files:
  "/opt/elasticbeanstalk/hooks/appdeploy/post/99_update_cron.sh"
  mode: "000755"
  owner: root
  group: root
  content: |
    #! /usr/bin/env bash
    . /opt/elasticbeanstalk/containerfiles/envvars
    . /opt/elasticbeanstalk/containerfiles/envvars.d/sysenv
    su -c "cd $EB_CONFIG_APP_CURRENT; bundle exec whenever --update-cron --set='environment=$RACK_ENV'" - $EB_CONFIG_APP_USER
```
