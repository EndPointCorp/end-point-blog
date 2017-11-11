---
author: Greg Sabino Mullane
gh_issue_number: 443
tags: database, performance, perl, postgres
title: Postgres query caching with DBIx::Cache
---



A few years back, I started working on a module named DBIx::Cache which would add a caching layer at the database driver level. The project that was driving it got put on hold indefinitely, so it's been on my long-term todo list to release what I did have to the public in the hope that someone else may find it useful. Hence, I've just released version 1.0.1 of DBIx::Cache. Consider it the closest thing Postgres has at the moment for query caching. :) The canonical webpage:

```nohighlight
http://bucardo.org/wiki/DBIx-Cache
```

You can also grab it via git, either directly:

```bash
git clone git://bucardo.org/dbixcache.git/
```

or through the indispensable github:

```nohighlight
https://github.com/bucardo/dbixcache
```

So, what does it do exactly? Well, the idea is that certain queries that are either repeated often and/or are very expensive to run should be cached somewhere, such that the database does not have to redo all the same work, just to return the same results over and over to the client application. Currently, the best you can hope for with Postgres is that things are in RAM from being run recently. DBIx::Cache changes this by caching the results somewhere else. The default destination is memcached.

DBIx::Cache acts as a transparent layer around your DBI calls. You can control which queries, or classes of queries get cached. Most of the basic DBI methods are overridden so that rather than query Postgres, they actually query memcached as needed (or other caching layer - could even query back into Postgres itself!). Let's look at a simple example:

```perl
use strict;
use warnings;
use Data::Dumper;
use DBIx::Cache;
use Cache::Memcached::Fast;

## Connect to an existing memcached server, 
## and establish a default namespace
my $mc = Cache::Memcached::Fast-&gt;new(
  {
    servers   =&gt; [ { address =&gt; 'localhost:11211' } ],
    namespace =&gt; 'joy',
  });

## Rather than DBI-&gt;connect, use DBIx-&gt;connect
## Tell it what to use as our caching source
## (the memcached server above)
my $dbh = DBIx::Cache-&gt;connect('', '', '',
  { RaiseError =&gt; 1,
    dxc_cachehandle =&gt; $mc
});

## This is an expensive query, that takes 30 seconds to run:
my $SQL = 'SELECT * FROM analyze_sales_data()';

## Prepare this query
my $sth = $dbh-&gt;prepare($SQL);

## Run it ten times in a row.
## The first time takes 30 seconds, the other nine return instantly.
for (1..10) {
    my $count = $sth-&gt;execute();
 my $info = $sth-&gt;fetchall_arrayref({});
    print Dumper $info;
} 
```

In the above, the prepare($SQL) is actually calling the DBIx::Class::prepare method. This parses the query and tries to determine if it is cacheable or not, then stores that decision internally. Regardless of the result, it calls DBI::prepare (which is techincally DBD::Pg::prepare), and returns the result.The magic comes in the call to execute() later on. As you might imagine, this is also actually the DBIx::Class::execute() method. If the query is not cacheable, it simply runs it as normal and returns. If it is cacheable, and this is the first time it is run, DBIx::Class runs an EXPLAIN EXECUTE on the original statement, and parses out a list of all tables that are used in this query. Then it caches all of this information into memcached, so that subsequent runs using the same list of arguments to execute() don't need to do that work again.

Finally, we come to fetchall_arrayref(). The first time it is run, we simply call the parent methods and get the data back. Then we build unique keys and store the results of the query into memcached. Finally, we mark the execute() as fully cached. Thus, on subsequent calls to execute(), we don't actually execute anything on the database server, but simply return the count as stashed inside of memcached (in the case of execute, this is the number of affected rows). For the various fetch() methods, we do the same thing - rather than fetch things from the database (via DBI, DBD::Pg, and libpq), we get the results from memcached (frozen via Data::Dumper), and then unpack and return them. Since we don't actually need to do any work against the database, everything returns as fast as we can query memcached - which is in general very fast indeed.

Most of the above is working, but the piece that is not written is the cache invalidation. DBIx::Cache knows which tables go to which queries, so in theory you could have (for example), an UPDATE/INSERT/DELETE trigger on table X which calls DBIx::Cache and tells it to invalidate all items related to table X, so that the next call to prepare() or execute() or fetch() will not find any memcached matches and re-run the whole query and store the results. You could also simply handle that in your application, of course, and have it decide when to invalidate items.

It's been a while since I've really looked at the code, but as far as I can tell it is close to being able to actually use somewhere. :) Patches and questions welcome!


