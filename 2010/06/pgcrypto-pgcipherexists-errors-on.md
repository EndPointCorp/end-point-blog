---
author: Greg Sabino Mullane
title: pgcrypto pg_cipher_exists errors on upgrade from PostgreSQL 8.1
github_issue_number: 317
tags:
- database
- postgres
date: 2010-06-10
---

<a href="/blog/2010/06/pgcrypto-pgcipherexists-errors-on/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5481227901047595058" src="/blog/2010/06/pgcrypto-pgcipherexists-errors-on/image-0.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 240px; height: 320px;"/></a>

 While migrating a client from a 8.1 Postgres database to a 8.4 Postgres database, I came across a very annoying pgcrypto problem. ([pgcrypto](https://www.postgresql.org/docs/current/static/pgcrypto.html) is a very powerful and useful contrib module that contains many functions for encryption and hashing.) Specifically, the following functions were removed from pgcrypto as of version 8.2 of Postgres:

- pg_cipher_exists- pg_digest_exists- pg_hmac_exists

While the functions listed above [were deprecated](https://www.mail-archive.com/pgsql-hackers@postgresql.org/msg81136.html), and marked as such for a while, their complete removal from 8.2 presents problems when upgrading via a simple pg_dump. Specifically, even though the client was not using those functions, they were still there as part of the dump. Here’s what the error message looked like:

```bash
$ pg_dump mydb --create | psql -X -p 5433 -f - >pg.stdout 2>pg.stderr
...
psql:<stdin>:2654: ERROR:  could not find function "pg_cipher_exists"
  in file "/var/lib/postgresql/8.4/lib/pgcrypto.so"
psql:<stdin>:2657: ERROR:  function public.cipher_exists(text) does not exist
</stdin></stdin>
```

While it doesn’t stop the rest of the dump from importing, I like to remove any errors I can. In this case, it really *was* a [SMOP](https://en.wikipedia.org/wiki/Small_matter_of_programming). Inside the Postgres 8.4 source tree, in the **contrib/pgcrypto** directory, I added the following declarations to **pgcrypto.h**:

```nohighlight
Datum       pg_cipher_exists(PG_FUNCTION_ARGS);
Datum       pg_digest_exists(PG_FUNCTION_ARGS);
Datum       pg_hmac_exists(PG_FUNCTION_ARGS);
```

Then I added three simple functions to the bottom of the **pgcrypto.c** file that simply throw an error if they are invoked, letting the user know that the functions are deprecated. This is a much friendlier way than simply removing the functions, IMHO.

```sql
/* SQL function: pg_cipher_exists(text) returns boolean */
PG_FUNCTION_INFO_V1(pg_cipher_exists);

Datum
pg_cipher_exists(PG_FUNCTION_ARGS)
{
    ereport(ERROR,
            (errcode(ERRCODE_EXTERNAL_ROUTINE_INVOCATION_EXCEPTION),
             errmsg("pg_cipher_exists is a deprecated function")));
    PG_RETURN_TEXT_P("0");
}

/* SQL function: pg_cipher_exists(text) returns boolean */
PG_FUNCTION_INFO_V1(pg_digest_exists);

Datum
pg_digest_exists(PG_FUNCTION_ARGS)
{

    ereport(ERROR,
            (errcode(ERRCODE_EXTERNAL_ROUTINE_INVOCATION_EXCEPTION),
             errmsg("pg_digest_exists is a deprecated function")));
    PG_RETURN_TEXT_P("0");
}
/* SQL function: pg_hmac_exists(text) returns boolean */
PG_FUNCTION_INFO_V1(pg_hmac_exists);

Datum
pg_hmac_exists(PG_FUNCTION_ARGS)
{

    ereport(ERROR,
            (errcode(ERRCODE_EXTERNAL_ROUTINE_INVOCATION_EXCEPTION),
             errmsg("pg_hmac_exists is a deprecated function")));
    PG_RETURN_TEXT_P("0");
}

```

After running **make install** from the pgcrypto directory, the dump proceeded without any further pgcrypto errors. From this point forward, if the anyone attempts to use one of the functions, it will be quite obvious that the function is deprecated, rather than leaving the user wondering if they typed the function name incorrectly or wondering if pgcrypto is perhaps not installed.

Why not just add some dummy SQL functions to the **pgcrypto.sql** file instead of hacking the C code? Because pg_dump by default will create the database as a copy of template0. While there are other ways around the problem (such as putting the SQL functions into template1 and forcing the load to use that instead of template0, or by creating the database, adding the SQL functions, and then loading the data), this was the simplest approach.

*[Photo](https://www.flickr.com/photos/mwichary/2297915254/) of [Enigma machine](https://en.wikipedia.org/wiki/Enigma_machine) by [Marcin Wichary](https://www.flickr.com/photos/mwichary/)*
