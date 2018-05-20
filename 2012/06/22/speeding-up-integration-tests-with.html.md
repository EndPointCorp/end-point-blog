---
author: Szymon Lipiński
gh_issue_number: 656
tags: performance, postgres, testing
title: Speeding Up Integration Tests with PostgreSQL
---

Many people tend to say they don’t want to write tests. One of the reasons is usually that the tests are too slow. The tests can be slow because they are written in a bad way. They can also be slow because of slow components. One such component is usually a database.

The great thing about PostgreSQL is that all types of queries are transactional. It simply means that you can start a transaction, then run the test, which can add, delete and update all the data and database structure it wants. At the end of the integration test, there should be called rollback which just reverts all the changes. It means the next test will always have the same database structure and data before running, and you don’t need to manually clear anything.

For running the integration tests we need a test database. One of the most important things when running test is speed. Tests should be fast, programmers don’t like to wait ages just to know that there is something wrong.

We can also have a read only databases for the tests. Then you don’t need to worry about the transactions, however you always need to ensure the tests won’t change anything. Even if you assume your tests won’t make any changes, it is always better to use a new transaction for each test and rollback at the end.

The main idea for fast integration tests using PostgreSQL is that those tests don’t change anything in the database. If they don’t change, we don’t need to worry about some possible data loss when the database suddenly restarts. Then we can just restart the tests. Tests should prepare the data before running, assuming the database is in unknown state.

This database should be as fast as possible, even if it means losing data when some unusual things happen. Normally PostgreSQL works really great when someone turns off the server plug suddenly or kills the database process. It just doesn’t lose the data.

However we really don’t need this stuff when running the tests. The database can be loaded before running tests. If the database is suddenly shut down, we should restart the tests.

The simplest thing is to change a couple of settings which enable great secure writes, however it slows down the database. We don’t need to have secure writes, they are only important when something crashes. Then we should restart all the components used for integration tests and load database before testing.

For testing I will use pgbench program which makes a test similar to TPC-B. The tests prepare the data in four tables and then performs a simple transaction:

```sql
BEGIN;

UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;

SELECT abalance FROM pgbench_accounts WHERE aid = :aid;

UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;

UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;

INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);

END;
```

where the params are randomly chosen during execution.

The database is created normally using SQL query:

```sql
  CREATE DATABASE pbench;
```

Before running the tests, pgbench has to prepare initial data. This is done using the -i param. My computer is not very slow, so the default size of the database is too small, I used a quite larger database size using the -s 25 param. This way the database size is about 380MB, including indexes.

```bash
  ./pgbench -h localhost pbench -i -s 25
```

The first test will just run using standard PostgreSQL configuration settings and will run for 5 minutes (the -T 300 param).

```bash
  ./pgbench -h localhost -T 300 pbench
```

The initial results show about 80 transactions per second (tps).

```bash
  number of clients: 1
  number of threads: 1
  duration: 300 s
  number of transactions actually processed: 23587
  tps = 78.621158 (including connections establishing)
  tps = 78.624383 (excluding connections establishing)
```

You may probably noticed the “number of clients” and “number of threads” values. It is the scenario where you have sequential tests, so all of them are run one by one. However integration tests written in a good way can be run in parallel, so let’s run the pgbench once again, but with three threads and three clients.

```bash
  ./pgbench -h localhost -c 3 -j 3 -T 300 pbench
```

The results show that it is a little bit faster now:

```bash
  number of clients: 3
  number of threads: 3
  duration: 300 s
  number of transactions actually processed: 29782
  tps = 99.268609 (including connections establishing)
  tps = 99.273464 (excluding connections establishing)
```

Let’s now change the PostgreSQL settings to some more dangerous, so it can lose some data when shut down suddenly, but in fact I don’t care as all the data is loaded just before running the test.

I’ve written at the end of the postgresql.conf file the following lines:

```bash
  fsync = off                # turns forced synchronization on or off
  synchronous_commit = off   # synchronization level; on, off, or local
  full_page_writes = off     # recover from partial page writes
```

Those changes need a database restart, and after restarting PostgreSQL, I just run the pgbench tests once again.

All the results are in the following table:

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
        <td class="name">change ratio</td>
        <td>531 %</td>
        <td>1131 %</td>
        <td>1227 %</td>
      </tr>
    </tbody>
</table>
```

As you can see, you can do three simple things to speed up your integration tests using PostgreSQL:

- Change default PostgreSQL settings to speed the database up.
- Change your tests to run in parallel.
- Run each test in one transaction.

This way I managed to speed up the tests from 78 tps to 1215 tps. It means that the integration tests which normally run in 60 minutes, should now run in 4 minutes.

I’ve also played with many other settings which could have some impact on the PostgreSQL speed. They really have, however the impact is so small that I don’t think it is worth mentioning here. Changing those three settings can make the PostgreSQL fast enough.
