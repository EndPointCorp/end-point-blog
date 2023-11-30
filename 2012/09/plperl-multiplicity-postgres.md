---
author: Greg Sabino Mullane
title: "PL/Perl multiplicity issues with PostgreSQL: the Highlander restriction"
github_issue_number: 688
tags:
- database
- perl
- postgres
date: 2012-09-04
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/09/plperl-multiplicity-postgres/image-0-big.jpeg" style="clear:both; float:center; margin-left:1em; margin-bottom:1em"><img border="0" height="400" src="/blog/2012/09/plperl-multiplicity-postgres/image-0.jpeg" width="351"/></a></div>

I came across this error recently for a client using PostgreSQL 8.4:

```plain
ERROR: cannot allocate multiple Perl interpreters on this platform
```

Most times when you see this error it indicates that someone was
trying to use both a
[PL/Perl function](https://www.postgresql.org/docs/current/static/plperl.html) and a
[PL/PerlU function](https://www.postgresql.org/docs/current/static/plperl-trusted.html) on a server in which Perl's
multiplicity flag is disabled. In such a case, only a single Perl
interpreter can exist for each Postgres backend, and trying to
create a new one, as happens when you execute two functions written
in PL/Perl and PL/PerlU, the error above is thrown.

However, in this case it was not a combination of PL/Perl and
PL/PerlU — I confirmed that only PL/Perl was installed. The error
was caused by a slightly less known limitation of a non-multiplicity
Perl and Postgres. As the docs mention at the very bottom of the page,
"...so any one session can only execute either PL/PerlU functions, or
PL/Perl functions that are all called by the same SQL role". So we
had two roles both trying to execute some PL/Perl code in the same
session. How is that possible — isn't each session tied to a single
role at login? The answer is the SECURITY DEFINER flag for functions,
which causes the function to run as if it was being invoked by the
role that created the function, not the role that is executing it.

There is still a bit of a gotcha here, because Perl interpreters
are created as needed, and thus the order of operations is very
important. In other words, you may be able to run function `foo()`
just fine, and run function `bar()` just fine, but you cannot run
them together in the same session! This applies to both the PL/Perl
and PL/PerlU limitation, as well as the PL/Perl multiple user
limitation.

While Postgres will validate functions as you create them, this is
subject to the same in-session limitation. All of the below examples assume
you have a non multiplicity-enabled Perl. (See
[the perlguts manpage](https://perldoc.perl.org/perlguts.html#How-multiple-interpreters-and-concurrency-are-supported) for gory details on what multiplicity means in Perl.)

To see what state your Perl is, you need to determine if the
'usemultiplicity' option is enabled. The `-V` option to the perl
executable tells it to output all of its configuration parameters. While
the canonical way to check is to issue a `perl -V:usemultiplicity`,
that's a hard string to remember, so I simply use grep:

```plain
$ perl -V | grep multi
 useithreads=define, usemultiplicity=define
```

The above indicates that Perl has been compiled with multiplicity
and thus not subject to the Postgres limitations — you can mix and match
Perl functions in your database with abandon. The only problem
occurs if the output looks like this:

```plain
$ perl -V | grep multi
 useithreads=undef, usemultiplicity=undef
```

Technically, you can also prevent the issue by setting `ithreads` on, but
there really is no reason to not just keep things simpler by
setting the multiplicity on.

Watch what happens when we try to create two Perl functions
using Postgres 9.2:

```plain
postgres=# \c test postgres
You are now connected to database "test" as user "postgres".

test=# create language plperl;
CREATE LANGUAGE

test=# create language plperlu;
CREATE LANGUAGE

test=# create or replace function test_perlver()
test-# returns text
test-# language plperl
test-# AS $$ return "Running test_perlver on Perl $^V"; $$;
CREATE FUNCTION

test=# create or replace function test_perlverU()
test-# returns text
test-# language plperlU
test-# AS $$ return "Running test_perlverU on Perl $^V"; $$;
ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "test_perlveru"
```

What's going on here? We've already used a perl (PL/Perl) in
*this session*, so we cannot create another one, even if just
to compile (but not execute) the function. However, if we start
a new session, we can create our PL/PerlU function!

```plain
test=# \c test postgres
You are now connected to database "test" as user "postgres".

test=# create or replace function test_perlverU()
test-# returns text
test-# language plperlU
test-# AS $$ return "Running test_perlverU on Perl $^V"; $$;
CREATE FUNCTION
```

This Highlander restriction (“there can be only one!”) applies to both
creation and execution of functions. Notice that we have both the PL/Perl
and PL/PerlU versions installed, but we can only use one in a particular session —
and which one depends on which is called first!

```plain
test=# \c test postgres
You are now connected to database "test" as user "postgres".

test=# select test_perlver();
             test_perlver
--------------------------------------
 Running test_perlver on Perl v5.10.0

test=# select test_perlverU();
ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "test_perlveru"

test=# \c test postgres
You are now connected to database "test" as user "postgres".

test=# select test_perlverU();
             test_perlveru
---------------------------------------
 Running test_perlverU on Perl v5.10.0

test=# select test_perlver();
ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "test_perlver"
```

As you can imagine, the nondeterministic nature of such functions can
make discovery and debugging of this issue on production servers tricky. :)
Here's the other variant we talked about, in which only the first of two
functions — both of which are PL/Perl — will run:

```plain
postgres=# create database test;
CREATE DATABASE

postgres=# \c test postgres
You are now connected to database "test" as user "postgres".

test=# create language plperl;
CREATE LANGUAGE

test=# create or replace function foo()
test-# returns text
test-# language plperl
test-# security invoker
test-# AS $$ return "Running as security invoker"; $$;
CREATE FUNCTION

test=# create or replace function bar()
test-# returns text
test-# language plperl
test-# security definer
test-# AS $$ return "Running as security definer"; $$;
CREATE FUNCTION
```

Now let's run as the user who created the function — no problemo, because we
are the same user that created the function:

```plain
test=# \c test postgres
You are now connected to database "test" as user "postgres".

test=# SELECT foo();
           foo
-----------------------------
 Running as security invoker
(1 row)

test=# SELECT bar();
           bar
-----------------------------
 Running as security definer
(1 row)
```

All is well. However, if we try it as a different user, the Highlander restriction
creeps in:

```plain
test=# \c test greg
You are now connected to database "test" as user "greg".

test=# SELECT foo();
           foo
-----------------------------
 Running as security invoker
(1 row)

test=# SELECT bar();
ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "bar"

test=# \c test greg
You are now connected to database "test" as user "greg".

test=# SELECT bar();
           bar
-----------------------------
 Running as security definer
(1 row)

test=# SELECT foo();
ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "foo"
```

This one took me a while to figure out on a production system, as
somewhere in a twisty maze of trigger functions there was one that
was set as security definer. Normally, this was not a problem, as
the user that created that function did much of the updates, but
a different user invoked a non-security definer function and then
the security definer function, causing the error at the top of
this article to show up.

So what can one do to prevent this problem from occurring? Luckily,
for most people this will not be a problem, as many (if not all)
distros and operating systems have the multiplicity compile flag
for Perl enabled. If you do have the restriction, one option is to
simply be careful about the use of security definer functions. You
could either declare everything as security definer, or perhaps make
sure that it is only called in a separate session if it really needs
to be called by a different user.

A better solution is to recompile your Perl to enable multiplicity.
I am not aware of any drawbacks to doing so. In theory, one could
even recompile Perl in-place and then restart Postgres, but I have
never tried this out. :)
