---
author: Josh Tolley
title: "Using pgTAP to automate database testing"
date: 2022-03-16
tags:
- sql
- postgres
- database
- testing
- security
github_issue_number: 1844
---

![Old piano outdoors, focused on keyboard with most keytops missing and some snow on it](/blog/2022/03/using-pgtap-automate-database-testing/piano.webp)
Photo from [PxHere](https://pxhere.com/en/photo/1292458)

Recently I started learning to tune pianos. There are many techniques and variations, but the traditional method, and the one apparently most accepted by ardent piano tuning purists, involves tuning one note to a reference, tuning several other notes in relation to the first, and testing the results by listening closely to different combinations of notes.

The tuner adjusts each new note in relation to several previously tuned notes. Physics being what it is, no piano can play all its tones perfectly, and one of the tricks of it all is adjusting each note to minimize audible imperfections. The tuner achieves this with an exacting series of musical intervals tested against each other.

### Databases need tests too

One of our customers needed to add security policies to their PostgreSQL database, to limit data visibility for certain new users. This can quickly become complicated and ticklish, ensuring that the rules work properly for the affected users while leaving other users unmolested.

This struck me as an excellent opportunity to create some unit tests, not that there's any short supply of good opportunities to add unit tests! This is not just because it helps prove that these security policies really do work properly, but because (confession time) I recently did a similar project for a different database without the help of unit tests, and it wasn't much fun.

So this seemed like a good time to use [pgTAP](https://pgtap.org/), a set of database functions designed to allow writing unit tests within the database itself. They produce ["Test Anything Protocol" (TAP)](http://testanything.org/) output, a simple protocol that displays unit test results in an easily understood report.

### What to test?

A good first step in writing unit tests is deciding on something to test. In my case, I figured I should make sure row-level security policies were turned on for the tables I was interested in, which is available from the `rowsecurity` field in the `pg_tables` view:

```sql
select ok(rowsecurity, tablename || ' has row security enabled') from pg_tables
    where schemaname = 'public'
        and (
            tablename in (
                -- ... some hard coded table names
            ) or tablename like 'some_other_tables_%'
        );
```

The `ok()` function comes from pgTAP. It counts as one test each time it's called; the test passes when the first argument is true, and fails when the argument is something else. The second argument is an optional comment describing what's being tested. Following a pretty common TAP-related naming convention, I put this in a file called `00-test.sql` in a directory under the root of my project, simply called `t`.

A more complicated set of tests could include several different files, where the numeric part of the name helps sort the tests in the desired run order, and the rest of the filename describes the subject of the tests within. But this will do just to get started. I can run it with `pg_prove`, included with the pgTAP package:

```sh
pg_prove -d mydatabase t/00-test.sql
```

### Iteratively improving

This fails, for several reasons.

First, I haven't yet installed the pgTAP extension in my database, with `CREATE EXTENSION pgtap`.

I also haven't actually done anything in my test to run the code I'm testing. The actual code in this project consists of some database functions, which we need to run to create the database security policies, and I haven't run any of them yet.

And finally, pgTAP requires me to "plan" my tests first, or in other words, I need to inform pgTAP how many tests I plan to run, before I run them. It's also nice to call `finish()` so pgTAP can clean up after itself.

I installed the pgTAP extension in my database, and modified the test as follows:

```sql
begin;

\i create_policy.sql

select plan(1);  -- plan for a single test

select ok(rowsecurity, tablename || ' has row security enabled') from pg_tables
    where schemaname = 'public'
        and (
            tablename in (
                -- ... some hard coded table names
            ) or tablename like 'some_other_tables_%'
        );

select finish();

rollback;
```

This wraps my test in a transaction, so that I can roll everything back to leave the database essentially as I found it. It also calls the actual code I'm testing, in `create_policy.sql`, and plans one test. And it gives me this new failure:

```plain
t/m.sql .. All 1 subtests passed

Test Summary Report
-------------------
t/m.sql (Wstat: 0 Tests: 226 Failed: 225)
  Failed tests:  2-226
Parse errors: Bad plan.  You planned 1 tests but ran 226.
Files=1, Tests=226,  1 wallclock secs ( 0.04 usr  0.00 sys +  0.03 cusr  0.01 csys =  0.08 CPU)
Result: FAIL
```

The problem here is that each call to `ok()` counts as one test, and my test apparently found 226 tables to check for row-level security. I can improve the planning like this:

```sql
select plan(count(*)::integer)
    from pg_tables where schemaname = 'public'
        and (
            tablename in (
                -- ... some hard coded table names
            ) or tablename like 'some_other_tables_%'
        );
```

`count()` returns a `bigint`, and `plan()` expects `integer`, so this requires a typecast, but is otherwise pretty simple. And now my tests pass:

```plain
josh@here:~dw$ pg_prove -d nedss t/00-test.sql
t/00-test.sql .. ok
All tests successful.
Files=1, Tests=226,  1 wallclock secs ( 0.03 usr  0.01 sys +  0.03 cusr  0.01 csys =  0.08 CPU)
Result: PASS
```

### Looking back and ahead

Suffice it to say that pgTAP includes many functions similar to `ok()`, to test various aspects of the database, its structure, and its behavior, and I'd recommend interested users review [the documentation](https://pgtap.org/documentation.html) for more details. I intended this post only as an introduction.

In its completed state, my test suite comprised several tests ensuring various required preliminaries were in place, a few tests like the one above that check for necessary table-specific settings, others that ensure the affected roles were created, and finally some which create some sample data and use `SET ROLE` to test the data visibility directly for roles with various policies applied.

And to be honest, I was surprised at the sense of security that came over me with this completed test suite. As I mentioned, I'd done similar work previously, and knew that although I was confident in the code when it was written, that confidence came only through fairly extensive manual testing. I know very well the struggles of bit rot, and I knew it would be at least as hard to repeat that testing regimen by hand sometime down the road after a year or two.

I also recognized that if I ever needed to set up similar policies again, I could use these tests themselves as a reference, because they show exactly how to run the code in question. Though of course I included that information in the project's associated `README` file as well ... right?

Let us know if you've used pgTAP, and what effect it has had on your database development.
