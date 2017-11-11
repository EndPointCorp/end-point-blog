---
author: Greg Sabino Mullane
gh_issue_number: 688
tags: database, perl, postgres
title: Pl/Perl multiplicity issues with PostgreSQL - the Highlander restriction
---



<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/09/04/plperl-multiplicity-postgres/image-0-big.jpeg" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="400" src="/blog/2012/09/04/plperl-multiplicity-postgres/image-0.jpeg" width="351"/></a></div>

I came across this error recently for a client using Postgres 8.4:

```
<span class="e">ERROR: cannot allocate multiple Perl 
interpreters on this platform</span>
```

Most times when you see this error it indicates that someone was 
trying to use both a 
[Pl/Perl function](http://www.postgresql.org/docs/current/static/plperl.html) and a 
[Pl/PerlU function](http://www.postgresql.org/docs/current/static/plperl-trusted.html) on a server in which Perl's 
multiplicity flag is disabled. In such a case, only a single Perl 
interpreter can exist for each Postgres backend, and trying to 
create a new one (as happens when you execute two functions written 
in Pl/Perl and Pl/PerlU), the error above is thrown.

However, in this case it was not a combination of Pl/Perl and 
Pl/PerlU - I confirmed that only Pl/Perl was installed. The error 
was caused by a slightly less known limitation of a non-multiplicity 
Perl and Postgres. As the docs mention at the very bottom of the page, 
"...so any one session can only execute either PL/PerlU functions, or 
PL/Perl functions that are all called by the same SQL role". So we 
had two roles both trying to execute some Pl/Perl code in the same 
session. How is that possible - isn't each session tied to a single 
role at login? The answer is the SECURITY DEFINER flag for functions, 
which causes the function to run as if it was being invoked by the 
role that created the function, not the role that is executing it.

There is still a bit of a gotcha here, because Perl interpreters 
are created as needed, and thus the order of operations is very 
important. In other words, you may be able to run function foo() 
just fine, and run function bar() just fine, but you cannot run 
them together in the same session! This applies to both the Pl/Perl 
and Pl/PerlU limitation, as well as the Pl/Perl multiple user 
limitation.

While Postgres will validate functions as you create them, this is 
subject to the same in-session limitation. All of the below examples assume 
you have a non multiplicity-enabled Perl
(see 
[the perlguts manpage](http://perldoc.perl.org/perlguts.html#How-multiple-interpreters-and-concurrency-are-supported) for gory details on what multiplicity means in Perl)
. To see what state your Perl is, 
you need to determine if the 'usemultiplicity' option is enabled. 
The **-V** option to the perl executable tells it to output all 
of its configuration parameters. While the canonical way to check is to issue a 
**perl -V:usemultiplicity**, that's a 
hard string to remember, so I simply use grep:

```
<span class="o">$ <span class="t">perl -V | grep multi</span>
 useithreads=define, usemultiplicity=define
</span>
```

The above indicates that Perl has been compiled with multiplicity 
and thus not subject to the Postgres limitations - you can mix and match 
Perl functions in your database with abandon. The only problem 
occurs if the output looks like this:

```
<span class="o">$ <span class="t">perl -V | grep multi</span>
 useithreads=undef, usemultiplicity=undef
</span>
```

Technically, you can also prevent the issue by setting ithreads on, but 
there really is no reason to not just keep things simpler by 
setting the multiplicity on.

Watch what happens when we try to create two Perl functions 
using Postgres 9.2:

```
<span class="o">postgres=# <span class="t">\c test postgres</span>
You are now connected to database "test" as user "postgres".

test=# <span class="t">create language plperl;</span>
CREATE LANGUAGE

test=# <span class="t">create language plperlu;</span>
CREATE LANGUAGE

test=# <span class="t">create or replace function test_perlver()</span>
test-# <span class="t">returns text</span>
test-# <span class="t">language plperl</span>
test-# <span class="t">AS $$ return "Running test_perlver on Perl $^V"; $$;</span>
CREATE FUNCTION

test=# <span class="t">create or replace function test_perlverU()</span>
test-# <span class="t">returns text</span>
test-# <span class="t">language plperlU</span>
test-# <span class="t">AS $$ return "Running test_perlverU on Perl $^V"; $$;</span>
<span class="e">ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "test_perlveru"</span>
</span>
```

What's going on here? We've already used a perl (Pl/Perl) in 
*this session*, so we cannot create another one, even if just 
to compile (but not execute) the function. However, if we start 
a new session, we can create our Pl/PerlU function!

```
<span class="o">test=# <span class="t">\c test postgres</span>
You are now connected to database "test" as user "postgres".

test=# <span class="t">create or replace function test_perlverU()</span>
test-# <span class="t">returns text</span>
test-# <span class="t">language plperlU</span>
test-# <span class="t">AS $$ return "Running test_perlverU on Perl $^V"; $$;</span>
CREATE FUNCTION
</span>
```

This Highlander restriction ("there can be only one!") applies to both 
creation and execution of functions. Notice that we have both the Pl/Perl
and Pl/PerlU versions installed, but we can only use one in a particular session - 
and which one depends on which is called first!:

```
<span class="o">test=# <span class="t">\c test postgres</span>
You are now connected to database "test" as user "postgres".

test=# <span class="t">select test_perlver();</span>
             test_perlver
--------------------------------------
 Running test_perlver on Perl v5.10.0

test=# <span class="t">select test_perlverU();</span>
ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "test_perlveru"

test=# <span class="t">\c test postgres</span>
You are now connected to database "test" as user "postgres".

test=# <span class="t">select test_perlverU();</span>
             test_perlveru
---------------------------------------
 Running test_perlverU on Perl v5.10.0

test=# <span class="t">select test_perlver();</span>
<span class="e">ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "test_perlver"</span>
</span>
```

As you can imagine, the nondeterministic nature of such functions can 
make discovery and debugging of this issue on production servers tricky. :)
Here's the other variant we talked about, in which only the first of two 
functions - both of which are Pl/Perl - will run:

```
<span class="o">postgres=# <span class="t">create database test;</span>
CREATE DATABASE

postgres=# <span class="t">\c test postgres</span>
You are now connected to database "test" as user "postgres".

test=# <span class="t">create language plperl;</span>
CREATE LANGUAGE

test=# <span class="t">create or replace function foo()</span>
test-# <span class="t">returns text</span>
test-# <span class="t">language plperl</span>
test-# <span class="t">security invoker</span>
test-# <span class="t">AS $$ return "Running as security invoker"; $$;</span>
CREATE FUNCTION

test=# <span class="t">create or replace function bar()</span>
test-# <span class="t">returns text</span>
test-# <span class="t">language plperl</span>
test-# <span class="t">security definer</span>
test-# <span class="t">AS $$ return "Running as security definer"; $$;</span>
CREATE FUNCTION
</span>
```

Now let's run as the user who created the function - no problemo, because we 
are the same user that created the function:

```
<span class="o">test=# <span class="t">\c test postgres</span>
You are now connected to database "test" as user "postgres".

test=# <span class="t">SELECT foo();</span>
           foo
-----------------------------
 Running as security invoker
(1 row)

test=# <span class="t">SELECT bar();</span>
           bar
-----------------------------
 Running as security definer
(1 row)
</span>
```

All is well. However, if we try it as a different user, the Highlander restriction 
creeps in:

```
<span class="o">test=# <span class="t">\c test greg</span>
You are now connected to database "test" as user "greg".

test=# <span class="t">SELECT foo();</span>
           foo
-----------------------------
 Running as security invoker
(1 row)

test=# <span class="t">SELECT bar();</span>
<span class="e">ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "bar"</span>

test=# <span class="t">\c test greg</span>
You are now connected to database "test" as user "greg".

test=# <span class="t">SELECT bar();</span>
           bar
-----------------------------
 Running as security definer
(1 row)

test=# <span class="t">SELECT foo();</span>
<span class="e">ERROR:  cannot allocate multiple Perl interpreters on this platform
CONTEXT:  compilation of PL/Perl function "foo"</span>
</span>
```

This one took me a while to figure out on a production system, as 
somewhere in a twisty maze of trigger functions there was one that 
was set as security definer. Normally, this was not a problem, as 
the user that created that function did much of the updates, but 
a different user invoked a non- security definer function and then 
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


