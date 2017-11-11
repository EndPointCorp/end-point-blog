---
author: Spencer Christensen
gh_issue_number: 1117
tags: camps, database, environment, storage, sysadmin
title: Handling databases in dev environments for web development
---

One of the biggest problems for web development environments is copying large amounts of data.  Every time a new environment is needed, all that data needs to be copied.  Source code should be tracked in version control software, and so copying it should be a simple matter of checking it out from the code repository.  So that is usually not the problem.  The main problem area is database data.  This can be very large, take a long time to copy, and can impact the computers involved in the copy (usually the destination computer gets hammered with IO which makes load go high).

Often databases for development environments are created by copying a database dump from production and then importing that database dump.  And since database dumps are text, they can be highly compressed, which can result in a relatively small file to copy over.  But the import of the dump can still take lots of time and cause high load on the dev computer as it rebuilds tables and indexes.  As long as your data is relatively small, this process may be perfectly acceptable.

## Your database WILL get bigger

At some point though your database will get so big that this process will take too long and cause too much load to be acceptable.

To address the problem you can try to reduce the amount of data involved by only dumping a portion of the database data instead of all of it, or possibly using some "dummy sample data" instead.  These techniques may work if you don't care that development environments no longer have the same data as production.  However, one serious problem with this is that a bug or behavior found in production can't be replicated in a development environment because the data involved isn't the same.  For example, say a customer can't checkout on the live site but you can't replicate the bug in your development environment to fix the bug.  In this example, the root cause of the problem could be a bug in the code handling certain products that are out of stock, and since the dev database didn't have the same data it could make finding and fixing these types of problems *a lot harder*.

## Snapshots

Another option is to use file system snapshots, like LVM snapshots, to quickly make clones of the database without needing to import the database dump each time.  This works great if development environments live on the same server, or at least the development databases live on the same server.  You would need to create a volume to hold a single copy of the database; this copy would be the origin for all snapshots.  Then for each development environment, you could snapshot the origin volume, mount it read-write in a place accessible by the developer, customize the database configuration (like setting a unique port number to listen on), and then start up the database.  This then provides a clone of the entire database in a tiny fraction of the time and uses less disk space and other system resources too.

In using snapshots there are some things you'll need to be careful about.  Snapshots are usually created using copy-on-write tables.  The more snapshots mounted read-write, the more IO overhead is involved for the volumes involved.  For this reason it is important that writes to the origin volume be avoided as much as possible while the snapshots are open.  Also, snapshots that get a lot of writes can fill up their copy-on-write table, and depending on the file system and database that you are using this can be a big problem.  So it is important to monitor each open snapshot for how full it is and increase their size if needed so they don't fill up.  Updating the origin database will require shutting down and removing all snapshots first, then update the origin database, then create and mount all the snapshots again.  This is because all the copy-on-write tables would get full if you tried to update the origin while the snapshots are open.

Using snapshots like this may sound more complicated, and it is, but the processes involved can be scripted and automated and the benefits can be pretty significant if you have several developers and a lot of data to copy.
