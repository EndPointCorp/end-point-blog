---
author: Selena Deckelmann
gh_issue_number: 188
tags: postgres, tips
title: "Two quick tips: egrep &amp; SQL dumps, Vim and deleting things that don’t match"
---

Sometimes, I just don't want to restore a full SQL dump.  The restore might take too long, and maybe I just want a small subset of the records anyway.

I was in exactly this situation the other day - faced with a 10+ hour restore process, it was way faster to grep out the records and then push them into the production databases, than to restore five different versions.

So! egrep and vim to the rescue!

In my case, the SQL dump was full of COPY commands, and I had a username that was used as a partial-key on all the tables I was interested in. So:

> egrep "((^COPY)|username)" PostgresDump.sql > username.out

I get a pretty nice result from this. But, there are some records I'm not so interested in that got mixed in, so I opened the output file in vim and turned line numbers on (:set numbers).

The first thing that I do is insert the '\.' needed to tell Postgres that we're at the end of a COPY statement.

> :2,$s/^COPY/\\\.^V^MCOPY/

The '^V^M' is a control sequence that results in a '^M' (a newline character, essentially). And the '2' starts the substitution command on the second line rather than the first COPY statement (which, in my case, was on the first line).

Next, I want to strip out any records that the egrep found that I really don't want to insert into the database:

> :.,2000g!/stuff_i_wanna_keep/d

Broken down:

- '.,2000' - start from the current line and apply the command through line 2000
- 'g!' - find lines that do not match the following regular expression
- '/stuff_i_wanna_keep/' - the regular expression
- 'd' - delete what you find

I also use the ':split' command to divide my vim screen. This lets me look at both the start of a series of records as well as the end, and most importantly find the line number for where I want to stop my line deletion command.

I also add a 'BEGIN;' and 'ROLLBACK;' to the file to run tests on the script before applying to the database.

Once I got the system down, I was able to pull and process about 3000 records I needed out of a 15 GB dump file in about 5 minutes.  Testing and finally applying the records took another 10 minutes.
