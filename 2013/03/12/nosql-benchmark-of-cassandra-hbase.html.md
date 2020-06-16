---
author: Jon Jensen
gh_issue_number: 768
tags: database, mongodb, nosql, performance, cassandra
title: NoSQL benchmark of Cassandra, HBase, MongoDB
---

<a href="https://www.datastax.com/wp-content/uploads/2013/02/WP-Benchmarking-Top-NoSQL-Databases.pdf" target="_blank"><img alt="Benchmarking Top NoSQL Databases" height="194" rel="facebox" src="/blog/2013/03/12/nosql-benchmark-of-cassandra-hbase/image-0.png" style="border: 1px solid #999;" width="150"/>Benchmark White Paper</a>

We’re excited to have recently worked on an interesting [benchmarking project for DataStax](https://www.datastax.com/2013/02/datastax-releases-independent-benchmark-results-showing-that-apache-cassandra-outperforms-nosql-competitors-by-a-wide-margin), the key company supporting the Cassandra “NoSQL” database for large horizontally-scalable data stores. This was done over the course of about 2 months.

This benchmark compares the performance of MongoDB, HBase, and Cassandra on the widely-used Amazon Web Services (AWS) EC2 cloud instances with local storage in RAID, in configurations ranging from 1-32 database nodes. The software stack included 64-bit Ubuntu 12.04 LTS AMIs, Oracle Java 1.6, and YCSB (Yahoo! Cloud Serving Benchmark) for its lowest-common-denominator NoSQL database performance testing features. Seven different test workloads were used to get a good mix of read, write, modify, and combined scenarios.

Because cloud computing resources are subject to “noisy neighbor” situations of degraded CPU or I/O performance, the tests were run 3 times each on 3 different days, with different EC2 instances to minimize any AWS-related variance.

The project involved some interesting automation challenges for repeatedly spinning up the correct numbers and types of nodes, configuring the node software, running tests, and gathering and collating results data. We kept the AWS costs more reasonable by using Spot Instances for most instances.

You can read more at [DataStax’s white paper page](https://www.datastax.com/resources/whitepapers/benchmarking-top-nosql-databases) and see all the details in the white paper itself.
