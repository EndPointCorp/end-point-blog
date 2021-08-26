---
author: Brian Buchalter
title: Case Sensitive MySQL Searches
github_issue_number: 710
tags:
- database
- mysql
date: 2012-10-18
---



MySQL’s support for case sensitive search is explained somewhat opaquely in the aptly titled [Case Sensitivity in String Searches](https://dev.mysql.com/doc/refman/5.6/en/case-sensitivity.html) documentation. In short, it explains that by default, MySQL won’t treat strings as case sensitive when executing a statement such as:

```sql
SELECT first_name FROM contacts WHERE first_name REGEXP '^[a-z]';
```

This simple search to look for contacts whose first name starts with a lower case letter, will return *all* contacts because in the default character set used by MySQL ([latin1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1)), upper and lower case letters share the same “sort value”.

UPDATE: After many helpful comments from readers, it would seem the term I should have used was collation, not sort value. The documentation for both [MySQL](https://dev.mysql.com/doc/refman/5.6/en/charset-general.html) and [PostgreSQL](https://www.postgresql.org/docs/9.2/static/collation.html) have lengthy discussions on the topic.

### Enough with the backstory, how do I perform case sensitive searches!

The docs say to convert the string representation to a binary one. This allows “comparisons [to] use the numeric values of the bytes in the operands”. Let’s see it in action:

```sql
SELECT first_name FROM contacts WHERE BINARY(first_name) REGEXP '^[a-z]';
```

There are other strategies available, such as changing the character set being used for comparisons with the [COLLATE](https://dev.mysql.com/doc/refman/5.0/en/charset-collate.html) function. This would likely work better for cases where you had many columns to compare.

```sql
SELECT first_name FROM contacts WHERE first_name REGEXP '^[a-z]' COLLATE latin1_bin;
```

You can even go so far as to have MySQL switch character sets and collations. But you do have to do this for each database, each table, and each column you need to convert. Not terribly fun.


