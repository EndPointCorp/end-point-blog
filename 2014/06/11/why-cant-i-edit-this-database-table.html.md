---
author: Mark Johnson
gh_issue_number: 994
tags: database, mysql
title: Why Can't I Edit this Database Table? Don't Forget the Client!
---

A client of mine recently informed me of an issue he'd been having for years, where he was unable to edit a single table in his database. He uses Access to connect to a MySQL database via ODBC, and his database has a few dozen tables, all of which are editable except this one. He reports that, when trying to edit just this one table, putting the cursor into any of the fields and attempting to change any of the data is blocked. As he put it, "It's like the keyboard won't respond."

We confirmed through conversation that the issue was not a MySQL permissions problem--not that I would have expected MySQL permissions to result in such client behavior. We also confirmed that, when using a different application to connect to MySQL with Perl's DBI, the table was editable just as the rest of the database. At this point, I didn't have any good suspects (as neither Access nor ODBC are my strong suit) and agreed to bring up the issue with the rest of the End Point engineering team.

After sending out a description of the problem, it wasn't long before [Josh Williams](/team/josh_williams) responded. He had seen this sort of behavior with Access before, where the client will lock out the table if the table does not have a unique key defined. Not surprisingly, it turned out this particular table's implied primary key was in fact a non-unique index. I applied a primary key to the field, dropped the original index, and received confirmation from the client that the table was now editable like the rest of the database.

Setting up your database is a combination of server *and* client behaviors. While most of the focus goes into configuring the server, if you encounter unusual circumstances, don't forget the possibility that a given client may also have requirements impacting actions normally confined to the realm of the server.
