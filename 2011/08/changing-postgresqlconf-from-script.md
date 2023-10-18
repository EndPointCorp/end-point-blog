---
author: Greg Sabino Mullane
title: Changing postgresql.conf from a script
github_issue_number: 485
tags:
- database
- perl
- postgres
- tools
date: 2011-08-10
---



<a href="/blog/2011/08/changing-postgresqlconf-from-script/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img 207px;"="" 320px;="" alt="" border="0" cursor:hand;width:="" cursor:pointer;="" height:="" id="BLOGGER_PHOTO_ID_5639288985207208354" src="/blog/2011/08/changing-postgresqlconf-from-script/image-0.jpeg"/></a>

Image by [“TheBusyBrain” on Flickr](https://www.flickr.com/photos/thebusybrain/)

The modify_postgres_conf script for Postgres allows you to change your postgresql.conf file from the command line, via a cron job, or any time when you want to automate the process.

Postgres runs as a background daemon. The configuration parameters it runs with are stored in a file named postgresql.conf. To change the behavior of Postgres, one must usually edit this file, and then tell Postgres that you have made the changes. Sometimes all that is needed is to ‘HUP’ or reload Postgres. Most changes fall into this category. Other changes require a full restart of Postgres, which entails disconnecting all current clients.

Thus, to make a change, one must edit the file, find the item to change (the file consists of “name = value” lines), change it, then send a signal to the main Postgres process so it picks up the change. Finally, you should then connect to Postgres to make sure it is still running and has accepted the latest change.

Doing this automatically (such as via a cron script) is very difficult. One method, if you are doing something simple like toggling between two known configuration files, is to simply store copies of both files and replace them, like this example cronjob:

```bash
30 10 * * * cp -f conf/postgresql.conf.1 /etc/postgresql.conf; /etc/init.d/postgresql reload
50 10 * * * cp -f conf/postgresql.conf.2 /etc/postgresql.conf; /etc/init.d/postgresql reload
```

The major problem with that approach, as I quickly learned when I tried it, is that despite nobody making changes to the postgresql.conf file in *years*, a few days after I put the above change in place, someone decided to edit postgresql.conf. At 10:30AM the next day, their changes were blown away. A better way is to simply write a program to make the change for you. Thus, the modify_postgres_conf.pl script.

The basic usage is to tell the script where the conf file is, and list what changes you want to make. Here’s an example that will change the random_page_cost to **2** on a Debian system:

```bash
./modify_postgres_conf.pl --pgconf /etc/postgresql/9.0/main/postgresql.conf --change random_page_cost=2
```

Here is exactly what the script does for the above statement:

- For each item to be changed, we:

        <ul>
          <li>Ask the database what the current value is (and die if that parameter does not exist)</li>
          <li>If the current and new value are the same, do nothing</li>
          <li>Otherwise, open (and flock) the configuration file and change the parameter</li>
        </ul>

- If no changes were made, exit
- Otherwise, close the configuration file
- Figure out the Postgres PID and send it a HUP signal
- Reconnect to the database and confirm each change has taken effect

By default, it adds a comment after the changed value as well, to help in tracking down who made the change. A diff of the postgresql.conf file after running the example above produces:

```diff
diff -r1.1 postgresql.conf
499c499
< random_page_cost = 4
---
> random_page_cost = 2 ## changed by modify_postgres_conf.pl on Wed Aug 10 13:31:34 2011
```

The addition of the comment can be stopped by added a --no-comment argument. If the script runs successfully, it also returns two items of information: the size and name of the current Postgres log file. This is useful so you can know exactly where in the log this change took place. Note that this only works for items that are already explicitly set in your configuration file. However, [as discussed before](/blog/2010/09/postgres-configuration-best-practices/), you should already have all the items that you may possibly change explicitly listed out at the bottom of the file already. Whitespace is preserved as well, for those (like me) who like to keep things lined up neatly inside the file (see examples in the link above).

Here are some more examples of the script in action:

```bash
$ ./modify_postgres_conf.pl --pgconf /etc/postgresql/9.0/main/postgresql.conf --change random_page_cost=2
114991 /var/log/postgres/postgres-2011-08-10.log

$ ./modify_postgres_conf.pl --pgconf /etc/postgresql/9.0/main/postgresql.conf --change random_page_cost=2
No change made: value of "random_page_cost" is already 2

$ ./modify_postgres_conf.pl --pgconf /etc/postgresql/9.0/main/postgresql.conf \
> --change random_page_cost=2 \
> --change log_statement=ddl \
> --change log_min_duration_statement=100

No change made: value of "random_page_cost" is already 2
118459 /var/log/postgres/postgres-2011-08-10.log

$ ./modify_postgres_conf.pl --pgconf /etc/postgresql/9.0/main/postgresql.conf \
> --change default_statitics_target=200 --no-comment
There is no Postgres variable named "default_statitics_target"!

$ ./modify_postgres_conf.pl --pgconf /etc/postgresql/9.0/main/postgresql.conf \
> --change default_statistics_target=200 --no-comment
123396 /var/log/postgres/postgres-2011-08-10.log
```

Note that we make no attempt to automatically check changes in to version control: as you will see in an upcoming blog post on a real-life use case, such a checkin is usually not wanted, as we are making temporary changes.

This is a fairly simple Perl script, but I thought I would put it out there in the hopes of helping others out (and preventing the reinventing of wheels). Of course, if you find a bug or want to write a patch for it, those are welcome additions at any time! The code can be [found on github](https://github.com/bucardo/modify_postgres_config):

```bash
git clone git://git@github.com:bucardo/modify_postgres_config.git
```

