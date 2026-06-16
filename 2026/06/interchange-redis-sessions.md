---
author: "Mark Johnson"
title: "Interchange Redis Sessions"
description: "Interchange 5.12 can now store user sessions in Redis for better performance on busy catalogs—with optional compression, atomic locking, and built-in resistance to bot-driven session bloat."
featured:
  image_url: /blog/2026/06/interchange-redis-sessions/cover.webp
date: 2026-06-16
github_issue_number: 2191
tags:
- interchange
- redis
- performance
- ecommerce
---

![An eastern bluebird with a rust-orange breast and blue-gray head perched on a bare branch, set against a soft blue sky with white clouds.](/blog/2026/06/interchange-redis-sessions/cover.webp)<br>
Photo by Josh Ausborne, 2022.

Interchange[^1] now supports storing user sessions in Redis[^2], an in-memory data store, as a core feature of Interchange 5.12. Sessions are where Interchange keeps client state that makes a catalog operate as a continuous experience--the shopping cart, form values, login status, and other data that persist from one request to the next. How and where that state is stored have a direct impact on a busy catalog's performance, and Redis gives developers a fast, purpose-built option that sits alongside the storage backends Interchange has always offered.

### Session storage in Interchange

By default, Interchange writes each session to a file on disk, and it has long been able to store sessions in a relational database instead by way of `Vend::SessionDB`, configured with the `SessionType DBI` and `SessionDB` directives. The database approach is the natural choice once a catalog is served by more than one Interchange server, since every server needs to read and write the same pool of sessions.

Relational databases certainly can function in this capacity, but a high-traffic session table is not where they shine. Every page view reads, writes, and locks a session row, and that constant churn competes with database performance for the application. Redis is built precisely for this kind of small, hot, frequently updated key/value data, and that makes it a compelling choice for session storage.

### Using Redis for sessions

Enabling Redis sessions takes two directives in your catalog's `catalog.cfg`. Set `SessionType` to `Redis`, and point `SessionDB` at the address and port of your Redis server:

```
Variable REDIS_SERVER 127.0.0.1:6379
SessionType Redis
SessionDB   __REDIS_SERVER__
```

That is the whole of the required configuration. Behind the scenes, the new `Vend::SessionRedis` module ties Interchange's session storage to Redis through the standard Redis CPAN module[^3], so Redis and that module must be installed and reachable from your Interchange host.

Redis sessions also work optionally with the session compression recently introduced.[^4] If you set `SessionDBCompression` to a viable compression algorithm, session data is compressed on the way into Redis and decompressed on the way out, exactly as it is for database sessions:

```
SessionDBCompression Zstd
```

### More lists and MoreDBTable

Some catalogs use Interchange's MoreDB feature to cache search-result sets ("more" lists) into the session database rather than writing to files on disk. This feature is often leveraged for the same reason that `SessionDB` is used: to support a distributed, load-balanced server environment. `MoreDB` relies on a real database table, and Redis--having no support in Interchange's database abstraction layer--cannot provide one. To bridge that gap, there is a new `MoreDBTable` directive that tells `MoreDB` which relational table to use for more lists, independent of where sessions themselves live:

```
MoreDB yes
ifdef REDIS_SERVER
   include dbconf/__SESSIONDB_ENGINE__/sessions.__SESSIONDB_ENGINE__.__MOREDB_EXT__
   MoreDBTable sessions
endif
```

When you run Redis sessions together with `MoreDB`, `MoreDBTable` is required. Without Redis it remains optional: `MoreDB` falls back to `SessionDB` just as it always has. The strap demo ships ready-made schema definitions for MySQL, PostgreSQL, and SQLite, so the supporting table is created with the right column types.

### Locking and a friendlier welcome for bots

Concurrent requests for the same session have to be serialized so two clicks don't trample each other's data. For this release, the RDBMS session backend was reworked to lock session records with proper database transactions rather than the old approach of inserting and deleting lock rows. Redis gets its own locking scheme built on Redis's atomic `SETNX` ("set if not exists") operation, exposed through a new `has_lock()` method. The mechanism is general enough that any other storage system able to offer the same primitive--Memcached, for example--could adopt it.

Redis sessions add one more practical refinement. Automated crawlers generate an enormous number of "hit and run" sessions that are created once and never used again, and on a database-backed catalog they pile up until something prunes them. `Vend::SessionRedis` instead gives every brand-new session a fixed 30-minute expiration. A human user comfortably makes a second request within that window, at which point the session is promoted to the full lifetime set by your `SessionExpire` directive. A bot that never returns simply expires on its own quickly, limiting data bloat, and Redis reclaims the memory without any housekeeping on your part.

### Wrapping up

Redis sessions give Interchange developers a fast, horizontally scalable place to keep session state, with optional compression, a robust locking model, and built-in resistance to bot-driven session bloat--all configured with a couple of lines in `catalog.cfg`. As with the rest of Interchange, the implementation lives in core and is open for the community to extend; the `has_lock()` interface in particular invites support for additional storage backends.

### References

[^1]: [Interchange - https://www.interchangecommerce.org](https://www.interchangecommerce.org)
[^2]: [Redis - https://redis.io/](https://redis.io/)
[^3]: [Perl's Redis module on CPAN - https://metacpan.org/pod/Redis](https://metacpan.org/pod/Redis)
[^4]: [Interchange Compression for SessionDB](https://www.endpointdev.com/blog/2025/04/interchange-compress-sessiondb/)
