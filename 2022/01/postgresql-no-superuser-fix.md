---
author: "Jon Jensen"
title: "Fixing a PostgreSQL cluster that has no superuser"
date: 2022-01-07
tags:
- postgres
- security
- tips
github_issue_number: 1819
---

![Stone building with arched windows, a tower, steps leading up, and lush lawn, flowers, and trees](/blog/2022/01/postgresql-no-superuser-fix/20210721-081257-sm.jpg)

<!-- photo by Jon Jensen -->

Normally in a newly-created PostgreSQL database cluster there is a single all-powerful administrative role (user) with "superuser" privileges, conventionally named `postgres`, though it can have any name.

After the initial cluster setup you can create other roles as needed. You may optionally grant one or more of your new roles the superuser privilege, but it is best to avoid granting superuser to any other roles because you and your applications should generally connect as roles with lower privilege to reduce the risk of accidental or malicious damage to your database.

### Let's break something 😎

Imagine you have a cluster with two or more superuser roles. If you accidentally remove superuser privilege from one role, you can simply connect as the other superuser and re-grant it.

But if you have a cluster where only the single `postgres` role is a superuser, what happens if you connect as that role and try to remove its superuser privilege?

```plain
$ psql -U postgres postgres
psql (14.1)
Type "help" for help.

postgres=# \du
                       List of roles
 Role name |            Attributes             | Member of
-----------+-----------------------------------+-----------
 postgres  | Superuser, Create role, Create DB | {}
 somebody  | Create DB                         | {}

postgres=> \conninfo
You are connected to database "postgres" as user "postgres" via socket in "/tmp" at port "5432".
postgres=# ALTER ROLE postgres NOSUPERUSER;
ALTER ROLE
postgres=# \du
                 List of roles
 Role name |       Attributes       | Member of
-----------+------------------------+-----------
 postgres  | Create role, Create DB | {}
 somebody  | Create DB              | {}

postgres=# ALTER ROLE postgres SUPERUSER;
ERROR:  must be superuser to alter superuser roles or change superuser attribute
postgres=# \q
```

PostgreSQL happily lets us do that, and now we have **no** superuser, and so we cannot re-grant the privilege to that role or any other!

### Homebrew PostgreSQL problem

Aside from such a severe operator error, there are other situations where you may find no superuser exists. One happened to me recently while experimenting with PostgreSQL installed by Homebrew on macOS.

I used Homebrew to install `postgresql@14` and later noticed that it left me with a single role named after my OS user, and it was not a superuser. It couldn't even create other roles. I'm not sure how that happened, perhaps somehow caused by an earlier installation of `postgresql` on the same computer, but so it was.

Since there wasn't any data in there yet, I could have simply deleted the existing PostgreSQL cluster and created a new one. But in other circumstances there could have been data in there that I needed to preserve, which wasn't accessible to my one less-privileged user, and which caused errors in `pg_dumpall`.

So how can we solve this problem the right way?

### First, stop the server

We need to get lower-level access to our database. To do that, first we stop the running database server.

On a typical modern Linux server running systemd, that looks like:

```plain
# systemctl stop postgresql-14
```

On macOS using Homebrew services, that could be:

```plain
$ brew services stop postgresql
```

Or in my experimental case with Homebrew using a temporary Postgres server which I'm showing here:

```plain
$ pg_ctl -D /opt/homebrew/var/postgresql@14 stop
waiting for server to shut down.... done
server stopped
```

### Next, start the PostgreSQL stand-alone backend

Next we start the "stand-alone backend" which a single user can interact with directly, not using a separate client.

No privilege checks are done here, so we can re-grant the superuser privilege to our `postgres` role.

Interestingly, SQL statements entered here end with a newline, no `;` needed, though adding one doesn't hurt. And statements here can't span multiple lines without being continued with `\` at the end of each intermediate line.

In the command below, note that the `--single` option must come first, and the `postgres` at the end of the command is the name of the database we want to connect to:

```plain
$ postgres --single -D /opt/homebrew/var/postgresql@14 postgres

PostgreSQL stand-alone backend 14.1
backend> ALTER ROLE postgres SUPERUSER
2022-01-07 20:32:51.321 MST [27246] LOG:  statement: ALTER ROLE postgres SUPERUSER

2022-01-07 20:32:51.322 MST [27246] LOG:  duration: 1.242 ms
backend>
```

The `postgres` server stand-alone prompt does not have all the niceties of `psql` including line editing features, history, and backslash metacommands such as `\q` to quit, so we type control-D there to mark "end of file" on our input stream and exit the program.

### Back to normal

Now we can again start the normal multi-user client/​server PostgreSQL service:

```plain
$ pg_ctl -D /opt/homebrew/var/postgresql@14 start
waiting for server to start.... done
server started
```

And finally we can connect to the server and confirm our change persisted:

```plain
$ psql -U postgres postgres
psql (14.1)
Type "help" for help.

postgres=# \du
                       List of roles
 Role name |            Attributes             | Member of
-----------+-----------------------------------+-----------
 postgres  | Superuser, Create role, Create DB | {}
 somebody  | Create DB                         | {}

postgres=#
```

### Reference

* [PostgreSQL single-user mode](https://www.postgresql.org/docs/current/app-postgres.html#APP-POSTGRES-SINGLE-USER)
* [PostgreSQL ALTER ROLE documentation](https://www.postgresql.org/docs/current/sql-alterrole.html)
