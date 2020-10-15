---
author: Mike Farmer
gh_issue_number: 521
tags: camps, rails, testing
title: Running Integration Tests in WebKit Without a Browser
---

As your ruby web applications increase in UI complexity, they get harder to test using the standard Cucumber or even RSpec integration test suites. This is because of introduction of JavaScript in your UI. You’ve probably been there before. Here’s the use case: You’ve written your integration tests for your Rails app and up to this point, you’ve been able to get away with not tagging your cucumber scenarios with the “@javascript” tag. Everything is going smoothly and then it’s time to implement that one UI feature that is going to require an Ajax call or some javascript to hide or unhide a crucial piece of the user experience. This **must** be included in your integration tests.

So you go through the pain of setting up cucumber to work with selenium and tag your scenario as javascript so that it will run the test in the browser. At first, there’s this thrill of excitement as you get to see Firefox load, and then run through a series of steps, executing your tests and then seeing them pass. Job done.

But maybe there’s a different scenario at play here. What if you don’t do your development in an environment that has a browser? At End Point, we are strong advocates of doing development on the [same environment that your app is going to run on](http://www.devcamps.org/why). It eliminates unexpected issues down the road. We believe in it so much, actually, that we’ve created [DevCamps](http://www.devcamps.org/) that allows you to setup development environments on a server.

Obviously, your selenium based tests are not going to work here without some work to get it to run headless.

The good folks at [thoughtbot](https://thoughtbot.com/) have come up with a great solution to this and it is called [capybara-webkit](https://github.com/thoughtbot). It assumes that you are using capybara for your testing framework. If you are using [webrat](https://github.com/brynary/webrat), the transition is fairly smooth. You’ll probably only need to change a few minor details in your tests.

What capybara-webkit does for you is enable you to run your tests inside of WebKit. This will simulate an environment that will be very close to what you would see in Google Chrome or Safari as well as many mobile browsers. I’ve found that except for some edge cases, it covers Firefox and IE as well.

To install capybara-webkit you will need to install the Qt development toolkit. It’s fairly straight forward so I’ll just refer you to the [github wiki](https://github.com/thoughtbot/capybara-webkit/wiki/Installing-QT) page for instructions for the various platforms. In Ubuntu, I just ran the following:

```nohighlight
sudo apt-get install libqt4-dev
```

If you are installing on a server environment, you’ll also need to install Xvfb. You can do that in Ubuntu with the following command:

```nohighlight
sudo apt-get install xvfb
```

It’s a little outside the scope of this blog post to go into other little things you need to setup with xvfb. The important thing is that you set it up to run on display 99. Another important note, is that you don’t have to set it up to run on boot. We will be starting it up when we run our tests if it isn’t running.

The next step is to configure your cucumber tests to use the capybara-webkit driver. To do that, add

```nohighlight
gem "capybara-webkit"
```

to your Gemfile in the development and test group. Then in your env.rb file for cucumber add the following lines:

```nohighlight
Capybara.javascript_driver = :webkit
```

In some cases, I’ve found it helpful to also specify a server port and app_host as follows:

```nohighlight
Capybara.server_port = '8000'
Capybara.app_host = 'http://localhost:8000'
```

Now your tests are setup to run in WebKit. The final step is running the tests. To do this, you’ll need to run them from within xvfb. You can do that with the following command:

```nohighlight
xvfb-run bundle exec cucumber
```

I’ve created an alias for this and dropped it in my .bashrc file. Here’s my entry, but you can set it up anyway you’d like.

```nohighlight
alias xcuke="xvfb-run bundle exec cucumber"
```

Now running tests is a simple as running xcuke from the root of my Rails application.

There are a couple of big benefits to running capybara-webkit. First is speed. In my experience tests run much faster than they do in Selenium. Second, all JavaScript errors are dumped to STDOUT so you can see them in the output of your cucumber tests. Third, all of your tests are being run on WebKit instead of rack so you get a test environment that acts more like a real browser would behave.

Thanks to the guys at thoughtbot for putting together this awesome gem.
