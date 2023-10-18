---
author: Selena Deckelmann
title: 'Filesystem I/O: what we presented'
github_issue_number: 66
tags:
- conference
- postgres
date: 2008-09-19
---



As [mentioned](/blog/2008/09/fun-with-72gb-of-disk-filesystem/) last week, Gabrielle Roth and I presented results from tests run in the new Postgres Performance Lab. [Our slides](https://www.slideshare.net/selenamarie/filesystem-io-from-a-database-perspective-presentation/) are available on Slideshare.

We tested eight core assumptions about filesystem I/O performance and presented the results to a room of filesystem hackers and a few database specialists. Some important things to remember about our tests: we were testing I/O only—​no tuning had been done on the hardware, filesystem defaults or for Postgres—​and we did not take reliability into account at all.  Tuning the database and filesystem defaults will be done for our next round of tests.

Filesystems we tested were ext2, ext3 (with or without data journaling), xfs, jfs, and reiserfs.

Briefly, here are our assumptions, and the results we presented:

1. RAID5 is the worst choice for a database. Our tests confirmed this, as expected.

1. LVM incurs too much overhead to use. Our test showed that for sequential or random reads on RAID0, LVM doesn’t incur much more overhead than hardware or software RAID.

1. Software RAID is slower. Same result as LVM for sequential or random reads.

1. Turning off ‘atime’ is a big performance gain. We didn’t see a big improvement, but you do generally get 2-3% improvement “for free” by turning atime off on a filesystem.

1. Partition alignment is a big deal. Our tests weren’t able to prove this, but we still think it’s a big problem. Here’s [one set of tests demonstrating](http://sqlblog.com/blogs/linchi_shea/archive/2007/02/01/performance-impact-of-disk-misalignment.aspx) the problem on Windows-based servers.

1. Journaling filesystems will have worse performance than non-journaling filesystems. Turn the data journaling off on ext3, and you will see better performance than ext2. We polled the audience, and nearly all thought ext2 would have performed better than ext3. People in the room suggested that the difference was because of seek-bundling that’s done in ext3, but not ext2.

1. Striping doubles performance. Doubling-performance is a best-case scenario, and not what we observed. Throughput increased about 35%.1. Your read-ahead buffer is big enough.  The default read-ahead buffer size is 128K. Our tests, and an independent set of tests by another author, confirm that increasing read-ahead buffers can provide a performance boost of about 75%.  We saw improvement leveling out when the buffer is sized at 8MB, with the bulk of the improvement occurring up to 1MB. We plan to test this further in the future.

All the data from these tests is available on the [Postgres Developers wiki](https://wiki.postgresql.org/wiki/HP_ProLiant_DL380_G5_Tuning_Guide).

Our hope is that someone in the Linux filesystem community takes up these tests and starts to produce them for other hardware, and on a more regular basis. We did have 3 people interested in running their own tests on our hardware from the talk!  In the future, we plan to focus our testing most on Postgres performance.

Mark Wong and Gabrielle will be presenting this talk again, with a few new results, at the [PostgreSQL Conference West](https://web.archive.org/web/20080912204757/http://postgresqlconference.org/west08/talks/).


