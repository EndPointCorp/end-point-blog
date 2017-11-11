---
author: Mike Farmer
gh_issue_number: 890
tags: rails, sysadmin
title: Zero Downtime Deploys with Unicorn
---



I was recently deploying a new Ruby on Rails application that used NGINX and Unicorn for production. During the deploy, my common practice was to stop the Unicorn processes and then restart them. I would do this by finding the PID (process id) of the running process, stop it using the kill command and then run the unicorn_rails command from my application root directory. This worked well enough that I put together a simple unicorn_init shell script to handle running the commands for me.

After a couple of deploys using this init script, I found that there was a significant inturruption caused to the site. This was due to the approximately 20 seconds it took for the Unicorn workers to launch. This was unaccepatble and I started a search for how to perform a zero downtime deploy for Unicorn.

My search lead me to the [Unicorn Signal Handling](http://unicorn.bogomips.org/SIGNALS.html) documentation. Unicorn makes use of [POSIX Signals](http://en.wikipedia.org/wiki/Unix_signal) for inter-process communication. You can send a signal to a process using the unfortunately named [kill system command](http://en.wikipedia.org/wiki/Kill_(command)). Reading through the different signals and what message they send to the Unicorn master and workers, I found a better approach to restarting my Unicorn processes that would result in no delay or inturruption to the website.

On the Signal Handling page (linked above) is a section called **Procedure to replace a running unicorn executable**. The key to my problem lied in this explanation:

> 
> 
> 
> You may replace a running instance of Unicorn with a new one without losing any incoming connections. Doing so will reload all of your application code, Unicorn config, Ruby executable, and all libraries.
> 
> 
> 

This was exactly what I needed. I did a quick search online to see if anyone had put together an init script that used this method for restarting Unicorn and found one on a [gist on github](https://gist.github.com/jaygooby/504875). With a few modifications, I assembled my new init script:

```bash
#!/bin/sh
# based on https://gist.github.com/jaygooby/504875
set -e

sig () {
  test -s "$PID" && kill -$1 `cat "$PID"`
}

oldsig () {
  test -s "$OLD_PID" && kill -$1 `cat "$OLD_PID"`
}

cmd () {
  case $1 in
    start)
      sig 0 && echo >&2 "Already running" && exit 0
      echo "Starting in environment $RAILS_ENV for config $CONFIG"
      $CMD
      ;;
    stop)
      sig QUIT && echo "Stopping" && exit 0
      echo >&2 "Not running"
      ;;
    force-stop)
      sig TERM && echo "Forcing a stop" && exit 0
      echo >&2 "Not running"
      ;;
    restart|reload)
      echo "Restarting with wait 30"
      sig USR2 && sleep 30 && oldsig QUIT && echo "Killing old master" `cat $OLD_PID` && exit 0
      echo >&2 "Couldn't reload, starting '$CMD' instead"
      $CMD
      ;;
    upgrade)
      sig USR2 && echo Upgraded && exit 0
      echo >&2 "Couldn't upgrade, starting '$CMD' instead"
      $CMD
      ;;
    rotate)
      sig USR1 && echo "rotated logs OK" && exit 0
      echo >&2 "Couldn't rotate logs" && exit 1
      ;;
    *)
      echo >&2 "Usage: $0 <start|stop|restart|upgrade|rotate|force-stop>"
      exit 1
      ;;
    esac
}

setup () {
  cd /home/mfarmer/camp2/rails # put your own path here
  export PID=/home/mfarmer/camp2/var/run/unicorn.pid # put your own path to the pid file here
  export OLD_PID="$PID.oldbin"
  export CONFIG=/home/mfarmer/camp2/unicorn/unicorn.conf # put your own path to the unicorn config file here
  export RAILS_ENV=development # Change for use on production or staging

  CMD="bundle exec unicorn_rails -c $CONFIG -E $RAILS_ENV -D"
}

start_stop () {
  . $CONFIG
  setup
  cmd $1
}

ARGS="$1"
start_stop $ARGS
```

The script is pretty self explanitory and it supports the major term signals outlined in the Unicorn documentation. With this new init script in hand, I now have a better way to restart Unicorn without negatively impacting the user experience.

There are a couple of caveats to this approach that you should be aware of before just slapping it into your system. First, in order to perform the restart, your application needs to essentially run twice until the old master is killed off. This means your hardware should be able to support running two instances of your application in both CPU and RAM at least temporarily. Second, you'll notice that the actual command being run looks something like bundle exec unicorn_rails -C /path/to/config/file -E development -D when interpolated by the script. This means that when you perform a rolling restart, those same parameters are used for the new application. So if anything changes in your config file or if you want to switch environments, you will need to completely stop the Unicorn processes and start them again for those changes to take effect.

Another thing you should be aware of is that your old application will be running for the 30 seconds it takes for the new application to load so if you perform any database migrations that could break the old version of your application, you may be better served by stopping the Unicorn process, running the migration, and then starting a new process. I'm sure there are ways to mitigate this but I just wanted to mention it here to help you be aware of the issue with this script in particular.


