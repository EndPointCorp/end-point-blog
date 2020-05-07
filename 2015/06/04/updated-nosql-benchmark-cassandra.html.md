---
author: Josh Williams
gh_issue_number: 1131
tags: benchmarks, big-data, database, nosql, cassandra, mongodb, couchdb
title: 'Updated NoSQL benchmark: Cassandra, MongoDB, HBase, Couchbase'
---

Back in April, we published a benchmark report on a number of NoSQL databases including Cassandra MongoDB, HBase, and Couchbase.  We endeavored to keep things fair and configured as identically as possible between the database engines.  But a short while later, DataStax caught two incorrect configuration items, in Cassandra and HBase, and contacted us to verify the problem.  Even with the effort we put in to keeping everything even, a couple erroneous parameters slipped through the cracks! I’ll save the interesting technical details for another post coming soon, but once that was confirmed we jumped back in and started work on getting corrected results.

With the configuration fixed we re-ran a full suite of tests for both Cassandra and HBase.  The updated results have published a revised report that you can [download in PDF format from the DataStax website](http://www.datastax.com/wp-content/themes/datastax-2014-08/files/NoSQL_Benchmarks_EndPoint.pdf) (or see the [overview link](http://www.datastax.com/apache-cassandra-leads-nosql-benchmark)).

The revised results still show Cassandra leading MongoDB, HBase, and Couchbase in the various YCSB tests.

For clarity the paper also includes a few additional configuration details that weren’t in the original report. We regret any confusion caused by the prior report, and worked as quickly as possible to correct the data. Feel free to get in contact if you have any questions.
