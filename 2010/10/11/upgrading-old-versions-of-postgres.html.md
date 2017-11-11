---
author: Greg Sabino Mullane
gh_issue_number: 364
tags: database, open-source, postgres
title: Upgrading old versions of Postgres
---

[](upgrading-old-versions-of-postgres/image-0-big.jpeg)

<a href="/blog/2010/10/11/upgrading-old-versions-of-postgres/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5526807649435102418" src="/blog/2010/10/11/upgrading-old-versions-of-postgres/image-0.jpeg"/></a>

Old elephant courtesy of [Photos8.com](http://photos8.com)

The recent release of Postgres 9.0.0 at the start of October 2010 was not the only big news from the project. Also released were versions 7.4.30 and 8.0.26, which, as I noted in [my usual PGP checksum report](http://www.gtsm.com/postgres_sigs.html), are going to be the last publicly released revisions in the 7.4 and 8.0 branches. In addition, the 8.1 branch will no longer be supported by the end of 2010. If you are still using one of those branches (or something older!), this should be the incentive you need upgrade as soon as possible. To be clear, this means that anyone running Postgres 8.1 or older is *not* going to get any official updates, including security and bug fixes.

A brief recap: Postgres uses major versions, containing two numbers, to indicate a major change in features and functionality. These are released about every two years. Each of these major versions has many revisions, which are released as often as needed. These revisions are designed to be completely binary compatible with the previous revision, meaning you can upgrade revisions very easily, with no dump and restore of the data needed.

Below are the options available for those running older versions of Postgres, from the most desirable to the least desirable. The three general options are to upgrade to the latest release (9.0 as I write this), migrate to a newer version, or stay on your release.

## 1. Upgrade to the latest release

This is the best option, as each new version of Postgres adds more features and becomes more efficient, all while maintaining the high code quality standards Postgres is known for. There are three general approaches to upgrading: pg_upgrade, pg_dump, and [Bucardo](http://bucardo.org/wiki/Bucardo) / [Slony](http://slony.info/).

### Using pg_upgrade

The [pg_upgrade utility](http://www.postgresql.org/docs/current/static/pgupgrade.html) is the preferred method for upgrading in the future. Basically, it rewrites your data directory from the "old" on-disk format to the "new" one. Unfortunately, pg_upgrade only works from version 8.3 and onwards, which means it cannot be used if you are coming from an older version. (This utility used to be called pg_migrator, in case you see references to that.)

### Dump and restore

The next best method is the tried and true "dump and restore". This involves using pg_dump to create a logical representation of the old database, and then loading it into your new database with pg_restore or psql. The disadvantage to this method is time - dump and reload can take a very, very long time for large databases. Not only does the data need to get loaded into the new database tables, but all the indexes must be recreated, which can be agonizingly slow.

### Replication systems

A third option is to use a replication system such as Slony or Bucardo to help with the upgrade. With Slony, you can set up a replication from the old version to the new version, and then failover to the new version once replication is caught up and running smooth. You can do something similar with Bucardo. Note that both systems can only replicate sequences, and tables containing primary keys or unique indexes. Bucardo has a "fullcopy" mode that will copy any table, regardless of primary keys, but it's slow as it's equivalent to a full dump and restore of the table. Note that Bucardo is really only tested on the 8.X versions: for anything older, you will need to use Slony.

Even if you cannot replicate all your tables, such systems can help a migration by replicating *most* of your data. For example, if you have a 750 GB table full of mostly historical data, you can have Bucardo start tracking changes to the table, set up a copy on the new version (perhaps by using warm standby or a snapshot to reduce load on the master), and then start Bucardo to catch up the rows that have changed since the changes were tracked. If you do this for all your large tables, the actual upgrade process can proceed with minimal downtime by shutting down the master, doing a pg_dump of only the non-tracked tables, and then pointing your apps at the new server.

## 2. Migrate to a newer version

Even if you don't go to 9.0, you may want to upgrade to a newer version. Why not go all the way to 9.0? There are only two good reasons not to. One, if your system's packaging system does not have 9.0 yet, or you have custom packaging requirements that prevent you from doing so. Two, if you have concerns about application compatibility between two versions. However, that latter concern should be minimal. The largest and most disruptive compatibility change appeared in version 8.3 with the removal of implicit casts. Since 8.2 is likely to be unsupported in the next couple years, you should be going to at least 8.3. And if you can go to 8.3, you can go to 9.0.

## 3. Stay on your release

This is obviously the least-desirable option, but may be necessary due to real-world constraints involving time, testing, compatibility with other programs, etc. At the bare minimum, make sure you are at least running the latest revision, e.g. 7.4.30 if running 7.4. Moving forward, you will need to keep an eye on the Postgres commits list and/or the detailed release notes for new versions, and examine if any of the fixed bugs apply to your version or your situation. If they do, you'll need to figure out how to apply the patch to your older version, and then release this new version into your environment. Sound risky? It gets worse, because your patch is only being used and tested by an extremely small pool of people, has no build farm support, and is not available to the Postgres developers. If you want to go this route, there are companies familiar with the Postgres code base (including End Point) that will help you do so. But know in advance that we are also going to push you very hard to upgrade to a modern, supported version instead (which we can help you with as well, of course :).


