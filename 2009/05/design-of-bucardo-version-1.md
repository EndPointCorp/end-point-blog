---
author: Jon Jensen
title: The design of Bucardo version 1
github_issue_number: 146
tags:
- database
- postgres
- bucardo
date: 2009-05-15
---

Since [PGCon 2009](http://www.pgcon.org/2009/) begins next week, I thought it would be a good time to start publishing some history of the [Bucardo replication system](https://bucardo.org/) for [PostgreSQL](https://www.postgresql.org/). Here I will cover only Bucardo version 1 and leave Bucardo versions 2 and 3 for a later post.

Bucardo 1 is an asynchronous multi-master and master/slave database replication system. I designed it in August-September 2002, to run in Perl 5.6 using PostgreSQL 7.2. It was later updated to support PostgreSQL 7.4 and 8.1, and changes in DBD::Pg’s COPY functionality. It was built for and funded by [Backcountry.com](https://www.backcountry.com/), and various versions of Bucardo have been used in production as a core piece of their infrastructure from September 2002 to the present.

Bucardo’s design is simple, relying on the consistently correct behavior of the underlying PostgreSQL database software. It made some compromises on ideal behavior in order to have a working system in a reasonable amount of time, but the compromises are few and are mentioned below.

### General design

Bucardo 1 needed to:

- Support asynchronous multimaster replication.

- Support asynchronous master/slave replication of full tables and changes to tables.

- Leave frequency of replication up to the administrator, which came by default since each replication event is a separate run of the program.

- Preserve transaction atomicity and isolation across databases.

- Continue collecting change information even when no replication process is running.

- Be fairly efficient in storing changes and in bandwidth usage sending them to the other database.

- Have a default “winner” in collision situations, with special handling possible for certain tables where more intelligent collision merges could be done.

- Not require any database downtime for maintenance, upgrades, etc.

- Be fairly simple to understand and support.

- Support a data flow arrangement such that the replicator is behind a firewall and reaches out to an external database, but doesn’t require inbound access to the internal database.

### Operations

There are four types of database operations Bucardo 1 can perform:

- **peer** — synchronize changes in one or more tables between two peer databases (multi-master)

- **pushdelta** — copy only changed rows from a table or set of tables from a master database to a slave database

- **push** — copy an entire table or set of tables from a master database to a slave database

- **compare** — compare all rows of one or more tables between two databases

I will discuss each of these operations in turn.

### Peer sync

The peer sync operation is the most groundbreaking feature of Bucardo 1. The much smaller Backcountry.com of 2002 wanted to have an internal master database in their office, which housed their customer service and warehouse employees, buyers, and management. Their office had a low-bandwidth and not entirely reliable Internet connection. Their e-commerce web, application, and database servers were at a colocation facility with a fast Internet connection, and they wanted an identical master database to reside there, so that in the case of any disruption in connectivity between their office and colocation facility, both locations could continue to function independently, and their databases would automatically synchronize after connectivity was restored.

To summarize, what they needed is multi-master replication. Their needs would be satisfied with asynchronous multi-master replication. That meant that it was acceptable for the databases to be current with each other with 1-2 minutes of lag time. (Synchronous multi-master replication requires a continuous connection between the two master databases, and transactions are not allowed to commit until the transaction is completed on both databases.)

I want to review some of the features that are required for multi-master replication to work. First, it needs to have [ACID properties](https://en.wikipedia.org/wiki/ACID) just as the underlying database itself. The most relevant properties for our multi-master replication system are atomicity and isolation. A transaction must be entirely visible on a given database, or not visible at all.

For example, let us imagine that a customer ecommerce order consists of exactly 1 row in the “orders” table, which references 1 row in the “users” table, and the following tables may have 0 or more rows pointing to the “orders” table:

- order_lines
- order_notes
- credit_cards
- payments
- gift_certificates
- coupon_uses
- affiliate_commissions
- inventory

To add an order to the source database, a transaction is started, rows are added to relevant tables, the transaction is committed, and then those rows will all appear to other database users at once. Until the transaction is committed, no changes are visible. If an error occurs, the entire transaction rolls back, and it will never have been seen by any other database user.

This ensures that warehouse employees, customer service representatives, etc. will never see a partial order. This is especially important since we don’t want to ship an order that is missing some of its line items, or double-charge a credit card because we didn’t have a payment record yet. And an order without its associated inventory records would have trouble shipping at the warehouse.

This is all standard ACID stuff. But since I was writing a multi-master replication system from scratch, I had to assure the same properties across two database clusters, for which PostgreSQL had no facilities.

Changes are tracked by having a “delta table” paired with every table that’s part of the multi-master replication system. The table has three columns: the primary key in the table being tracked, the wallclock timestamp, and an indicator of whether the change was due to an insert, update, or delete. Every change in the table being tracked is recorded by rules and triggers that insert a corresponding row in the delta table.

This is what the delta table for “orders” looks like (simplified a bit for readability):

```sql
                      Table "public.orders_delta"
    Column     |     Type    |                Modifiers 
---------------+-------------+-----------------------------------------
 delta_key     | varchar(14) | not null
 delta_action  | char(1)     | not null
 last_modified | timestamp   | not null default timeofday()::timestamp
Check constraints:
    "delta_action_valid" CHECK (delta_action IN ('I','U','D'))
Triggers:
    orders_delta_last_modified BEFORE INSERT OR UPDATE ON orders_delta
        FOR EACH ROW EXECUTE PROCEDURE update_last_modified()
```

The new row data itself in the tracked table is not copied, because the data is right there for the taking. It is enough to note that a change was made. If multiple changes are made, only the most recent version of the row is available, but that is fine because that’s the only one we need to replicate.

Because nothing outside of the database is required to track changes, the tracking continues even when Bucardo 1 is not running. As long as the delta table exists and can be written to, and the tracking rules and triggers are in place on the tracked table, the changes will be recorded.

Bucardo 1 achieves atomicity and isolation of the replication transaction with this process:

1. Open a connection to the first database, set transaction isolation to serializable, and disable triggers and rules.

1. Open a connection to the second database, set transaction isolation to serializable, and disable triggers and rules.

1. For each table to be synchronized in this group:

    1. Verify that the table’s column names and order match in the two databases.

    1. Walk through the delta table on the first database, making identical changes to the second database. Empty the delta table when done.

    1. Walk through the delta table on the second database, making identical changes to the first database. Empty the delta table when done.

    1. Make a note of any changes that were made to the same rows on both databases (“conflicts”). By default, we resolve the conflicts silently by allowing the designated “winner” database’s change be the one that remains. For certain tables such as “inventory”, appropriate table-specific conflict resolution code was added that merged the changes instead of designating a winner and loser version of the row.

1. Once all changes have succeeded, commit transactions on both databases.

This last step of the process does not satisfy the ACID durability requirement. Since Bucardo 1 was designed on PostgreSQL 7.2, with no 2-phase commit possible, there is a chance that one database will fail to commit its transaction after the other database already did, and the changes will be lost on one side only. This has never happened in practice, mostly due to the fact that committing a transaction in PostgreSQL is a nearly instantaneous operation, since the data is already in place and no separate rollback or log tables need to be modified. But it is certainly possible that it could happen, and it is an undesirable risk. With real 2-phase commit now available in PostgreSQL, complete durability could be achieved.

All of a sudden, the changes on each side are now available to the other side, all at once. Only entire orders are visible, never partial orders.

ACID consistency is achieved by assuming that due to PostgreSQL’s integrity checks on the source database, the data was already consistent there, and it is copied verbatim to the destination database where it will still be consistent. Thus, CHECK constraints, referential integrity constraints, etc. are expected to be identical between the two databases. Bucardo 1 does not propagate database schema changes.

Thus the main principles to provide fairly reliable replication are:

1. All related tables must be synchronized within the same transaction.

1. Synchronization must always be done in both directions in the same transaction, so that the code can detect simultaneous change conflicts.

1. The most recent change to a given row must of course be the last change, so changes should be replayed in order. (We optimize this by not copying over row changes that we know will be deleted later in the same transaction.)

Things to consider with multi-master replication:

1. Conflicts are less likely the more often the synchronization is performed. But conflicts can still happen, and must be resolved somehow. Creating a generic conflict resolution mechanism is difficult, but declaring a “winning” database is easy and special conflict resolution logic can be added for certain tables where lost changes would be troublesome.

1. Very large change sets can take a long time to synchronize. For example, consider an unintentionally large update like this:

```sql
UPDATE inventory SET quantity = quantity + 5
```

That may change hundreds of thousands of rows, all in a single transaction. Our replication system need to make all those changes in a single transaction to the other database, but it must do so over a comparatively slow Internet connection. As transactions run longer, they often encounter locks from other concurrent database activity, and rollback. Then the process must start over, but now there are even more changes to copy over, so it takes even longer. In the worst situations, the synchronization simply cannot complete until other concurrent database activity is temporarily stopped, so that no locks will conflict. And that means downtime of applications, and manual intervention of the system administrator.

Perhaps you could ship over all the data to the other database server ahead of time, then begin transactions on both databases and make the changes based on the local copy of the data, and expect the changes to be accepted more quickly since the network is no longer a bottleneck. But the destination database won’t have been idle during that copying, which needs to be accounted for.

Statement replication does not have this same weakness, but it has many weaknesses of its own.

1. Sequences need to be set up to operate independently without collisions on the two servers in a peer sync. Two easy ways to do this are:

    1. Set up sequences to cover separate ranges on each server. For example, MAXVALUE 999999 on the first server, and MINVALUE 1000000 on the second server. Make sure to spread the ranges far enough apart that they’ll never likely collide.

    1. Set up sequences to supply odd numbers on one server, and even on the other. For example, START 1 INCREMENT 2 on the first server, and START 2 INCREMENT 2 on the second server.

1. A primary key is required. Currently, it must be a single column, and must be the first column in the table.

1. Because each table’s primary key may be of a different datatype, and to keep queries on delta tables as simple as possible, Bucardo 1 uses a separate delta table for each table being tracked.

1. A more pluggable system for adding table-specific collision handling would be nice.

1. The delta table column “delta_action” isn’t actually necessary—​inserts and updates are already handled identically, and deletes can be inferred from the join on the tracked table. The “delta_action” is perhaps a nice bit of diagnostic information, and not burdensome as a CHAR(1), but otherwise could be removed.

1. It’s important that the delta table’s “last_modified” column be based on wallclock time, not transaction start time, because we only keep the most recent change, and if all changes within a transaction are tagged by transaction start time, we’d end up with an arbitrary row as the “most recent” one, resulting in inconsistent data between the databases.

### Pushdelta

The pushdelta operation uses the same kind of delta tables and associated triggers and rules that the peer sync uses, but is a one-way push of the changed rows from master to slave. It is useful for large tables that don’t have a high percentage of changed rows.

The pushdelta operation currently only supports a single target database. The ability to use pushdelta from a master to multiple slaves would be useful.

### Push

The push operation very simply copies entire tables from the master to one or more slaves, for each table in a group. It requires no delta tables, triggers, or rules.

Table pushes can optionally supply a query that will be used instead of a bare “SELECT *” on the source table. Any query is allowed that will result in matching columns for the target table. We’ve used this to push out only in-stock inventory, rather than the whole inventory table, for example.

No primary key is required on tables that are pushed out in full.

The push operation uses DELETE to empty the target table. It would be good to optionally specify that TRUNCATE be used instead, and to take advantage of the PostgreSQL 8.1 multi-table truncate feature on tables with foreign key references.

### Compare

The compare operation compares every row of the tables in its group, and displays any differences. It is a read-only operation. It can be used to make sure that tables to be used in multi-master replication start out identical, and later, to verify correct functioning of peer, pushdelta, and push operations.

The compare operation is fairly slow. It reads in all primary keys from both tables first, then fetches each row in turn. It could be made much more efficient.

### Options

Optionally, tables can be vacuumed and/or analyzed after each operation.

In earlier versions of Bucardo 1, there was also an option to drop and rebuild all indexes automatically, to reduce index bloat, but beginning with PostgreSQL 7.3, primary key indexes could not be dropped when foreign keys required them, and the index bloat problem was dramatically reduced in PostgreSQL 7.4, mostly eliminating the need for the feature.

### Limitations

Some of these are limitations that could easily be lifted, but no need had arisen. Some are minor annoyances, and others are major feature requests.

1. For peer, pushdelta, and compare operations, a primary key is required. There are currently limitations on that key:

    1. Only single-part primary keys are supported.

    1. The primary key is assumed to be the first column. It would be easy to allow specifying another column as the primary key, or to interrogate the database schema directly to determine the key column, but we’ve never needed it.

1. If an operation of one type is already underway, other operations of the same type will be rejected. It would be much more convenient for the users to add the newly requested operation to a queue and perform it when the current operation has finished.

1. The program stands alone, performing a single operation and exiting. It was designed to run from cron. A persistent daemon that accepts requests in a queue or by message passing could better handle the many operations needed on a busy server.

1. The program could use PostgreSQL’s LISTEN and NOTIFY feature to learn of changes in a table and run a peer sync based on that notification, instead of being run on a timed schedule or on demand.

1. Delta tables and triggers must be created or removed manually, though our helper script makes that fairly easy. It would be nice to have Bucardo automatically create delta tables and triggers as needed, or remove them when no longer needed (so that the overhead of tracking changes isn’t incurred).

1. Delta tables clutter the schema of the tables they are connected to. PostgreSQL didn’t yet have the schema (namespace) feature when Bucardo 1 was created, but it would be nice to centralize the delta tables and functions in a separate schema.

1. The datatypes of the fields in tables being replicated are not compared; only the names and order are compared.

1. The configuration file syntax is fairly unpleasant.

1. Only tables can be synchronized. It would be good to add support for views, sequences, and functions as first-class objects that could be pushed from master to slave or synchronized between two masters.

1. It would be more convenient, and could reduce the chance of trouble due to misconfiguration, if Bucardo would interrogate the database to learn of all foreign key relationships between tables so that it could automatically create groups of tables that need to be processed together. Trigger functions and rules can cause changes to one table’s row to modify rows in other table(s), in an opaque way that is resistant to introspection, but Bucardo could offer a location for users to declare what other tables a function can affect, and use that in building its dependency tree.

1. There is no unit test suite.

1. The insert trigger and update_last_modified function are written in PL/pgSQL, and are the only dependency on PL/pgSQL. They are both simple functions and should work fine as plain SQL functions, but it seems like there was a reason I had to use PL/pgSQL—​I just can’t remember why anymore.

1. In Bucardo 1, permission to insert to the various delta tables must be granted to any user that would change the base tables, or changes will be prevented by PostgreSQL. For a database with many users of varying access levels, this is a pain. It would be better to define the function to run as SECURITY DEFINER, and create the function as the superuser. Then no explicit permission would need to be granted on any delta table, and the delta tables would be inaccessible except through the Bucardo 1 API (except to the superuser). That would necessitate a change to using functions for updates and deletes, which currently are tracked by rules.

### Future

Bucardo 1 performed admirably for Backcountry.com for over 4 years. The most serious problems, already mentioned above, have been the lack of a queue for push and pushdelta requests, limitations of running one-off processes from cron, limited row collision resolution, and bogging under a large insert or update that happens inside a single transaction.

Greg Sabino Mullane then created Bucardo 2, which is a rearchitected system built around all new code. It has all the important features of Bucardo 1, addressed most of Bucardo 1’s deficiencies, and added many of the desired features listed above. We hope to publish some design notes about Bucardo 2 in the near future.

### The Name

I originally gave Bucardo 1 the fairly descriptive but uninspiring name “sync-tables”. Greg Sabino Mullane came up with the name Bucardo, a reference to the logo of this program’s patron, Backcountry.com. You can read about attempts to clone the extinct bucardo in the Wikipedia articles [Bucardo](https://en.wikipedia.org/wiki/Bucardo) and [Cloning](https://en.wikipedia.org/wiki/Cloning).
