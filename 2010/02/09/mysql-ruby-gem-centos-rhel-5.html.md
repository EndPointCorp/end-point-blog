---
author: Adam Vollrath
gh_issue_number: 266
tags: database, hosting, mysql, redhat, rails
title: MySQL Ruby Gem CentOS RHEL 5 Installation Error Troubleshooting
---



Building and installing the Ruby mysql gem on freshly-installed Red Hat based systems sometimes produces the frustratingly ambiguous error below:

```bash
# gem install mysql
/usr/bin/ruby extconf.rb
checking for mysql_ssl_set()... no
checking for rb_str_set_len()... no
checking for rb_thread_start_timer()... no
checking for mysql.h... no
checking for mysql/mysql.h... no
*** extconf.rb failed ***
Could not create Makefile due to some reason, probably lack of
necessary libraries and/or headers.  Check the mkmf.log file for more
details.  You may need configuration options.
```

Searching the web for info on this error yields two basic solutions:

1. [Install the mysql-devel package](https://serverfault.com/questions/54532/installing-mysql-ruby-gem-on-64-bit-centos/60296#60296) (this provides the mysql.h file in /usr/include/mysql/).
1. Run gem install mysql -- --with-mysql-config=/usr/bin/mysql_config or some [other additional options](http://www.wzzrd.com/2008/02/building-mysql-gem-centos5-hell-usually.html).

These are correct but not sufficient. Because this gem compiles a library to interface with MySQL’s C API, the gcc and make packages are also required to create the build environment:

```bash
# yum install mysql-devel gcc make
# gem install mysql -- --with-mysql-config=/usr/bin/mysql_config
```

Alternatively, if you’re using your distro’s ruby (not a custom build like [Ruby Enterprise Edition](/blog/2009/06/16/ruby-enterprise-edition-rpm-packages)), you can install [EPEL](https://fedoraproject.org/wiki/EPEL)’s ruby-mysql package along with their rubygem-rails and other packages.


