---
author: "David Christensen"
title: "Bucardo 5.6.0 Released"
tags: postgres, bucardo, replication, mongodb
gh_issue_number: 1596
---

<div style="float: left; margin-right: 40px"><img src="/blog/2020/03/01/bucardo-5-6-0-release/image-1.jpg" alt="bucardo logo" align="left"></div>

Bucardo 5.6.0 was released on February 28, 2020.

Bucardo is an asynchronous multi-master replication system for PostgreSQL. In addition to some bug fixes and minor compatibility tweaks for Pg 11 and 12, Bucardo 5.6.0 includes performance optimizations and an improved custom unique conflict handler.

Bucardo 5.6.0 is available for download here:

[https://bucardo.org/downloads/Bucardo-5.6.0.tar.gz](https://bucardo.org/downloads/Bucardo-5.6.0.tar.gz)

Detached signature (signed with key ID DF9B65B8):

[https://bucardo.org/downloads/Bucardo-5.6.0.tar.gz.asc](https://bucardo.org/downloads/Bucardo-5.6.0.tar.gz.asc)

### Detailed changes

  - Minor PostgreSQL 11/12 tweaks in `bucardo install`

  - Add config option `log_timer_format` to `glog()` to customize timestamp output

  - Change handling of file-path config settings so that they are no longer lower-cased—the new `log_timer_format` config will also be case-preserved

  - Fixed the relation parameter to the add customcode command to support schema-qualified relation names

  - Optimized table lookup when validating syncs to a single query, rather than separate queries for each table. Also added checks to avoid purging “toast” tables and old delta tables

  - Improve the unique conflict exception handler sample code and test

  - Map timestamp from PostgreSQL to MongoDB datetime

  - Safer system for determining Postgres version on install

  - Correction that `array_agg` was introduced in Postgres 8.4, not 8.3
