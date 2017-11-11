---
author: Tim Case
gh_issue_number: 716
tags: piggybak, rails
title: How to Build a Command Line Executable Installer with Rubygems and Thor
---



Gems for Rails often need the user to do something more for installation than just adding the gem to a Gemfile and running bundler install.  Sometimes it's a simple matter of copying over some migration files and sometimes it's just setting up a config file, and most of the time these simple installation steps are best handled with a well written installation section in the README file.  When the installation process is more complex a long README might not be so enticing to the potential gem user, in a world where everyone has a finger on the back button it's nice to be able to create an installer that allows the user to complete complex installation tasks by executing a one liner and that's where an installer made through Gem executables and [Thor](https://github.com/wycats/thor) can come in handy.

We wanted to make it easier for new users of Piggybak to get started and decided that an installer was the best way to do that.  Creating a binary installer that is installed by Rubygems is one of those esoteric things that may not be thought of as one of the core strengths of Rubygems and Rails but it's a bonus to be able to do something like this without a whole lot of fuss.

### Creating an installer with Rubygems, and Thor:

1. In your Rails app, create a file in your lib directory that inherits from Thor, this file will house all of your command line actions.  Thor is already included as a part of Rails so you don't need to add it to your Gemfile. 
1. Inside your Thor subclass, define methods which will in turn become invokable actions from the command line.  Installers usually need to copy files around and execute commands, Thor provides a library the covers the most common cases which can be added to your class by including Thor::Actions [(A list of the included actions)](http://rdoc.info/github/wycats/thor/master/Thor/Actions).  Have a look at the [Piggybak installer class](https://github.com/piggybak/piggybak/blob/master/lib/piggybak/cli.rb), and you'll see that the Thor actions are not too complicated to understand.
1. Create a bin directory in your Rails directory that will be used to start your Thor class, add a file with the name of your executable which starts your Thor class (details below)
1. Add an "executables" entry for the file in your bin directory to your gemspec file 

### Add a file to your bin folder than starts Thor

The code below shows the file located in the bin directory and it could act as a template for your own executable.  The things to note are the inclusion of the ruby shebang, and the requiring of the piggybak cli class.  Finally at the end of the file the start method is sent to the Thor class.

```ruby
#!/usr/bin/env ruby

require 'rubygems'

begin
  require 'piggybak/cli'
rescue LoadError => e
warn 'Could not load "piggybak/cli"'
  exit -1
end

Piggybak::CLI.start

```

### Add an entry to your gemspec for the executable

Rubygems expects the executable to be in a directory called bin which is in the same directory as the gemspec, if you want to place the executable in a different location you'll need to specify that in your gemspec with a "bindir" entry. (Check the [Rubygem docs](http://docs.rubygems.org/) for a more detailed explanation.)

```ruby
spec.executables << 'piggybak'
```

Once that's done your gem is ready to go and can be included inside the Gemfile of a Rails app.  When the gem is installed, Rubygems will place a file in your Ruby bin directory that can be invoked via the command line.

```bash
$ piggybak install
```


