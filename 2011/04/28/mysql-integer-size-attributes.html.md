---
author: Mark Johnson
gh_issue_number: 446
tags: database, mysql
title: MySQL Integer Size Attributes
---



MySQL has those curious size attributes you can apply to integer data types. For example, when creating a table, you might see:

```sql
mysql&gt; CREATE TABLE foo (
    -&gt; field_ti tinyint(1),
    -&gt; field_si smallint(2),
    -&gt; field_int int(4),
    -&gt; field_bi bigint(5)
    -&gt; );
Query OK, 0 rows affected (0.05 sec)

mysql&gt; desc foo;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| field_ti  | tinyint(1)  | YES  |     | NULL    |       |
| field_si  | smallint(2) | YES  |     | NULL    |       |
| field_int | int(4)      | YES  |     | NULL    |       |
| field_bi  | bigint(5)   | YES  |     | NULL    |       |
+-----------+-------------+------+-----+---------+-------+
3 rows in set (0.03 sec)

mysql&gt;
```

I had always assumed those size attributes were limiters, MySQL's way of providing some sort of constraint on the integers allowed in the field. While doing some recent work for a MySQL client, I attempted to enforce the range of a tinyint according to that assumption. In reality, I only wanted a sign field, and would have liked to have applied a "CHECK field IN (-1,1)", but without check constraints I figured at least keeping obviously incorrect data out would be better than nothing.

I wanted to see what MySQL's behavior would be on data entry that failed the limiters. I was hoping for an error, but expecting truncation. What I discovered was neither.

```sql
mysql&gt; INSERT INTO foo (field_ti) VALUES (-1);
Query OK, 1 row affected (0.00 sec)

mysql&gt; SELECT field_ti FROM foo;
+----------+
| field_ti |
+----------+
|       -1 |
+----------+
1 row in set (0.00 sec)

mysql&gt; INSERT INTO foo (field_ti) VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql&gt; SELECT field_ti FROM foo;
+----------+
| field_ti |
+----------+
|       -1 |
|        1 |
+----------+
2 rows in set (0.00 sec)

mysql&gt; INSERT INTO foo (field_ti) VALUES (10);
Query OK, 1 row affected (0.00 sec)

mysql&gt; SELECT field_ti FROM foo;
+----------+
| field_ti |
+----------+
|       -1 |
|        1 |
|       10 |
+----------+
3 rows in set (0.00 sec)

mysql&gt; INSERT INTO foo (field_ti) VALUES (100);
Query OK, 1 row affected (0.00 sec)

mysql&gt; SELECT field_ti FROM foo;
+----------+
| field_ti |
+----------+
|       -1 |
|        1 |
|       10 |
|      100 |
+----------+
4 rows in set (0.00 sec)

mysql&gt;
```

Two possible conclusions followed immediately: either the limiter feature was horribly broken, or those apparent sizes didn't represent a limiter feature. A full review of MySQL's [Numeric Types](http://dev.mysql.com/doc/refman/5.0/en/numeric-types.html) documentation provided the answer:

> 
> MySQL supports an extension for optionally specifying the display width of integer data types in parentheses following the base keyword for the type. For example, INT(4) specifies an INT with a display width of four digits. This optional display width may be used by applications to display integer values having a width less than the width specified for the column by left-padding them with spaces. (That is, this width is present in the metadata returned with result sets. Whether it is used or not is up to the application.)
> 
> **The display width does not constrain the range of values that can be stored in the column.**
> 

And, so, the lesson is repeated: Beware assumptions.


