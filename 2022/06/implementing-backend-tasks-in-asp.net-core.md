---
author: "Kevin Campusano"
title: "Implementing Backend Tasks in ASP.NET Core"
date: 2022-06-26
tags:
- csharp
- dotnet
---

# Implementing Backend Tasks in ASP.NET Core

[As we've already established](https://www.endpointdev.com/blog/2022/01/database-integration-testing-with-dotnet/), [Ruby on Rails](https://rubyonrails.org/) is great. The amount and quality of tools that Rails puts at our disposal when it comes to developing web applications is truly outstanding. One aspect of web application development that Rails makes particularly easy is that of creating backend tasks.

These can be anything from database maintenance, filesystem cleanup, overnight heavy computations, bulk email dispatch, etc. In general, functionality that is tipically initiated by an sysadmin in the backend, or scheduled in a [cron](https://en.wikipedia.org/wiki/Cron) job, which has no GUI, but rather, is invoked via command line.

By integrating with [Rake](https://github.com/ruby/rake), Rails allows us to [very easily write such tasks](https://guides.rubyonrails.org/command_line.html#custom-rake-tasks) as plain old [Ruby](https://ruby-doc.org/) scrips. These scripts have access to all the domain logic and data that the full fledged Rails app has access to. The cherry on top is that the command line interface to invoke such tasks is very straightforward. It looks something like this: `bin/rails fulfillment:process_new_orders`.

All this is included right out of the box for new Rails projects.

[ASP.NET Core](https://dotnet.microsoft.com/en-us/apps/aspnet), which is also great, doesn't support this out of the box like Rails does.

However, I think we should be able to implement our own without too much hassle, and have a similar sysadmin experience. Let's see if we can do it.

# What we want to accomplish

So, to put it in concrete terms. We want to be able to create a backend task that has access to all the logic and data of an existing ASP.NET Core application. The task should be ivokable via command line interface, so that it can be easily called via the likes of cron or other scripts.

In order to meet these requirements, we will create a new .NET console app that:

1. References the existing ASP.NET Core project.
2. Loads all the classes from it and makes instances of them available via dependency injection.
3. Has a usable, UNIX-like command line interface that sysadmins would be familiar with.
4. Is invokable via the [.NET CLI](https://docs.microsoft.com/en-us/dotnet/core/tools/).

Let's get to it.

