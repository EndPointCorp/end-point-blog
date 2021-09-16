---
author: Jeff Boes
title: PostgreSQL Supports Two-Phase Commit
github_issue_number: 10
tags:
- database
- postgres
date: 2006-05-08
---

The recent release of the 8.1 version of PostgreSQL provides a new feature that offers even more flexibility and scaling for End Point clients. That new feature is the support for "two-phase commit". But what is this feature, and why would you use it?

First, let's explore how database management systems (DBMS) do their jobs. Consider a simple example of editing a file. You open a file with a text editor or word processor. You make some changes. You save those changes. You close the file.

A little more complexity enters the picture if you make some changes, change your mind, and close the file without saving it. Now the file is in the original state. Even more complexity: what if the file is shared between two (or more) users, for instance, by use of a network system with shared drives?

Now we have to consider how the operations on the file occur over time. If Alan opens the file at 9:00 and starts making changes, but Becky opens the same file at 9:05, what file will Becky see? It depends on when Alan saves his changes. If he saves them at 9:04, then Becky sees those changes. If he saves at 9:06, Becky sees the original file.

If Becky is allowed to make changes to that file, what condition will it be in when she is finished? Again, it depends on when Alan saved his changes. If Alan saves at 9:04, Becky's changes will include Alan's. If Alan saves at 9:06, and Becky saves before that, then Becky's changes are lost. In fact, under these circumstances, unless Alan saves before Becky opens, whoever saves first loses: the file will reflect only the changes applied by the last user.

For this reason, modern network systems allow for the locking of files, so that the first user to open the file for editing gains a virtual lock, preventing later users from opening the file (to make changes; most modern network systems allow viewing the file in its pre-locked condition).

The same kind of approach is used by the modern DBMS, but the locking is more complex, as it can affect an entire table, or just one or more records (or rows) in that table. At the risk of over-simplifying: reading a row (or table) locks that row (or table) against alteration, until the reader's transaction (a collection of database operations intended to be performed as a unit) completes. The successful end of a database transaction is called a "commit". It's at this point that changes are "committed" to the database; not only are they no longer under the control of the transaction's owner, but the changes are now "visible" to other users of the DBMS.

Even more complexity enters the picture when two DBMSs must communicate and maintain data consistancy between themselves. This kind of operation is known as a "distributed transaction". The classic example is a transfer of money between two accounts in two different banks. For instance:

- My account at First Bank contains $100.
- Your account at Second Bank contains $50.
- I wish to transfer $25 from my account to yours.

The balance at First Bank is altered by subtracting $25. Then the balance at Second Bank is altered by adding $25. At the end of the transaction, both accounts should contain $75. If the transaction fails at either bank, then my account should contain $100, and yours $50. Any other condition is an error, and gets the bank examiners very excited.

Transactions (in both the database and banking sense of the word!) can be interrupted by many things, but let's take the real-world example of a power interruption. If the power goes off while money is being removed from my account, I'd really like to have that money back in the account when the power goes on. Likewise, if the power goes off while money is being put into your account, that money shouldn't be there when the power is restored.

If the database transaction at First Bank is completed, so the money is out of my account, and the transaction at Second Bank is interrupted, then my money has "vanished", and you didn't get it. If the transaction at First Bank is made to wait until Second's transaction completes, and THEN the power at First goes off, then I'll have an "extra" $75 in my account that shouldn't be there.

All this leads us to conclude that a plain "commit" at one database followed by a plain "commit" at the other is just not sufficient. For this, the concept of a "two-phase commit" evolved.

In a two-phase commit protocol, one of the databases acts as the coordinator for the distributed transaction. It starts the transaction at its side, then sends out a "prepare" message to the other database. The message usually contains a unique "transaction ID" which will appear in all subsequent messages, so the two databases know which distributed transaction to synchronize.

Both the sending and receiving of a "prepare" message means that the associated transaction will be "almost committed": in most DBMSs (and PostgreSQL is consistent here), the transaction will be written out, available after a database interruption to be re-applied.

A two-phase commit allows both databases to keep the details of the transaction on disk, but yet not committed (and thus invisible to other users of the database). When the two databases are each satisifed that the other has a permanent record of the transaction, then they can commit their part. If either side crashes, that database can look through its stored history of "almost committed" data: a sort of "while you were out" record.

For most PostgreSQL installations, in which a single database instance holds all the users' data, the two-phase commit isn't critical. But in larger installations, where data may be distributed (and partially replicated) on two or more platforms, the two-phase commit supplied by PostgreSQL 8.1 keeps everything in sync.
