---
author: Josh Tolley
gh_issue_number: 122
tags: postgres
title: Inside PostgreSQL — Multi-Batch Hash Join Improvements
---



A few days ago a [patch](https://www.postgresql.org/message-id/6EEA43D22289484890D119821101B1DF2C1683@exchange20.mercury.ad.ubc.ca) was [committed](https://www.postgresql.org/message-id/20090321000440.72E57754ADE@cvs.postgresql.org) to improve PostgreSQL’s performance when hash joining tables too large to fit into memory. I found this particularly interesting, as I was a minor participant in the patch review.

A hash join is a way of joining two tables where the database partitions each table, starting with the smaller one, using a hash algorithm on the values in the join columns. It then goes through each partition in turn, joining the rows from the first table with those from the second that fell in the same partition.

Things get more interesting when the set of partitions from the first table is too big to fit into memory. As the database partitions a table, if it runs out of memory it has to flush one or more partitions to disk. Then when it’s done partitioning everything, it reads each partition back from the disk and joins the rows inside it. That’s where the “Multi-Batch” in the title of those post comes in—​each partition is a batch. The database chooses the smaller of the two tables to partition first to help guard against having to flush to disk, but it still needs to use the disk for sufficiently large tables.

In practice, there’s one important optimization: after partitioning the first table, even if some partitions are flushed to disk, the database can keep some of the partitions in memory. It then partitions the second table, and if a row in that second table falls into a partition that’s already in memory, the database can join it and then forget about it. It doesn’t need to read in anything else from disk, or hang on to the row for later use. But if it can’t immediately join the row with a partition already in memory, the database has to write that row to disk with the rest of the partition it belongs to. It will read that partition back later and join the rows inside. So when the partitions of the first table get too big to fit into memory, there are performance gains to be had if it intelligently chooses which partitions go to disk. Specifically, it should keep in memory those partitions that are more likely to join with something in the second table.

How, you ask, can the database know which partitions those are? Because it has statistics describing the distribution of data in every column of every table: the histogram. Assume it wants to join tables A and B, as in “SELECT * FROM A JOIN B USING (id)”. If B.id is significantly skewed—​that is, if some values show up noticeably more frequently than others—​PostgreSQL can tell by looking its statistics for that column, assuming we have an adequately large statistics_target on the column and have analyzed the table appropriately. Using the statistics, PostgreSQL can determine approximately what percentage of the rows in B have a particular value in the “id” column. So when deciding to flush a partition to disk while partitioning table A, PostgreSQL now knows enough to hang on those partitions containing values that show up most often in B.id, resulting in a noticeable speed improvement in common cases.


