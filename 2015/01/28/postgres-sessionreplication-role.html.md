---
author: Greg Sabino Mullane
gh_issue_number: 1077
tags: bucardo, postgres, replication
title: Postgres session_replication role - Bucardo and Slony's powerful ally
---

One of the lesser known Postgres parameters is also one of the most powerful: **session_replication_role**. In a nutshell, it allows you to completely bypass all triggers and rules for a specified amount of time. This was invented to allow replication systems to bypass all foreign keys and user triggers, but also can be used to greatly speed up bulk loading and updating.

<div class="separator" style="clear: both; float:right; margin: 1em 1em 2em 1em; text-align: center;"><a href="/blog/2015/01/28/postgres-sessionreplication-role/image-0-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/01/28/postgres-sessionreplication-role/image-0.png"/></a>
<br/><small>(<a href="https://flic.kr/p/exW64Z">Triggerfish</a> picture by <a href="https://www.flickr.com/photos/96698561@N05/">Shayne Thomas</a>)</small>
</div>

### The problem with disabling triggers

Once upon a time, there were two replication systems, [Slony](http://slony.info/) and [Bucardo](http://bucardo.org/wiki/Bucardo), that both shared the same problem: triggers (and rules) on a "target" table could really mess things up. In general, when you are replicating table information, you only want to replicate the data itself, and avoid any side effects. In other words, you need to prevent any "post-processing" of the data, which is what rules and triggers may do. The disabling of those was done in a fairly standard, but very ugly method: updating the system catalogs for the tables in question to trick Postgres into thinking that there were no rules or triggers. Here's what such SQL looks like in the Bucardo source code:

```
$SQL = q{
    UPDATE pg_class
    SET    reltriggers = 0, relhasrules = false
    WHERE  (
};
$SQL .= join "OR\n"
    => map { "(oid = '$_->{safeschema}.$_->{safetable}'::regclass)" }
      grep { $_->{reltype} eq 'table' }
      @$goatlist;
$SQL .= ')';
```

This had a number of bad side effects. First and foremost, updating the system catalogs is never a recommended step. While it is *possible*, it is certainly discouraged. Because access to the system catalogs do not follow strict MVCC rules, odd things can sometimes happen. Another problem is that editing the system catalogs causes locking issues, as well as bloat on the system tables themselves. Yet another problem is that it was tricky do get this right; even the format of the system catalogs change over time, so that your code would need to have alternate paths for disabling and enabling triggers depending on the version of Postgres in use. Finally, the size of the SQL statements needed grew with the number of tables to be replicated: in other words, you had to specifically disable and enable each table. All in all, quite a mess.

### The solution to disabling triggers

The solution was to get away from editing the system catalogs altogether, and provide a cleaner way to temporarily disable all triggers and rules on tables. Jan Wieck, the inventor of Slony, wrote a new user parameter and named it "session_replication_role". As you can tell by the name, this is a session-level setting. In other words, only the current user will see the effects of setting this, and it will last as long as your session does (which is basically equivalent to as long as you are connected to the database). This setting applied to all tables, and can be used to instruct Postgres to not worry about triggers or rules at all. So the new code becomes:

```
$SQL = q{SET session_replication_role TO 'replica'};
```

Much cleaner, eh? (you may see session_replication_role abbreviated as s_r_r or simply srr, but Postgres itself needs it spelled out). You might have noticed that we are setting it to 'replica', and not 'on' and 'off'. The actual way this parameter works is to specify which types of triggers should be fired. Previous to this patch, triggers were all of one type, and the only characteristic they could have was "enabled" or "disabled". Now, a trigger can have one of four states: **origin**, **always**, **replica**, or **disabled** (stored in the 'tgenabled' field of the pg_trigger table as 'O', 'A', 'R', or 'D'). By default, all triggers that are created are of type 'origin'. This applies to the implicitly created system triggers used by foreign keys as well. Thus, when session_replication_role is set to replica, only triggers of the type 'replica' will fire - and not the foreign key enforcing ones. If you really need a user trigger to fire on a replica (aka target) table, you can adjust that trigger to be of type replica. Note that this trigger will *only* fire when session_replication_role is set to replica, and thus will be invisible in day to day use.

Once the replication is done, session_replication_role can be set back to the normal setting like so:

```
$SQL = q{SET session_replication_role TO 'origin'};
```

You can also set it to DEFAULT, which in theory could be different from origin as one can set the default session_replication_role to something other than origin inside of the postgresql.conf file. However, it is much cleaner to always specify the exact role you want; I have not come across a use case that required changing the default from origin.

This feature only exists in Postgres 8.3 or better. As such, Bucardo still contains the old system catalog manipulation code, as it supports versions older than 8.3, but it uses session_replication_role whenever possible. Slony always uses one or the other, as it made session_replication_role a backwards-incompatible change in its major version. Thus, to replicate versions of Postgres before 8.3, you need to use the older Slony 1.2

There are some good use cases other than a replication system for using this feature. The most common is simply bulk loading or bulk updating when you do not want the effects of the triggers, or simply do not want the performance hit. Remember that system triggers are disabled as well, so use this with care (this is one of the reasons you must be a superuser to change the session_replication_role parameter).

What if you are not a superuser and need to disable triggers and/or rules? You could create a wrapper function that runs as a superuser. The big downside to that is the all-or-nothing nature of session_replication_role. Once it is changed, it is changed for *everything*, so handing that power to a normal user could be dangerous. My colleague Mark Johnson came up with [another great solution](http://blog.endpoint.com/2012/09/enforcing-transaction-compartments-with.html): a function that runs as the superuser, and does the old-style system catalog manipulations, but uses an ingenious foreign key trick to ensure that the matching "enable" function *must* be run. Great for fine-grained control of table triggers.

You might wonder about the other setting, "local". It's used mostly to have a third type of trigger, for times when you want "normal" triggers to fire, but want some way to differentiate from "origin" mode. Slony uses this setting when it does some of it DDL trickery, [peruse the Slony documentation](http://slony.info/documentation/triggers.html) for more details.

Postgres will also show you what state a trigger is in when you are viewing a table using the "backslash-d" command inside of [psql](http://www.postgresql.org/docs/current/static/app-psql.html). Here are some examples. Remember that psql never shows "system-level" triggers, but they are there, as we shall see below. First, let's create two test tables linked by a foreign key, and a trigger with supporting function that raises a simple notice when fired:

```
greg=# create table foo (id int primary key);
CREATE TABLE
greg=# create table bar(id int primary key, fooid int references foo(id));
CREATE TABLE
greg=# insert into foo values (1),(2),(3);
INSERT 0 3
greg=# insert into bar values (10,1), (11,2);
INSERT 0 2

greg=# create function alertalert() returns trigger language plpgsql AS $$ BEGIN RAISE NOTICE 'cookie dough'; RETURN null; END $$;
CREATE FUNCTION

greg=# create trigger mytrig after update on foo for each statement execute procedure alertalert();
CREATE TRIGGER
```

Now that those are setup, let's see what psql shows us about each table:

```
greg=# \d foo
      Table "public.foo"
 Column |  Type   | Modifiers
--------+---------+-----------
 id     | integer | not null
Indexes:
    "foo_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "bar" CONSTRAINT "bar_fooid_fkey" FOREIGN KEY (fooid) REFERENCES foo(id)
Triggers:
    mytrig AFTER UPDATE ON foo FOR EACH STATEMENT EXECUTE PROCEDURE alertalert()

greg=# \d bar
      Table "public.bar"
 Column |  Type   | Modifiers
--------+---------+-----------
 id     | integer | not null
 fooid  | integer |
Indexes:
    "bar_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "bar_fooid_fkey" FOREIGN KEY (fooid) REFERENCES foo(id)
```

Everything looks good. Let's see the trigger in action:

```
greg=# update foo set id=id;
NOTICE:  cookie dough
UPDATE 3
```

Although the output of psql only shows a single trigger on the foo table, their are actually two others, created by the foreign key, which helps to enforce the foreign key relationship. We can see them by looking at the pg_trigger table:

```

greg=# select tgname, tgenabled, tgisinternal, tgconstraint from pg_trigger where tgrelid::regclass::text = 'foo';
            tgname            | tgenabled | tgisinternal | tgconstraint
------------------------------+-----------+--------------+--------------
 RI_ConstraintTrigger_a_73776 | O         | t            |        45313
 RI_ConstraintTrigger_a_57169 | O         | t            |        45313
 mytrig                       | O         | f            |            0
(3 rows)
```

We can see that they are internal triggers (which prevents psql from showing them), and that they have an associated constraint. Let's make sure these triggers are doing their job by causing one of them to fire and complain that the underlying constraint is being violated:

```
## Try and fail to delete id 1, which is being referenced by the table bar:
greg=# delete from foo where id = 1;
ERROR:  update or delete on table "foo" violates foreign key constraint "bar_fooid_fkey" on table "bar"
DETAIL:  Key (id)=(1) is still referenced from table "bar".
## Check the name of the constraint referenced above by pg_trigger:
greg=# select conname, contype from pg_constraint where oid = 45313;
    conname     | contype
----------------+---------
 bar_fooid_fkey | f
```

Time to demonstrate the power and danger of the session_replication_role attribute. First let's set it to 'replica' and verify that all triggers fail to fire. We should be able to perform the  "illegal" deletion we tried before, and an update should fail to raise any notice at all:

```
greg=# show session_replication_role;
 session_replication_role
--------------------------
 origin
greg=# set session_replication_role = 'replica';
SET
greg=# delete from foo where id = 1;
DELETE 1
greg=# update foo set id=id;
UPDATE 2
greg=# show session_replication_role;
 session_replication_role
--------------------------
 replica
```

Let's force our trigger to fire by setting it to replica:

```
greg=# alter table foo enable replica trigger mytrig;
ALTER TABLE
greg=# \d foo
      Table "public.foo"
 Column |  Type   | Modifiers
--------+---------+-----------
 id     | integer | not null
Indexes:
    "foo_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "bar" CONSTRAINT "bar_fooid_fkey" FOREIGN KEY (fooid) REFERENCES foo(id)
Triggers firing on replica only:
    mytrig AFTER UPDATE ON foo FOR EACH STATEMENT EXECUTE PROCEDURE alertalert()
greg=# set session_replication_role = 'replica';
SET
greg=# update foo set id=id;
NOTICE:  cookie dough
UPDATE 2
```

So what is the consequence of the above DELETE command? The foreign key relationship is now a lie, as there are rows in **bar** that do not point to a row in **foo**!

```
greg=# select * from bar where not exists (select 1 from foo where fooid = foo.id);
 id | fooid
----+-------
  1 |     1
(1 row)
```

Ouch! This shows why session_replication_role is such a dangerous tool (indeed, this is the primary reason it is only allowed to be changed by superusers). If you find yourself reaching for this tool, don't. But if you really have to, double-check everything twice, and make sure you always change it back to 'origin' as soon as possible.
