---
author: Jon Jensen
gh_issue_number: 361
tags: conference, scalability
title: Surge 2010 wrap-up
---

Following up on my earlier post about [day 1 of the conference](/blog/2010/10/01/surge-2010-day-1), here is an unsorted collection of what I felt were noteworthy observations made in talks at [Surge 2010](http://omniti.com/surge/2010):

Web engineering as a separate discipline from computer science or software development started around 1999. It is interdisciplinary, involving [human factors engineering](http://en.wikipedia.org/wiki/Human_factors_engineering), [systems engineering](http://en.wikipedia.org/wiki/Systems_engineering), [operations research](http://en.wikipedia.org/wiki/Operations_research), [fault-tolerant design](http://en.wikipedia.org/wiki/Fault-tolerant_design), and [control systems engineering](http://en.wikipedia.org/wiki/Control_Systems_Engineering). (John Allspaw)

A real-time system is one in which the correctness of a system is tied to its timeliness. Eventual consistency is an oxymoron if timeliness is part of the data itself. Caching by CDNs can't solve our problems here. (Bryan Cantrill)

Pre-fab metrics are worth less (and maybe worthless) when not tied to something in your business. Message queues enable lots of new uses because of the ability to have multiple observers. See [Esper](http://www.espertech.com/) (Java, GPL) for live ongoing SQL-like queries of messages from AMQP sources, etc. (Theo Schlossnagle)

On scaling up vs. out: If your numbers show "up" is enough, be happy you can keep your system simpler. (Theo Schlossnagle)

Anyone can only ever know the past in a distributed system. There's no such thing as global state in reality. Our systems are always at least slightly inconsistent with the world. "Eventually consistent" just acknowledges the reality of delay and focuses on measuring and dealing with that. (Justin Sheehy)

Reliability compared to resiliency: Being resilient means success of your mission despite partial failure of components. How do you deal with failure? Degrade, and know before your users do. (Justin Sheehy)

Build in monitoring during development, so it's not a bottleneck right before deployment. (John Allspaw)

Data comes from the devil. Models come from God. Data + Models = Insight. Data needs to be put in a prison (a model) and made to confess the truth. Measurement is a process. Numbers aren't right. What is the error range? Visualization is helpful, but analyze the raw data looking for anomalies (such as > 100% efficiency, etc.). VAMOOS = visualize, analyze, modelize, over & over till satisfied. (Neil Gunther)

Anycast for DNS alone tends to localize on the user's recursive resolver, not their actual location. Anycast for the actual content delivery automatically localizes on the user's actual location. (Tom Daly)

To scale up, add more capacity to do X, make system do X faster, or stop doing so much X. What makes a task take time? It's utilizing a resource, it's waiting for a response, or it's waiting for synchronization. "Shard early & often" is expensive & unnecessary for most situations. Sharding makes sense when write demand exceeds capacity. (Baron Schwartz)

[Eight fallacies of distributed computing](http://en.wikipedia.org/wiki/Fallacies_of_Distributed_Computing) were discussed by Ruslan Belkin.

Mike Mallone of SimpleGeo gave a fascinating talk on [working with geolocation data in Cassandra](http://omniti.com/surge/2010/speakers/mike-malone). It'd be wonderful to see an open source release of their order-preserving partitioner that allows for range queries in a single dimension. Or to start with, just the slides from Mike's talk!

In summary, it was a very good conference!
