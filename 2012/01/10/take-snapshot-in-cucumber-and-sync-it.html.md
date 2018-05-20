---
author: Mike Farmer
gh_issue_number: 540
tags: rails
title: Take a snapshot in Cucumber and sync it with Dropbox!
---

In a previous [post](/blog/2011/12/08/running-integration-tests-in-webkit) I talked about running cucumber using [capybara-webkit](https://github.com/thoughtbot/capybara-webkit). In a recent project using this setup I noticed that I couldn’t use capybara in connection with [launchy](https://github.com/copiousfreetime/launchy) to open up a page in the browser for debugging tests. The “save and open page” step is one that I used a lot when I was developing locally. But now that I’m developing on a server, I don’t have any way save the page or open it for review.

The solution I found to this comes in two parts. First, create a “take a snapshot” cucumber step that drops a snapshot of the HTML and a PNG of the page in a temp directory. Second, add that temp directory to [dropbox](http://www.dropbox.com) so that it gets synced to my desktop automatically when it is created.

Wait, seriously? Dropbox? 

Yes, absolutely. Dropbox.

I often develop inside of my dropbox folder because A) all my code is automatically backed up, even with versions and B) because it’s really simple to sync my code to other computers. I’ll admit that one problem I had early on was that log files were using an awful amount of bandwidth getting copied up constantly, but I solved this by adding the log directory to an exclusions list. I’ll show you how to do that below.

### Step 1: Create a “take a snapshot” step.

The first thing we need to do is setup our take a snapshot step. For our app, it made the most sense to put this in web_steps.rb but you can add it to any of your step_definitions files.  The step looks like this:

```nohighlight
Then /take a snapshot/ do
  # save a html snapshot
  html_snapshot = save_page
  puts "Snapshot saved: \n#{html_snapshot}"

  # save a png snapshot
  png_snapshot = html_snapshot.gsub(/html$/, "png")
  page.driver.render png_snapshot
  puts "Snapshot saved: \n#{png_snapshot}"

end
```

The first line there is fairly simple. Capybara provides a save_page method by default which is going to save the page to tmp/capybara off the root of your app. The file will look something like this: capybara-20111228210921591550991.html. You can see the source code [on the rdoc page](http://rubydoc.info/github/jnicklas/capybara/master/Capybara/Session:save_page) for more information on how this works. If you want to customize the file name, you can do that by calling Capybara.save_page directly like this:

```nohighlight
Capybara.save_page(body, 'my_custom_file.html')
```

This reveals what save_page is actually doing. Every cucumber step has available to it by default Capybara::Session. The source html of the current page is stored in Capybara::Session#body. The save_page method is just writing the source html to a file.

The next block of code saves the page as a PNG file. This comes from the capybara-webkit driver so this will only work if you are using that driver specifically. (You can [explore the code on github](https://github.com/thoughtbot/capybara-webkit/blob/5adab74465f42efcf286f0f94ed5a5d1a04ce6cd/lib/capybara/driver/webkit.rb#L106) to get more information, but [basically it’s calling](https://github.com/thoughtbot/capybara-webkit/blob/5adab74465f42efcf286f0f94ed5a5d1a04ce6cd/lib/capybara/driver/webkit/browser.rb#L99) the “Render” command on webkit and then storing the image as a PNG.)

All I’m doing here is changing out the html file extension for png so that the files will be easy to find. You can also pass width and height options if you’d like with a hash {:width => 1000, :height => 10}.

### Step 2: Setup Dropbox.

I didn’t know this until recently but you can [run dropbox on a linux server](https://www.dropbox.com/install?os=lnx) without a UI. It is available as a binary for Ubuntu (.deb), Fedora (.rpm), Debian (.deb). You can also compile from source if you’d like. Since I’m doing my development on a server, however, I wanted a little bit more of an isolated installation and luckily Dropbox has the answer for me. It’s called their command line installation and it works great. Here are the instructions from the [web site](https://www.dropbox.com/install?os=lnx):

For 32 bit: 

```nohighlight
cd ~ && wget -O - http://www.dropbox.com/download?plat=lnx.x86 | tar xzf -
```

or 64 bit: 

```nohighlight
cd ~ && wget -O - http://www.dropbox.com/download?plat=lnx.x86_64 | tar xzf -
```

You’ll also need a small python script for working with the daemon. You can download it from the web site or from [here](https://www.dropbox.com/download?dl=packages/dropbox.py).

The dropbox cli will walk you through a simple authentication process and then start downloading your dropbox folder in your ~/Dropbox directory when you run dropbox.py start for the first time. If your dropbox folder is like mine, this is going to download way more stuff than you’d probably want on your server so you’ll need to add some exceptions. I created a folder in Dropbox for my screenshots called ~/Dropbox/cuke_snapshots and then excluded everything else. Here’s how I did it with the dropbox.py file (I renamed dropbox.py to just dropbox for ease and clarity. It’s also helpful to put it in a directory that’s in your PATH):

```nohighlight
cd ~/Dropbox
dropbox exlcude add Public Photos
```

That adds the Public and Photos folders to the exclusion list and Dropbox deletes them from the system for you. The nice thing is that you can continue to add folder names to the end of that command so you can get rid of stuff really quick. There are a bunch of options using the dropbox cli that make working with dropbox on the server very simple and flexible.

```nohighlight
status       get current status of the dropboxd
help         provide help
puburl       get public url of a file in your dropbox
stop         stop dropboxd
running      return whether dropbox is running
start        start dropboxd
filestatus   get current sync status of one or more files
ls           list directory contents with current sync status
autostart    automatically start dropbox at login
exclude      ignores/excludes a directory from syncing
lansync      enables or disables LAN sync
```

The last step is to create a symbolic link from your app into your dropbox folder. I did this with the following command:

```nohighlight
mkdir -p ~/Dropbox/cuke_snapshots/my_app/capybara
cd ~/rails_apps/my_app/tmp
rm -rf capybara   (if it already exists)
ln -s ~/Dropbox/cuke_snapshots/my_app/capybara
```

Of course there are many ways you could set this up, but this will get the job done.

### Using “take a snapshot”

Once you have everything setup, all you need to do is call the cucumber step from within your scenarios. Here’s a contrived example:

```nohighlight
@javascript   # may not be needed if everything is using webkit-capybara
Scenario: A shopper wants to checkout
  When I go to the address step
  And I fill in the address information
  And I follow "Next"
  Then I should be on the delivery step
  And take a snapshot
```

When the scenario runs, it will drop the html and png file in your dropbox directory which will immediately be synced to your local machine. In my experience, by the time I open up the folder on my local machine, the file is there ready for inspection.
