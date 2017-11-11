---
author: Jon Jensen
gh_issue_number: 912
tags: containers, open-source, perl, redhat, ruby
title: News of FreeOTP, RHEL/CentOS, Ruby, Docker, HTTP
---

I've had interesting tech news items piling up lately and it's time to mention some of those that relate to our work at End Point. In no particular order:

- [FreeOTP](https://play.google.com/store/apps/details?id=org.fedorahosted.freeotp) is a relatively new open source 2-factor auth app for Android by Red Hat. It can be used instead of Google Authenticator which last year became proprietary as noted in [this Reddit thread](http://www.reddit.com/r/privacy/comments/1dl2xl/google_authenticator_now_closedsource_to/). The [Google Authenticator](https://code.google.com/p/google-authenticator/) open source project now states: "This open source project allows you to download the code that powered version 2.21 of the application. Subsequent versions contain Google-specific workflows that are not part of the project." Whatever the reason for that change was, it seems unnecessary to go along with it, and to sweeten the deal, FreeOTP is quite a bit smaller. It's been working well for me over the past month or more.

- [Perl 5.18.2 was released.](https://metacpan.org/pod/perldelta)

- [Ruby 2.1.0 was released.](https://www.ruby-lang.org/en/news/2013/12/25/ruby-2-1-0-is-released/)

- [Ruby 1.9.3 end of life set for February 2015](https://www.ruby-lang.org/en/news/2014/01/10/ruby-1-9-3-will-end-on-2015/), and the formerly end-of-life Ruby 1.8.7 &amp; 1.9.2 have had their [maintenance extended](https://www.ruby-lang.org/en/news/2013/12/17/maintenance-of-1-8-7-and-1-9-2/) for security updates until June 2014 (thanks, [Heroku](https://www.heroku.com/)!).

- Red Hat and CentOS have joined forces, in an unexpected but exciting move. Several CentOS board members will be working for Red Hat, but *not* in the Red Hat Enterprise Linux part of the business. [Red Hat's press release](http://www.redhat.com/about/news/press-archive/2014/1/red-hat-and-centos-join-forces) and the [CentOS announcement](http://lists.centos.org/pipermail/centos-announce/2014-January/020100.html) give more details.

- [Red Hat Enterprise Linux 7](http://www.redhat.com/about/news/archive/2013/12/red-hat-announces-availability-of-red-hat-enterprise-linux-7-beta) is available in beta release. The closer working with CentOS makes me even more eagerly anticipate the RHEL 7 final release.

- [Docker](http://www.docker.com/) has been getting a lot of well-deserved attention. Back in September, [Red Hat announced](http://www.redhat.com/about/news/press-archive/2013/9/red-hat-and-dotcloud-collaborate-on-docker-to-bring-next-generation-linux-container-enhancements-to-openshift) it would help modify Docker to work on RHEL. To date only very recent Ubuntu versions have been supported by Docker because it relies on AUFS, a kernel patch never expected to be accepted in the mainline Linux kernel, and deprecated by the Debian project. Now [Linode announced their latest kernels support Docker](https://blog.linode.com/2014/01/03/docker-on-linode/), making it easier to experiment with various Linux distros.

- New maintenance releases of PostgreSQL, PHP, Python 2.7, and Python 3.3 are also out. Not to take all the small steps for granted!

- Finally, for anyone involved in web development or system/network administration I can recommend a nice reference project called [Know Your HTTP * Well](https://github.com/for-GET/know-your-http-well). I've looked most closely at the headers section. It helpfully groups headers, has summaries, and links to relevant RFC sections.

And we're already two weeks into January!
