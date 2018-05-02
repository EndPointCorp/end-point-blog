---
author: Greg Sabino Mullane
gh_issue_number: 1140
tags: database, heroku, postgres
title: Selectively firing Postgres triggers
---

<div class="separator" style="clear: both; float:right; text-align: center; padding-left: 3em; padding-bottom: 1em;"><a href="/blog/2015/07/15/selectively-firing-postgres-triggers/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/07/15/selectively-firing-postgres-triggers/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/fnSBJW">Lake Wallaga</a> by <a href="https://www.flickr.com/people/tonyheywardimages/">Tony Heyward</a></small></div>

Being able to disable Postgres triggers selectively can be an important skill when doing tasks like bulk updates, in which you only want a subset of the triggers on the table
to be fired. Read below for the long explanation, but the [TL;DR version](https://en.wikipedia.org/wiki/TL;DR) of the best solution is to set a WHEN clause on the trigger you wish to skip, making it conditional on a variable such as **session_replication_role**, or **application_name**

```
CREATE TRIGGER mytrig AFTER INSERT ON foobar FOR EACH
  ROW WHEN (current_setting('session_replication_role') <> 'local') EXECUTE PROCEDURE myfunc();
BEGIN;
SET LOCAL session_replication_role = 'local';
UPDATE foobar SET baz = 123;
COMMIT;
```

I decided to spin up a free [Heroku](https://www.heroku.com/)
[“Hobby Dev” database](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier) to illustrate the solutions. Generating a test table was done by using the Pagila project, as it has tables which contain triggers. Heroku gives you a randomly generated user and database name. To install [the Pagila schema](http://www.postgresql.org/ftp/projects/pgFoundry/dbsamples/pagila/pagila/), I did:

```
$ export H="postgres://vacnvzatmsnpre:2iCDp-46ldaFxgdIx8HWFeXHM@ec2-34-567-89.compute-1.amazonaws.com:5432/d5q5io7c3alx9t"
$ cd pagila-0.10.1
$ psql $H -q -f pagila-schema.sql
$ psql $H -q -f pagila-data.sql
```

Errors appeared on the import, but they can be safely ignored.
One error was because the Heroku database does not have a user named “postgres”, and the other error was due to the fact that the Heroku user is not a superuser. The data, however, was all intact. The sample data is actually quite funny, as the movie titles were semi auto-generated at some point. For example, seven random movie descriptions:

- A Brilliant Panorama of a Madman And a Composer who must Succumb a Car in Ancient India
- A Touching Documentary of a Madman And a Mad Scientist who must Outrace a Feminist in An Abandoned Mine Shaft
- A Lackluster Reflection of a Eskimo And a Wretch who must Find a Fanny Pack in The Canadian Rockies
- A Emotional Character Study of a Robot And a A Shark who must Defeat a Technical Writer in A Manhattan Penthouse
- A Amazing Yarn of a Hunter And a Butler who must Defeat a Boy in A Jet Boat
- A Beautiful Reflection of a Womanizer And a Sumo Wrestler who must Chase a Database Administrator in The Gulf of Mexico
- A Awe-Inspiring Reflection of a Waitress And a Squirrel who must Kill a Mad Cow in A Jet Boat

The table we want to use for this post is named **“film”**, and comes with two triggers on it,
‘film_fulltext_trigger’, and ‘last_updated’:

```
heroku=> \d film
                            Table "public.film"
        Column        |            Type             |       Modifiers
----------------------+-----------------------------+---------------------------------
 film_id              | integer                     | not null default
                                                      nextval('film_film_id_seq'::regclass)
 title                | character varying(255)      | not null
 description          | text                        |
 release_year         | year                        |
 language_id          | smallint                    | not null
 original_language_id | smallint                    |
 rental_duration      | smallint                    | not null default 3
 rental_rate          | numeric(4,2)                | not null default 4.99
 length               | smallint                    |
 replacement_cost     | numeric(5,2)                | not null default 19.99
 rating               | mpaa_rating                 | default 'G'::mpaa_rating
 last_update          | timestamp without time zone | not null default now()
...
Triggers:
    film_fulltext_trigger BEFORE INSERT OR UPDATE ON film FOR EACH ROW EXECUTE
       PROCEDURE tsvector_update_trigger('fulltext', 'pg_catalog.english', 'title', 'description')
    last_updated BEFORE UPDATE ON film FOR EACH ROW EXECUTE PROCEDURE last_updated()
```

The last_updated trigger calls the last_updated() function, which simply sets the last_update column to
[CURRENT_TIMESTAMP](http://www.postgresql.org/docs/current/static/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT), which is often seen as its shorter-to-type form, now(). This is a handy metric to track,
but there are times when you want to make changes and *not* update this field. A typical
example is some sort of bulk change that does not warrant changing all the rows’ last_update
field. How to accomplish this? We need to ensure that the trigger does not fire when
we do our UPDATE. The way many people are familiar with is to simply disable all triggers on the table. So you would do something like this:

```
BEGIN;
ALTER TABLE film DISABLE TRIGGER ALL;
UPDATE film SET rental_duration = 10;
ALTER TABLE film ENABLE TRIGGER ALL;
COMMIT;
```

When using Heroku, you are given a regular user, not a Postgres superuser, so the above will generate an error that looks like this:

```
ERROR:  permission denied: "RI_ConstraintTrigger_a_88776583" is a system trigger.
```

This is caused by the failure of a normal user to disable the internal triggers Postgres uses to maintain foreign key relationships between tables. So the better way is to simply disable the specific trigger like so:

```
BEGIN;
ALTER TABLE film DISABLE TRIGGER last_updated;
UPDATE film SET rental_duration = 10;
ALTER TABLE film ENABLE TRIGGER last_updated;
COMMIT;
```

This works on Heroku, but there are two major problems with the ALTER TABLE solution. First, the ALTER TABLE will take a very heavy lock on the entire table, meaning that nobody else will be able to access the table—even to read it!—until your transaction is complete (although Postgres 9.5 will reduce this lock!). The other problem
with disabling triggers this way is that it is too easy to accidentally leave it in a disabled state (although the check_postgres program has a
[specific check for this!](https://bucardo.org/check_postgres/check_postgres.pl.html#disabled_triggers)). Let’s take a
look at the lock, and double check that the trigger has been disabled as well:

```
heroku=> SELECT last_update FROM film WHERE film_id = 123;
        last_update
----------------------------
 2015-06-21 16:38:00.891019
heroku=> BEGIN;
heroku=> ALTER TABLE film DISABLE TRIGGER last_updated;
heroku=> SELECT last_update FROM film WHERE film_id = 123;
heroku=> UPDATE film SET rental_duration = 10;
-- We need the subselect because we share with a gazillion other Heroku databases!
heroku=> select relation::regclass,mode,granted from pg_locks where database =
heroku->   (select oid from pg_database where datname = current_database());
 relation |        mode         | granted
----------+---------------------+---------
 pg_locks | AccessShareLock     | t
 film     | RowExclusiveLock    | t
 film     | AccessExclusiveLock | t  ## This is a very heavy lock!
## Version 9.5 and up will have a ShareRowExclusive lock only!
heroku=> ALTER TABLE film ENABLE TRIGGER last_updated;
heroku=> COMMIT;

-- This is the same value, because the trigger did not fire when we updated
heroku=> select last_update FROM film WHERE film_id = 123;
        last_update
----------------------------
 2015-06-21 16:38:00.891019
```

What we really want is to use the
[powerful session_replication_role parameter](/blog/2015/01/28/postgres-sessionreplication-role) to safely disable the triggers. The problem is that the canonical way to disable triggers, by setting session_replication_role to ‘replica’, will disable ALL triggers and rules, for ALL tables. This is not wanted. In our example, we want to stop the **last_updated** trigger from firing, but also want all the other user triggers to fire, as well as the hidden system triggers that are enforcing foreign key referential integrity.

You can set session_replication_role to one of three values: **origin** (the default), **local**, and **replica**. Setting it to “replica” is commonly used in replication systems such as Bucardo and Slony to prevent all rules and triggers from firing. It can also be used for careful bulk loading. Only triggers explicitly set as “replica triggers” will fire when the session_replication_role is set to ‘replica’. The **local** setting is a little harder to understand, as it does not have a direct mapping to a trigger state, as ‘origin’ and ‘replica’ do. Instead, it can be thought of as an alias to ‘origin’—same functionality, but with a different name. What use is that? Well, you can check the value of session_replication_role and do things differently depending on whether it is ‘origin’ or ‘local’. Thus, it is possible to teach a trigger that it should not fire when session_replication_role is set to ‘local’ (or to fire *only* when it is set to ‘local’).

Thus, our previous problem of preventing the last_updated trigger from firing can be solved by careful use of
the session_replication_role. We want the trigger to NOT fire when session_replication_role is set to ‘local’. This can be accomplished in two ways: modification of the trigger, or modification of the underlying function. Each has its
strengths and weaknesses. Note that session_replication_role can only be set by a superuser, which means I’ll
be switching from Heroku (which only allows connecting as a non-superuser) to a local Pagila database.

For the modify-the-function route, add a quick block at the top to short-circuit the trigger
if the session_replication_role (srr) is set to ‘local’. An advantage to this method is that all triggers that
invoke this function will be affected. In the pagila database, there are 14 tables that have a trigger that
calls the last_updated function. Another advantage is that the exception to the function firing is
clearly visible in the functions definition itself, and thus easy to spot when you examine the
function. Here is how you would modify the last_updated function to only fire when in ‘local’ srr mode:

```
CREATE OR REPLACE FUNCTION public.last_updated()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $bc$
BEGIN
  IF current_setting('session_replication_role') = 'local' THEN
    RETURN NEW;
  END IF;

  NEW.last_update = CURRENT_TIMESTAMP;
  RETURN NEW;
END
$bc$;
```

To invoke it, we change session_replication_role (temporarily!) to ‘local’, then make our
changes. Observe how the value of last_update does not change when we are in ‘local’ mode:

```
pagila=# show session_replication_role \t\g
 origin

pagila=# begin;
BEGIN
pagila=# select last_update from film where film_id = 203;
 2015-06-21 16:38:00.711411

pagila=# update film set rental_duration = 10 WHERE film_id = 203;
UPDATE 1
pagila=# select last_update from film where film_id = 203;
 2015-06-21 16:38:03.543831
pagila=# commit;
COMMIT

pagila=# begin;
BEGIN
pagila=# set LOCAL session_replication_role = 'local';
SET
pagila=# select last_update from film where film_id = 203;
 2015-06-21 16:38:03.543831
pagila=# update film set rental_duration = 10 WHERE film_id = 203;
UPDATE 1
pagila=# select last_update from film where film_id = 203;
 2015-06-21 16:38:03.543831
pagila=# commit;
COMMIT

pagila=# show session_replication_role;
 origin
```

The second method for skipping a trigger by using session_replication_role is to modify the
trigger definition itself, rather than changing the function. This has the advantage of not having
to touch the function at all, and also allows you to see that the trigger has been modified when
doing a **\d** of the table. Using ALTER TRIGGER only allows a rename, so we will need to
drop and recreate the trigger. By adding a WHEN clause to the trigger, we can ensure that
it does NOT fire when session_replication_role is set to ‘local’. The SQL looks like this:

```
pagila=# begin;
BEGIN
pagila=# drop trigger last_updated ON film;
DROP TRIGGER
pagila=# create trigger last_updated before update on film for each row
pagila-#   when (current_setting('session_replication_role') <> 'local') execute procedure last_updated();
CREATE TRIGGER
pagila=# commit;
COMMIT
```

Voila! As before, we can test it out by setting session_replication_role to ‘local’ and confirming that the function does not modify the last_update column. Before doing that, let’s also change the function back to its original form, to keep things honest:

```
-- Restore the original version, with no session_replication_role logic:
pagila=# CREATE OR REPLACE FUNCTION public.last_updated() RETURNS TRIGGER LANGUAGE plpgsql
AS $bc$ BEGIN NEW.last_update = CURRENT_TIMESTAMP; RETURN NEW; END $bc$;
CREATE FUNCTION

-- Normal update will change the last_update column:
pagila=# select last_update from film where film_id = 203;
        last_update
----------------------------
 2015-06-21 16:38:00.121011

pagila=# update film set rental_duration = 10 WHERE film_id = 203;
UPDATE 1
pagila=# select last_update from film where film_id = 203;
        last_update
----------------------------
 2015-06-21 16:38:03.011004

pagila=# begin;
pagila=# set LOCAL session_replication_role = 'local';
SET
pagila=# update film set rental_duration = 10 WHERE film_id = 203;
UPDATE 1
pagila=# select last_update from film where film_id = 203;
        last_update
----------------------------
 2015-06-21 16:38:03.011004

-- Show that we are not holding a heavy lock:
pagila=# select relation::regclass,mode,granted from pg_locks where relation::regclass::text = 'film';
 relation |       mode       | granted
----------+------------------+---------
 film     | AccessShareLock  | t
 film     | RowExclusiveLock | t

pagila=# commit;
COMMIT
```

Those are the three main ways to selectively disable a trigger on a table: using ALTER TABLE to completely disable it (and invoking a heavy lock), having the function check session_replication_role (affects all triggers using it, requires superuser), and having the trigger use a WHEN clause (requires superuser). Sharp readers may note that being a superuser is not really required, as something other than session_replication_role could be used. Thus, a solution is to use a parameter that can be changed by anyone, that will not affect anything else, and can be set to a unique value. Here is one such solution, using the handy “application_name” parameter. We will return to the Heroku database for this one:

```
heroku=> drop trigger last_updated on film;
heroku=> create trigger last_updated before update on film for each row
  when (current_setting('application_name') <> 'skiptrig') execute procedure last_updated();

heroku=> select last_update from film where film_id = 111;
 2015-06-21 16:38:00.365103
heroku=> update film set rental_duration = 10 WHERE film_id = 111;
UPDATE 1
heroku=> select last_update from film where film_id = 111;
 2015-06-21 16:38:03.101115

heroku=> begin;
BEGIN
heroku=> set LOCAL application_name = 'skiptrig';
SET
heroku=> update film set rental_duration = 10 WHERE film_id = 111;
UPDATE 1
heroku=> select last_update from film where film_id = 111;
 2015-06-21 16:38:03.101115

-- Show that we are not holding a heavy lock:
heroku=> select relation::regclass,mode,granted from pg_locks where database =
heroku->   (select oid from pg_database where datname = current_database());
 relation |       mode       | granted
----------+------------------+---------
 film     | AccessShareLock  | t
 film     | RowExclusiveLock | t

heroku=> commit;
COMMIT
```

So there you have it: four solutions to the problem of skipping a single trigger. Which to use depends on your circumstances. I prefer the WHEN + session_replication_role option, as it forces you to be a superuser, and is very visible when looking at the trigger via \d.
