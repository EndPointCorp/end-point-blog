---
author: Adam Vollrath
title: Packaging Ruby Enterprise Edition into RPM
github_issue_number: 159
tags:
- hosting
- redhat
- ruby
- spree
date: 2009-06-16
---

It’s unfortunate that past versions of Ruby have gained a reputation of [performing poorly](http://www.rubyinside.com/ruby-implementation-shootout-a-bright-future-for-ruby-performance-1390.html), consuming too much memory, or otherwise being “[unfit for the enterprise](http://duckdown.blogspot.com/2006/03/more-thoughts-on-ruby-and-why-it-isnt.html).” According to the fine folks at Phusion, this is partly [due to the way Ruby does memory management](http://www.rubyenterpriseedition.com/faq.html#what_is_this). And they’ve created an alternative branch of Ruby 1.8 called “[Ruby Enterprise Edition](http://www.rubyenterpriseedition.com/).” This code base includes [many](http://railsbench.rubyforge.org/) [significant](http://code.google.com/p/google-perftools/) [patches](http://timetobleed.com/ruby-threading-bugfix-small-fix-goes-a-long-way/) to the stock Ruby code which dramatically improve performance.

Phusion [advertises an average memory savings](http://www.rubyenterpriseedition.com/comparisons.html) of 33% when combined with [Passenger](https://www.phusionpassenger.com/), their Apache module for serving Rails apps. We did some testing of our own, using virtualized Xen servers from our [Spreecamps.com](http://www.spreecamps.com/) offering. These servers use the [DevCamps](http://www.devcamps.org/) system to run several separate instances of httpd for each developer, so reducing the usage of Passenger was crucial to fitting into less than a gigabyte of memory. Our findings were dramatic: one instance dropped 100MB down to 40MB. (The [status tools](https://web.archive.org/web/20090626230840/http://www.modrails.com/documentation/Users%20guide.html#_analysis_and_system_maintenance_tools) included with Passenger were very helpful in confirming this.)

There has been some discussion on the [Phusion Passenger](https://groups.google.com/forum/#!forum/phusion-passenger) and [other mailing lists](https://groups.google.com/forum/#!forum/emm-ruby) about packaging [Ruby Enterprise Edition](http://www.rubyenterpriseedition.com/) for Red Hat Enterprise Linux and its derivatives ([CentOS](https://www.centos.org/) and [Fedora](https://getfedora.org/)). [ Packages are available](http://www.rubyenterpriseedition.com/download.html#ubuntu) from Phusion for Ubuntu Linux, but many of our clients prefer RHEL’s reputation as a stable platform for e-commerce hosting. So we’ve packaged ruby-enterprise into RPM and made them available to give back to the community.

We want our SpreeCamps systems to be easy to maintain, following the “[Principle of Least Astonishment](http://wiki.c2.com/?PrincipleOfLeastAstonishment).” By default, Phusion’s script installs ruby-enterprise into /opt, so invocation must include the full path to the executable. This would be unsettling to a developer who mistakenly installed gems to Red Hat’s rubygems path while intending to install gems usable by REE and Passenger. It is important to install the ruby and gem executables into all users’ $PATH.

We took a cue from our customized local-perl packages. These packages install themselves into /usr/local. This means that all executables reside in /usr/local/bin; no $PATH modifications are necessary to utilize them via the command-line. Our ruby-enterprise packages are configured the same way. (If another /usr/local/bin/ruby exists, package installation will fail before clobbering another ruby installation.) Applications which specify #!/usr/bin/ruby will continue to use Red Hat’s packaged ruby.

Similar to a source-based installation, once these packages are installed you may do gem install passenger and any other gems your application needs. Phusion’s REE installer also installs several “useful gems”. However we elected not to include these in the main ruby-enterprise RPM package. More, smaller packages limited to a particular module or piece of software, is better than one or two big fat RPMs with a bunch of stuff you may or may not need. We will likely package individual gems in the near future.

These packages are publicly available from our repository. We’ve just begun using these but are finding them reliable and very helpful so far. Any of you who would like to are welcome to try them out via direct download, or much easier, adding our Yum repository to your system as described here:

[https://packages.endpoint.com/](https://packages.endpoint.com/)

Once you’ve done that, a simple command should get you most of the way there:

yum install ruby-enterprise ruby-enterprise-rubygems

If you prefer to download them directly, the .rpm packages are available on that site as well, just browse through the repo.

The .spec file is available for review and forking on GitHub:
[https://gist.github.com/axisofentropy/108940](https://gist.github.com/axisofentropy/108940)

Many thanks to list member Tim Charper for providing an example .spec, and my colleagues at End Point for reviewing this work.

We appreciate any comments or questions you may have. This package repo is for us and our clients primarily, but if there’s a package you need that isn’t in there, let us know and maybe we’ll add it.
