---
author: Daniel Browning
gh_issue_number: 69
tags: conference, perl, postgres
title: PostgreSQL Conference West 2008 Report
---

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/26685765114/in/album-72157668881033466/" title="2008-10-12_IMG_9662"><img alt="2008-10-12_IMG_9662" height="465" src="/blog/2008/10/13/postgresql-conference-west-2008-report/image-0.jpeg" width="800"/></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

I attended the PostgreSQL Conference West and had a great time again this year. My photos of the event are [up here](https://www.flickr.com/photos/end-point/sets/72157668881033466/).

In addition, I shot some footage of the event in an attempt to highlight the benefits of the conference, Postgres itself, and the community strengths. I'm looking for a talented Editor willing to donate time; if none volunteer then I'll probably do it in January. My guess is that there will be several web sites willing to host it for free when it's done.

The Code Sprint was really interesting. Selena Deckelmann gave everyone a lot of ideas to get the most out of the time available for hacking code. At regular intervals, each team shared the progress they made and recieved candy as a reward. It was neat to see other people hacking on and committing changes to the Postgres source tree in meatspace.

Bruce Momjian's Postgres training covered a wide gamut of information about Postgres. He polled everyone in the room for their particular needs, which varied from administration to performance, then tailored the training to cover information relating to those needs in particular detail. Those who attended reported that they learned a great deal of new information from the training. From here, a lot of folks went out to continue interacting with Postgres people, but I headed for home.

Windowing Functions were covered by David Fetter in a talk that addressed ways to make OLAP easier with new features coming to Postgres 8.4. Functionality that used to be slow and difficult in client-side applications can be handled easily right in the database. I made a note to check this out when 8.4 hits the streets.

Jesse Young spoke about using Linux-HA + DRBD to build high availability Postgres clusters. It is working very well for him in over 30 different server installations; he proved this by taking down a production server in the middle of the presentation and demonstrating the rapid transition to the failover server. Just set-it-and-forget-it. I was able to weigh the advantages and disadvantages compared to other clustering options such as shared disk (e.g. GFS) and Postgres-specific replication options (Slony, Postgres Replicator, Bucardo, etc.).

In his talk, PostgreSQL Optimizer Exposed, Tom Raney delved into a variety of interesting topics. He described the general workings of the optimizer, then showed a variety of interesting plans that are evaluated for the example query, how each plan was measured for cost, and why the cost varied. He uncovered several interesting facts, such as demonstrating that the Materialization step (pushing sorts to disk that are too large for memory) doesn't increase the cost associated with that plan. Tom Lane explained that this would rarely, if ever, affect real world results, but that is the kind of information made obvious in the Visual Planner, but hidden by textual EXPLAIN ANALYZE. Tom Raney also demonstrated the three-fold difference (in one case) between the cost of the clustered index and the rest. Optimizing query performance is one of my favorite pastimes, so I enjoyed this talk a lot.

I learned a bit about what was going in Postgres community organizations during Joshua Drake's talk, "PostgreSQL - The happening since EAST". The PostgreSQL.US and other organizations are doing a lot to increase awareness of Postgres among education, government, business, and other developers. The point was made that we should do as much as we can to reach out to widely prevalent PHP applications and web hosting providers.

Common Table Expressions (CTE) were given a good explanation by David Fetter in his talk about doing Trees and More in SQL. Having worked on Nested Set and Adjacency List models, I was very interested in this new feature coming to 8.4. Starting with a simple recursive example, David built on it slide-by-slide until he had built and executed a brute force solution to a Traveling Salesman Problem (for a small number of cities in Italy) using only plain SQL. I'm excited to try this out and measure the performance.

Mark Wong & Gabrielle Roth presented the results of testing that they completed. Selena also covered that information in her post about [Testing filesystems and RAID](/blog/2008/09/19/filesystem-io-what-we-presented). After that we talked Perl on the way to the Portland Paramount for the party.

On Sunday, I sat in on "Developing a PL (Procedural Language) for PostgreSQL", by Joshua Tolley, as he carefully explained the parts and steps involved. LOLCODE humor peppered the useful information on the related Postgres libraries, Bison usage, and pitfalls.

I was glad to see Catalyst boosted in Matt Trout's presentation. He very quickly covered the design and advantages of Catalyst, DBIx::Class, and Postgres as they related to the implementation of a high profile and complex web site. It was very informative to see the Class structure for the View model, which gave me several ideas to take use for my own development. He demonstrated how a complex 56-way join was coded in very brief and comprehensible perl code relying on the underlying modules to provide the underlying support. The explain tree is so large that it couldn't fit on the screen even in microscopic font, and even with very large data sets, the Postgres optimizer found a way to return the results in one tenth of a second. Matt also demonstrated several flaws in his design, such as how his use of rules to implement updatable views caused multi-row updates to be slower than the equivalent trigger-based system. I use Catalyst for several projects, but I think Interchange still has more advantages. I'm definitely going to take another look at DBIx::Class.

Before lunch, I asked if I could shoot a group photo, so we went to the park. Several people were not in attendance, and I didn't want to take more than a minute or two, so the shots are not as good as I would have liked. Next time I'll ask if we can plan some time for arranging the group. At lunch I had a great time talking to fellow Postgres developers and learning more about their work.

Lightning Talks followed lunch and included a variety of interesting topics. One of my favorites was "I can't do that" by Matt Trout. He explained how wrong it is to believe you can't contribute something to Postgres or any other open source project. If you think your code will be incomplete or buggy, do it anyway, because it may prompt someone else to work on it, or scrap yours and do it right. Don't think you can't contribute to documentation because of your infamiliarity with the system, because that's exactly the advantage you have for documentation contributions: those who need the docs are in exactly your shoes.

Matt also gave the closing talk, "Perl 5 is Alive!", which was a concise, water-tight presentation of Perl 5's superiority over other development environments, including CPAN and job statistics that demonstrate its growing popularity.

Some attendees went out afterwards to finish the conference over a drink. I slept about 11 hours straight to recover from the whirlwind of weekend activity. Overall I'm grateful for the opportunity to interact with the community again and I'm excited for what the future has in store for Postgres.
