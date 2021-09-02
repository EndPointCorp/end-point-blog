---
author: Dan Collis-Puro
title: Authorize.Net Transaction IDs to increase in size
github_issue_number: 55
tags:
- database
- postgres
- payments
- ecommerce
date: 2008-09-02
---

A sign of their success, [Authorize.net](https://www.authorize.net/) is going to break through [Transaction ID numbers greater than 2,147,483,647 (or 2^31)](https://web.archive.org/web/20080912094254/http://www.authorize.net/transid#238187), which happens to exceed the maximum size of a [signed MySQL int() column](http://dev.mysql.com/doc/refman/4.1/en/numeric-types.html) and the default [Postgres “integer”](https://web.archive.org/web/20080912144714/http://dev.mysql.com/doc/refman/4.1/en/numeric-types.html).

It probably makes sense to ensure that your transaction ID columns are large enough proactively—​this would not be a fun bug to run into ex-post-facto.
