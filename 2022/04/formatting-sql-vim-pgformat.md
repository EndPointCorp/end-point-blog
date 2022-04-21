---
author: Josh Tolley
title: "Formatting SQL code with pgFormatter within Vim"
date: 2022-04-21
tags:
- tips
- open-source
- tools
- postgres
---

Sometimes a little, seemingly simple tip can make a world of difference. I've got enough gray hair these days that it would be pretty easy for me to start thinking I'd seen an awful lot, yet quite frequently when I watch a colleage working in a meeting or a [`tmux`](https://github.com/tmux/tmux) session or somewhere, I learn some new and simple thing that makes my life demonstrably easier. [Luca Ferrari's recent post](https://fluca1978.github.io/2022/04/13/EmacsPgFormatter.html) about using pgFormatter in Emacs reminded me that I'd meant for a while to share that essentially the same thing works in Vim. I don't especially want to get involved an editor war, and offer the following only in the spirit of friendly cooperation for the vim users out there.

As Luca mentioned, pgFormatter is a convenient way to make SQL queries readable, automatically. It's easy enough to feed it some SQL, and get a nice-looking result as output:

```
josh@igtre:~$ pg_format < create_outbreaks.sql
INSERT INTO outbreak                      
SELECT                              
    nextval('outbreak_id'::regclass),
    extract('year' FROM now())::text || '-' || nextval('outbreak_number_seq')::text, --number
    (                        
        SELECT  
            first_name
        FROM person TABLESAMPLE BERNOULLI (10)
LIMIT 1), -- name
    NOW() - interval '1 day' * random() * 100, (
        SELECT
            id
        FROM "user" TABLESAMPLE BERNOULLI (10)
...
```

In my perfect world I might quibble with some of its formatting decisions, but not so much that I've bothered to investigate whether I can change any of them to my liking. I just use it, and it's good enough for me. And because vim lets me highlight a region, pipe it through an external program, and replace the region with that program's output, it's easy to use it simply by selecting a section of code and typing `:!pg_format`:
![pgformatter example](/blog/2022/04/formatting-sql-via-pgformat/sample.gif)
