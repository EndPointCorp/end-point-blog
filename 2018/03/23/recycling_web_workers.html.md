---
author: Josh Williams
title: "Recycling Web Workers: Just Proper Hygiene"
tags: database, python, ruby, sysadmin
gh_issue_number: 1394
---

<img src="/blog/2018/03/23/recycling_web_workers/recycling.jpg" alt="Neat recycling bins"><br/>
<small>[Photo by Dano](https://www.flickr.com/photos/mukluk/441228222/), CC BY 2.0</small>

A long while back we were helping out a client with a mysterious and serious problem: The PostgreSQL instance was showing gradual memory growth, each of the processes slowly ballooning memory across a few days until the system triggered the OOM (out of memory) killer. Database at that point kicks out all connections and restarts. Downtime is bad, yo.

Spoiler alert: It was a [prepared SQL statements bug in Rails](https://github.com/rails/rails/issues/14645). Sometimes it’s fun to take you through all the hair-pulling that goes into debugging something like this, but instead this Friday I’m feeling preachy.

Of course there’s a few different directions you could go to work around a problem like this:

- **Update your framework.** If, of course, the fix has been released, or determined in the first place. And if your application doesn’t have any compatibility trouble preventing it from running on the updated version, or you feel comfortable back-patching the fix yourself. And if the Change Management Officer doesn’t try to string you up for wanting to update production willy nilly. (Not everyone works at a startup!) But do add it as a milestone. It should be one anyway.
- **Take a different code path.** Feature switches, like three-point seat belts and pocket breath mints, fall into the category of neat things that seem like a little burden until you really need them. In fact in this case, turning off prepared statements in unpatched Rails deployments is the recommended workaround. It’ll still take some testing, but is likely less risky than changing the framework code itself. It might also be a slight performance hit, but then so is a crashing database.
- **Recycle your worker processes periodically.** Simple. Readily doable. And usually entirely undisruptive. And thus I’m here advocating that you think about doing it occasionally as a matter of course.

The usual way to get worker processes to recycle gracefully is to send a SIGHUP signal to the application master process. At that point each worker process finishes handling its current request and then quits, after which the master starts up a new one to handle the next request. It’s typically a seamless process.

You could do that through cron every now and then, perhaps daily or whatever is appropriate. But some app servers have this built in, usually after processing some given number of requests (it’ll usually be a “max\_requests” parameter, or something very close to that.)

- One the Python side, both gunicorn and uwsgi both have it. The name variation is ever so slightly different (max\_requests, sometimes, versus max-request).
- For Ruby, Passenger has it as a parameter, while unicorn has a [separate gem, unicorn-worker-killer](https://rubygems.org/gems/unicorn-worker-killer), that does this.
- php-fpm has it as a parameter as well, though if you’re using Apache httpd to host the application through mod\_php directly, MaxConnectionsPerChild is what you want to set.

I would be remiss if I didn’t mention a couple potential downsides. The first is that while no request will be left behind, the first one that hits each new worker process might see a slight delay as code is reloaded and any process cache is warmed.

The second is that it may happen unexpectedly, which could be a problem if some changes had been made but the app process hadn’t seen it yet. This could be a deploy that’s still in progress, or some change that was left out there to be completed later. (On one hand, tsk, tsk; on the other, eh, it does happen.)

There you have it. As a coworker said in chat: Recycling worker processes, it’s just good hygiene.
