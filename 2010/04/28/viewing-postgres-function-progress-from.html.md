---
author: Greg Sabino Mullane
gh_issue_number: 296
tags: database, postgres
title: Viewing Postgres function progress from the outside
---



Getting visibility into what your PostgreSQL function is doing can be a difficult task. While you can sprinkle notices inside your code, for example with the [RAISE feature](https://www.postgresql.org/docs/current/static/plpgsql-errors-and-messages.html) of plpgsql, that only shows the notices to the session that is currently running the function. Let’s look at a solution to peek inside a long-running function from any session.

While there are a few ways to do this, one of the most elegant is to use [Postgres sequences](https://www.postgresql.org/docs/current/static/functions-sequence.html), which have the unique property of living “outside” the normal [MVCC](https://wiki.postgresql.org/wiki/MVCC) visibility rules. We’ll abuse this feature to allow the function to update its status as it goes along.

First, let’s create a simple example function that simulates doing a lot of work, and taking a long time to do so. The function doesn’t really do anything, of course, so we’ll throw some random sleeps in to emulate the effects of running on a busy production machine. Here’s what the first version looks like:

```sql
DROP FUNCTION IF EXISTS slowfunc();

CREATE FUNCTION slowfunc()
RETURNS TEXT
VOLATILE
SECURITY DEFINER
LANGUAGE plpgsql
AS $BC$
DECLARE
  x INT = 1;
  mynumber INT;
BEGIN
  RAISE NOTICE 'Start of function';

  WHILE x <= 5 LOOP
    -- Random number from 1 to 10
    SELECT 1+(random()*9)::int INTO mynumber;
    RAISE NOTICE 'Start expensive step %: time to run=%', x, mynumber;
 PERFORM pg_sleep(mynumber);
    x = x + 1;
  END LOOP;

  RETURN 'End of function';
END
$BC$;
```

Pretty straightforward function: we simply emulate doing five expensive steps, and output a small notice as we go along. Running it gives this output (with pauses from 1-10 seconds of course):

```sql
<span class="c">$</span><span class="t"> psql -f slowfunc.sql</span>
DROP FUNCTION
CREATE FUNCTION
psql:slowfunc.sql:30: NOTICE:  Start of function
psql:slowfunc.sql:30: NOTICE:  Start expensive step 1: time to run=2
psql:slowfunc.sql:30: NOTICE:  Start expensive step 2: time to run=7
psql:slowfunc.sql:30: NOTICE:  Start expensive step 3: time to run=3
psql:slowfunc.sql:30: NOTICE:  Start expensive step 4: time to run=8
psql:slowfunc.sql:30: NOTICE:  Start expensive step 5: time to run=5
    slowfunc     
-----------------
 End of function
```

To grant some visibility to other processes about where we are, we’re going to change a sequence from within the function itself. First we need to decide on what sequence to use. While we could pick a common name, this won’t allow us to run the function in more than one process at a time. Therefore, we’ll create unique sequences based on the PID of the process running the function. Doing so is fairly trivial for an application: just create that sequence before the expensive function is called. For this example, we’ll use some psql tricks to achieve the same effect like so:

```sql
\t
\o tmp.drop.sql
SELECT 'DROP SEQUENCE IF EXISTS slowfuncseq_' || pg_backend_pid() || ';';
\o tmp.create.sql
SELECT 'CREATE SEQUENCE slowfuncseq_' || pg_backend_pid() || ';';
\o
\t
\i tmp.drop.sql
\i tmp.create.sql
```

From the top, this script turns off everything but tuples (so we have a clean output), then arranges for all output to go to the file named “tmp.drop.sql”. Then we build a sequence name by concatenating the string ‘slowfuncseq_‘ with the current PID. We put that into a DROP SEQUENCE statement. Then we redirect the output to a new file named “tmp.create.sql” (this closes the old one as well). We do the same thing for CREATE SEQUENCE. Finally, we stop sending things to the file, turn off “tuples only” mode, and import the two files we just created, first to drop the sequence if it exists, and then to create it. The files will look something like this:

```sql
$ more tmp.*.sql
::::::::::::::
tmp.drop.sql
::::::::::::::
DROP SEQUENCE IF EXISTS slowfuncseq_8762;

::::::::::::::
tmp.create.sql
::::::::::::::
CREATE SEQUENCE slowfuncseq_8762;
```

The only thing left is to add the calls to the sequence from within the function itself. Remember that the sequence called must exist, or the function will throw an exception, so make sure you create the sequence before the function is called! (Alternatively, you could use the same named sequence every time, but as explained before, you lose the ability to track more than one iteration of the function at a time.)

```sql
DROP FUNCTION IF EXISTS slowfunc();

CREATE FUNCTION slowfunc()
RETURNS TEXT
VOLATILE
SECURITY DEFINER
LANGUAGE plpgsql
AS $BC$
DECLARE
  x INT = 1;
  mynumber INT;
  seqname TEXT;
BEGIN
  SELECT INTO seqname 'slowfuncseq_' || pg_backend_pid();
  PERFORM nextval(seqname);

  RAISE NOTICE 'Start of function';

  WHILE x <= 5 LOOP
    -- Random number from 1 to 10
    SELECT 1+(random()*9)::int INTO mynumber;
    RAISE NOTICE 'Start expensive step %: time to run=%', x, mynumber;
 PERFORM pg_sleep(mynumber);
    PERFORM nextval(seqname);
    x = x + 1;
  END LOOP;

  RETURN 'End of function';
END
$BC$;
```

Again, it’s important that the steps become to create the sequence, run the function, and then drop the sequence. While access to sequences lives outside MVCC, creation of the sequence itself is not. Here’s what the whole thing will look like in psql:

```sql
\t
\o tmp.drop.sql
SELECT 'DROP SEQUENCE IF EXISTS slowfuncseq_' || pg_backend_pid() || ';';
\o tmp.create.sql
SELECT 'CREATE SEQUENCE slowfuncseq_' || pg_backend_pid() || ';';
\o
\t
\i tmp.drop.sql
\i tmp.create.sql
SELECT slowfunc();
\i tmp.drop.sql
```

Now you can see how far along the function is from any other process. For example, if we kick off the script above, then go into psql from another window, we can use the process id from the pg_stat_activity view to see how far along our function is:

```sql
$ select procpid, current_query from pg_stat_activity;
 procpid |                    current_query                     
---------+------------------------------------------------------
   10206 | SELECT slowfunc();
   10313 | select procpid, current_query from pg_stat_activity;

$ select last_value from slowfuncseq_10206;
 last_value 
------------
          3
```

You can assign your own values and meanings to the numbers, of course: this one simply tells us that the script is on the third iteration of our sleep loop. You could use multiple sequences to convey even more information.

There are other ways besides sequences to achieve this trick: one that I’ve used before is to have a plperlu function open a new connection to the existing database and update a text column in a simple tracking table. Another idea is to update a small semaphore table within the function, and check the modification time of the underlying file underneath your data directory.


