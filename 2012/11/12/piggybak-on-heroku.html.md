---
author: Steph Skardal
gh_issue_number: 723
tags: ecommerce, hosting, piggybak, rails
title: Piggybak on Heroku
---

Several weeks ago, we were contacted through our website with a request for Heroku support on [Piggybak](http://www.piggybak.org). Piggybak is an open source Ruby on Rails ecommerce platform developed and maintained by End Point. Piggybak is similar to many other Rails gems in that it can be installed from Rubygems in any Rails application, and Heroku understands this requirement from the application’s Gemfile. This is a brief tutorial for getting a Rails application up and running with Piggybak. For the purpose of this tutorial, I’ll be using the existing [Piggybak demo](http://www.piggybak.org/demo_details.html) for deployment, instead of creating a Rails application from scratch.

**a)** First, clone the existing [Piggybak demo](http://www.piggybak.org/demo_details.html). This will be your base application. On your development machine (local or other), you must run bundle install to get all the application’s dependencies.

**b)** Next, add config.assets.initialize_on_precompile = false to config/application.rb to allow your assets to be compiled without requiring creating a local database.

**c)** Next, compile the assets according to [this Heroku article](https://devcenter.heroku.com/articles/rails3x-asset-pipeline-cedar) with the command RAILS_ENV=production bundle exec rake assets:precompile. This will generate all the application assets into the public/assets/ directory.

**d)** Next, add the assets to the repo by removing public/assets/ from .gitignore and committing all modified files. Heroku’s disk read-only limitation prohibits you from writing public/assets/ files on the fly, so this is a necessary step for Heroku deployment. It is not necessary for standard Rails deployments.

**e)** Next, assuming you have a Heroku account and have installed the [Heroku toolbelt](https://toolbelt.heroku.com/debian), run heroku create to create a new Heroku application.

**f)** Next, run git push heroku master to push your application to your new Heroku application. This will push the code and install the required dependencies in Heroku.

**g)** Next, run heroku pg:psql, followed by \i sample.psql to load the sample data to the Heroku application.

**h)** Finally, run heroku restart to restart your application. You can access your application through a browser by running heroku open.

That should be it. From there, you can manipulate and modify the demo to experiment with Piggybak functionality. The major difference between Heroku deployment and standard deployment is that all your compiled assets must be in the repository because Heroku cannot write them out on the fly. If you plan to deploy the application elsewhere, you will have to make modifications to the repository regarding public/assets.

A full set of commands for this tutorial includes:

```nohighlight
# Clone and set up the demo app
git clone git://github.com/piggybak/demo.git
bundle install
# add config.assets.initialize_on_precompile = false
# to config/application.rb

# Precompile assets and add to repository
RAILS_ENV=production bundle exec rake assets:precompile
# edit .gitignore here to stop ignoring public/assets/
git add .
git commit -m "Heroku support commit."

# Deploy to Heroku
heroku create
git push heroku master
heroku pg:psql
>> \i sample.psql
heroku restart
heroku open
```
