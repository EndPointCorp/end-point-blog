---
author: Jeff Boes
title: Sanity, thy name is not MySQL
github_issue_number: 960
tags:
- mysql
date: 2014-04-10
---

Probably old news, but I hit this MySQL oddity today after a long day dealing with unrelated crazy stuff and it just made me go cross-eyed:

```sql
CREATE TABLE foo (id integer, val enum('','1'));
INSERT INTO foo VALUES (1, '');
INSERT INTO foo VALUES (2, '1');
SELECT * FROM foo WHERE val = 1;
```

What row do you get? I’ll wait while you second- and third-guess yourself.

It turns out that the “enum” datatype in MySQL just translates to a set of unique integer values. In our case, that means:

- '' == 1 
- '1' == 2 

So you get the row with (1,''). Now, if *that* doesn’t confuse readers of your code, I don’t know what will.


