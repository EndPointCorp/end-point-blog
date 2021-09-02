---
author: Greg Sabino Mullane
title: Using cron and psql to transfer data across databases
github_issue_number: 95
tags:
- postgres
date: 2009-02-01
---



I recently had to move information from one database to another in an automatic function. I centralized some auditing information such that specific information about each database in the cluster could be stored in a single table, inside a single database. While I still needed to copy the associated functions and views to each database, I was able to make use of the new [“COPY TO query”](https://www.postgresql.org/docs/current/interactive/sql-copy.html)feature to do it all on one step via cron.

At the top of the [cron script](/blog/2008/12/best-practices-for-cron), I added two lines defining the database I was pulling the information from (“alpha”), and the database I was sending the information to (“postgres”):

```
PSQL_ALPHA='/usr/bin/psql -X -q -t -d alpha'
PSQL_POSTGRES='/usr/bin/psql -X -q -t -d postgres'
```

From left to right, the options tell psql to not use any psqlrc file found (-X), to be quiet in the output (-q), to print tuples only and no header/footer information (-t), and the name of the database to connect to (-d).

The cron entry that did the work looked like this:

```
*/5 * * * * (echo "COPY audit_mydb_stats FROM STDIN;" && $PSQL_ALPHA -c "COPY (SELECT *, current_database(), now(), round(date_part('epoch'::text, now())) FROM audit_mydb_stats()) TO STDOUT" && echo "\\.") | $PSQL_POSTGRES -f -
```

From right to left, the command does this:

- Run once every five minutes.
- Take the entire output of the first parenthesized command and pipe it to the second command.
- We build a complete COPY command to feed to the second database.

        - First, we echo the line that tells it where to store the data (COPY ... FROM STDIN)
        - Next, we run the ‘COPY TO’ command on the first database, which, instead of dumping a table, outputs the results of a function, plus three other columns indicating the current database, the current time and the current time as an epoch value.
        - After all the data is dumped out, we echo a “backslash dot” to indicate the end of the copied data

- All of this is now piped to the second database by calling psql with a -f argument, indicating that we are reading from a file. In this case, the file is stdin via the newly opened pipe, indicated by a single dash after the -f argument. li

This allowed me to simply move the data from one database to the other, with a transformation in the middle, neatly avoiding any need to make changes on either the functions output or the columns on the target table.


