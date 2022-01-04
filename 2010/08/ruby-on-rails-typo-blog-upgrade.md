---
author: Jon Jensen
title: Ruby on Rails Typo blog upgrade
github_issue_number: 339
tags:
- hosting
- redhat
- ruby
- rails
date: 2010-08-11
---

I needed to migrate a Typo blog (built on Ruby on Rails) from one RHEL 5 x86_64 server to another. To date I’ve done Ruby on Rails deployments using Apache with FastCGI, mongrel, and Passenger, and I’ve been looking for an opportunity to try out an nginx + Unicorn deployment to see how it compares. This was that opportunity, and here are the changes that I made to the stack during the migration:

- [Apache](https://httpd.apache.org/) 2.2.3 to [nginx](https://nginx.org/) 0.7.64
- [Passenger](https://www.phusionpassenger.com/) 2.2.1 to [Unicorn](https://bogomips.org/unicorn/) 1.1.2
- [PostgreSQL](https://www.postgresql.org/) 8.3.8 to 8.4.4
- [Ruby on Rails](https://rubyonrails.org/) 2.2.2 to 2.3.8
- [Typo](http://typosphere.org/) 5.3 to 5.5

I used the following packages from [End Point’s Yum repository](https://packages.endpointdev.com/) for RHEL 5 x86_64:

- nginx-0.7.64-2.ep
- ruby-enterprise-1.8.7-3.ep
- ruby-enterprise-rubygems-1.3.6-3.ep

The rest were standard [Red Hat Enterprise Linux](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) packages, including the new RHEL 5.5 postgresql84 packages. The exceptions were the Ruby gems, which were installed locally with the `gem` command as root.

I had to install an older version of one gem dependency manually, sqlite3-ruby, because the current version requires a newer version of sqlite than comes with RHEL 5. The installation commands were roughly:

```bash
yum install sqlite-devel.x86_64
gem install sqlite3-ruby -v 1.2.5

gem install unicorn
gem install typo

yum install postgresql84-devel.x86_64
gem install postgres
```

Then I followed (mostly) the instructions in [Upgrading to Typo 5.4](https://web.archive.org/web/20100225134725/http://wiki.github.com/fdv/typo/upgrading-to-typo-54), which are still pretty accurate even though outdated by one release. One difference was the need to specify PostgreSQL to override the default of MySQL (even though the default is documented as being sqlite):

```bash
typo install /path/to/typo database=postgresql
```

Then I ran pg_dump on the old Postgres database and imported the data into the new database, and put in place the database.yml configuration file.

The Typo upgrade went pretty smoothly this time. I had to delete the sidebars configuration from the database to stop getting a 500 error for that, and redo the sidebars manually—​which I’ve had to do with every past Typo upgrade as well. But otherwise it was easy.

I first tested the migrated blog by running unicorn_rails manually in development mode. Then to have Unicorn start at boot time, I wrote this little shell script and put it in ~/bin/start-unicorn.sh:

```bash
#!/bin/bash
cd /path/to/app || exit 1
unicorn_rails -E production -D -c config/unicorn.conf.rb
```

Then added a cron job to run it:

```bash
@reboot bin/start-unicorn.sh
```

That unicorn.conf.rb file contains only:

```plain
listen 8080
worker_processes 4
```

The listen port 8080 is the default, but I may need to change it. Unicorn defaults to only 1 worker process, so I increased it to 4.

I added the following nginx configuration inside the http { ... } block (actually in a separate include file):

```nginx
upstream app_server {
    server 127.0.0.1:8080 fail_timeout=0;
}

server {
    listen       the.ip.add.ress:80;
    server_name  the.host.name;

    location / { 
        root   /path/to/rails/typo/public/cache;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        #proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        rewrite ^/blog/xml/atom/feed\.xml$ /articles.atom permanent;
        rewrite ^/blog/xml/rss20/feed\.xml$ /articles.rss permanent;

        if (-f $request_filename) {
            break;
        }   

        set $possible_request_filename $request_filename/index.html;
        if (-f $possible_request_filename) {
            rewrite (.*) $1/index.html;
            break;
        }   

        set $possible_request_filename $request_filename.html;
        if (-f $possible_request_filename) {
            rewrite (.*) $1.html;
            break;
        }   

        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }   
    }   

    # Rails error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root   /path/to/rails/typo/public;
    }   
}
```

The configuration was a little complicated to get nginx serving static content directly, including cache files that Typo writes out. I had to add special handling for / which gets cached as /index.html, but can’t be called that when passing URIs to Typo, as it doesn’t know about any /index.html. And all HTML cache files end in .html, though the URIs don’t, so those need special handling too.

But when all is said and done, the blog is now running on the latest version of Typo, on the latest Unicorn, Rails, Ruby Enterprise Edition, PostgreSQL, and nginx, with all static content and fully-cached pages served directly by nginx, and for the most part only dynamic requests being served by Unicorn. I need to tweak the nginx rewrite rules a bit more to get 100% of static content served directly by nginx.

As far as blogging platforms go, I can recommend Typo mainly for Rails enthusiasts who want to write their own plugins, tweak the source, etc. WordPress or Movable Type are so much more widely used that non-programmers are going to have a lot easier time deploying and supporting them. They’ve had a lot more security vulnerabilities requiring updates, though that may also be a function of popularity and payoff for those exploiting them.

Rails deployment seems to take a lot of memory no matter how you do it. I don’t think nginx + Unicorn uses much less RAM than Apache + Passenger, mostly the difference between nginx and Apache themselves. But using Unicorn does allow for running the application processes on another server or several servers without needing nginx or Apache on those other servers. It does provide for clean separation between the web server and the application(s), including possibly different SELinux contexts rather than always httpd_sys_script_t as we see with Passenger. Passenger at least switches the child process UID to run with different permissions from the main web server, which is good. Both Passenger and Unicorn are much nicer than FastCGI, which I’ve always found to be a little buggy, and mongrel, which required specifying a range of ports and load-balancing across all of them in the proxy—​managing multiple port ranges is a pain with multiple apps on the same machine, especially when some need more than others.

I think if you have plenty of RAM, going with Apache + Passenger may still be the easiest Rails web deployment method overall, when mixed with other static content, server-side includes, PHP, and CGIs. But for high-traffic and custom setups, nginx + Unicorn is a nice option.
