---
author: Steph Skardal
gh_issue_number: 657
tags: hosting, piggybak, rails
title: '.rbenv and Passenger: Working through an Upgrade'
---

Yesterday, I worked on upgrading the [Piggybak demo](https://github.com/piggybak/demo) application, which runs on [Piggybak](https://github.com/piggybak/piggybak), an open source Ruby on Rails ecommerce plugin developed and maintained by End Point. The demo was running on Ruby 1.8.7 and Rails 3.1.3, but I wanted to update it to Ruby 1.9.* and Rails 3.2.6 to take advantage of improved performance in Ruby and the recent Rails security updates. I also wanted to update the Piggybak version, since there have been [several recent bug fixes and commits](https://github.com/piggybak/piggybak/commits/master).

One of the constraints with the upgrade was that I wanted to upgrade via [.rbenv](https://github.com/rbenv/rbenv), because End Point has been happily using .rbenv recently. Below are the steps [Richard](/team/richard_templet) and I went through for the upgrade, as well as a minor Passenger issue.

### Step 1: .rbenv Installation

First, I followed the instructions [here](https://github.com/rbenv/rbenv) to install rbenv and Ruby 1.9.3 locally under the user that Piggybak runs under (let’s call it the **steph** user). I set the local Ruby version to my local install. I also installed bundler using the local Ruby version.

### Step 2: bundle update

Next, I blew away the existing bundle config for my application, as well as the installed bundler gem files for the application. I followed the standard steps to install and update the new gems with the local updated Ruby and updated Rails. Then I restarted the app.

### Step 3: Fail

At this point, my application would not restart, and the backtrace complained of a Passenger issue, *and* it referenced Ruby 1.8. Richard and I investigated the errors and concluced that the application’s Passenger configuration was still referencing the system Ruby install and the outdated Passenger installation.

Here’s where I hit the catch 22: I needed root access to update the passenger.conf as well as to install Passenger against Ruby 1.9.3. This defeated the purpose of using .rbenv and working with a local Ruby install only.

### Step 4: Local Passenger Installation

To install Passenger against the local Ruby version, I decided to install it as the **steph** user. First, I installed the gem:

```ruby
gem install passenger
```

Then, I went to the local installed version of Passenger to run the installation:

```bash
cd /home/steph/.rbenv/versions/1.9.3-p194/lib/ruby/gems/1.9.1/gems/passenger-3.0.13/bin
./passenger-install-apache2-module
```

Next, I copied the passenger installation output to the passenger.conf file:

```
   LoadModule passenger_module /home/steph/.rbenv/versions/1.9.3-p194/lib/ruby/gems/\
     1.9.1/gems/passenger-3.0.13/ext/apache2/mod_passenger.so
   PassengerRoot /home/steph/.rbenv/versions/1.9.3-p194/lib/ruby/gems/1.9.1/gems/passenger-3.0.13
   PassengerRuby /home/steph/.rbenv/versions/1.9.3-p194/bin/ruby
```

With a server restart, the Piggybak demo was up and running on updated Ruby and Rails!

<img border="0" src="/blog/2012/06/22/rbenv-passenger-upgrade/image-0.png" width="600"/>

### Conclusion

Retrospectively, I could have avoided the Passenger issue by installing Ruby 1.9.3 on the server as root, because there isn’t much else on the server. But I like using .rbenv and it’s possible that a Passenger upgrade won’t be required with every Ruby update, so the new Passenger configuration is acceptable [to me, for now].
