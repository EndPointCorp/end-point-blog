---
author: Steph Skardal
gh_issue_number: 1099
tags: company, environment, tools, remote-work
title: On End Point's Development Environment
---

A few recent conversations have sparked my interest in writing up a blog post that summarizes the familiar elements of our development environments. The majority of End Pointers work remotely, but many of the tools listed below are common to many developers.

- **ssh/sftp**: We do primarily remote development. Many of us are familiar with local development, but remote development with camps (see next point) is typically the most efficient arrangement in working with multiple development instances that are accessible to clients for testing and staging.
- **camps**: [DevCamps](http://www.devcamps.org/) are a tool specific to and created by End Point, which are development instances with an entire webserver, database, and app server stack, similar to containers like [Docker](https://www.docker.com/). Check out [the DevCamps website](http://www.devcamps.org/) for more information.
- **vim/emacs/nano**: While most of our employees use vim or emacs for command-line editors, nano is an inefficient but easy to use editor that we can suggest to new developers. Not many of us use [IDEs](http://en.wikipedia.org/wiki/Integrated_development_environment), if at all.
- **screen/tmux**: screen and tmux are our preferred terminal multitasking and sharing.
- **command-line database interaction (specifically psql and mysql ad-hoc querying)**: Working with an SQL database through an [ORM](http://en.wikipedia.org/wiki/Object-relational_mapping) like [Active Record](http://guides.rubyonrails.org/active_record_basics.html), [DBIC](http://www.dbix-class.org/), etc. is not enough for us.
- ***nix / basic command-line interaction**: This topic could make up its own blog post, but some of the tools we use frequently are netstat/ss, ifconfig/ip, lsof, ps/top/htop/atop, free, df, nice/ionice, tail -f, sort, uniq -c, grep.
- **git &amp; [github](https://github.com/)**: Not uncommon to devshops these days, git is the most popular version control system, and github an extremely popular host of both open source and private repositories.
- **IRC, Skype, Google Hangouts, [appear.in](https://github.com/), [talky.io](https://talky.io/), [glideroom.com](https://glideroom.com/), Google Voice, &amp; *gasp* regular phones**: As remote developers, we communicate often and there are a number of tools available in the communication space that we leverage.

It's interesting to note that if any new developers come in with a preference for a trendy new tool, while we are happy to let them work in an environment that allows them to be efficient, ultimately we can't provide support for those tools that we are unfamiliar with.
