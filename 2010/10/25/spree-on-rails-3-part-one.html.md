---
author: Steph Skardal
gh_issue_number: 376
tags: ecommerce, rails, spree
title: 'Spree on Rails 3: Part One'
---



A couple of weeks ago, I jumped into development on Spree on Rails 3. [Spree](http://spreecommerce.com/) is an open source Ruby on Rails ecommerce platform. End Point has been involved in Spree since its inception in 2008, and we continue to develop on Spree with a growing number of clients. Spree began to transition to Rails 3 several months ago. The most recent stable version of Spree (0.11.2) runs on Rails 2.*, but the edge code runs on Rails 3. My personal involvement of Rails 3 based Spree began recently; I waited to look at edge Spree until Rails 3 had a bit of momentum and until Rails 3 based Spree had more documentation and stability. My motivation for looking at it now was to determine whether End Point can recommend Rails 3 based Spree to clients and to share insight to my coworkers and other members of the Spree community.

First, I looked at the messy list of gems that have built up on my local machine throughout development of various Rails and Spree projects. I found this simple little script to remove all my old gems:

```bash
#!/bin/bash

GEMS=`gem list --no-versions`
for x in $GEMS; do sudo gem uninstall $x --ignore-dependencies -a; done
```

Then, I ran gem install rails to install Rails 3 and dependencies. The following gems were installed:

```nohighlight
abstract (1.0.0)
actionmailer (3.0.1)
actionpack (3.0.1)
activemodel (3.0.1)
activerecord (3.0.1)
activeresource (3.0.1)
activesupport (3.0.1)
arel (1.0.1)
builder (2.1.2)
bundler (1.0.2)
erubis (2.6.6)
i18n (0.4.1)
mail (2.2.7)
mime-types (1.16)
polyglot (0.3.1)
rack (1.2.1)
rack-mount (0.6.13)
rack-test (0.5.6)
rails (3.0.1)
railties (3.0.1)
rake (0.8.7)
thor (0.14.3)
treetop (1.4.8)
tzinfo (0.3.23)
```

Next, I cloned the Spree edge with the following command from [here](http://github.com/railsdog/spree):

```nohighlight
git clone http://github.com/railsdog/spree.git
```

In most cases, developers will run Spree from the gem and not the source code ([see the documentation for more details](http://edgeguides.spreecommerce.com/)). In my case, I wanted to review the source code and identify changes. You might notice that the new spree core directory doesn't look much like the old one, which can be explained by the following: the Spree core code has been broken down into 6 separate core gems (api, auth, core, dash, promo, sample) that run as Rails Engines.

After checking out the source code, the first new task to run with edge Spree was bundle install. The bundler gem is intalled by default in Rails 3. It works out of the box in Rails 3, and can work in Rails 2.3 with  additional file and configuration changes. Bundler is a dependency management tool. Gemfile and Gemfile.lock in the Spree core specify which gems are required for the application. Several gems were installed with Spree's bundler configuration, including:

```nohighlight
Installing webrat (0.7.2.beta.1) 
Installing rspec-rails (2.0.0.beta.19) 
Installing ruby-debug-base (0.10.3) with native extensions 
Installing ruby-debug (0.10.3) 
Installing state_machine (0.9.4) 
Installing stringex (1.1.0) 
Installing will_paginate (3.0.pre2) 
Using spree_core (0.30.0.beta2) from source at /var/www/spree 
Using spree_api (0.30.0.beta2) from source at /var/www/spree 
Using spree_auth (0.30.0.beta2) from source at /var/www/spree 
Using spree_dash (0.30.0.beta2) from source at /var/www/spree 
Using spree_promo (0.30.0.beta2) from source at /var/www/spree
Using spree_sample (0.30.0.beta2) from source at /var/www/spree
```

The only snag I hit during bundle install was that the nokogiri gem required two dependencies be installed on my machine (libxslt-dev and libxml2-dev).

To create a project and run all the necessary setup, I ran rake sandbox, which completed the tasks listed below. The tasks created a new project, completed the basic gem setup, installed sample data and images, and ran the sample data bootstrap migration. In some cases, Spree sample data will not be used – the latter two steps can be skipped. The sandbox/ application directory contained a directory of folders that one might expect when developing in Rails (app, db, lib, etc.) and sandbox/ itself runs as a Rails Engine.

```nohighlight
steph@machine:/var/www/spree$ rake sandbox
(in /var/www/spree)
         run  rails new sandbox -GJT from "."
      append  sandbox/Gemfile
         run  rails g spree:site -f from "./sandbox"
         run  rake spree:install from "./sandbox"
         run  rake spree_sample:install from "./sandbox"
         run  rake db:bootstrap AUTO_ACCEPT=true from "./sandbox"
```

After setup, I ran rails server, the new command for starting a server in Rails 3.*, and verified my site was up and running.

<a href="/blog/2010/10/25/spree-on-rails-3-part-one/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5532048412737352690" src="/blog/2010/10/25/spree-on-rails-3-part-one/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 204px;"/></a>

Hooray - it's up!

There wasn't much to getting a Rails 3 application up and running locally. I removed all my old gems, installed Rails 3, grabbed the repository, allowed bundler to install dependencies and worked through one snag. Then, I ran my Spree specific rake task to setup the project and started the server. Tomorrow, I [share my experiences on extension development in Rails 3 based Spree](/blog/2010/10/25/spree-on-rails-3-part-two).


