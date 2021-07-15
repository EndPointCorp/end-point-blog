---
author: Kamil Ciemniewski
title: Debugging Sinatra with racksh and pry
github_issue_number: 709
tags:
- ruby
- sinatra
date: 2012-10-17
---



One of the most beloved features of the Ruby on Rails framework is certainly its “console” facility. Ruby on Rails programmers often don’t need any debugger simply because they can view their application state in their app’s console. But what do we have at our disposal when using Sinatra?

### The sheer beauty of Sinatra

Many of us who had an opportunity to play with Sinatra stand in awe of its pure simplicity. It gives you raw power as a programmer to structure a whole project however you like. It isn’t as opinionated as Ruby on Rails - in fact, there is even a framework called [Padrino](http://www.padrinorb.com/) built upon Sinatra leveraging its unopinionated nature.

Sinatra’s way (®) was also employed in many other languages like JavaScript (through Node.js), Clojure and even in Haskell.

### The elephant in the room

The above paragraph seems cool, doesn't it? It provides a catchy and exciting marketing copy, just enough to make you a little bit curious about this whole Sinatra thing. And while Sinatra stands the test of practicality, otherwise it wouldn't be hailed as widely as it is today, there are “gotchas” waiting just around the corner.

Almost every web application could be simplified just to this description: managing persistent data state and rendering this state back to the user. I don’t have to remind us all how tricky this state-management can be at times...

### Dude, where is my console?

The first of many Sinatra gotchas is there is no such thing as “Sinatra console”. You’re doomed to write all those pesky “puts” in almost every place in your code and then make countless number of requests while watching the output, right? No! Chin up, my friend. Racksh to the rescue!

### Racksh? You mean console for ... Rack?

Yup! It’s not only a solution for Sinatra, but virtually all Rack-based applications. Taken from its GitHub description:

*It's like script/console in Rails or merb -i in Merb, but for any app built on Rack. You can use it to load application environment for Rails, Merb, Sinatra, Camping, Ramaze or your own framework provided there is config.ru file in app's root directory.*

*Its purpose is to allow developer to introspect his application and/or make some initial setup. You can for example run DataMapper.auto_migrate! or make a request to /users/666 and check response details. It's mainly aimed at apps that don't have console-like component (i.e. app built with Sinatra) but all frameworks can benefit from interactive Rack stack and request introspection.*

Pretty cool, isn’t it? To install it just put in Gemfile:

```ruby
gem "racksh"
```

Then:

```bash
bundle install 
```

and e-voilà - you’ve got your Sinatra console at your disposal. To run it just do:

```bash
racksh
```

Assuming you have config.ru in current directory - otherwise just specify the path to it with CONFIG_RU env variable, like:

```bash
CONFIG_RU=/some/path/config.ru racksh
```

### But what if I still need to examine state in my handlers?

We all know how cumbersome it is to get our old ruby-debugger to play nice with ruby-1.9.3. But fear not, we’ve got more cool tools under the belt. One of these is called “pry”.

Taken from its website: Pry is a powerful alternative to the standard irb shell for Ruby. It features syntax highlighting, a flexible plugin architecture, runtime invocation and source and documentation browsing.

Coupled with gem called “pry-debugger” it gives you far better experience debugging than you ever had in the old days with ruby-debugger.

To use it you just call binding.pry wherever you want the execution of your code to suspend giving you an opportunity to play with its current state. So the only difference in usage from old ruby-debugger is putting “binding.pry” instead of “debugger”.

For example:

```ruby
def index
  @collection = SomeModel.where(name: params[:name])
  binding.pry # let’s see what we have here in @collection..
  (...)
end
```

Executing second line of this handler will hold further execution and start a REPL session with same execution state as this line in handler would have.

Now, having included pry-debugger in your Gemfile allows you to inspect all the state as well as execute usual debugging commands: step, next, continue, finish and breakpoints.

Read more at:

- Sinatra: [http://www.sinatrarb.com/](http://www.sinatrarb.com/)
- Racksh: [https://github.com/sickill/racksh](https://github.com/sickill/racksh)
- Pry: [http://pryrepl.org/](http://pryrepl.org/)
- Pry-Debugger: [https://github.com/nixme/pry-debugger](https://github.com/nixme/pry-debugger)


