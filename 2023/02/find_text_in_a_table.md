---
author: "Joshua Tolley"
title: "Find Text in Any Column"
date: 2023-02-03
tags:
- postgres
- data-processing
- database
---

It's not uncommon for me to want to find a particular text snippet in a
PostgreSQL database. Easy enough, you might say. After all, that's what
databases are for: you feed them a bunch of information, ask them questions in
the form of a query, and they give you the answer. So just write a query,
right?

Well, maybe.

SQL stands for "Structured Query Language", and the fact that it's "structured"
means not only that the database abides by some defined structure, but that
your queries do, too, which implies that you know at the time you're writing
the query where in the structure you want to look. And that's where the problem
arises. What if I know "Kilroy" is somewhere in a table, but I don't know
what column to look in to find him? How do I write <b>that</b> query?

The first answer I came up with to that question depends on `pg_dump`: dump the
contents of a table, search the results with `grep`, and there you have it.

```bash
$ pg_dump -t person mydb | grep -i kilroy
633132  F       NH      \N      Cristen212      3e588085-5151-41dd-7592-560163842571    Kilroy44        1983-09-28 00:00:00     \N      t       \N      \N      \N      \N      F       USA  \N       \N      \N      \N      \N      \N      \N      \N

```

Here I know I want to look in the `person` table, so I specify that in the call to `pg_dump`, but this works as well when I want to search the entire database:

```bash
$ pg_dump  mydb | grep -i kilroy
716565  public  person  18185   {"session_user": "josh"}        {"id": 633132}  {"last_name": "Feeney44"}       {"last_name": "Kilroy44"}       U       123349  2023-02-03 11:19:40.587883-062023-02-03 11:19:40.587883-06    2023-02-03 11:19:40.592103-06   josh    \N      \N
633132  F       NH      \N      Cristen212      3e588085-5151-41dd-7592-560163842571    Kilroy44        1983-09-28 00:00:00     \N      t       \N      \N      \N      \N      F       USA  \N       \N      \N      \N      \N      \N      \N      \N
```

I can switch `pg_dump` to `--inserts` mode and thus see the table these entries were found in:
```
$ pg_dump --inserts mydb | grep -i kilroy
INSERT INTO audit.modification_log VALUES (716565, 'public', 'person', 18185, '{"session_user": "josh"}', '{"id": 633132}', '{"last_name": "Feeney44"}', '{"last_name": "Kilroy44"}', 'U', 123349, '2023-02-03 11:19:40.587883-06', '2023-02-03 11:19:40.587883-06', '2023-02-03 11:19:40.592103-06', 'josh', NULL, NULL);
INSERT INTO public.person VALUES (633132, 'F', 'NH', NULL, 'Cristen212', '3e588085-5151-41dd-7592-560163842571', 'Kilroy44', '1983-09-28 00:00:00', NULL, true, NULL, NULL, NULL, NULL, 'F', 'USA', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
```

But `pg_dump` is considerably slower with `--inserts` turned on (about 200% slower, in my rudimentary testing on this one database), so perhaps I can get fancier with `grep` and achieve the same thing:

```bash
$ pg_dump mydb | grep -ie kilroy -e '^COPY' | grep -B1 -i kilroy
COPY audit.modification_log (id, table_schema, table_name, table_relid, app_user_info, id_columns, old_data, new_data, operation, transaction_id, ts_transaction, ts_statement, ts_clock, session_user_name, client_addr, query_text) FROM stdin;
716565  public  person  18185   {"session_user": "josh"}        {"id": 633132}  {"last_name": "Feeney44"}       {"last_name": "Kilroy44"}       U       123349  2023-02-03 11:19:40.587883-062023-02-03 11:19:40.587883-06    2023-02-03 11:19:40.592103-06   josh    \N      \N
--
COPY public.person (id, birth_gender, ethnicity, language, first_name, middle_name, last_name, birth_date, date_of_death, live, days_old_no_birthday, from_pregnant_id, fatal_condition_id, death_status, current_gender, country_of_birth, people_id, entity_id, birth_gender_id, ethnicity_id, primary_language_id, age_type_id, approximate_age_no_birthday, updated_at) FROM stdin;
633132  F       NH      \N      Cristen212      3e588085-5151-41dd-7592-560163842571    Kilroy44        1983-09-28 00:00:00     \N      t       \N      \N      \N      \N      F       USA  \N       \N      \N      \N      \N      \N      \N      \N
```

But the other day I realized I could easily search every a single table without leaving the database, thanks to `\copy`:

```bash
mydb=# \copy person to program 'grep -i kilroy';
COPY 117
633132  F       NH      \N      Cristen212      3e588085-5151-41dd-7592-560163842571    Kilroy44        1983-09-28 00:00:00     \N      t       \N      \N      \N      \N      F       USA  \N       \N      \N      \N      \N      \N      \N      \N
```

`\copy` requires copying the entire table to the client side, which wasn't a concern in my instance but could be a problem for some folks, and you need to be a superuser to use server-side `COPY ... TO PROGRAM`, so there are some limitations to this approach. I started thinking about this problem fresh off an encounter with row types, and realized we could do the whole thing in SQL:

```sql
mydb=# select * from person where person::text ~* 'kilroy';
   id   | birth_gender | ethnicity | language | first_name |             middle_name              | last_name |     birth_date      | date_of_death | live | days_old_no_birthday | from_pregnant_id | fatal_condition_id | death_status | current_gender | country_of_birth | people_id | entity_id | birth_gender_id | ethnicity_id | primary_language_id | age_type_id | approximate_age_no_birthday | updated_at
--------+--------------+-----------+----------+------------+--------------------------------------+-----------+---------------------+---------------+------+----------------------+------------------+--------------------+--------------+----------------+------------------+-----------+-----------+-----------------+--------------+---------------------+-------------+-----------------------------+------------
 633132 | F            | NH        |          | Cristen212 | 3e588085-5151-41dd-7592-560163842571 | Kilroy44  | 1983-09-28 00:00:00 |               | t    |                      |                  |                    |              | F              | USA              |           |           |                 |              |                     |             |                             |
(1 row)
```

This is my new favorite way of solving this problem, when I know what table I'm looking in but don't know the column. In cases where I don't know either, there's always this monstrosity:

```sql
mydb=# select 'select ' || quote_literal(relname) || ' as relname, f.*
from ' || oid::regclass || ' f where f::text ~* ''kilroy''' from pg_class
where relkind = 'r' and relnamespace = 'public'::regnamespace; \gexec
```

This will work only in `psql`, as it depends on the `\gexec` command. It composes one query for each table, and then executes them in turn. It produces rather a lot of probably useless output you'll need to sort through, and if you have (as I do) some tables with a large number of columns, I recommend trying it with `\x` turned on, to avoid having to page through quite so many results. But it did work, to find the entry I was looking for:

```bash
... Lots of output
(0 rows)

-[ RECORD 1 ]---------------+-------------------------------------
relname                     | person
id                          | 633132
birth_gender                | F
ethnicity                   | NH
language                    |
first_name                  | Cristen212
middle_name                 | 3e588085-5151-41dd-7592-560163842571
last_name                   | Kilroy44
birth_date                  | 1983-09-28 00:00:00
date_of_death               |
live                        | t
days_old_no_birthday        |
from_pregnant_id            |
fatal_condition_id          |
death_status                |
current_gender              | F
country_of_birth            | USA
people_id                   |
entity_id                   |
birth_gender_id             |
ethnicity_id                |
primary_language_id         |
age_type_id                 |
approximate_age_no_birthday |
updated_at                  |

(0 rows)
... Lots more output
```

If I'm willing to expand beyond one-liner solutions, I can get `psql` to filter that useless output for me:

```bash
mydb=# \o | grep -i kilroy | grep -v select
mydb=# select 'select ' || quote_literal(relname) || ' as rname, f.* from ' || oid::regclass || ' f where f::text ~* ''kilroy'''
from pg_class where relkind = 'r' and relnamespace = 'public'::regnamespace; \gexec
mydb=# \o
 person | 633132 | F            | NH        |          | Cristen212 | 3e588085-5151-41dd-7592-560163842571 | Kilroy44  | 1983-09-28 00:00:00 |               | t    |                      |                  |                    |              | F              | USA              |           |           |                 |              |                     |             |                             |
```

When I did this, I had to use a final `\o` to set the output mode back to normal, before I saw results.

Do you have a different technique to solve this problem? I'm sure there are many other possibilities out there! Comment below!
