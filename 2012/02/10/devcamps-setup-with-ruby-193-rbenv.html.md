---
author: Richard Templet
gh_issue_number: 552
tags: camps, hosting, rails
title: DevCamps setup with Ruby 1.9.3, rbenv, Nginx and Unicorn
---

I was working with Steph Skardal on the setup of a new [DevCamps](http://www.devcamps.org/) installation that was going to need to use [Ruby 1.9.3](http://www.ruby-lang.org/en/), [Rails 3](http://rubyonrails.org/), [Unicorn](http://unicorn.bogomips.org/) and [Nginx](http://wiki.nginx.org/Main). This setup was going to be much different than a standard setup due to the different application stack that was required.

The first trick for this was going to get Ruby 1.9.3 on the server. We were using Debian Squeeze but that still only comes with Ruby 1.9.1. We wanted Ruby 1.9.3 for the increased overall speed and significant speed increase with Rails 3. We decided on using [rbenv](https://github.com/sstephenson/rbenv) for this task. It’s a very easy to setup utility that allows you to maintain multiple version of Ruby in your system user account without the headache of adjusting anything but the PATH environment variable. It takes advantage of another easy to setup utility called [ruby build](https://github.com/sstephenson/ruby-build) to handle the actual installation of the Ruby source code.

A quick and easy version for setting up a user with this is as follows:

Ensure you are in the home directory. Then, clone the repository into a .rbenv directory

```nohighlight
git clone git://github.com/sstephenson/rbenv.git .rbenv
```
Adjust your users path to find the newly installed commands

```nohighlight
echo 'export PATH=$HOME/.rbenv/shims:$HOME/.rbenv/bin:$PATH' >> ~/.bash_profile
```
Install Ruby version 1.9.3-p0

```nohighlight
rbenv install 1.9.3-p0
```
Make Ruby version 1.9.3-p0 your default version every time you log in

```nohighlight
rbenv global 1.9.3-p0
```
Install the bundler gem for Ruby version 1.9.3-p0

```nohighlight
gem install bundler
```
Refresh rbenv to let it know the new system command bundler exists

```nohighlight
rbenv rehash
```

Now you are ready to use the bundler gem to install any other gems required for the application.

The normal camps setup assumes you are going to be using Apache for the web server. In this case, we wanted to use Nginx due to memory constraints. We decided to use the proxy capability and just proxy through to Unicorn instead of having to build our own version Nginx to use Passenger. To do this, we had to use a feature in the local-config file in camps that allows you to skip the Apache setup and use your own commands to start, stop and restart your web server and application.  Here is the example from our local-config that controlls Nginx and Unicorn. This approach could also be used with Interchange or any other application if you need other services started when mkcamp is run.

```nohighlight
skip_apache:1
httpd_start:/usr/sbin/nginx -c __CAMP_PATH__/nginx/nginx.conf
httpd_stop:pid=`cat __CAMP_PATH__/var/run/nginx.pid 2>/dev/null` && kill $pid
httpd_restart:pid=`cat __CAMP_PATH__/var/run/nginx.pid 2>/dev/null` && kill -HUP $pid || /usr/sbin/nginx -c __CAMP_PATH__/nginx/nginx.conf
app_start:__CAMP_PATH__/bin/start-app
app_stop:pid=`cat __CAMP_PATH__/var/run/unicorn.pid 2>/dev/null` && kill $pid
app_restart:pid=`cat __CAMP_PATH__/var/run/unicorn.pid 2>/dev/null` && kill $pid ; sleep 5 ;  __CAMP_PATH__/bin/start-app
```
The contents of the start-app script is simply.

```nohighlight
cd __CAMP_PATH__ && bundle exec unicorn_rails -c __CAMP_PATH__/config/unicorn.conf.rb -D
```

You could create one script that handles all aspects of start, stop and restart if you wanted. This setup really wasn’t much harder than a normal Ruby on Rails setup. The added time here required to set up rbenv per camp user is offset by the fact that users can manage and try multiple versions of ruby.
