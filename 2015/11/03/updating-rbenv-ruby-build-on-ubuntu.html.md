---
author: Steph Skardal
gh_issue_number: 1171
tags: ruby, rails
title: 'Updating rbenv, ruby-build on Ubuntu: ruby version not found'
---



*Hi! Steph here, former long-time End Point employee now blogging from afar as a software developer for [Pinhole Press](https://pinholepress.com/). While I’m no longer an employee of End Point, I’m happy to blog and share here.*

A while back, I was in the middle of upgrading [Piggybak](http://www.piggybak.org/), an open source Ruby on Rails platform developed and supported by End Point, and I came across a quick error that I thought I'd share.

I develop locally and I use [rbenv](https://github.com/sstephenson/rbenv) on Ubuntu. I need to jump from Ruby 1.9.3 to Ruby 2.1.1 in this upgrade. When I attempt to run rbenv install 2.1.1, I see errors reporting *ruby-build: definition not found: 2.1.1*, meaning that rbenv and ruby-build (a plugin used with rbenv to ease installation) do not include version 2.1.1 in the available versions. My version of rbenv is out of date, so this isn't surprising. But how do I fix it?

I found many directions for updating rbenv and ruby-build with [Homebrew](http://brew.sh/) via Google, but that doesn't apply here. Most of the instructions point to running a git pull on rbenv (probably located in ~/.rbenv), but give no references to upgrading ruby-build.

```nohighlight
cd ~/.rbenv
git pull
```

I did a bit of experimenting and simply tried pulling to update the ruby-build plugin (also a git repo):

```nohighlight
cd ~/.rbenv/plugins/ruby-build/
git pull
```

And tada - that was all that was needed. rbenv version -l now includes ruby 2.1.1, and I can install it with rbenv install 2.1.1.


