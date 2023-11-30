---
author: Jon Jensen
title: PostgreSQL 8.1 Shows Database Progress
github_issue_number: 5
tags:
- database
- postgres
date: 2005-11-14
---

At End Point we recommend [PostgreSQL](https://www.postgresql.org/) for most of our database-backed software development due to its powerful features, reliability, speed, and liberal license. On November 8, 2005, PostgreSQL 8.1 was released, and it offers a number of useful new features, including:

- Two-phase commit (transactions across distant servers).

- Numerous new SQL features (regexp_replace function; indexed MIN and MAX aggregates; SQL-standard quoting; non-blocking SELECT FOR UPDATE, better time zone handling; cross-table DELETE and TRUNCATE).

- More powerful in-database functions with mutable function parameters and improved PL/Perl language support (return_next and spi_fetchrow; use strict; return arrays).

- Convenient interactive error retry in psql client (coded by End Point's own [Greg Sabino Mullane](/blog/authors/greg-sabino-mullane/)).

- Integrated encryption (pgcrypto module for PGP, SHA, AES, and DES encryption functions).

- Improved performance (better multiprocessor support; shared row locking; bitmap scan of indexes; ability to use multi-column indexes on single columns in any order).

- Easier database administration (autovacuum integration; ROLE replaces USER and GROUP; functions to determine on-disk storage space).

- Temporary views.

We are consistently pleased with the steady improvements shown by the PostgreSQL Global Development Group and have already begun using this new version in our development.
