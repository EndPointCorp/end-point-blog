---
author: Josh Tolley
title: "Formatting SQL code with pgFormatter within Vim"
date: 2022-04-26
tags:
- tips
- open-source
- tools
- postgres
github_issue_number: 1861
---

![Outdoor view of a creek bank with dry trees and old wooden buildings against a blue sky](/blog/2022/04/formatting-sql-vim-pgformat/20220411_091408.webp)
Photo by Garrett Skinner

Sometimes a little, seemingly simple tip can make a world of difference. I've got enough gray hair these days that it would be pretty easy for me to start thinking I'd seen an awful lot, yet quite frequently when I watch a colleague working in a meeting or a [tmux](https://github.com/tmux/tmux) session or somewhere, I learn some new and simple thing that makes my life demonstrably easier.

[Luca Ferrari recently authored a post](https://fluca1978.github.io/2022/04/13/EmacsPgFormatter.html) about using pgFormatter in Emacs; essentially the same thing works in Vim, my editor of choice, and it's one of my favorite quick tips when working with complicated queries. I don't especially want to get involved an editor war, and offer the following only in the spirit of friendly cooperation for the Vim users out there.

As Luca mentioned, [pgFormatter](https://github.com/darold/pgFormatter) is a convenient way to make SQL queries readable, automatically. It's easy enough to feed it some SQL, and get a nice-looking result as output:

```sql
$ pg_format < create_outbreaks.sql
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

In my perfect world I might quibble with some of its formatting decisions, such as the lack of indent on the `LIMIT 1` line above. But in practice the results are good enough for my tastes that I haven't bothered to investigate whether I can improve them. I just use it, and it's good enough for me.

And because Vim lets me highlight a region, pipe it through an external program, and replace the region with that program's output, it's easy to use it simply by selecting a section of code and typing `:!pg_format` like this:

<img src="/blog/2022/04/formatting-sql-vim-pgformat/sample.gif" width=250 height=492 alt="pgformatter example animation of terminal" />
