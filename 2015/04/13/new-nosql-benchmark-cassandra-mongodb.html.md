---
author: Jon Jensen
gh_issue_number: 1112
tags: benchmarks, big-data, database, nosql, cassandra, mongodb, couchdb
title: 'New NoSQL benchmark: Cassandra, MongoDB, HBase, Couchbase'
---

Today we are pleased to announce the results of a new NoSQL benchmark we did to compare scale-out performance of Apache Cassandra, MongoDB, Apache HBase, and Couchbase. This represents work done over 8 months by [Josh Williams](/team/josh_williams), and was commissioned by [DataStax](http://www.datastax.com/) as an update to a similar [3-way NoSQL benchmark we did two years ago](/blog/2013/03/12/nosql-benchmark-of-cassandra-hbase).

The database versions we used were Cassandra 2.1.0, Couchbase 3.0, MongoDB 3.0 (with the Wired Tiger storage engine), and HBase 0.98. We used YCSB (the [Yahoo! Cloud Serving Benchmark](https://github.com/brianfrankcooper/YCSB)) to generate the client traffic and measure throughput and latency as we scaled each database server cluster from 1 to 32 nodes. We ran a variety of benchmark tests that included load, insert heavy, read intensive, analytic, and other typical transactional workloads.

We avoided using small datasets that fit in RAM, and included single-node deployments only for the sake of comparison, since those scenarios do not exercise the scalability features expected from NoSQL databases. We performed the benchmark on Amazon Web Services (AWS) EC2 instances, with each test being performed three separate times on three different days to avoid unreproduceably anomalies. We used new EC2 instances for each test run to further reduce the impact of any “lame instance” or “noisy neighbor” effect on any one test.

Which database won? It was pretty overwhelmingly Cassandra. One graph serves well as an example. This is the throughput comparison in the Balanced Read/Write Mix:

<img height="398" src="/blog/2015/04/13/new-nosql-benchmark-cassandra-mongodb/image-0.png" width="732"/>

Our full report, [Benchmarking Top NoSQL Databases](http://www.datastax.com/wp-content/themes/datastax-2014-08/files/NoSQL_Benchmarks_EndPoint.pdf), contains full details about the configurations, and provides this and other graphs of performance at various node counts. It also provides everything needed for others to perform the same tests and verify in their own environments. But beware: Your AWS bill will grow pretty quickly when testing large numbers of server nodes using EC2 i2.xlarge instances as we did!

Earlier this morning we also sent out a [press release to announce our results](http://www.prnewswire.com/news-releases/apache-cassandra-leads-all-others-in-latest-nosql-benchmark-300064570.html) and the availability of the report.

**Update:** See our [note about updated test runs and revised report](/blog/2015/06/04/updated-nosql-benchmark-cassandra) as of June 4, 2015.
