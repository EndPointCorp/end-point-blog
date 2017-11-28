---
author: Christopher Nehren
gh_issue_number: 117
tags: tips
title: She sells C shells by the seashore
---

In contrast to my previous post on [tabs in vim](/blog/2009/03/11/vim-tip-of-day-tabbed-editing), here's a different way of managing multiple files, multiple SQL console sessions, multiple nearly anything. This works with any program that behaves well with regard to Unix job control, and really allows Unix to shine as an IDE in its own right. The emphasis here will be on using whatever tools are suitable to do the job, rather than on one specific editor. Note that the details given here will not work very well for network programs that assume a constant connection like an IRC client. However, at least the Postgres and MySQL consoles both support this feature, and they're the only "networked" applications I can imagine using in this way. This post will focus more on a way of thinking than on technical know-how, though there is a bit of how-to mixed in.

Most readers are familiar with backgrounding a task at a Unix terminal with ^Z and then bg. Something that is less common, at least in my experience (in favor of GNU screen and the like), is using shell job control for anything more than detaching a running program from one's terminal. When applied liberally, the tactic allows one to harness the power of Unix all via one login. To better envision this workflow, let us envision a scenario that many MVC developers have experienced: extending all three parts of an existing application.

This setup comprises at least five different tasks:

- modifying the model, either directly through an RDBMS console or indirectly via an ORM mapper;- modifying the view, which typically involves editing template files of some flavor;- modifying the controller, which typically involves editing code files;- restarting the application;- testing the application, which may involve watching log files;- and perhaps modifying code files that comprise either the model or the view of the MVC implementation.

Many users would either log in multiple times and start editors / RDBMS consoles in multiple shells, or use a terminal multiplexer like GNU Screen to achieve the same goal. These are both respectable and venerable means of achieving the same task, each with pros and cons. I trust that people reading this are familiar enough with both methods to grasp what these pros and cons are.

However, in my experience, I have found that using shell job control is the fastest and most efficient way to manage this sort of workflow. The general idea works something like this:

1. Start every program one anticipates needing in this session. This includes text editors, RDBMS consoles, logfile watchers, etc.1. Background suspend every started program and then start the next. This, then, sets everything up for bringing programs to the foreground when needed.1. As one is working, foreground each task when needed, backgrounding when not finished.1. Remember to hit ^Z rather than quitting the programs.1. Repeat until the desired goal is achieved.

Now, this is quite handy, but typing fg 2 and the like is rather annoying and requires one to pay attention to job numbers. I thought IDEs were supposed to make one's job easier? There's a handy sequence for bringing jobs to the foreground that bash, zsh, and tcsh all support. To bring to the foreground a job matching a specific string, one can use %?string where the string is a unique bit of the job name--file names work well, here.

Given this, then, it's not too much of a stretch to start each job, ^Z it, and then bring it to the foreground when needed. In this way, one can use an editor when needed, restart the application when needed, view log files when needed, etc., all from one shell. This is not the sort of thing where a demo is useful. Workflows vary among developers, and this is something that everyone must adapt to their own way of doing things. When a colleague shared the idea with me, its simple but powerful elegance surprised me--the same sort of simple, powerful elegance I see everywhere in Unix.

