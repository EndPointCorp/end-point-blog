---
author: Greg Sabino Mullane
gh_issue_number: 1326
tags: postgres
title: Working on production systems
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2017/09/27/working-on-production-systems/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" data-original-height="392" data-original-width="324" src="/blog/2017/09/27/working-on-production-systems/image-0.jpeg"/></a><br/><small>(Not as easy as it looks) <br/><a href="https://flic.kr/p/Y4yDHm">Photo</a> by Flickr user <a href="https://www.flickr.com/photos/edenpictures/">'edenpictures'</a></small></div>

As consultants, the engineers at End  Point are often called upon to do work on production systems — 
in other words, one or more servers that are vital to our client’s business. These range from doing years 
of planning to perform a major upgrade for a long-standing client, down to jumping into a brand-new client for an 
emergency fix. Either way, the work can be challenging, rewarding, and a little bit nerve-wracking. 

Regardless of how you end up there, following some basic good practices may reduce the chance 
of problems coming up, keep you calm during the chaos, and make the process easier for both 
you and the client.

### Preparation

Unless this is a true emergency, doing major work on a production system (e.g. upgrading a database 
server) should involve a good amount or preparation. By the time the big night arrives 
(yes, it is always  late at night!) you should have gone through this list:

- Do lots and lots of testing. Use systems as close as possible to production, and run through the process until it becomes second nature.
- Know the impact on the business, and the downtime window anticipated by the rest of the company.
- Have a coworker familiar with everything on standby, ready to call in if needed.
- Document the process. For a large project, a spreadsheet or similar document can be quite helpful.
    - Who are the people involved, how to contact them, and what general role do they play?
    - Which task is being done at what time, who is the primary and backup for it, and what other tasks does it block?
    - How is success for each stage measured?
    - What is the rollback plan for each step? When is the point of no return reached?
- Setup a shared meeting space (IRC, Skype, Slack, Zulip, HipChat, etc.)
- Confirm connections (e.g. VPN up and running? Passwords not set to expire soon? Can everyone get to Slack? SSH working well?)

### Screen Up

The night usually begins with connecting to a client server via SSH. The first order of business should be to invoke ‘screen’ or ‘tmux’, 
which are persistent session managers (aka terminal multiplexers). These keep your connections; if your network drops, 
so you can easily pick up where you left off. They also allow other people to view  and/or join in on 
what you are doing. Finally, they enable you to easily view and control multiple windows. Some screen-specific tips:

- Name your screen something obvious to the task such as “bucardo-production-rollout”. Always give it a name to prevent people from joining it by accident. I often use just my email, i.e. screen -S greg@endpoint.com or tmux new -s greg_endpoint_com.
- Keep organized. Try to keep each window to one general task, and give each one a descriptive name:
    - screen: Ctrl-a A     tmux: Ctrl-b ,
    - I find that uppercase names stand out nicely from  your terminal traffic.
    - Splitting windows by task also helps scrollback searching.
- Boost your scrollback buffer so you can see what happened a while ago. The default value is usually much too low.
    - Inside /etc/screenrc or ~/.screenrc: defscrollback 50000
    - Inside /etc/tmux.conf or ~/.tmux.conf: set-option -g history-limit 50000
- Develop a good configuration file. Nothing too fancy is needed, but being able to see all the window names at once on the bottom of the screen makes things much easier.
- Consider [logging all your screen output](/blog/2013/07/24/gnu-screen-logtstamp-string).

### Discovery and Setup

If you don’t already know, spend a little bit of time getting to know the server. A deep analysis is not needed, but you should have a rough 
idea how powerful it is (CPU, memory), how  big it is (disk space), what OS it is (distro/version), and what else is running on it. Although 
one should be able to easily work on any unmodified *nix server, I almost always make a few changes:

- Install minimal support software. For me, that usually means apt-get install git-core emacs-nox screen mlocate.
- Put in some basic aliases to help out. Most important being rm='rm -i'.
- Switch to a lower-priv account and do the work there when possible. Use sudo instead of staying as root.

For Postgres, you also want to get some quick database information as well. There are many things you could learn, but 
at a bare minimum check out the version, and per-user settings, the databases and their sizes, and what all the 
non-default configuration settings are:

```text
select version();
\drds
\l+
select name, setting, source from pg_settings where source <> 'default' order by 1;
```

### Version Control (git up)

One of the earliest steps is to ensure all of your work is done in a named subdirectory in a non-privileged account. Everything in this 
directory should be put into version control. This not only timestamps file changes for you, but allows quick recovery from accidentally 
removing important files. All your small scripts, your configuration files (except .pgpass), your SQL files - put 
them all in version control. And by version control, I of course mean [git](https://www.atlassian.com/git/tutorials/what-is-git), which has won the version control wars (a happy example of the most 
popular tool also being the best one). Every time you make a change, git commit it.

### psql

As a Postgres expert, 99% of my work is done through [psql](https://www.postgresql.org/docs/current/static/app-psql.html), the canonical command-line client for Postgres. I am often connecting 
to various database servers in quick succession.
Although psql is an amazing tool, there are important considerations to keep in mind.

The .psql_history file, along with readline support, is a wonderful thing. However, 
 it is also a great footgun, owing to the ease of using the “up arrow” and “Ctrl-r” rerun SQL statements. This can lead to running a command on server B that was previously run on server A (and which should never, 
ever be run on server B!). Here are some ways around this issue:

One could simply remove the use of readline when on a production database. In this way, you will be forced to type everything 
out. Although this has the advantage of not accidentally toggling back to an older command, the loss of history is very annoying - and it 
greatly increases the chance of typos, as each command needs to be typed anew.

Another good practice is to empty out the psql_history file if you know it has some potentially damaging commands in it (e.g. you just 
did a lot of deletions on the development server, and are now headed to production.). Do not simply erase it, however, as the 
.psql_history provides  a good audit trail of exactly what commands you ran. Save the file, then empty it out:

```
$ alias clean_psql_history='cat ~/.psql_history >> ~/.psql_history.log; truncate -s0 ~/.psql_history'
```

Although the .psql_history file can be set per-database, I find it too confusing and annoying in practice to use. I  like being 
able to run the same command on different databases via the arrow keys and Ctrl-r.

It is important to exit your psql sessions as soon as possible - never leave it hanging around 
while you go off and do something else. There are multiple reasons for this:

- Exiting psql forces a write of the .psql_history file. Better to have a clean output rather than allowing all the sessions to interleave with each other. Also, a killed psql session will not dump its history!
- Exiting frees up a database connection, and prevents you from unintentionally leaving something idle in transaction.
- Coming back to an old psql session risks a loss of mental context - what was I doing here again? Why did I  leave this around?
- Less chance of a accidental paste into a window with a psql prompt (/voice_of_experience).

Another helpful thing for psql is a good custom prompt. There should always be some way of telling which 
database - and server - you are using just by looking at the psql prompt. Database names are often the 
same (especially with primaries and their replicas), so you need to add a little bit more. Here’s a decent recipe, but you can 
consult [the documentation](https://www.postgresql.org/docs/current/static/app-psql.html#APP-PSQL-PROMPTING) to design your own.

```text
$ echo "\set PROMPT1 '%/@%m%R%#%x '" >> ~/.psqlrc
$ psql service=PROD
product_elements@topeka=> 
```

### Connection Service File

Using a [connection service file](/blog/2016/10/26/postgres-connection-service-file) to access Postgres can help keep things sane and organized. Connection files allow you to associate 
a simple name with multiple connection parameters, allowing abstraction of those details in a manner much safer and cleaner than using shell aliases. 
Here are some suggestions on using connection files:

- If possible, use the local user’s file (~/.pg_service.conf), but the global file is fine too. Whichever you choose, do not put the password inside them - use the .pgpass file for that.
- Use short but descriptive service names. Keep them very distinct from each other, to reduce the chance of typing in the wrong name.
- Use uppercase names for important connections (e.g. PROD for the connection to an important production database). This provides another little 
reminder to your brain that this is not a normal psql connection. (Remember, PROD = Please Respect Our Data)
- Resist the temptation to alias them further. Force yourself to type everything out each time, e.g. “psql service=PROD” each time. This keeps your head focused on where you are going.

### Dangerous SQL

Some actions are so dangerous, it is a good idea to remove any chance of direct invocation on the wrong server. 
The best example of this is the SQL ‘truncate’ command. If I find myself working on multiple servers in which I need 
to truncate a table, I do NOT attempt to invoke the truncate command directly. Despite all precautions, 
there are many ways to accidentally run the same truncate command on the wrong server, whether via 
a .psql_history lookup, or simply an errant cut-n-paste error. One solution is to put the truncate into a text file, 
and then invoke that text file, but that simply 
adds the chance that this file may be invoked on the wrong database. Another solution is to use a text file, but 
change it when done (e.g. search and replace “truncate” to “notruncate”). This is slightly better, but still 
error prone as it relies on someone remembering to change the file after each use, and causes the file to 
no longer represent what was actually run.

For a better solution, create a function that only exists on one of the databases. For example, if you have 
a test database and a production database, you can run truncate via a function that only exists on the 
test database. Thus, you may safely run your function calls on the test server, and not worry if the functions accidentally get 
run on the production server. If they do, you end up with a “function not found error” rather than 
realizing you just truncated a production table. Of course, you should add some safeguards so that the function 
itself is never created on the production server. Here is one sample recipe:

```text
\set ON_ERROR_STOP on

DROP FUNCTION IF EXISTS safetruncate(text);

CREATE FUNCTION safetruncate(tname text)
RETURNS TEXT
LANGUAGE plpgsql
AS $ic$
  BEGIN
    -- The cluster_name setting can be quite handy!
    PERFORM 1 FROM pg_settings WHERE name = 'cluster_name' AND setting = 'testserver';
    IF NOT FOUND THEN
      RAISE EXCEPTION 'Cannot create this function on this server!';
    END IF;

    EXECUTE FORMAT('truncate table %s', tname);

    RETURN 'Truncated table ' || tname;
  END;
$ic$;
```

Now you can create text files full of indirect truncate calls - filled with SELECT safetruncate('exultations'); 
instead of literal truncate calls. This file may be safely checked into git, and copy and pasted without worry.

### Record keeping

The value of keeping good records of what you are doing on production systems cannot be overstated. While you should 
utimately use whatever system is best for you, I like to keep a local text file that spells out exactly what I did, 
when I did it, and what happened. These should be detailed enough that you can return to them a year later and 
explain to the client exactly what happened.

The primary way to document things as you go along is with good old fashioned cut and paste. Both the 
.bash_history 
and .psql_history files provide automatic tracking of entered commands, as a nice backup to your notes. 
Make liberal use of the tee(1) command to store command output into discrete files (which reduces the need to rely on 
scrollback).

Rather than entering commands directly into a psql prompt, consider putting them into a text file 
and then feeding that file to psql. It’s a little extra work, but the file can be checked into git, 
giving an excellent audit trail. Plus, you may have to run those commands again someday.

If you find yourself doing the same thing over and over, write a shell script. This even applies to 
psql commands. For example, I recently found myself having to examine tables on two servers, 
and needed to quickly examine a table’s size, indexes, and if anyone was currently modifying it. Thus 
a shall script:

```text
psql service=PROD -c "\\d $1"
psql service=PROD -Atc "select pg_relation_size('$1')"
psql service=PROD -Atc "select query from pg_stat_activity where query ~ '$1'"
```

### Wrap Up

When you are done with all your production tasks, write up some final thoughts on how it went, and what the next steps are. 
Read through all your notes while it is all fresh in your mind and clean them up as needed. Revel in your 
success, and get some sleep!


