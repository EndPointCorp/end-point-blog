---
author: Joshua Tolley
gh_issue_number: 375
tags: nagios, postgres
title: check_postgres meets pgbouncer
---



Recently the already well-known PostgreSQL monitoring tool [check_postgres](http://bucardo.org/wiki/Check_postgres) gained an ability to monitor [pgbouncer](http://pgfoundry.org/projects/pgbouncer/), the PostgreSQL connection pooling daemon more closely. Previously check_postgres could verify pgbouncer was correctly proxying connections, and make sure its settings hadn't been modified. The pgbouncer [administrative console](http://pgbouncer.projects.postgresql.org/doc/usage.html#toc5), reports many useful pgbouncer statistics and metrics; now check_postgres can monitor some of those as well.

pgbouncer's description of its pools consists of "client" elements and "server" elements. "Client" refers to connections coming from clients, and "server" to connections to the PostgreSQL server. The new check_postgres actions pay attention only to the pgbouncer "SHOW POOLS" command, which provides the following metrics:

- **cl_active**: Connections from clients which are associated with a PostgreSQL connection. Use the *pgb_pool_cl_active* action.
- **cl_waiting**: Connections from clients that are waiting for a PostgreSQL connection to service them. Use the *pgb_pool_cl_waiting* action.
- **sv_active**: Connections to PostgreSQL that are in use by a client connection. Use the *pgb_pool_sv_active* action.
- **sv_idle**: Connections to PostgreSQL that are idle, ready to service a new client connection. Use the *pgb_pool_sv_idle* action.
- **sv_used**: PostgreSQL connections recently released from a client session. Use the *pgb_pool_sv_used* action.
- **sv_tested**: PostgreSQL connections in process of being tested. Use the *pgb_pool_sv_tested* action.
- **sv_login**: PostgreSQL connections currently logging in. Use the *pgb_pool_sv_login* action.
- **maxwait**: The length of time the oldest waiting client has been waiting for a connection. Use the *pgb_pool_maxwait* action.

Most installations probably don't want any client connections stuck waiting for PostgreSQL connections to service them, meaning the cl_waiting and maxwait metrics ought to be zero. This example will check those two metrics and complain when they're nonzero, for a pgbouncer installation on port 5433 with pools "pgbouncer" and "maindb":

```nohighlight
postgres@db:~$ ./check_postgres.pl --action=pgb_pool_cl_waiting -p 5433 -w 3 -c 8
POSTGRES_PGB_POOL_CL_WAITING OK: (port=5433) pgbouncer=0 * maindb=0 | time=0.01 time=0.01

postgres@db:~$ ./check_postgres.pl --action=pgb_pool_maxwait -p 5433 -w 5 -c 15 
POSTGRES_PGB_POOL_MAXWAIT OK: (port=5433) pgbouncer=0 * maindb=0 | time=0.01 time=0.01
```

The typical check_postgres filtering rules will work; to filter out a pool called "ignore_this_pool", for instance, add --exclude ignore_this_pool to the command line. Other connection options mean exactly what they would when connection to PostgreSQL directly.

These new actions are available in the [latest version from git](http://github.com/bucardo/check_postgres/blob/master/check_postgres.pl).


