---
author: Greg Sabino Mullane
gh_issue_number: 354
tags: database, postgres, git
title: Postgres configuration best practices
---

This is the first in an occasional series of articles about configuring PostgreSQL. The main way to do this, of course, is the postgresql.conf file, which is read by the Postgres daemon on startup and contains a large number of parameters that affect the database’s performance and behavior. Later posts will address specific settings inside this file, but before we do that, there are some global best practices to address.

### Version Control

The single most important thing you can do is to put your postgresql.conf file into version control. I care not which one you use, but go do it right now. If you don’t already have a version control system on your database box, git is a good choice to use. Barring that, RCS. Doing so is extremely easy. Just change to the directory postgresql.conf is in. The process for git:

- Install git if not there already (e.g. “sudo yum install git”)
- Run: git init
- Run: git add postgresql.conf pg_hba.conf
- Run: git commit -a -m “Initial commit”

For RCS:

- Install as needed (e.g. “sudo apt-get install rcs”)
- Run: mkdir RCS
- Run: ci -l postgresql.conf pg_hba.conf

Note that we also checked in pg_hba.conf as well. You want to check in any file in that directory you may possibly change. For most people, that only means postgresql.conf and pg_hba.conf, but if you use other files (pg_ident.conf) check those in as well.

Ideally you want the version checked in to be the “raw” configuration files that came with the system—​in other words, before you started messing with them. Then you make your initial changes and check it in. From then on of course, you commit every time you change the file.

At a bare minimum, the version control system should be telling you:

- Exactly what was changed
- When it was changed
- Who made the change
- Why it was changed

The first two items happen automatically in all version control systems, so you don’t have to worry about those. The third item, “who made the change”, must be entered manually if on a shared account (e.g. postgres) and using RCS. If you are using git, you can simply set the environment variables GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL. For shared accounts, I have a custom bashrc file called “gregbashrc” that is called when I log in that sets those ENVs as well as a host of other items.

The fourth item, “why it was changed”, is generally the content of the commit message. Never leave this blank, and be as descriptive and verbose as possible—​someone later on will be grateful you did. It’s okay to be repetitive and state the obvious. If this was done as part of a specific ticket number or project name, mention that as well.

### Safe Changes

It’s important that the changes you make to the postgresql.conf file (or other files) actually work and don’t cause Postgres to be unable to parse the file, or handle a changed setting. Never make changes and restart Postgres, because if it doesn’t work, you’ve got a broken config file, no Postgres daemon, and most likely unhappy applications and/or users. At the very least, do a reload first (e.g. /etc/init.d/postgresql reload or just kill -HUP the PID). Check the logs and see if Postgres was happy with your changes. If you are lucky, it won’t even require a restart (some changes do, some do not).

A better way to test your changes is to make it on an identical test box. That way, all the wrinkles are ironed out before you make the changes on production and attempt a reload or restart.

Another way I’ve found handy is to simply start a new Postgres daemon. Sounds like a lot of work, but it’s pretty automatic once you’ve done it a few times. The process generally looks like this, assuming your production postgresql.conf is in the “data” directory, and your changes are in data/postgresql.conf.new:

- cd ..
- initdb testdata
- cp -f data/postgresql.conf.new testdata/
- echo port=5555 >> testdata/postgresql.conf
- echo max_connections=10 >> testdata/postgresql.conf

The max_connections is not strictly necessary, of course, but unless you are changing something that relies on that setting, it’s nicer to keep it (and the resulting memory) low.

- pg_ctl -D testdata -l test.log start
- cat test.log- pg_ctl -D testdata stop
- rm -fr testdata (or just keep it around for next time)

The test.log file will show you any problems that might have popped up with your changes, and once it works you can be fairly confident it will work for the “main” daemon as well, so to finish up:

- cd data- mv -f postgresql.conf.new postgresql.conf- git commit postgresql.conf -m "Adjusted random_page_cost to 2, per bug #4151"- kill -HUP `head -1 postmaster.pid`- psql -c 'show random_page_cost'

### Keeping it Clean

The postgresql.conf file is fairly long, and can be confusing to read with its mixture of comments, in-line comments, strange wrapping, and the commented out vs. not-commented-out variables. Hence, I recommend this system:

- Put a big notice at the top of the file asking people to make changes to the bottom- Put all important variables at the bottom, sans comments, one per line- Line things up- Put into logical groups.

This avoids having to hunt for settings, prevents the gotcha of when a setting is changed twice in the file, and makes things much easier to read visually. Here’s what I put at the top of the postgresql.conf:

```nohighlight
##
## PLEASE MAKE ALL CHANGES TO THE BOTTOM OF THIS FILE!
##
```

I then add a good 20+ empty lines, so anyone viewing the file is forced to focus on the all-caps message above.

The next step is to put all the settings you care about at the bottom of the file. Which ones should you care about? Any setting you have changed (obviously), any setting that you *might* change in the future, and any that you may not have changed, but someone may want to look up. In practice, this means a list of about 25 items. After aligning all the values to the right and breaking things into logical groups, here’s what the bottom of the postgresql.conf looks like:

```nohighlight
## Connecting
port                            = 5432
listen_addresses                = '*'
max_connections                 = 100

## Memory
shared_buffers                  = 400MB
work_mem                        = 1MB
maintenance_work_mem            = 1GB

## Disk
fsync                           = on
synchronous_commit              = on
full_page_writes                = on
checkpoint_segments             = 100

## PITR
archive_mode                    = off
archive_command                 = ''
archive_timeout                 = 0

## Planner
effective_cache_size            = 18GB
random_page_cost                = 2

## Logging
log_destination                 = 'stderr'
logging_collector               = on
log_filename                    = 'postgres-%Y-%m-%d.log'
log_truncate_on_rotation        = off
log_rotation_age                = 1d
log_rotation_size               = 0
log_min_duration_statement      = 200
log_statement                   = 'ddl'
log_line_prefix                 = '%t %u@%d %p'

## Autovacuum
autovacuum                      = on
autovacuum_vacuum_scale_factor  = 0.1
autovacuum_analyze_scale_factor = 0.3
```

Because everything is in one place, at the bottom of the file, and not commented out, it’s very easy to see what is going on. The groups above are somewhat arbitrary, and you can leave them out or create your own, but at least keep things grouped together as much as possible. When in doubt, use the same order as they appear in the original postgresql.conf.

Sometimes people change important settings in a group, such as for bulk loading of data. In this case, I usually make a separate group for it at the very bottom. This makes it easy to switch back and forth, and helps to prevent people from (for example) forgetting to switch fsync back on:

```nohighlight
## Bulk loading only - leave 'on' for everyday use!
autovacuum                      = off
fsync                           = off
full_page_writes                = off
```

### Ownership and permissions

All the conf files should be owned by the postgres user, and the configuration files should be world-readable if possible (indeed, it’s a requirement for Debian based system that postgresql.conf be readable for psql to work!). Be careful about SELinux as well: it can get ornery if you do things like use symlinks.

### Backups

One final note—​make sure you are backing up your changes as well. PITR and pg_dump won’t save your postgresql.conf! If you are checking things in to a remote version control system, then some of the pressure is off, but you should have some sort of policy for backing up all your conf files explicitly. Even if using a local git repo, tarring and copying up the whole thing is usually a very quick and cheap action.
