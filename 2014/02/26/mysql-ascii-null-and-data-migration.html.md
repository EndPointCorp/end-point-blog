---
author: Mark Johnson
gh_issue_number: 934
tags: database, mysql, postgres
title: MySQL, ASCII Null, and Data Migration
---

Data migrations always have a wide range of challenges. I recently took on a request to determine the difficulty of converting an ecommerce shop’s MySQL 5.0 database to PostgreSQL 9.3, with the first (presumably “easier”) step being just getting the schema converted and data imported before tackling the more challenging aspect of doing a full assessment of the site’s query base to re-write the large number of custom queries that leverage MySQL-specific language elements into their PostgreSQL counterparts.

During the course of this first part, which had contained a number of difficulties I had anticipated, I hit one that I definitely had not anticipated:

```
ERROR:  value too long for type character varying(20)
```

Surely, the error message is absolutely clear, but how could this possibly be? The obvious answer—​that the varchar definitions were different lengths between MySQL and PostgreSQL—​was sadly quite wrong (which you knew, or I wouldn’t have written this).

After isolating out the row in question, the first clear distinction of the data in question was the presence of the ASCII null character in it:

```
'07989409006\007989409'
```

OK, sure, that’s weird (and I have a hunch why it’s there) but I’m still puzzled how the “too long” data could be in MySQL in the first place. Then, things become both weirder and more clear when I go to take a look at the record as it exists in the source database of the dump. The table in question has many columns, so naturally I look at the results with the left-justified output of \G. Without displaying the full record for a number of reasons, here’s what I saw for that field:

```
*************************** 1. row ***************************
xxxxx: 07989409006
1 row in set (0.00 sec)
```

Wow! OK, so in MySQL, even though the ASCII null is clearly maintained in the data (the row came from a mysqldump directly from that same database) somehow the data are truncated to the string before the ASCII null, and so it must be determining string length from the same process that is truncating. To “prove” this to myself, I added to the where clause on the above query “AND xxxxx = '07989409006'”, and sure enough the record was not found.

I discussed all of my findings with a colleague, who was equally bewildered and recommended I post something describing the issue. I agreed, and to make sure I was talking about an existing problem (this was MySQL 5.0 after all) I went to reproduce the issue on a more modern release (v 5.5 to be exact).

I created a test case, with a new table having a single field into which I would insert a too-long string that had an ASCII null at a point such that the string to that point was less than the field length. My testing *seemed* to indicate the problem had been fixed sometime between 5.0 and 5.5:

```
mysql> select version();
+-----------------+
| version()       |
+-----------------+
| 5.5.35-33.0-log |
+-----------------+
1 row in set (0.00 sec)

mysql> create table foo (foo_var varchar(5));
Query OK, 0 rows affected (0.60 sec)

mysql> insert into foo values ('123\0456');
Query OK, 1 row affected, 1 warning (0.93 sec)

mysql> select * from foo;
+---------+
| foo_var |
+---------+
| 123 4   |
+---------+
1 row in set (0.00 sec)
```

Now to run the exact same test on my MySQL 5.0 instance, prove the deviation in behavior, and we’ll be good to go:

```
mysql> select version();
+------------+
| version()  |
+------------+
| 5.0.95-log |
+------------+
1 row in set (0.00 sec)

mysql> create table foo (foo_var varchar(5));
Query OK, 0 rows affected (0.00 sec)

mysql> insert into foo values ('123\0456');
Query OK, 1 row affected, 1 warning (0.00 sec)

mysql> select * from foo;
+---------+
| foo_var |
+---------+
| 123 4   |
+---------+
1 row in set (0.00 sec)
```

So, my contrived test also worked on the original MySQL server that had dumped out the data that led to this problem in the first place. What was going on here?

By now, I’m pretty seriously flailing about in indignation. What was so special about the data from the dump, and its behavior in the original table, that I had failed to understand and reproduce? I begin devising tests that seemed too absurd to be believed, as though I had two apples that, if I repositioned them just right, would prove 1+1 is actually 3. Then, by a stroke of fortune, I hit on the missing clue. It was a bug, all right, but not anything like what I was thinking:

```
mysql> select version();
+------------+
| version()  |
+------------+
| 5.0.95-log |
+------------+
1 row in set (0.00 sec)

mysql> select * from foo;
+---------+
| foo_var |
+---------+
| 123 4   |
+---------+
1 row in set (0.00 sec)

mysql> select * from foo \G
*************************** 1. row ***************************
foo_var: 123
1 row in set (0.00 sec)
```

Eureka! The bug was an issue rendering the output using the \G query terminator, whether restricted just to ASCII null or perhaps to other backslash-escaped characters, I do not know. Finally, to confirm whether the issue was still an issue or fixed over the intervening versions, I ran my new test on 5.5:

```
mysql> select version();
+-----------------+
| version()       |
+-----------------+
| 5.5.35-33.0-log |
+-----------------+
1 row in set (0.00 sec)

ql> select * from foo;
+---------+
| foo_var |
+---------+
| 123 4   |
+---------+
1 row in set (0.00 sec)

mysql> select * from foo \G
*************************** 1. row ***************************
foo_var: 123 4
1 row in set (0.00 sec)
```

Now I had a clear explanation for the behavior of the data with ASCII nulls, but it threw me back to starting over on the original length problem. However, without the red herring of the “too long” data being truncated to explain the size problem, I looked more closely at the specific data causing the problem and realized that counting \ and 0 as literal characters, instead of the metadata represetnation of ASCII null, the width of the data ended up exceeding the field length. Testing this hypothesis was simple enough:

```
mysql> select length('07989409006\007989409') AS len;
+-----+
| len |
+-----+
|  20 |
+-----+
1 row in set (0.00 sec)

#####

postgres=# select length('07989409006\007989409') AS len;
 len
-----
  21
(1 row)
```

This answer leaves some confusion on a couple of fronts. Why doesn’t PostgreSQL properly treat the \0 representation of ASCII null? The answer to this is, itself, a mixed answer. PostgreSQL will treat a string as a literal unless explicitly told to do otherwise. In order to tell the database a string has escape sequences in it, you have to open the string with the “E” (or “e”) identifier. However, doing that, we still don’t match the behavior we see in MySQL:

```
postgres=# select length(E'07989409006\007989409') AS len;
 len
-----
  18
(1 row)
```

The escape sequence consumed two additional characters because PostgreSQL interpreted the escape as octal \007:

> \o, \oo, \ooo (o = 0 - 7) -> octal byte value[1](http://www.postgresql.org/docs/9.3/static/sql-syntax-lexical.html#SQL-SYNTAX-STRINGS-ESCAPE)

The other potentially confusing point, then, is *why* didn’t MySQL interpret the escape sequence as octal \007? The simple answer there is, it just doesn’t do that; MySQL makes a special case of recognizing the ASCII null character as \0:

> MySQL recognizes the escape sequences shown in Table 9.1, "Special Character Escape Sequences". For all other escape sequences, backslash is ignored.[2](http://dev.mysql.com/doc/refman/5.6/en/string-literals.html#character-escape-sequences)

If you look at Table 9.1, you’ll see the list of escape sequences is rather short and does not include general handling for octal or hex numeric representations.

