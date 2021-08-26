---
author: Steph Skardal
title: Adventures in Downgrading my Linode Plan
github_issue_number: 1028
tags:
- hosting
- sysadmin
date: 2014-09-09
---

I recently went through the process of downgrading and downsizing my [Linode](https://www.linode.com/) plan and I wanted to share a few of the [small] hoops that I had to jump through to get there, with the help of the Linode Support team.

### Background

I’ve had a small personal [WordPress](https://wordpress.org/) site running for more than a few years now. I also use this server for personal Ruby on Rails development. When I began work on that site, I tried out a few shared hosting providers such as Bluehost and GoDaddy because of the low cost (Bluehost was ~$6/mo) at the time. However, I quickly encountered common limitations of shared server hosting:

- Shared hosting providers typically make it very difficult to run Ruby on Rails, especially edge versions of Ruby on Rails. It’s possible this has improved over the last few years, but when you are a developer and want to experiment (not locally), shared hosting providers are not going to give you the freedom to do so.
- Shared hosting providers do not give you control of specific performance settings (e.g. use of [mod_gzip](https://en.wikipedia.org/wiki/Mod_gzip), [expires headers](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)), so I was suffering from lack of control for my little WordPress site as well as my Rails sites. While this is another limitation that may have improved over the last few years, ultimately you are limited by non-root access as a shared server user.

### Enter Linode

I looked to virtual server providers such as Linode, Slicehost, and Rackspace after experiencing these common limitations. At the time of my transition, Linode and Slicehost were comparatively priced, but because End Point had successful experiences with Linode for several clients up to that point, I decided to make the jump to Linode. I can’t remember what my initial Linode size was (I think 512MB), but I chose the smallest available option at $20/mo, plus $5/mo for backups. I am not a sysadmin expert like my fellow coworkers ([Richard](/team/richard-templet), [Jon](/team/jon-jensen), the list goes on ...), but I managed to get PHP and Ruby on Rails running on Apache with MySQL, and several of the [best practices for speeding up your web site](https://developer.yahoo.com/performance/rules.html) in place.

Fast forward about 2 years, and I’ve been very happy with Linode. I can only remember one specific instance where my server has gone down, and the support team has always been very responsive. They also release occasionally free upgrades at the $20/mo price point, and the current offering at that price point is the Linode 2GB ([see more here](https://www.linode.com/pricing)). But lately, I’ve been hearing that [Digital Ocean](https://www.digitalocean.com/) has been gaining momentum with a few cheaper options, and I considered making the jump. But I missed the [recent announcement](https://blog.linode.com/2014/06/16/11th-linode-birthday-10-linode-plan/) that Linode introduced a new $10/mo. plan back in June (hooray!), so I’m happy to stay with Linode at this lower price point that is suitable for my small, but optimized WordPress site and small Ruby on Rails experiments.

### How to Downsize

In a perfect world, it would seem that to quickly downsize your Linode instance, you would first click on the “Resize” tab upon logging in to the Linode dashboard, click on the lower plan that you want, and then click “Resize this Linode now!”, as shown in the screenshot below:

<div class="separator" style="clear: both; text-align: center;padding-bottom:15px;"><img border="0" src="/blog/2014/09/adventures-downgrading-linode-plan/image-0.png" style="width:750px;padding-bottom:2px;"/>The Linode resize options.</div>

Things went a little differently for me. First, I received this message when I tried to resize:

*“Pending free upgrades must be performed before you are able to resize. Please visit the dashboard to upgrade.”*

So I headed to my dashboard and clicked on the free upgrade link on the bottom right in the dashboard. I then encountered this message:

*“Linodes with configuration profiles referencing a 32 bit kernel are currently not eligible for this upgrade. For more information please see our switching kernels guide, or redeploy this Linode using a 64 bit distro.”*

My main Linode Configuration Profile was 64 bit, but my Restore Configuration Profile was running the 32 bit kernel. So, I first had to update that by clicking on the “Edit” link, selecting the right kernel, and saving those changes. That took a few minutes to take effect.

<div class="separator" style="clear: both; text-align: center;padding-bottom:15px;"><img border="0" src="/blog/2014/09/adventures-downgrading-linode-plan/image-1.png" style="width:750px;padding-bottom:2px;"/><br/>
My two configuration profiles needed to be on 64 bit kernel to allow for the Linode upgrade.</div>

*Then*, I was ready for the free upgrade, which took another few minutes after the server booted down, migrated, and booted back up. Next, I headed back to the "Resize" tab on the dashboard and tried to proceed on the downgrade. I immediately received an error message notifying me that my disk images exceeded the resized option I wanted to switch to (24GB). Upon examining my dashboard, my disk images showed ~28GB allocated to the various disk images:

<div class="separator" style="clear: both; text-align: center;padding-bottom:15px;"><img border="0" src="/blog/2014/09/adventures-downgrading-linode-plan/image-2.png" style="width:750px;padding-bottom:2px;"/><br/>
My disk image space exceeded the 24GB allotted for the Linode 1024 plan.</div>

I was directed by the Linode support team to edit the disk image to get under that 24GB allowed amount. They also explained that I must verify my current app(s) didn’t exceed what I was going to downsize to, using "df -h" while logged into my server. I had already verified previously where disk space was going on my server and cleaned out some cached files and old log files, so I knew the space used was well under 24GB. The only additional step here was that I had to shut down my server first from the dashboard before reducing the disk image space. So I went through all that, and the disk image adjustment took another few minutes. After the disk image size was adjusted, I booted up the server again and verified it was still running.

<div class="separator" style="clear: both; text-align: center;padding-bottom:15px;"><img border="0" src="/blog/2014/09/adventures-downgrading-linode-plan/image-3.png" style="width:750px;padding-bottom:2px;"/><br/>
Editing my Disk Image</div>

Finally, after all that, I went to the “Resize” tab again and selected the Linode 1024 plan and proceeded. The new plan was implemented within a few minutes, automagically booting down my server and restarting it after completion. My billing information was also updated almost immediately, showing that I will now pay $12.50/mo for the Linode 1024 plan with backups.

### Conclusion

In list form, here are the steps I went through to reach my final destination:

- Updated kernels to 64 bit for all configuration profiles.
- Applied pending, free upgrades.
- Manually shut down server.
- Applied change to reduce disk image space.
- Rebooted server (not necessary, but I verified at this point things were still running).
- Resized to Linode 1024 plan.

While this process wasn’t as trivial as I had hoped, the support folks were super responsive, often responding within a minute or two when I had questions. I’m happy to stay with Linode at this offering and it allows them to remain competitive with both virtual private hosting providers and as an appealing alternative to shared hosting providers. The Linode 1024 plan is also a great starting point for a proof-of-concept or staging server that may be scaled up later as applications move to production and increase in traffic. Linode has plans ranging from the $10/mo plan I have (1GB of RAM, 24GB SSD storage, etc.) all the way up to a 96GB RAM, 1920 GB SSD storage plan at $960/mo.
