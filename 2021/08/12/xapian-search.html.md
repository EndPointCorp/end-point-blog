---
author: "Marco Pessotto"
title: "Xapian"
tags:
- search
- xapian
---

Over the years I've seen and implemented different full-text search
solutions in different installations: plain SQL-based ones,
[PostgreSQL-based](https://www.postgresql.org/docs/13/textsearch.html),
[Elastic Search](https://www.elastic.co/elasticsearch/),
[Solr](https://solr.apache.org/) and finally
[Xapian](https://xapian.org/).

While Solr and Elastic are very well known, Xapian, despite the fact
that it's available and packaged in all the major GNU/Linux
distributions, doesn't seem to be so famous, at least not among the
project managers.

But Xapian is fast, advanced, can be configured to do faceted search
(so the user can filter the search results), and, my favorite, is fast
to build and has virtually no maintenance overhead.

Its main feature is that it's not a stand-alone application, like Solr
or Elastic Search, but instead it's a library written in C++ which has
bindings for all the major languages (as advertised on its homepage).
It has also great [documentation](https://github.com/xapian/xapian-docsprint).

Now, being in the e-commerce business, my typical use-case is that the
client's shop needs something more fast and advanced than a search
with an SQL query in the products table. And beware, even implementing
a non-trivial SQL-based search could burn more hours than setting up
Xapian.

With Xapian you can prototype very quickly, without losing hours in
a gazillion of obscure options, and still you have something which you
can build upon all the features a typical full-text search needs.



















