---
author: Ethan Rowe
gh_issue_number: 246
tags: scalability
title: Common Topics in Scalability
---

It rarely makes sense for a startup business to tackle scalability questions from the outset, because it raises the cost and complexity of development and operational support, while solving problems that a start-up business doesn't typically yet need solved (i.e. handling tons of users). From a cost-effectiveness perspective, it makes sense to solve these problems when the need is actually evident.

That said, systems can be designed with scalability in mind such that the system easily lends itself to incremental changes that scale up its capacity.

The basic principles and techniques that typically come up in scalability discussions:

- **horizontal scalability**: a particular component is "horizontally scalable" if you can deploy redundant instances of that component in parallel; this is the ultimate scalability win, as it means you can readily add raw processing power for that component at low cost.

- **vertical scalability**: the practice of increasing a single component's power/capacity to improve performance/throughput is referred to as "vertically scaling" that component. From the layperson's perspective, this is the most easily-understood technique, as it effectively amounts to buying a faster server, adding RAM to an existing server, etc.

- **caching**: caching can be about raw speed, but is more important from a scalability perspective; caches reduce the overall work a system needs to do for any given request, and can simplify the overall request to entirely eliminate the overhead of multiple-component involvement (for instance, a cache in the application layer can potentially eliminate any calls to the database for a given request)

Horizontal scalability brings the biggest win in terms of potential system capacity, as it allows you to handle increased demand (whether that demand is visitors, orders, etc.) through the simple means of adding more servers to your infrastructure. Virtualization and, its logical result, cloud hosting make this kind of infrastructure expansion simpler and often more cost-effective than ever before.

Some examples of horizontal scalability:

- Running your appserver (Rails, Django, etc.) on multiple servers, with a load balancer distributing traffic more-or-less evenly across those servers

        - The entire application tier is scaled horizontally and can expand/contract as needed.

        - Session management becomes an issue; sessions either get moved to a shared component like the database, or server affinity techniques are used with the load balancer such that a single client/user always hits the same application server, so sessions can be file-based on each app server.

        - The database likely becomes the bottleneck for system capacity and performance.

- Master/slave database replication, with multiple slave databases fronted by a load balancer distributing database reads across the slaves.

        - Database reads, which in typical webapps account for the bulk of database queries, can be spread across multiple servers and are thus scaled horizontally.

        - The total number of slave databases is likely limited by the capacity of the master; each additional slave adds some overhead to the master, so diminishing returns eventually kick in.

The ease with which a given component can be scaled horizontally largely comes down to how it manages state, or, in other words: how it manages the data that it works with.

Application servers are generally designed to be "stateless", which effectively means that the response for a given request is not dependent on a previous request (though the idea of the "session" is obviously a big exception here). Due to this stateless nature, it's usually cheap and easy to run your application server in a horizontally-scalable configuration.

By contrast, relational databases are all about state: the entire point of the database is to act as the arbiter of state, maintain that data on disk, and answer questions about that data. We typically expect the database to tell the truth and give a consistent answer about each piece of data. The consistency expectation leads to the need for each piece of data to have one and only one canonical location, which means it cannot be scaled across multiple servers. You can scale *copies* of data across multiple servers (as done in master/slave replication), but the True Value for a bit of state has to live in one place. Therefore, master databases are generally cut off from the glories of horizontal scalability. (Note: "sharding" offers a way to scale writes, but it doesn't make your database literally horizontally scalable; any given datum still has one canonical location which is limited to vertical scalability per usual).

Enter caching. When you cannot horizontally scale a given component, you can instead store and reuse copies of the results of that component's operations, to reduce the overall work done by that component. Most modern application server frameworks provide a variety of helpful caching tools right out of the box, and a good cache strategy can squeeze a great deal of throughput out of a simple architecture. However, caching is bigger than the app tier, as the examples show:

- **HTTP caching**: HTTP clients (i.e. web browsers) can cache the resources they request from your system, if you give them the proper instructions on how to do so (via various HTTP headers). At a minimum, browsers ought to be able to cache the images, CSS, and JavaScript files that make up your site's large scale visual design, which means they don't need to request those files repeatedly.

- **HTTP caching redux**: HTTP caching reverse proxies (Varnish, Squid, etc.) can sit between your web/app tier and your users' browsers, and can cache resources from your site based on HTTP headers and other configurable aspects; when users request a resource, they hit the HTTP reverse proxy first, and if the resource is available in the cache, the cached version is used. This means the user gets a faster response and your actual application does less work.

- **Page caching**: By caching full copies of your dynamically-generated resources (web pages), your system can see enormous scalability gains. This can fall logically under HTTP caching or under application-tier caching or somewhere between; the important point is to consider the idea that you cache an entire dynamic page in some manner, as it brings both such big performance wins and potential design complexities/constraints.

- **Application tier caching**: using simple file-based caches, or scalable, shared, distributed cache layers like memcached or redis, your application can cache the results of expensive queries, frequently-used operations/widgets, etc. and thus reuse the fruits of its own labors; this can reduce the computational cost for handling any given request and thus improve both raw request speed and overall throughput (scalability).

- **Database replication**: though not typically referred to as "caching", the classic master/slave database replication strategy is effectively a very fancy cache. By pushing out copies of data at near-real-time, this lets your master database server do less work while still giving your application servers highly accurate results.

- **Controlled denormalization**: within your database, you can use triggers and such to manage denormalized data, allowing frequently-used or expensive calculations to be cached as part of the database schema. This allows the application to rely upon such calculations at lower cost. Materialized views fit within this category.

These caching examples/categories vary in complexity of implementation, but they share a common principle: increase system capacity by reusing the system's work. The use of caching naturally involves trade-offs, but in the simple case, a straightforward expiry-based cache can have a dramatic impact on performance. A sluggish webapp can get a second wind by wrapping the most common database-driven components within a timed cache. For new development, for which your caching strategy can factor in at design time, caching can yield great performance/scalability with extremely high accuracy. In particular, the refresh-on-write strategy (in which the code paths in your app responsible for changing state are also responsible for updating related caches) can be a huge scalability win (this was exactly the strategy we used -- with great results -- for Backcountry.com's SteepandCheap site in fall of 2007 and the initial launch of their product Q&A features in early 2008).

Ideally, a good caching strategy does not merely reuse the results of earlier work, but in fact cuts out calls to other services; good caching in the application tier may mean that most requests do not need to involve the database at all; good HTTP caching techniques cut down the number of requests that involve your application server. And so on.

Beyond these topics, scalability benefits can frequently come from:

- **query optimization**: poor database usage can result in slow page load times, excess I/O, and can overload the database unnecessarily; query optimization can have a significant impact there. This is rather like a corollary to vertically scaling your database: your database scales better relative to the hardware because its demands on the hardware are reduced.

- **data management optimization**: big scalability gains can often come from revising the structure of the data involved at the scalability pinch points; for instance, having a single inventory count for a given SKU is a scalability bottleneck compared to having an inventory item record per 1 inventory count per sku. The former results in lock contention in high-order-volume situations, while the latter can minimize such locking and prevent one user's order from blocking another.

- **application database usage**: related to query optimization is the issue of how the application structures its queries. In an age where people increasingly interact with their datasources through an object-relational mapper (ORM), one commonly finds cases in which the application issues per-record queries within a loop, meaning that a set of *N* records yields *N+1* queries (1 query for the initial set, 1 query per iteration). This kind of database usage brings unnecessary I/O overhead and leads to sluggish app performance; rewrite the queries or tweak the ORM as necessary such that the first query loads all the data, or that a second query fetches all the extra data for all members of the first query's result set (ORMs often will do the second strategy for you if you let them know what you want).

The unfortunately-named "NoSQL" movement has a lot of exciting possibilities for systems that need to handle large volumes of data, or scale out to very high write volumes (I find both Cassandra and HBase to be particularly interesting). However, unless you know from the outset that your dataset size or write volume will be pushing the limits of the traditional relational database, or that you need distributed operations for availability purposes, the NoSQL offerings are quite possibly counterproductive.

These solutions typically offer some particular advantage but with a trade-off of some kind; for small businesses with a rapidly-evolving sense of self and the problem space, the traditional RDBMS brings a huge amount of flexibility in how one works with data, as well as a well-understood operational paradigm (for high availability, reliability, backups, etc.). The "Big Data" benefits of NoSQL probably don't apply for such systems and the ease with which RDBMSes handle arbitrarily-complex queries allow the growing business/system to develop iteratively and arrive at a better understanding of the true underlying needs. The trade-offs and such are beyond the scope of these musings, so I just won't give them further consideration here; however, the NoSQL ecosystem is good to know about and certainly can factor into scalability discussions depending on your use cases. Several of them may in fact fit well within a caching strategy, rather than as an authoritative datasource.

Here are some general rules of thumb I would recommend if you want to be ready to scale up when the need arises (as is the whole point of these ramblings):

- *Write well-organized code*: Maintain separation of concerns in your application code, maximize code reuse, and keep your classes, modules, functions, etc. limited in their scope. This keeps each individual code piece simple, maximizes the ease with which things like caching can be introduced, and minimizes the code paths that have to be changed in order to optimize the performance of any given component.

- *Keep your canonical data normalized*: This could probably be stated instead as "model your data relationally", but that assumes an RDBMS, which isn't necessarily your only datastore. In any case, normalized data is easier to manage over the life of a system, and just as better-organized code is more-easily optimized for performance/scalability than poorly-organized code, well-organized data is more-easily rearranged or cached, etc. Introduce denormalization in a targeted, needs-based manner, but don't let that denormalization ever be considered part of your canonical dataset; denormalized data is broken data that you should be able to throw out and rebuild at any time.

- *Avoid session usage*: Sessions are handy, but they in fact violate the statelessness of the application server, introduce one point of complexity (though a manageable point) for horizontal scaling, potentially introduce database scaling problems (if you're using database-backed sessions), etc. If the state matters enough to keep it from one request to the next, consider modeling it and storing it properly in the database. For state that just can't go in the database and you just can't live without...

- *Use the client*: The majority of clients for the majority of webapps are web browsers. Those web browsers typically have storage (cookies for now, and more options coming) and frequently have programming capacity (JavaScript). Use it!  In particular, cookies can take the role of the user session, and potentially eliminate (or at least reduce) the need for server-side session state. Work done by the client is work not done by your servers.

- *Think RESTfully*: While you don't necessarily need to literally design a RESTful application, be mindful of the RESTful design principles and keep your URLs well-designed. Critically, don't allow the same URL to front wildly-varying resources; such resources are the bane of page/HTTP caching.

- *Be mindful of user-specific resources*: Any resource, document, etc. that you serve with user (or session) specific information therein is a resource that is potentially more difficult to cache effectively. Consider crafting your URLs such that the URL is per-user, if that can fit your problem-space effectively (this allows HTTP or page-level caching to still be an option). If common resources (like a "home page") need to show per-user details, consider using the client (cookies, JavaScript) to encapsulate the user-specific stuff such that the common resource itself is identical for all users (and thus also remains open to HTTP or page-level caching).
