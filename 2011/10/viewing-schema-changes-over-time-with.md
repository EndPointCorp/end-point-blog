---
author: Greg Sabino Mullane
title: Viewing schema changes over time with check_postgres
github_issue_number: 505
tags:
- audit
- database
- postgres
date: 2011-10-05
---



<a href="/blog/2011/10/viewing-schema-changes-over-time-with/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5659427784859186034" src="/blog/2011/10/viewing-schema-changes-over-time-with/image-0.jpeg" style="cursor:pointer; cursor:hand;width: 320px; height: 308px;"/></a>

Image by Flickr user [edenpictures](https://www.flickr.com/photos/edenpictures/)

Version 2.18.0 of [check_postgres](https://bucardo.org/check_postgres/), a monitoring tool for PostgreSQL, has just been released. This new version has quite a large number of changes: see the [announcement](https://mail.endcrypt.com/pipermail/check_postgres-announce/2011-October/000027.html) for the full list. One of the major features is the overhaul of the [same_schema](https://bucardo.org/check_postgres/check_postgres.pl.html#same_schema) action. This allows you to compare the structure of one database to another and get a report of all the differences check_postgres finds. Note that "schema" here means the database structure, not the object you get from a "CREATE SCHEMA" command. Further, remember the same_schema action does not compare the actual data, just its structure.

Unlike most check_postgres actions, which deal with the current state of a single database, same_schema can compare databases to each other, as well as audit things by finding changes over time. In addition to having the entire system overhauled, same_schema now allows comparing as many databases you want to each other. The arguments have been simplified, in that a comma-separated list is all that is needed for multiple entries. For example:

```bash
./check_postgres.pl --action=same_schema \
  --dbname=prod,qa,dev --dbuser=alice,bob,charlie
```

The above command will connect to three databases, as three different users, and compare their schemas (i.e. structures). Note that we don’t need to specify a warning or critical value: we consider this an ‘OK’ Nagios check if the schemas match, otherwise it is ‘CRITICAL’. Each database gets assigned a number for ease of reporting, and the output looks like this:

```nohighlight
POSTGRES_SAME_SCHEMA CRITICAL: (databases:prod,qa,dev)
  Databases were different. Items not matched: 1 | time=0.54s 
DB 1: port=5432 dbname=prod user=alice
DB 1: PG version: 9.1.1
DB 1: Total objects: 312
DB 2: port=5432 dbname=qa user=bob
DB 2: PG version: 9.1.1
DB 2: Total objects: 312
DB 3: port=5432 dbname=dev user=charlie
DB 3: PG version: 9.1.1
DB 3: Total objects: 313
Language "plpgsql" does not exist on all databases:
  Exists on:  3
  Missing on: 1, 2
```

The second large change was a simplification of the filtering options. Everything is now controlled by the **--filter** argument, and basically you can tell it what things to ignore. For example:

```bash
./check_postgres.pl --action=same_schema \
  --dbname=A,B --filter=nolanguage,nosequence
```

The above command will compare the schemas on databases A and B, but will ignore any difference in which languages are installed, and ignore any differences in the sequences used by the databases. Most objects can be filtered out in a similar way. There are also a few other useful options for the --filter argument:

- noposition: Ignore what order columns are in
- noperms: Do not worry about any permissions on database objects
- nofuncbody: Do not check function source

The final and most exciting large change is the ability to compare a database to itself, over time. In other words, you can see exactly what changed during a certain time period. We have a client using that now to send a daily report on all schema changes made in the last 24 hours, for all the databases in their system. This is a very nice thing for a DBA to receive: not only is there a nice audit trail in your email, you can answer questions such as:

- Was this a known change, or did someone make it without letting anyone else know?
- Did somebody fat-finger and drop an index by mistake?
- Were the changes applied to database X also applied to database Y and Z?

To enable time-based checks, simply provide a single database to check. The first time it is run, same_schema simply gathers all the schema information and stores it on disk. The next time it is run, it detects the file, reads it in as database "2", and compares it to the current database (number "1"). The **--replace** argument will rewrite the file with the current data when it is done. So the cronjob for the aforementioned client is as simple as:

```nohighlight
10 0 * * * ~/bin/check_postgres.pl --action=same_schema \
  --host=bar --dbname=abc --quiet --replace
```

The **--quiet** argument ensures that no output is given if everything is ‘OK’. If everything is not okay (i.e. if differences are found), cron gets a bunch of input sent to it and duly mails it out. Thus, a few minutes after 10AM each day, a report is sent if anything has changed in the last day. Here’s a slightly redacted version of this morning’s report, which shows that a schema named "stat_backup" was dropped at some point in the last 24 hours (which was a known operation):

```nohighlight
POSTGRES_SAME_SCHEMA CRITICAL: DB "abc" (host:bar)
  Databases were different. Items not matched: 1 | time=516.56s
DB 1: port=5432 host=bar dbname=abc user=postgres
DB 1: PG version: 8.3.16
DB 1: Total objects: 11863
DB 2: File=check_postgres.audit.port.5432.host.bar.db.abc
DB 2: Creation date: Sun Oct  2 10:06:12 2011  CP version: 2.18.0
DB 2: port=5432 host=bar dbname=abc user=postgres
DB 2: PG version: 8.3.16
DB 2: Total objects: 11864
Schema "stat_backup" does not exist on all databases:
  Exists on:  2
  Missing on: 1
```

As you can see, the first part is a standard Nagios-looking output, followed by a header explaining how we defined database "1" and "2" (the former a direct database call, and the latter a frozen version of the same.)

Sometimes you want to store more than one version at a time: for example, if you want both a daily and a weekly view. To enable this, use the **--suffix** argument to create different instances of the saved file. For example:

```nohighlight
10 0 * * * ~/bin/check_postgres.pl --action=same_schema \
  --host=bar --dbname=abc --quiet --replace --suffix=daily
10 0 * * Fri ~/bin/check_postgres.pl --action=same_schema \
  --host=bar --dbname=abc --quiet --replace --suffix=weekly
```

The above command would end up recreating this file every morning at 10:**check_postgres.audit.port.5432.host.bar.db.abc.daily** and this file each Friday at 10: **check_postgres.audit.port.5432.host.bar.db.abc.weekly**.

Thanks to all the people that made 2.18.0 happen (see the [release notes](https://mail.endcrypt.com/pipermail/check_postgres-announce/2011-October/000027.html) for the list). There are still some rough edges to the same_schema action: for example, the output could be a little more user-friendly, and not all database objects are checked yet (e.g. no custom aggregates or operator classes). Development is ongoing; patches and other contributions are always welcome. In particular, we need more translators. We have French covered, but would like to include more languages. The code can be checked out at:

```bash
git clone git://bucardo.org/check_postgres.git
```

There is also a github mirror if you so prefer: [https://github.com/bucardo/check_postgres](https://github.com/bucardo/check_postgres).

You can also [file a bug](https://github.com/bucardo/bucardo/issues) (or feature request), or join one of the mailing lists: [general](https://mail.endcrypt.com/mailman/listinfo/check_postgres), [announce](https://mail.endcrypt.com/mailman/listinfo/check_postgres-announce), and [commit](https://mail.endcrypt.com/mailman/listinfo/check_postgres-commit).


