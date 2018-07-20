---
author: David Christensen
gh_issue_number: 250
tags: database, postgres, tips
title: Postgres SQL Backup Gzip Shrinkage, aka DON’T PANIC!!!
---



I was investigating a recent Postgres server issue, where we had
discovered that one of the RAM modules on the server in question had
gone bad. Unsurprisingly, one of the things we looked at was the
possibility of having to do a restore from a SQL dump, as if there had
been any potential corruption to the data directory, a base backup
would potentially have been subject to the same possible errors that
we were trying to restore to avoid.

As it was already the middle of the night (anyone have a server
emergency during the normal business hours?), my investigations were
hampered by my lack of sleep.

If there had been some data directory corruption, the pg_dump process
would likely fail earlier than in the backup process, and we’d expect
the dumps to be truncated; ideally this wasn’t the case, as memory
testing had not shown the DIMM to be bad, but the sensor had alerted
us as well.

I logged into the backup server and looked at the backup dumps; from
the alerts that we’d gotten, the memory was flagged bad on January 3.
I listed the files, and noticed the following oddity:

```nohighlight
 -rw-r--r-- 1 postgres postgres  2379274138 Jan  1 04:33 backup-Jan-01.sql.gz
 -rw-r--r-- 1 postgres postgres  1957858685 Jan  2 09:33 backup-Jan-02.sql.gz
```

Well, this was disconcerting. The memory event had taken place on the
3rd, but there was a large drop in size of the dumps between January
1st and January 2nd (more than 400MB of *compressed* output, for those of
you playing along at home). This indicated that either the memory
event took place earlier than recorded, or something somewhat
catastrophic had happened to the database; perhaps some large deletion
or truncation of some key tables.

Racking my brains, I tried to come up with an explanation: we’d had a
recent maintenance window that took place between January 1 and
January 2; we’d scheduled a CLUSTER/REINDEX to reclaim some of the
bloat which was in the database itself. But this would only reduce
the size of the data directory; the amount of live data would have
stayed the same or with a modest increase.

Obviously we needed to compare the two files in order to determine
what had changed between the two days. I tried:

```nohighlight
 diff <(zcat backup-Jan-01.sql.gz | head -2300) <(zcat backup-Jan-02.sql.gz | head -2300)
```

Based on my earlier testing, this was the offset in the SQL dumps
which defined the actual schema for the database excluding the data;
in particular I was interested to see if there had been (say) any
temporarily created tables which had been dropped during the
maintenance window. However, this showed only minor changes (updates
to default sequence values). It was time to do a full diff of the
data to try and see if some of the aforementioned temporary tables had
been truncated or if some catastrophic deletion had occurred or...you
get the idea. I tried:

```nohighlight
 diff <(zcat backup-Jan-01.sql.gz) <(zcat backup-Jan-02.sql.gz)
```

However, this approach fell down when diff ran out of memory. We
decided to unzip the files and manually diff the two files in case it
had something to do with the parallel unzips, and here was a mystery;
after unzipping the dumps in question, we saw the following:

```nohighlight
 -rw-r--r-- 1 root root 10200609877 Jan  8 02:19 backup-Jan-01.sql
 -rw-r--r-- 1 root root 10202928838 Jan  8 02:24 backup-Jan-02.sql
```

The uncompressed versions of these files showed sizes consistent with
slow growth; the Jan 02 backup was slightly larger than the Jan 01
backup. This was really weird! Was there some threshold in gzip
where given a particular size file it switched to a different
compression algorithm? Had someone tweaked the backup script to gzip
with a different compression level? Had I just gone delusional from
lack of sleep? Since gzip can operate on streams, the first option
seemed unlikely, and something I would have heard about before. I
verified that the arguments to gzip in the backup job had not changed,
so that took that choice off the table. Which left the last option,
but I had the terminal scrollback history to back me up.

We finished the rest of our work that night, but the gzip oddity stuck
with me through the next day. I was relating the oddity of it all to
a co-worker, when insight struck: since we’d CLUSTERed the table, that
meant that similar data (in the form of the tables’ multi-part primary
keys) had been reorganized to be on the same database pages, so when
pg_dump read/wrote out the data in page order, gzip had that much more
similarity in the same neighborhood to work with, which resulted in
the dramatic decrease in the compressed gzip dumps.

So the good news was that CLUSTER will save you space in your SQL
dumps as well (if you’re compressing), the bad news was that it took
an emergency situation and an almost heart-attack for this engineer to
figure it all out. Hope I’ve saved you the trouble... :-)


