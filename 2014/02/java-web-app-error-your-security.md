---
author: Emanuele “Lele” Calò
title: 'Java Web app error: “Your security settings have blocked a self-signed application
  from running”'
github_issue_number: 927
tags:
- java
- linux
- security
- update
date: 2014-02-13
---

There’s a growing number people complaining that *Java* does not seem secure enough and that they feel vulnerable every time they open (and confirm to “Trust”) Java Web applications.

Since after the last update Java had at the end of January, this shouldn’t be a problem anymore as you can read in the [Java Changelog for the latest release](http://www.oracle.com/technetwork/java/javase/7u51-relnotes-2085002.html) there has been many efforts toward making “the Web” a safer place for everyone.

Unfortunately is also quite known that security and usability often fight one against each other, so it’s fairly possible that after installing the last Java Update and when trying to use Web Apps that worked until a few minutes earlier, you found yourselves facing the following error: “Your security settings have blocked a self-signed application from running”.

What happened is that Oracle changed the behavior your Java browser plugin will have when dealing with self signed Web applications by actually denying the execution of those since considered harmful by default.

In order to fix this situation you’ll need to launch the command **jcontrol**. Most Linux distributions will install it under */usr/bin/jcontrol* while others will place that binary in different places, as an example ArchLinux packages places it in /opt/java/bin/jcontrol. If you can’t find where it is, simply use **which jcontrol** and if it’s in your *PATH* its location will be shown.

Open jcontrol as your regular user and use it to whitelist the site you’re trying to use. Once the main window will be open, move to the *Security* tab and press the *Edit Site List..* button. Here you should *Add* a new row and in there write the site which is hosting the Java Web Applications you want to use. It’s important to put the **complete URL scheme://domain:port/path**, otherwise it won’t simply be detected as whitelisted.

Press *OK* to definitely put the new settings in use and reload the offending page. Everything should be working again now.

Sometimes things works quick and easy for Linux users too.


