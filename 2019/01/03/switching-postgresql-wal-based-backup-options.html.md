---
author: "Josh Williams"
title: "Switching PostgreSQL WAL-based Backup Options"
tags: database, postgres, sysadmin
---

<img src="/blog/2019/01/03/switching-postgresql-wal-based-backup-options/image-0.jpg" alt="Sunbury hoard" /><br><a href="https://www.flickr.com/photos/pahudson/4911869716/">Photo by Paul Hudson</a> · <a href="https://www.flickr.com/photos/pahudson/4911869716/">CC BY 2.0, modified</a>

I was woken up this morning. It happens every morning, true, but not usually by a phone call requesting for help with an out-of-space database server.

It turns out that one of the scripts we're in the process of retiring, but still had in place, got stuck in a loop and filled most of the available space with partial, incomplete base backups. So, since I'm awake, I might as well talk about Postgres backup options. I don't mean for it to be a gripe session, but I'm tired and it kind of is.

For this particular app, since it resides partially on AWS we looked specifically at options that are able to work natively with S3. We've currently settled on [pgBackRest](https://pgbackrest.org/). There's a bunch of options out there, which doesn't make the choice easy. But I suppose that's the nature of things these days.

At first we'd tried out [pghoard](https://github.com/aiven/pghoard). It looks pretty good on the tin, especially with its ability to connect to multiple cloud storage services beyond S3: Azure, Google, Swift, etc. Having options is always nice. And for the most part it works well, apart from a couple idiosyncrasies.

We had the most trouble with the encryption feature. It didn't have any problem on the encryption side. But for some reason on the restore the process would hang and eventually fail out without unpacking any data. Having a backup solution is a pretty important thing, but it doesn't mean anything unless we can get the data back from it. So this was a bit of a sticking point. We probably could have figured out how to get it functioning, and at least been a good citizen and reported it upstream to get it resolved in the source. But we kind of just needed it working, and giving something else a shot is a quicker path to that goal. Sorry, pghoard devs.

The other idiosyncratic behaviors that are probably worth mentioning are that it does its own scheduling. The base backups, for instance, happen at a fixed hour interval in the configuration file, starting from when the service is first spun up. So if I set it to 24 hours, and then `service pghoard start` at 1 PM, well, that's the schedule now. So much for having it run overnight. Nor can tell it "create a base backup right now" at other times. And, so far as I can find, there's no way to override that.

Also rather than using an archive\_command, it connects as a streaming replica and pulls WAL files that way. Which is great from a perspective of it not being invasive. But during a load test we generated activity faster than it could write to S3, and hit the classic streaming replica problem of it needing WAL files that had already been removed from the master. It doesn't handle this condition, though, and just retried and retries after the error, even after another base backup happened. I don't know that I'd let it run long enough to see if it would eventually give up when the base backup that needed those WAL files had been pushed out by the retention policies. But I eventually killed it and had it make a fresh start. There's some chatter out there about having it use replication slots, which would be the natural solution for this case, so maybe that's fixed by now.

So, we switched to something else, and elected pgBackRest next. It'd since been used in another project or two, so it had some bonus points for recently acquired institutional knowledge. It supports storage in S3 (and only S3, but whatevs.) And this time we didn't have to build and distribute deb's, it's already available in the Postgres apt repo.

I like things neat and tidy. A base backup I've always seen as essentially one unit; it's the database cluster as a whole (even though I know it's in a potentially inconsistent state by being spread over an interval of time.) Stored and delivered as a compressed tar file or some such. pgBackRest takes a different view, and instead stores its base backup as separate relation files, essentially as they are on disk, and individually compressed. Which, given it's something I don't have to touch and move around manually, is a format that's growing on me.

Because it does this, pgBackRest brings back a concept I haven't thought about in a long time: "Incremental" or "Differential" backups. If a relation (or part of a really big relation, since it's chopped up into 1 GB sections) doesn't change between base backups, pgBackRest can skip those and point back to an earlier copy of the file. In most databases (at least I'd argue) this won't matter so much, as between user activity, background tasks like vacuum, and such, things are frequently changing in those relation files. But in this case, the client has a large table of file blob's that mostly gets appended to. So the data has been loaded, we ran a `VACUUM FREEZE` on it, and now the daily differential backups avoid a little bit of S3 cost.

Between the entries we have to add to cron and the edit of the archive\_command parameter to save WAL pgBackRest takes a couple more steps to get fully in place. But it's all in configuration management now, so, meh. Besides, the fixed schedule does make it possible to run at a specific time. And the WAL archival is guaranteed not to fall behind and get stuck.

Like pghoard, pgBackRest does encryption. pghoard's is based on public/private keys, which I might have preferred because the base backups are used to seed development systems, and only distributing the public key to those would be neat. pgBackRest's is symmetric with a passphrase. Both also do automatic retention maintenance; we have it maintain two weekly full base backups and daily differentials in between. WAL retention is similarly automatic.

The cool thing was we could run both side by side for a while, and confirm that pgBackRest would shake out before disabling pghoard. At least I thought that was cool, until that call came through. I kind of wish I knew what got it there in the first place; we found pghoard in a base backup attempt loop, where it'd ended up mostly filling the disk, and just ended up killing it and manually cleaned up its storage to get things back to green.

So I suppose the morals of the story are:

- Keep your options open. There's lots of projects out there that do similar things a little differently. Try them out, and don't be afraid to pivot if something is a little more to your liking.
- The things you do try, test out fully. Restore the backups. Let them run for a while to see how it fares long term and make sure all the assumptions hold up.
- I need a second cup of coffee. BRB.
