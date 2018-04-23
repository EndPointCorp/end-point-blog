---
author: Emanuele “Lele” Calò
gh_issue_number: 893
tags: database, mysql
title: 'How to Enable MySQL Event Scheduler'
---

You may think that you already know what’s the opposite of “DISABLED”, but with MySQL Event Scheduler you’ll be wrong.

In fact MySQL Event Scheduler may have three different states[1][2]:

```
DISABLED -  The Event Scheduler thread does not run [1]. In addition, the Event Scheduler state cannot be changed at runtime.
OFF (default) - The Event Scheduler thread does not run [1]. When the Event Scheduler is OFF it can be started by setting the value of event_scheduler to ON.
ON - The Event Scheduler is started; the event scheduler thread runs and executes all scheduled events.
```

So if you’re going to find it in the **DISABLED** state and instinctively set it to **ENABLED** you’ll end up with a non-starting MySQL daemon.

Be warned and stay safe out there!

[1]: http://dev.mysql.com/doc/refman/5.5/en/events-configuration.html

[2]: When the Event Scheduler is not running does not appear in the output of SHOW PROCESSLIST
