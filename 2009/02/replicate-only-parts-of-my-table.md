---
author: Josh Tolley
title: Replicate only parts of my table
github_issue_number: 105
tags:
- postgres
date: 2009-02-19
---

A day or two ago in [#slony](irc://irc.freenode.net/slony), someone asked if Slony would replicate only selected columns of a table. A natural response might be to create a view containing only the columns you’re interested in, and have Slony replicate that. But Slony is trigger-based—​the only reason it knows there’s something to replicate is because a trigger has told it so—​and you can’t have a trigger on a view. So that won’t work. [Greg](/blog/authors/greg-sabino-mullane) chimed in to say that Bucardo could do it, and mentioned a Bucardo feature I’d not yet noticed.

[Bucardo](https://bucardo.org/) is trigger-based, like Slony, so defining a view won’t work. But it allows you to specify a special query string for each table you’re replicating. This query is called a “customselect”, and can serve to limit the columns you replicate, transform the rows as they’re being replicated, etc., and probably a bunch of other stuff I haven’t thought of yet. A simple example:

1. Create a table in one database as follows:

```
CREATE TABLE synctest (
   id INTEGER PRIMARY KEY,
   field1 TEXT,
   field2 TEXT,
   field3 TEXT
);
```

Also create this table in the replication destination database; Bucardo won’t replicate schema changes or database structure.

1. Tell Bucardo about the table. I won’t give the SQL here because it’s already available in the [Bucardo documentation](https://bucardo.org/Bucardo/Documentation/Overview/). Suffice it to say you need to tell the goat table about a customselect query. For my testing, I used ‘SELECT id, field1 FROM synctest’. Note that the fields returned by this query must

    <ul>
      <li>Include all the primary key fields from the table. Bucardo will complain if it can’t find the primary key in the results of the customselect query.</li>

      <li>Return field names matching those of the table. This means, for example, that if you somehow transform the contents of a field, you need to make sure the query explicitly names the results something Bucardo can recognize, e.g. ‘SELECT id, do_some_transformation(field1) AS field1 FROM synctest’</li>
    </ul>

2. Tell the sync to use the custom select statements by setting the ‘usecustomselect’ field in the sync table to TRUE for the sync in question

3. Fire up Bucardo and see the results. Here’s my source table:

```
58921 josh@bucardo_test# select * from uniq_test ;
 id |  field1  | field2 | field3
----+----------+--------+---------
  1 | alpha    | bravo  | charlie
  2 | delta    | echo   | foxtrot
  3 | hotel    | india  | juliet
  4 | kilo     | lima   | mike
  5 | november | oscar  | papa
  6 | romeo    | sierra | tango
  7 | uniform  | victor | whiskey
  8 | xray     | yankee | zulu
(8 rows)
```

...and here’s my destination table...

```
58922 josh@bucardo_test# select * from uniq_test;
 id |  field1  | field2 | field3
----+----------+--------+--------
  1 | alpha    |        |
  2 | delta    |        |
  3 | hotel    |        |
  4 | kilo     |        |
  5 | november |        |
  6 | romeo    |        |
  7 | uniform  |        |
  8 | xray     |        |
(8 rows)
```

Note that at least for now, customselect works only with fullcopy sync types. Also, the destination table must match the source table in structure, even if you’re not going to copy all the fields. That is, even though I’m only replicating the ‘id’ and ‘field1’ fields in the example above, the destination table needs to contain all the fields in the source table. This is one of Bucardo’s TODO items...
