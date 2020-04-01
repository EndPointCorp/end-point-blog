---
author: Szymon Lipiński
gh_issue_number: 660
tags: optimization, postgres, testing
title: Speeding Up Integration Tests with PostgreSQL - Follow Up
---

Last week I wrote a blog article about [speeding up integration tests using PostgreSQL](/blog/2012/06/22/speeding-up-integration-tests-postgresql). I proposed there changing a couple of PostgreSQL cluster settings. The main drawback of this method is that those settings need to be changed for the whole cluster. When you have some important data in other databases, you can have a trouble.

In one of the comments Greg proposed using the unlogged table. This feature appeared in PostgreSQL 9.1. The whole difference is that you should use CREATE UNLOGGED TABLE instead of CREATE TABLE for creating all your tables.

For the unlogged table, the data is not written to the write-ahead log. All inserts, updates and deletes are much faster, however the table will be truncated at the server crash or unclean shutdown. Such table is not replicated to standby servers, which is obvious as there are replicated write-ahead logs. What is more important, the indexes created on unlogged tables are unlogged as well.

All the things I describe here are for integrations tests. When database crashes, then all the tests should be restarted and should prepare the database before running, so I really don’t care what happens with the data when something crashes.

The bad thing about unlogged tables is that you cannot change normal table to unlogged. There is nothing like:

```sql
ALTER TABLE SET UNLOGGED;
```

The easiest way which I found for changing the table into unlogged was to create a database dump and add UNLOGGED to all the table creation commands. To have it a little bit faster, I used this command:

```bash
pg_dump pbench | sed 's/^CREATE TABLE/CREATE UNLOGGED TABLE/' > pbench.dump.sql
```

This time I will just delete all the tables in the database and load this dump before running the tests instead of using pg_bench for generating the data:

```bash
psql -c "drop database pbench"
psql -c "create database pbench"
psql pbench < pbench.dump.sql
```

Time for tests. The previous tests results are in the previous blog article. I’m using standard PostgreSQL settings (the secure ones) and the same scale value for pg_bench.

The tests were made using exactly the same command as last time:

```bash
./pgbench -h localhost -c 1 -j 1 -T 300 pbench
```

Below are results combined with the results from previous article.

```
<table id="testres">
    <thead>
      <tr>
        <th class="noborder"> </th>
        <th colspan="3"> number of clients and threads </th>
      </tr>
      <tr>
        <th class="noborder"> </th>
        <th>1
        </th><th>2
        </th><th>3
      </th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="name">normal settings</td>
        <td>78 tps</td>
        <td>80 tps</td>
        <td>99 tps</td>
      </tr>
      <tr>
        <td class="name">dangerous settings</td>
        <td>414 tps</td>
        <td>905 tps</td>
        <td>1215 tps</td>
      </tr>
      <tr>
        <td class="name">unlogged table</td>
        <td>420 tps</td>
        <td>720 tps</td>
        <td>1126 tps</td>
      </tr>
    </tbody>
</table>
```

As you can see, the efficiency with unlogged tables is almost as good as with the unsafe settings. The great thing is that it doesn’t influence other databases in the cluster, so you can use safe/default settings for other databases, and only use unlogged tables for the integration tests, which should be much faster now.

This solution works only with the PostgreSQL 9.1 and newer. If you have older PostgreSQL you have to use the previous method with unsafe settings, or better: just upgrade the database.
