---
author: Dan Collis-Puro
gh_issue_number: 55
tags: database, postgres, payments, ecommerce
title: Authorize.Net Transaction IDs to increase in size
---

A sign of their success, [Authorize.net](http://www.authorize.net/) is going to break through [Transaction ID numbers greater than 2,147,483,647 (or 2^31)](http://www.authorize.net/transid#238187), which happens to exceed the maximum size of a [signed MySQL int() column](http://dev.mysql.com/doc/refman/4.1/en/numeric-types.html) and the default [Postgres "integer"](http://www.postgresql.org/docs/8.1/static/datatype.html#DATATYPE-NUMERIC).

It probably makes sense to ensure that your transaction ID columns are large enough proactively - this would not be a fun bug to run into ex-post-facto.
