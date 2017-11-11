---
author: Josh Williams
gh_issue_number: 1270
tags: postgres, replication
title: 'Throw It Away: Suppressing Writes on PostgreSQL Replicas'
---

We needed a way to suppress specific write commands on a Postgres streaming replica. The replica was set up for a DR configuration, with the applications able to be brought up into full service at a moment's notice. But since it's a hot standby, we'd like to still allow the applications to be used in a working but read-only state.

One of the applications on this database is MediaWiki, which worked great in this configuration. But a couple of the other apps have the classic behavior of updating its user object's "last login" field in one form or another when someone authenticates, which would cause the login process to fail entirely.

Of course we want updates to fail, up until that point when (knock on wood) the master server is declared down for the count and the official fail-over happens. Except for the one command that executes on login.

We don't really care about the "last login" type field -- the data is available through logs and other means. The affected apps could probably all be monkey patched to work around that part of the process. But we had a couple different apps doing this, and that adds a maintenance burden for each. And if we could figure out how to make it work at the database level then it'd work for all of them, plus anything else that might pop up.

The first thing we looked at was writing a trigger to intercept the commands, but triggers don't execute on a hot standby replica so that was out pretty quickly. The next hypothesis was that we could write a foreign data wrapper that'd just absorb the writes, or even just use postgres_fdw to route the commands to a local writable database that's more or less a throw-away data sink. But to our surprise, even writes to foreign tables get rejected on a hot standby. I'm slightly tempted to dig in and see what it'd take to enable that.

The third time was the charm: [rules](https://www.postgresql.org/docs/current/static/rules.html). Rules hook in pretty far down into the query parser, and they can be notoriously tricky to work with. But since they're embedded pretty deep, down to the point where [views rely on them](https://www.postgresql.org/docs/current/static/rules-views.html) they're obeyed even on a replica.

So the technique was this: On the master (... obviously) we set up a separate schema, inside which a view was created with the same name as the target table and which had certain commands suppressed:

```sql
CREATE SCHEMA replica;

CREATE VIEW replica.users AS SELECT * FROM public.users;

CREATE RULE users_disable_update AS ON UPDATE TO replica.users DO INSTEAD NOTHING;
```

Plus any permission adjustments the app user might need. On the master server this schema and view are pretty much ignored, as the application user just uses the default search path. But on the replica, we adjust the default search path in postgresql.conf so that it applies to just that server:

```nohighlight
search_path = '"$user",replica,public'
```
```sql
app@app:5432=> UPDATE "auth_user" SET "last_login" = now() WHERE "auth_user"."id" = 13;
UPDATE 0
```

It doesn't quite work everywhere, sadly! Notice the "UPDATE 0"? We found Django actually checks that, and panics with an error to the user when it tries to change something and the row count it gets back is different than what it expects.

Another caveat is that if the target table's schema changes, the view won't automatically follow. Presumably your user table doesn't receive changes all that often, but if you're applying this technique to something else, that might not be the case. Something to be aware of!
