---
author: Josh Tolley
title: Anonymous code blocks
github_issue_number: 353
tags:
- database
- open-source
- postgres
date: 2010-09-23
---



With the release of PostgreSQL 9.0 comes the ability to execute “anonymous code blocks” in various of the PostgreSQL procedural languages. The idea stemmed from work back in autumn of 2009 that tried to respond to a common question on IRC or the mailing lists: how do I grant a permission to a particular user for all objects in a schema? At the time, the only solution short of manually writing commands to grant the permission in question on every object individually was to write a script of some sort. [Further discussion uncovered several people](https://www.postgresql.org/message-id/4A803A89.9020509@dunslane.net) that often found themselves writing simple functions to handle various administrative tasks. Many of those people, it turned out, would rather simply call one statement, rather than create a function, call the function, and then drop (or just ignore) the function they’d never need again. Hence, [the new DO command](https://www.postgresql.org/docs/9.0/static/sql-do.html).

The first language to support DO was PL/pgSQL. The PostgreSQL documentation provides an example to answer the original question: how do I grant permissions on everything to a particular user.

```plain
DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_schema, table_name FROM information_schema.tables
             WHERE table_type = 'VIEW' AND table_schema = 'public'
    LOOP
        EXECUTE 'GRANT ALL ON ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) || ' TO webuser';
    END LOOP;
END$$;
```

Notice that this doesn’t actually tell us what language to use. If no language is specified, DO defaults to PL/pgSQL (which, in 9.0, is enabled by default). But you can use other languages as well:

```plain
DO $$
HAI
    BTW Calculate pi using Gregory-Leibniz series
    BTW This method does not converge particularly quickly...
    I HAS A PIADD ITZ 0.0
    I HAS A PISUB ITZ 0.0
    I HAS A ITR ITZ 0
    I HAS A T1
    I HAS A T2
    I HAS A PI ITZ 0.0
    I HAS A ITERASHUNZ ITZ 1000

    IM IN YR LOOP
        T1 R QUOSHUNT OF 4.0 AN SUM OF 3.0 AN ITR
        T2 R QUOSHUNT OF 4.0 AN SUM OF 5.0 AN ITR
        PISUB R SUM OF PISUB AN T1
        PIADD R SUM OF PIADD AN T2
        ITR R SUM OF ITR AN 4.0
        BOTH SAEM ITR AN BIGGR OF ITR AN ITERASHUNZ, O RLY?
            YA RLY, GTFO
        OIC
    IM OUTTA YR LOOP
    PI R SUM OF 4.0 AN DIFF OF PIADD AN PISUB
    VISIBLE "PI R: "
    VISIBLE PI
    FOUND YR PI
KTHXBYE
$$ LANGUAGE PLLOLCODE;
```

I tried to rewrite the GRANT function shown above in PL/LOLCODE for this example, until I discovered that some of PL/LOLCODE’s limitations make it extremely difficult, if not impossible. So far as I know, PL/LOLCODE was the second language to support anonymous blocks, thanks to what turned out to be a relatively simple programming exercise. After finishing PL/LOLCODE’s DO support, I decided to do the same for PL/Perl. I wasn’t particularly surprised to find that PL/Perl was harder to extend than PL/LOLCODE; PL/Perl is a much more feature-rich (and hence, complicated) language and I wasn’t as familiar with its internals. However, after my initial submission and with helpful commentary from several other people, Andrew Dunstan tied off the loose ends and got it committed. It looks like this:

```perl
DO $$
    my $row;
    my $rv = spi_exec_query(q{
        SELECT quote_ident(table_schema) || '.' || quote_ident(table_name) AS relname
        FROM information_schema.tables WHERE table_type = 'VIEW' AND table_schema = 'public'
    });
    my $nrows = $rv->{processed};
    foreach my $i (0 .. $nrows - 1) {
        my $row = $rv->{rows}[$rn];
        spi_exec_query("GRANT ALL ON $row->{relname} TO webuser");
    }
$$ LANGUAGE plperl;
```

DO wasn’t the only thing to come from the pgsql-hackers discussion I mentioned above. In PostgreSQL 9.0, the [GRANT](https://www.postgresql.org/docs/9.0/static/sql-grant.html) command has also been modified, so it’s now possible to grant permissions several objects in one stroke syntax. For instance:

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO webuser
```

