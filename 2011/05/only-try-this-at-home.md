---
author: Josh Williams
title: Only Try This At Home
github_issue_number: 455
tags:
- database
- postgres
- python
date: 2011-05-19
---

<img alt="Taken by Josh 6 years to the day before the release of 9.1 beta 1" border="0" src="https://joshwilliams.name/PLPython/run_server.jpg"/>
Taken by Josh 6 years to the day before the release of 9.1 beta 1

For the record, 9.1 is gearing up to be an awesome release. I was tinkering and testing [PostgreSQL 9.1 Beta 1](https://www.postgresql.org/about/news/1313/) (... You are beta testing, too, right?) ... and some of the new [PL/Python](https://www.postgresql.org/docs/devel/static/plpython.html) features caught my eye. These are minor among all the really cool high profile features, to be sure. But it made me think back to a little bit of experimental code written some time ago, and how these couple language additions could make a big difference.

For one reason or another I’d just hit the top level [postgresql.org](https://www.postgresql.org/) website, and suddenly realized just how many Postgres databases it took to put together what I was seeing on the screen. Not only does it power the content database that generated the page, of course, but even the lookup of the .org went through [Afilias](https://www.postgresql.org/about/press/presskit90) and their Postgres-backed domain service. It’s a pity the DBMS couldn’t act as the middle layer between those.

Or could it?

That’s a shortened form of it just for demonstration purposes (the original one had things like a table browser) ... but it works. For example, on this test 9.1 install, hit http://localhost:8000/public/webtest and the following table appears:

<table><thead><tr><th>generate_series</th><th>lh</th><th>rnd</th></tr></thead><tbody><tr><td>1</td><td>0</td><td>0.548577250913</td></tr><tr><td>2</td><td>1</td><td>1.70926172473</td></tr><tr><td>3</td><td>1</td><td>1.24841631576</td></tr><tr><td>(etc)</td><td>...</td><td>...</td></tr></tbody></table>

Note the use of two specific 9.1 features, though. The plpy object contains nice query building helper utilities like quote_ident that you may be familiar with in other languages. But this also makes use of subtransactions, which helps recover from db errors. That’s important here, as something like a typo in a table name will generate an error from Postgres and without that in place the database will end the transaction and ignore any subsequent commands the function tries to run.

But with that in place, the page shows the 404 error, and picks up where it left off with subsequent requests:

```plain
Error code 404.

Message: Table not found.
```

By the way, if it’s not clear by now don’t take this anywhere near a production database, if not any other reason that a transaction will be held open as long as that function runs. That will hold back all the nice maintenance stuff that keeps things running efficiently. Still, I think it helps show off what just a handful of lines of code can do in a powerful language like PL/Python. I’m sure with the right module PL/PerlU could do something very similar. But even more I think it shows how Postgres is growing and innovating by leaps and bounds, seemingly every day!


