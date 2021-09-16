---
author: Greg Sabino Mullane
title: Postgres Upgrades — Ten Problems and Solutions
github_issue_number: 251
tags:
- database
- postgres
- tips
date: 2010-01-11
---



<a href="https://2.bp.blogspot.com/_BSsdd9WIV2k/S0qUgYgEA4I/AAAAAAAAAAM/FCCruUmtrCQ/s1600-h/elephant_upgrade.jpg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5425311985174840194" src="/blog/2010/01/postgres-upgrades-ten-problems-and/image-0.jpeg" style="margin: 0pt 0pt 10px 10px; float: right; cursor: pointer; width: 200px; height: 125px;"/></a>

Upgrading between major versions of Postgres is a fairly straightforward affair, but Murphy’s law often gets in the way. Here at End Point we perform a lot of upgrades, and the following list explains some of the problems that come up, either during the upgrade itself, or afterwards.

When we say upgrade, we mean going from an older major version to a newer major version. We’ve (recently) migrated client systems as old as 7.2 to as new as 8.4. The canonical way to perform such an upgrade is to simply do:

```bash
pg_dumpall -h oldsystem > dumpfile
psql -h newsystem -f dumpfile
```

The reality can be a little more complicated. Here are the top ten gotchas we’ve come across, and their solutions. The more common and severe problems are at the top.

### 1. Removal of implicit casting

Postgres 8.3 removed many of the "implicit casts", meaning that many queries that used to work on previous versions now gave an error. This was a pretty severe regression, and while it is technically correct to not have them, the sudden removal of these casts has caused *lots* of problems. Basically, if you are going from any version of PostgreSQL 8.2 or lower to any version 8.3 or higher, expect to run into this problem.

Solution: The best way of course is to "fix your app", which means specifically casting items to the proper datatype, for example writing "123::int" instead of "123". However, it’s not always easy to do this—​not only can finding and changing all instances across your code base be a huge undertaking, but the problem also exists for some database drivers and other parts of your system that may be out of your direct control. Therefore, the other option is to add the casts back in. Peter Eisentraut posted a [list of casts](http://petereisentraut.blogspot.com/2008/03/readding-implicit-casts-in-postgresql.html) that restore some of the pre-8.3 behavior. Do not just apply them all, but add in the ones that you need. We’ve found that the first one (integer AS text) solves 99% of our clients’ casting issues.

### 2. Encoding issues (bad data)

Older databases frequently were not careful about their [encoding](https://www.postgresql.org/docs/current/static/multibyte.html), and ended up using the default "no encoding" mode of SQL_ASCII. Often this was done because nobody was thinking about, or worrying about, encoding issues when the database as first being designed. Flash forward years later, and people want to move to something better than SQL_ASCII such as the now-standard UTF-8. The problem is that SQL_ASCII accepts everything without complaint, and this can cause you migration to fail as the data will not load into the new database with a different encoding. (Also note that even UTF-8 to UTF-8 may cause problems as it was not until Postgres version 8.1 that UTF-8 input was strictly validated.)

Solution: The best remedy is to clean the data on the "old" database and try the migration again. How to do this depends on the nature of the bad data. If it’s just a few known rows, manual updates can be done. Otherwise, we usually write a Perl script to search for invalid characters and replace them. Alternatively, you can pipe the data through iconv in the middle of the upgrade. If all else fails, you can always fall back to SQL_ASCII on the new database, but that should really be a last resort.

### 3. Time

Since the database is almost always an integral part of the business, minimizing the time it is unavailable for use is very important. People tend to underestimate how much time an upgrade can take. (Here we are talking about the actual migration, not the testing, which is a very important step that should not be neglected.) Creating the new database and schema objects is very fast, of course, but the data must be copied row by row, and then all the constraints and indexes created. For large databases with many indexes, the index creation step can take longer than the data import!

Solution: The first step is to do a practice run with as similar hardware as possible to get an idea of how long it will take. If this time period does not comfortably fit within your downtime window (and by comfortable, I mean add 50% to account for Murphy), then another solution is needed. The easiest way is to [use a replication system like Bucardo](/blog/2009/09/migrating-postgres-with-bucardo-4) to "pre-populate" the static part of the database, and then the final migration only involves a small percentage of your database. It should also be noted that recent versions of Postgres can speed things up by using the "-j" flag to [the pg_restore utility](https://www.postgresql.org/docs/current/static/app-pgrestore.html), which allows some of the restore to be done in parallel.

### 4. Dependencies

When you upgrade Postgres, you’re upgrading the libraries as well, which many other programs (e.g. database drivers) depend on. Therefore, it’s important to make sure everything else relying on those libraries still works. If you are installing Postgres with a packaging system, this is usually not a problem as the dependencies are taken care of for you.

Solution: Make sure your test box has all the applications, drivers, cron scripts, etc. that your production box has and make sure that each of them either works with the new version, or has a sane upgrade plan. Note: Postgres may have some hidden indirect dependencies as well. For example, if you are using Pl/PerlU, make sure that any external modules used by your functions are installed on the box.

### 5. Postgres contrib modules

Going from one version of Postgres to another can introduce some serious challenges when it comes to contrib modules. Unfortunately, they are not treated with the same level of care as the Postgres core is. To be fair, most of them will continue to just work, simply by doing a "make install" on the new database before attempting to import. Some modules, however, have functions that no longer exist. Some are not 100% forward compatible, and some even lack important pieces such as uninstall scripts.

Solution: Solving this depends quite a bit on the exact nature of the problem. We’ve done everything from carefully modifying the --schema-only output, to modifying the underlying C code and recompiling the modules, to removing them entirely and getting the functionality in other ways.

### 6. Invalid constraints (bad data)

Sometimes when upgrading, we find that the existing constraints are not letting the existing data back in! This can happen for a number of reasons, but basically it means that you have invalid data. This can be mundane (a check constraint is missing a potential value) or more serious (multiple primary keys with the same value).

Solution: The best bet is to fix the underlying problem on the old database. Sometimes this is a few rows, but sometimes (as in a case with multiple identical primary keys), it indicates an underlying hardware problem (e.g. RAM). In the latter case, the damage can be very widespread, and your simple upgrade plan has now turned into a major damage control exercise (but aren’t you glad you found such a problem now rather than later?) Detecting and preventing such problems is the topic for another day. :)

### 7. tsearch2

This is a special case for the contrib module situation mentioned above. The tsearch2 module first appeared in version 7.4, and was moved into core of Postgres in version 8.3. While there was a good attempt at providing an upgrade path, upgrades can still cause an occasional issue.

Solution: Sometimes the only real solution is edit the pg_dump output by hand. If you are not using tsearch in that many places (e.g. just a few indexes or columns on a couple tables), you can also simply remove it before the upgrade, then add it back in afterwards.

### 8. Application behavior

In addition to the implicit casting issues above, applications sometimes have bad behaviors that were tolerated in older versions of Postgres, but now are not. A typical example is writing queries without explicitly naming all of the tables in the "FROM" section.

Solution: As always, fixing the app is the best solution. However, for some things you can also flip a compatibility switch inside of postgresql.conf. In the example above, one would change the "add_missing_from" from its default of ‘off’ to ‘on’. This should be considered an option of last resort, however.

### 9. System catalogs

Seldom a major update goes by that doesn’t see a change in the system catalogs, the low-level meta-data tables used by Postgres to describe everything in the database. Sometimes programs rely on the catalogs looking a certain way.

Solution: Most programs, if they use the system catalogs directly, are careful about it, and upgrading the program version often solves the problem. At other times, we’ve had to rewrite the program right then and there, either by having it abstract out the information (for example, by using the information_schema views), or (less preferred) by adding conditionals to the code to handle multiple versions of the system catalogs.

### 10. Embedded data

This is a rare but annoying problem: triggers on a table rely on certain data being in other tables, such that doing a --schema-only dump before a --data-only dump will always fail when importing.

Solution: The easiest way is to simply use pg_dumpall, which loads the schema, then the data, then the constraints and indexes. However, this may not be possible if you have to separate things for other reasons (such as contrib module issues). In this case, you can break the --schema-only pg_dump output into pre and post segments. We have a script that does this for us, but it is also slated to be an option for pg_dump in the future.

That’s the list! If you’ve seen other things, please make a note in the comments. Don’t forget to run a database-wide ANALYZE after importing into your new database, as the table statistics are not carried across when using pg_dump.


