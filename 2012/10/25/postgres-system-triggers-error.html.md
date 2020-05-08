---
author: Greg Sabino Mullane
gh_issue_number: 712
tags: database, postgres, rails
title: 'Postgres system triggers error: permission denied'
---

This mystifying Postgres error popped up for one of my coworkers lately while using Ruby on Rails:

```plain
ERROR:  permission denied: "RI_ConstraintTrigger_16410" is a system trigger
```

On PostgreSQL version 9.2 and newer, the error may look like this:

```plain
ERROR:  permission denied: "RI_ConstraintTrigger_a_32778" is a system trigger

ERROR:  permission denied: "RI_ConstraintTrigger_c_32780" is a system trigger
```

I labelled this as mystifying because, while Postgres’ error system is generally 
well designed and gives clear messages, this one stinks. A better one would 
be something similar to:

```plain
ERROR:  Cannot disable triggers on a table containing foreign keys unless superuser
```

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2012/10/25/postgres-system-triggers-error/image-0-big.png" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" src="/blog/2012/10/25/postgres-system-triggers-error/image-0.png"/></a></div>

As you can now guess, this error is caused by a non-superuser trying to disable triggers 
on a table that is used in a foreign key relationship, via the SQL command:

```sql
ALTER TABLE foobar DISABLE TRIGGERS ALL;
```

Because Postgres 
enforces foreign keys through the use of triggers, and because data 
integrity is very important to Postgres, one must be 
a superuser to perform such an action and bypass the foreign keys. (A superuser 
is a Postgres role that has “do anything” privileges). 
We’ll look at an example of this in action, and then discuss solutions 
and workarounds.

Note that if you are not a superuser *and* you are not the owner of the 
table, you will get a much better error message when you try to disable 
all the triggers:

```plain
ERROR:  must be owner of relation foobar
```

To reproduce the original error, we will create two tables, and then link them together 
via a foreign key:

```plain
postgres=# create user alice;
CREATE ROLE

postgres=# \c postgres alice
You are now connected to database "postgres" as user "alice".

-- Verify that we are not a superuser
postgres=> select usename, usesuper from pg_user where usename = (select current_user);
 usename | usesuper 
---------+----------
 alice   | f

postgres=> create table foo(a int unique);
NOTICE:  CREATE TABLE / UNIQUE will create implicit index "foo_a_key" for table "foo"
CREATE TABLE

postgres=> create table bar(b int);
CREATE TABLE

postgres=> alter table bar add constraint baz foreign key (b) references foo(a);
ALTER TABLE
```

Let’s take a look at both tables, and then try to disable triggers on each one. 
Because the triggers enforcing the foreign key are internal, they will not show up 
when we do a `\d`:

```plain
postgres=> \d foo
      Table "public.foo"
 Column |  Type   | Modifiers 
--------+---------+-----------
 a      | integer | 
Indexes:
    "foo_a_key" UNIQUE CONSTRAINT, btree (a)
Referenced by:
    TABLE "bar" CONSTRAINT "baz" FOREIGN KEY (b) REFERENCES foo(a)

postgres=> \d bar
      Table "public.bar"
 Column |  Type   | Modifiers 
--------+---------+-----------
 b      | integer | 
Foreign-key constraints:
    "baz" FOREIGN KEY (b) REFERENCES foo(a)

postgres=> alter table foo disable trigger all;
ERROR:  permission denied: "RI_ConstraintTrigger_41047" is a system trigger

postgres=> alter table bar disable trigger all;
ERROR:  permission denied: "RI_ConstraintTrigger_41049" is a system trigger
```

If we try the same thing as a superuser, we have no problem:

```plain
postgres=# \c postgres postgres
You are now connected to database "postgres" as user "postgres".

postgres=# select usename, usesuper from pg_user where usename = (select current_user);
 usename  | usesuper 
----------+----------
 postgres | t

postgres=# alter table foo disable trigger all;
ALTER TABLE

postgres=# alter table bar disable trigger all;
ALTER TABLE

-- Don’t forget to re-enable the triggers!

postgres=# alter table foo enable trigger all;
ALTER TABLE

postgres=# alter table bar enable trigger all;
ALTER TABLE
```

So, this error has happened to you - now what? Well, it depends on exactly 
what you are trying to do, and how much control over your environment you have. If you are 
using Ruby on Rails, for example, you may not be able to change anything 
except the running user. As you may imagine, this is the 
most obvious solution: **become a superuser** and run the command, as in the example above.

If you do have the ability to run as a superuser however, it is usually 
much easier to **adjust the session_replication_role**. In short, this 
disables *all* triggers and rules, on all tables, until it is switched 
back again. Do NOT forget to switch it back again! Usage is like this:

```plain
postgres=# \c postgres postgres
You are now connected to database "postgres" as user "postgres".

postgres=# set session_replication_role to replica;
SET

-- Do what you need to do - triggers and rules will not fire!

postgres=# set session_replication_role to default;
SET
```

Note: While you can do “SET LOCAL” to limit the changes to the current 
transaction, I always feel safer to explicitly set it before and after 
the changes, rather than relying on the implicit change back via 
commit and rollback.

It may be that you are simply trying to disable one or more of the 
"normal” triggers that appear on the table. In which case, you can 
simply **disable user triggers manually** rather than use “all”:

```plain
postgres=# \c postgres alice
You are now connected to database "postgres" as user "alice".

postgres=> \d bar
      Table "public.bar"
 Column |  Type   | Modifiers 
--------+---------+-----------
 b      | integer | 
Foreign-key constraints:
    "baz" FOREIGN KEY (b) REFERENCES foo(a)
Triggers:
    trunk AFTER INSERT ON bar FOR EACH STATEMENT EXECUTE PROCEDURE funk()
    vupd BEFORE UPDATE ON bar FOR EACH ROW EXECUTE PROCEDURE verify_update();

postgres=> alter table bar disable trigger trunk;
ALTER TABLE

postgres=> alter table bar disable trigger vupd;
ALTER TABLE

-- Do what you need to do, then:

postgres=> alter table bar enable trigger trunk;
ALTER TABLE

postgres=> alter table bar enable trigger vupd;
ALTER TABLE
```

Another option for a regular user (in other words, a non super-user) 
is to remove the foreign key relationship yourself. You cannot disable 
the trigger, but you can **drop the foreign key** that created it in 
the first place. Of course, you have to add it back in as well:

```plain
postgres=# \c postgres alice
You are now connected to database "postgres" as user "alice".

postgres=> alter table bar drop constraint baz;
ALTER TABLE

-- Do what you need to do then:

postgres=> alter table bar add constraint baz foreign key (b) references foo(a);
ALTER TABLE
```

The final solution is to work around the problem. Do you really 
need to disable triggers on this table? Then you can simply 
**not disable any triggers**. Perhaps the action you 
are ultimately trying to do (e.g. update/delete/insert to the table) 
can be performed some other way.

All of these solutions have their advantages and disadvantages. 
And that’s what charts are good for!:

<table>
<tbody><tr class="h1">
<th colspan="3">Permission denied: "RI_ConstraintTrigger" is a system trigger - now what?</th>
</tr>

<tr class="h2">
<th>Solution</th>
<th>Good</th>
<th>Bad</th>
</tr>

<tr class="a">
<th>Become a superuser</th>
<td>Works as you expect it to</td>
<td>Locks the table<br/>Must re-enable triggers</td>
</tr>

<tr class="b">
<th>Adjust session_replication_role</th>
<td>No table locks!<br/>Bypasses triggers and rules on ALL tables</td>
<td>Must be superuser<br/>MUST set it back to default setting</td>
</tr>

<tr class="a">
<th>Disable user triggers manually</th>
<td>Regular users can perform<br/>Very clear what is being done<br/>Less damage if forget to re-enable</td>
<td>Locks the table<br/>May not be enough</td>
</tr>

<tr class="b">
<th>Drop the foreign key</th>
<td>Regular users can perform<br/>Very clear what is being done</td>
<td>Locks the tables<br/>Must recreate the foreign key</td>
</tr>

<tr class="a">
<th>Not disable any triggers</th>
<td>No locking<br/>Nothing to remember to re-enable</td>
<td>May not work in all situations</td>
</tr>
</tbody></table>

For the rest of this article, we will tie up two loose ends. First, 
how can we see the triggers if `\d` will not show them? Second, what’s 
up with the crappy trigger name?

As seen above, the output of `\d` in the psql program shows us the triggers 
on a table, but not the internal system triggers, such as those created 
by foreign keys. Here is how triggers normally appear:

```plain
postgres=# \c postgres postgres
You are now connected to database "postgres" as user "postgres".

postgres=# create language plperl;
CREATE LANGUAGE

postgres=# create function funk() returns trigger language plperl as $$ return undef; $$;
CREATE FUNCTION

postgres=# create trigger trunk after insert on bar for each statement execute procedure funk();
CREATE TRIGGER

postgres=# \d bar
      Table "public.bar"
 Column |  Type   | Modifiers 
--------+---------+-----------
 b      | integer | 
Foreign-key constraints:
    "baz" FOREIGN KEY (b) REFERENCES foo(a)
Triggers:
    trunk AFTER INSERT ON bar FOR EACH STATEMENT EXECUTE PROCEDURE funk()

postgres=# alter table bar disable trigger all;
ALTER TABLE

postgres=# \d bar
      Table "public.bar"
 Column |  Type   | Modifiers 
--------+---------+-----------
 b      | integer | 
Foreign-key constraints:
    "baz" FOREIGN KEY (b) REFERENCES foo(a)
Disabled triggers:
    trunk AFTER INSERT ON bar FOR EACH STATEMENT EXECUTE PROCEDURE funk()
```

Warning: Versions older than 8.3 will not tell you in the `\d` output 
that the trigger is disabled! Yet another reason to upgrade as soon 
as possible because 
[8.2 and earlier are end of life](https://www.postgresql.org/support/versioning/).

If you want to see all the triggers on a table, even the internal ones, 
you will need to look at the pg_trigger table directly. Here is the query 
that psql uses when generating a list of triggers on a table. Note the 
exclusion based on the tgisinternal column:

```plain
SELECT t.tgname, pg_catalog.pg_get_triggerdef(t.oid, true), t.tgenabled
FROM pg_catalog.pg_trigger t
WHERE t.tgrelid = '32774' AND NOT t.tgisinternal
ORDER BY 1;
```

So in our example table above, we should find the trigger we created, as well as the 
two triggers created by the foreign key. All of them are enabled. Disabled 
triggers will show as a ‘D’ in the tgenabled column. (O stands for origin, 
and has to do with session_replication_role).

```plain
postgres=# select tgname,tgenabled,tgisinternal from pg_trigger 
postgres-#  where tgrelid = 'bar'::regclass;
            tgname            | tgenabled | tgisinternal 
------------------------------+-----------+--------------
 RI_ConstraintTrigger_c_32780 | D         | t
 RI_ConstraintTrigger_c_32781 | D         | t
 trunk                        | D         | f

postgres=# alter table bar enable trigger all;
ALTER TABLE

postgres=# select tgname,tgenabled,tgisinternal from pg_trigger
postgres-#  where tgrelid = 'bar'::regclass;
            tgname            | tgenabled | tgisinternal 
------------------------------+-----------+--------------
 RI_ConstraintTrigger_c_32780 | O         | t
 RI_ConstraintTrigger_c_32781 | O         | t
 trunk                        | O         | f

```

As you recall, the original error — with the system trigger that had a rather 
non-intuitive name — looked like this:

```plain
ERROR:  permission denied: "RI_ConstraintTrigger_16509" is a system trigger
```

We can break it apart to see what it is doing. The “RI” is short for 
"Referential Integrity", and anyone who manages to figure that out can 
probably make a good guess as to what it does. The “Constraint” means 
it is a constraint on the table - okay, simple enough. The “Trigger” 
is a little redundant, as it is extraordinarily unlikely you will ever come across 
this trigger without some context (such as the error message above) that 
tells you it is a trigger. The final number is simply the oid 
of the trigger itself. Stick them all together and you get a fairly obscure trigger name that is hopefully not as mysterious now!
