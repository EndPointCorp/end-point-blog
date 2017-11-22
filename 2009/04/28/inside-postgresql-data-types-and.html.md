---
author: Josh Tolley
gh_issue_number: 134
tags: postgres
title: Inside PostgreSQL - Data Types and Operator Classes
---



Two [separate](https://mail.endcrypt.com/pipermail/check_postgres/2009-April/000406.html) [posts](https://mail.endcrypt.com/pipermail/bucardo-general/2009-April/000272.html) taken from two separate mailing lists I'm on have gotten me thinking about PostgreSQL data types and operator classes today. The first spoke of a table where the poster had noticed that there was no entry in the [pg_stats](http://www.postgresql.org/docs/8.3/static/view-pg-stats.html) table for a particular column using the [point data type](http://www.postgresql.org/docs/8.3/static/datatype-geometric.html#AEN5480). The second talks about Bucardo failing when trying to select DISTINCT values from a [polygon](http://www.postgresql.org/docs/8.3/static/datatype-geometric.html#AEN5582) type column. I'll only talk about the first, here, but both of these behaviors stem from the fact that the data types in question lack a few things more common types always have.

The first stems from the point type's lack of a default b-tree operator class and lack of an explicitly-declared analyze function. What are those, you ask? In the pg_type table, the column typanalyze contains the OID of a function that will analyze the data type in question, so when you call ANALYZE on a table containing that data type, that function will be run. In a default installation of PostgreSQL, all rows contain 0 in this column, meaning use the default analyze function.

This default analyze function tries, among other things, to build a histogram of the data in the column. Histograms depend on the values in a table having a defined one-dimensional ordering (e.g. X <> Y, like numbers on a number line or words in alphabetical order). Now it gets a bit more complex. Index access methods define "strategies", which are numbers that correspond to the function of a particular index. Per [this page](http://www.postgresql.org/docs/8.4/static/xindex.html), the b-tree access method defines the following:

<table border="1" class="CALSTABLE"><colgroup><col/><col/></colgroup><thead><tr><th>Operation</th><th>Strategy Number</th></tr></thead><tbody><tr><td>less than</td><td>1</td></tr><tr><td>less than or equal</td><td>2</td></tr><tr><td>equal</td><td>3</td></tr><tr><td>greater than or equal</td><td>4</td></tr><tr><td>greater than</td><td>5
</td></tr></tbody></table>

To build a histogram we might use strategies 1, 3, and 5, to determine whether two given values are equal, or which is greater. So having found that there's an appropriate operator class for this data type, the analyze function would finally look in the pg_amop table to get the operators it needs to build its histogram. pg_amop matches these strategy numbers with actual function OIDs to find the functions it should actually call.

This whole line of thought stemmed from the point data type not having these functions. B-tree indexes try to sort their data in some order, as determined by the functions talked about above. But point types don't have an obvious one-dimensional ordering, so the b-tree index isn't really appropriate for them. So there's no b-tree operator class, and thus no statistics from columns of point type.

All that said, if you can think of a nice set of statistics ANALYZE might get from point data that would be useful for later query planning, you might implement a custom analyze function to fill the pg_stats table, and selectivity estimation functions to consume the data you generate, to make queries on point data that much better...

UPDATE: Those interested in the guts of a type-specific analyze function might take a look at [ts_typanalyze](http://doxygen.postgresql.org/ts__typanalyze_8c.html#608b1ac4a7bdb227da47459c9ef716e3), which is [in 8.4](http://archives.postgresql.org/pgsql-committers/2008-07/msg00104.php). Note that on its own, the typanalyze function doesn't do any good -- it needs selectivity functions, defined in [this file](http://doxygen.postgresql.org/ts__selfuncs_8c-source.html), which also were [committed in 8.4](http://archives.postgresql.org/pgsql-committers/2008-09/msg00203.php). Both patches courtesy of Jan Urbanski, and various reviewers.


