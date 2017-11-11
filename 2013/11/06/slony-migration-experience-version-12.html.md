---
author: David Christensen
gh_issue_number: 875
tags: postgres, replication
title: Slony Migration experience version 1.2 to version 2.2
---

We recently had a client who upgraded from Slony 1.2 to Slony 2.2, and I want to take this opportunity to report on our experiences with the migration process.

A little background: This client has a fairly large database (300GB) replicated across 5 database nodes, with the slon daemons running on a single shared box.  We wanted to upgrade to the latest Slony 2 version for stability and to resolve some known and unresolvable issues with the 1.2 branch of Slony when replication lags a specific amount.

As is usual for any large migration projects such as this, we had to deal with a set of tradeoffs:

- Firstly, minimize any necessary downtime.

- Secondly, allow for rollback due to any discovered issues.

- Thirdly, ensure that we have sufficient redundancy/capacity whichever final state we were to end up in (i.e., successful migration to Slony 2 or reversion to Slony 1.2).

We of course tested the process several times in order to ensure that the processes we came up with would work and that we would be well-equipped to handle issues were they to arrive.

The upgrade from Slony 1.2 to Slony 2.2 necessarily requires that we uninstall the Slony 1.2 system and triggers from the indicated databases, which means that in order to ensure that the data stayed the same on all nodes in the cluster we needed to disallow any queries which modify the tables or sequences in the replication sets.  We chose to disable connectivity to the database entirely for the duration of the migration.

One of the features of Slony 2 is the ability to use the OMIT COPY option in the SUBSCRIBE SET command, which will tell Slony to trust that the data in the tables already reflects the current state of the origin for that set.  In previous versions of Slony, a SUBSCRIBE SET would TRUNCATE and COPY the tables in question in order to guarantee to itself that the data in the tables matched the state of the origin set at the time of the SUBSCRIBE event.

For the purposes of our consideration, this was a major factor in ensuring we could hit the downtime targets; with Slony 1.2, subscribing a new node to the cluster would take around 8-10 hours based on the size of the replication set.  Since this was an unavoidable cost, setting a new cluster up from scratch with Slony 1.2 would leave a large window of time where there was not a complete replica node.  With Slony 2, we were able to ensure that the cluster was set up identically while being able to take advantage of the fact we knew the data had not changed, and thus be able to bootstrap replication from this process.

Because there was always the possiblity that something would go wrong and we would be prevented from deploying the Slony 2-based cluster, we needed to consider how best to manage the possibility of a rollback.  We also wanted to ensure that if we *did* have to rollback, we would not end up in a situation without a backup replica.

While this database cluster had 5 nodes, we were fortunate in that due to natural seasonal traffic levels, not all nodes were needed to handle the site traffic; in fact, just 2 servers would be sufficient to handle the traffic for a period of time.  This meant that if we needed to roll back, we could have redundancy for the old cluster while allowing us to resubscribe the dropped Slony 1.2 nodes at our leisure if necessary.

Because the expected state of the final cluster was to have the Slony 2 cluster be the new production cluster, we chose to keep 2 nodes from the existing Slony 1.2 cluster (those with the lowest-powered servers) as a rollback point for the project while converting the 3 most powerful nodes to Slony 2.  Fortunately, one of the lower-powered 1.2 nodes was the existing origin node for the Slony 1.2 cluster, so we did not need to make any further topology modifications (although it would have been easy enough to use MOVE SET if we needed).

We dropped the nodes that were targetted for Slony 2 from the Slony 1.2 cluster and cleaned up their schema to ensure the database was clean from Slony 1.2 artifacts, while still populated with the latest data from the origin.  We then shut down the remaining Slony 1.2 postgresql and slon processes.

For the nodes targetted as Slony 2 nodes, we installed the new slony libraries in the postgres lib directory.  As of Slony 2.2, the library objects are named uniquely for major versions, so we were able to install concurrently with the Slony 1.2 support libraries in case we needed to roll back.

We were able to reuse the slon_tools.conf definitions from the initial cluster, as we had ensured that this configuration stayed consistent with any database modifications.  We had of course verified that all tables that were in the Slony 1.2 subscription sets existed in the slon_tools.conf definitions.

After installing Slony 2 and initializing the base cluster, we utilized Slony 2's SUBSCRIBE SET (OMIT COPY = true) to set up the subscriptions for the indiviual sets to utilize the data.  The altperl scripts do not provide a way to set this by default, so we used sed to modify the output of the slonik_subscribe_set script.

We also took advantage of this time to reorganize where we were running the individual Slony daemons.  The 1.2 cluster had the slony daemons running on a single machine with the cluster config mirrored across all other servers in the cluster so we could bring the daemons up on another node in the cluster if we needed.  This was of course sub-optimal, being a single point of failure; our revised architecture included each slony daemon running on the same server as the postgresql server.

In short, we were able to reshape the cluster, verify and test everything with a very short downtime (the site itself was down for roughly 30 minutes of an allocated 4 hour maintenance window for the upgrade, testing, etc; just a few minutes were needed for the Slony upgrade proper) and bring things back up after a fraction of the scheduled maintenance window, and the client has overall been very happy with the upgrade.
