---
author: Brian Buchalter
gh_issue_number: 700
tags: hosting, rails, security
title: Setting user ownership of nginx and Passenger processes
---



Do this now on all your production Rails app servers:

```nohighlight
ps ux | grep Rails
```

The first column in the results of that command show which user runs your Rails and Passenger processes. If this is a privileged user (sudoer, or worse yet password-less sudoer), then this article is for you.

### Assumptions Check

There are several different strategies for modifying which user your Rails app runs as. By default the owner of config/environment.rb is the user which Passenger will run your application as. For some, simply changing the ownership of this file is sufficient, but in some cases, we may want to force Passenger to always use a particular user.

This article assumes you are running nginx compiled with Passenger support and that you have configured an unprivileged user named rails-app. This configuration has been tested with nginx version 0.7.67 and Passenger version 2.2.15. (Dated I know, but now that you can't find the docs for these old versions, this article is extra helpful.)

### Modifying nginx.conf

The changes required in nginx are very straight forward.

```nohighlight
# Added in the main, top-level section
user rails-app;

# Added in the appropriate http section among your other Passenger related options
passenger_user_switching off;
passenger_default_user rails-app;
```

The first directive tells nginx to run it's worker processes as the rails-app user. It's not completely clear to me why this was required, but failing to include this resulted in the following error. Bonus points to any one who can help me understand this one.

```nohighlight
[error] 1085#0: *1 connect() to unix:/tmp/passenger.1064/master/helper_server.sock failed (111: Connection refused) while connecting to upstream, client: XXX, server: XXX, request: "GET XXX HTTP/1.0", upstream: "passenger://unix:/tmp/passenger.1064/master/helper_server.sock:", host: "XXX"
```

The second directive, passenger_user_switching off, tells Passenger to ignore the ownership of config/environment.rb and instead use the user specified in the passenger_default_user directive. Pretty straight forward!

### Log File Permissions Gotcha

Presumably you're not storing your production log files in your apps log directory, but instead in /var/log/app_name and using logrotate to archive and compress your logs nightly. Make sure you update the configuration of logrotate to create the new log files with the appropriate user. Additionally, make sure you change the ownership of the current log file so that Passenger can write your applications logs!


