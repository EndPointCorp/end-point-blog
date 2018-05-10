---
author: Spencer Christensen
gh_issue_number: 1051
tags: redhat, postgres
title: Where is pg_ctl on CentOS 6 for Postgres 9.3?
---

When installing PostgreSQL 9.3 onto a CentOS 6 system, you may notice that some postgres commands appear to be missing (like **pg_ctl**, **initdb**, and **pg_config**). However, they actually are on your system but just not in your path. You should be able to find them in /usr/pgsql-9.3/bin/. This can be frustrating if you don’t know that they are there.

To solve the problem, you could just use full paths to these commands, like /usr/pgsql-9.3/bin/initdb, but that may get ugly quick depending on how you are calling these commands. Instead, we can add them to the path.

You could just copy them to /usr/bin/ or create symlinks for them, but both of these methods are hack-ish and could have unintended consequences. Another option is to add /usr/pgsql-9.3/bin/ to your path manually, or to the path for all users by adding it to /etc/bashrc. But again, that seems hack-ish and when you upgrade postgres to 9.4 down the road things will break again.

So instead, let’s look at how Postgres’ other commands get installed when you install the rpm. When you run “yum install postgresql93” the rpm contains not only all the files for that package but it also includes some scripts to run (in this case one at install time and another at uninstall time). To view everything that is getting installed and to see the scripts that are run use this command: “rpm -qilv --scripts postgresql93”. There will be a lot of output, but in there you will see:

```nohighlight
...
postinstall scriptlet (using /bin/sh):
/usr/sbin/update-alternatives --install /usr/bin/psql pgsql-psql /usr/pgsql-9.3/bin/psql 930
/usr/sbin/update-alternatives --install /usr/bin/clusterdb  pgsql-clusterdb  /usr/pgsql-9.3/bin/clusterdb 930
/usr/sbin/update-alternatives --install /usr/bin/createdb   pgsql-createdb   /usr/pgsql-9.3/bin/createdb 930
...
```

That line “postinstall scriptlet (using /bin/sh):” marks the beginning of the list of commands that are run at install time. Ah ha! It runs update-alternatives! If you’re not familiar with alternatives, the short description is that it keeps track of different versions of things installed on your system and automatically manages symlinks to the version you want to run.

Now, not all the commands we’re interested in are installed by the package “postgresql93”—​you can search through the output and see that **pg_config** gets installed but is not set up in alternatives. The commands **initdb** and **pg_ctl** are part of the package “postgresql93-server”. If we run the same command to view its files and scripts we’ll see something interesting—​it doesn’t set up any of its commands using alternatives! Grrr. :-(

In the postgresql93-server package the preinstall and postinstall scripts only set up the postgres user on the system, set up /var/log/pgsql, add postgres to the init scripts, and set up the postgres user’s .bash_profile. That’s it. But, now that we know what commands are run for getting psql, clusterdb, and createdb into the path, we can manually run the same commands for the postgres commands that we need. Like this:

```nohighlight
/usr/sbin/update-alternatives --install /usr/bin/initdb pgsql-initdb /usr/pgsql-9.3/bin/initdb 930
/usr/sbin/update-alternatives --install /usr/bin/pg_ctl pgsql-pg_ctl /usr/pgsql-9.3/bin/pg_ctl 930
/usr/sbin/update-alternatives --install /usr/bin/pg_config pgsql-pg_config /usr/pgsql-9.3/bin/pg_config 930
```

These commands should be available in your path now and are set up the same as all your other postgres commands. Now, the question about why these commands are not added to alternatives like all the others is a good one. I don’t know. If you have an idea, please leave it in the comments. But at least now you have a decent work-around.
