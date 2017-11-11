---
author: Greg Sabino Mullane
gh_issue_number: 1044
tags: postgres
title: Postgres copy schema with pg_dump
---



<div class="separator" style="clear: both; float:right; text-align: center; padding-bottom: 1px"><a href="/blog/2014/10/09/postgres-copy-schema-with-pgdump/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/10/09/postgres-copy-schema-with-pgdump/image-0.jpeg"/></a>
<br/><small><a href="http://en.wikipedia.org/wiki/Grim_Fandango">Manny Calavera</a> (animated by Lua!)<br/><a href="https://flic.kr/p/6mkS3M">Image</a> by <a href="https://www.flickr.com/photos/kittwalker/">Kitt Walker</a></small></div>

Someone on the #postgresql IRC channel was asking how to make a copy of a schema; presented here are a few solutions and some wrinkles I found along the way. The goal is to create a new schema based on an existing one, in which everything is an exact copy. For all of the examples, 'alpha' is the existing, data-filled schema, and 'beta' is the newly created one. It should be noted that creating a copy of an entire database (with all of its schemas) is very easy: CREATE DATABASE betadb TEMPLATE alphadb;

The first approach for copying a schema is the ["clone_schema" plpgsql function](https://wiki.postgresql.org/wiki/Clone_schema)
written by Emanuel Calvo. Go check it out, it's short. Basically, it gets a list of tables from the information_schema and then runs CREATE TABLE statements of the format CREATE TABLE beta.foo (LIKE alpha.foo INCLUDING CONSTRAINTS INCLUDING INDEXES INCLUDING DEFAULTS). This is a pretty good approach, but it does leave out many types of objects, such as functions, domains, [FDWs](https://wiki.postgresql.org/wiki/Foreign_data_wrappers), etc. as well as having a minor sequence problem. It's also slow to copy the data, as it creates all of the indexes before populating the table via INSERT.

My preferred approach for things like this is to use the [venerable
pg_dump program](http://www.postgresql.org/docs/current/static/app-pgdump.html), as it is in the PostgreSQL 'core' and its purpose in life is to smartly interrogate the system catalogs to produce [DDL](http://en.wikipedia.org/wiki/Data_definition_language) commands. Yes, parsing the output of pg_dump can get a little hairy, but that's always preferred to trying to create DDL yourself by parsing system catalogs. My quick solution follows.

```
pg_dump -n alpha | sed '1,/with_oids/ {s/ alpha/ beta/}' | psql
```

Sure, it's a bit of a hack in that it expects a specific string ("with_oids") to exist at the top of the dump file, but it is quick to write and fast to run; pg_dump creates the tables, copies the data over, and then adds in indexes, triggers, and constraints. (For an explanation of the sed portion, visit [this post](http://blog.endpoint.com/2013/10/postgres-sed-pgdump-warnings.html)). So this solution works very well. Or does it? When playing with this, I found that there is one place in which this breaks down: assignment of ownership to certain database objects, especially functions. It turns out pg_dump will *always* schema-qualify the ownership commands for functions, even though the function definition right above it has no schema, but sensibly relies on the search_path. So you see this weirdness in pg_dump output:

```
--
-- Name: myfunc(); Type: FUNCTION; Schema: alpha; Owner: greg
--
CREATE FUNCTION myfunc() RETURNS text
    LANGUAGE plpgsql
    AS $$ begin return 'quick test'; end$$;

ALTER FUNCTION alpha.myfunc() OWNER TO greg;
```

Note the fully qualified "alpha.myfunc". This is a problem, and the sed trick above will not replace this "alpha" with "beta", nor is there a simple way to do so, without descending into a dangerous web of regular expressions and slippery assumptions about the file contents. Compare this with the ownership assignments for almost every other object, such as tables:

```
--
-- Name: mytab; Type: TABLE; Schema: alpha; Owner: greg
--
CREATE TABLE mytab (
    id integer
);

ALTER TABLE mytab OWNER TO greg;
```

No mention of the "alpha" schema at all, except inside the comment! Before going into why pg_dump is acting like that, I'll present my current favorite solution for making a copy of a schema: using pg_dump and some creative renaming:

```
$ pg_dump -n alpha -f alpha.schema
$ psql -c 'ALTER SCHEMA alpha RENAME TO alpha_old'
$ psql -f alpha.schema
$ psql -c 'ALTER SCHEMA alpha RENAME TO beta'
$ psql -c 'ALTER SCHEMA alpha_old TO alpha'
```

This works very well, with the obvious caveat that for a period of time, you don't have your schema available to your applications. Still, a small price to pay for what is most likely a relatively rare event. The sed trick above is also an excellent solution if you don't have to worry about setting ownerships.

Getting back to pg_dump, why is it schema-qualifying some ownerships, despite a search_path being used? The answer seems to lie in **src/bin/pg_dump/pg_backup_archiver.c**:

```
  /*                                                                                                                                                      
     * These object types require additional decoration.  Fortunately, the                                                                                  
     * information needed is exactly what's in the DROP command.                                                                                            
     */
    if (strcmp(type, "AGGREGATE") == 0 ||
        strcmp(type, "FUNCTION") == 0 ||
        strcmp(type, "OPERATOR") == 0 ||
        strcmp(type, "OPERATOR CLASS") == 0 ||
        strcmp(type, "OPERATOR FAMILY") == 0)
    {
        /* Chop "DROP " off the front and make a modifiable copy */
        char       *first = pg_strdup(te-&gt;dropStmt + 5);
```

Well, that's an ugly elegant hack and explains why the schema name keeps popping up for functions, aggregates, and operators: because their names can be tricky, pg_dump hacks apart the already existing DROP statement built for the object, which unfortunately is schema-qualified. Thus, we get the redundant (and sed-busting) schema qualification!

Even with all of that, it is still always recommended to use pg_dump when trying to create DDL. Someday Postgres will have a DDL API to allow such things, and/or commands like MySQL's SHOW CREATE TABLE, but until then, use pg_dump, even if it means a few other contortions.


