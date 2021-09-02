---
author: Steph Skardal
title: Spree on Heroku for Development
github_issue_number: 275
tags:
- hosting
- rails
- spree
date: 2010-03-08
---

Yesterday, I worked through some issues to setup and run Spree on Heroku. One of End Point’s clients is using Spree for a multi-store solution. We are using the the [recently released Spree 0.10.0.beta gem](https://web.archive.org/web/20101128022443/http://spreecommerce.com/blog/2010/03/06/spree-0100beta-now-available/), which includes some significant Spree template and hook changes discussed [here](/blog/2010/01/rails-ecommerce-spree-hooks-tutorial) and [here](/blog/2010/01/rails-ecommerce-spree-hooks-comments) in addition to other substantial updates and fixes. Our client will be using Heroku for their production server, but our first goal was to work through deployment issues to use Heroku for development.

<a href="https://www.heroku.com/" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5446672221379055490" src="/blog/2010/03/spree-heroku-development-environment/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 194px; height: 66px;"/></a>

Since Heroku includes a free offering to be used for development, it’s a great option for a quick and dirty setup to run Spree non-locally. I experienced several problems and summarized them below.

## Application Changes

**1.** After a failed attempt to setup the basic Heroku installation described [here](https://devcenter.heroku.com/articles/how-heroku-works) because of a RubyGems 1.3.6 requirement, I discovered the need for [Heroku’s bamboo deployment stack](https://web.archive.org/web/20100308035824/http://docs.heroku.com/bamboo), which requires you to declare the gems required for your application. I also found a Spree Heroku extension and reviewed the code, but I wanted to take a more simple approach initially since the extension offers several features that I didn’t need. After some testing, I created a .gems file in the main application directory including the contents below to specify the gems required on the Badious Bamboo Heroku stack.

```nohighlight
rails -v 2.3.5
highline -v '1.5.1'
authlogic -v '>=2.1.2'
authlogic-oid -v '1.0.4'
activemerchant -v '1.5.1'
activerecord-tableless -v '0.1.0'
less -v '1.2.20'
stringex -v '1.0.3'
chronic -v '0.2.3'
whenever -v '0.3.7'
searchlogic -v '2.3.5'
will_paginate -v '2.3.11'
faker -v '0.3.1'
paperclip -v '>=2.3.1.1'
state_machine -v '0.8.0'
```

**2.** The next block I hit was that git submodules are not supported by Heroku, mentioned [here](https://web.archive.org/web/20100310162053/http://docs.heroku.com/constraints#git-submodules). I replaced the git submodules in our application with the Spree extension source code.

**3.** I also worked through addressing [Heroku’s read-only filesystem](https://web.archive.org/web/20100310162053/http://docs.heroku.com/constraints#read-only-filesystem) limitation. The setting perform_caching is set to true for a production environment by default in an application running from the Spree gem. In order to run the application for development purposes, perform_caching was set to false in RAILS_APP/config/environments/production.rb:

```ruby
config.action_controller.perform_caching             = false
```

Another issue that came up due to the read-only filesystem constraint was that the Spree extensions were attempting to copy files over to the rails application public directory during the application restart, causing the application to die. To address this issue, I removed the public images and stylesheets from the extension directories and verified that these assets were included in the main application public directory.

I also removed the frozen Spree gem extension public files (javascripts, stylesheets and images) to prevent these files from being copied over during application restart. These files were moved to the main application public directory.

**4.** Finally, I disabled the allow_ssl_in_production to turn SSL off in my development application. This change was made in the extension directory *extension_name*_extensions.rb file.

```ruby
AppConfiguration.class_eval do
  preference :allow_ssl_in_production, :boolean, :default => false
end
```

Obviously, this isn’t the preference setting that will be used for the production application, but it works for a quick and dirty Heroku development app. Heroku’s SSL options are described [here](http://docs.heroku.com/ssl).

## Deployment Tips

**1.** To create a Heroku application running on the Bamboo stack, I ran:

```nohighlight
heroku create --stack bamboo-ree-1.8.7 --remote bamboo
```

**2.** Since my git repository is hosted on github, I ran the following to push the existing repository to my heroku app:

```nohighlight
git push bamboo master
```

**3.** To run the Spree database bootstrap (or database reload), I ran the following:

```nohighlight
heroku rake db:bootstrap AUTO_ACCEPT=1
```

As a side note, I ran the command heroku logs several times to review the latest application logs throughout troubleshooting.

Despite the issues noted above, the troubleshooting yielded an application that can be used for development. I also learned more about Heroku configurations that will need to be addressed when moving the project to production, such as SSL setup and multi domain configuration. We’ll also need to determine the best option for serving static content, such as using Amazon’s S3, which is supported by the Spree Heroku extension mentioned above.
