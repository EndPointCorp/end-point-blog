---
author: Josh Tolley
gh_issue_number: 157
tags: postgres
title: Inside PostgreSQL - Clause selectivity
---



One of the more valuable features of any conference is the so-called “hall track”, or in other words, the opportunity to talk to all sorts of people about all sorts of things. PGCon was no exception, and I found the hall track particularly interesting because of suggestions I was able to gather regarding multi-column statistics, not all of which boiled down to “You’re dreaming—​give it a rest”. One of the problems I’d been trying to solve was where, precisely, to put the code that actually applies the statistics to a useful problem. There are several candidate locations, and certainly quite a few places where we could make use of such statistics. The lowest-hanging fruit, however, seems to be finding groups of query clauses that aren’t as independent as we would normally assume. Between PGCon sessions one day, Tom Lane pointed me to a place where we already do something very similar: [clausesel.c](https://doxygen.postgresql.org/clausesel_8c.html)

“Clause selectivity” means much the same thing as any other selectivity: it’s the proportion of rows from a relation that an operation will return. A “clause”, in this case, is a filter on a relation, such as the “X = 1” and the “Y < 10” in “WHERE X = 1 AND Y < 10”. PostgreSQL uses functions in clausesel.c to find clauses whose combined selectivity differs from the product of their individual selectivities. For instance, in “WHERE X < 4 AND X < 5”, the “X < 5” is redundant; the clauses’ combined selectivity is simply that of “X < 4”. With “WHERE Y > 4 AND Y < 10”, clausesel.c can determine that we really want the selectivity of the clause “4 < Y < 10”. It’s also smart enough to recognize “pseudo-constants”: values from non-volatile functions, or from the outer relation of a nested loop. Although these values aren’t truly constants, they remain constant at the level of the query where the clause will be applied, and can be treated as constants.

With any luck, one day clausesel.c will also know enough to notice cases where, for instance, although “foo.x = 3” and “foo.y > 10” are individually true for much of table “foo”, there are very few rows where both conditions are true.


