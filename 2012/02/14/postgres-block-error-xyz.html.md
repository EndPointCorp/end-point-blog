---
author: Greg Sabino Mullane
gh_issue_number: 554
tags: database, postgres
title: 'Tracking down PostgreSQL XYZ error: tablespace, database, and relfilnode'
---

One of our Postgres clients recently had this error show up in their logs:

```nohighlight
ERROR: could not read block 3 of relation 1663/18421/31582:
read only 0 of 8192 bytes
```

<a href="/blog/2012/02/14/postgres-block-error-xyz/image-0-big.png"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5706852464520734962" src="/blog/2012/02/14/postgres-block-error-xyz/image-0.png" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 310px; height: 320px;"/></a>

Because we were using  [the tail_n_mail program](http://bucardo.org/wiki/Tail_n_mail), the above error was actually mailed to us within a minute of it occurring. The message is fairly cryptic, but it basically means that Postgres could not read data from a physical file that represented a table or index. This is generally caused by corruption or a missing file. In this case, the “read only 0 of 8192” indicates this was most likely a missing file.

When presented with an error like this, it’s nice to be able to figure out which relation the message is referring to. The word “relation” is Postgres database-speak for a generic object in the database: in this case, it is almost certainly going to be a table or an index. Both of those are, of course, represented by actual files on disk, usually inside of your [data_directory](https://www.postgresql.org/docs/current/static/runtime-config-file-locations.html). The number given, 1663/18421/31582, is in the standard **X/Y/Z** format Postgres uses to identify a file, where **X** represents the tablespace, **Y** is the database, and **Z** is the file.

-----------

<a href="/blog/2012/02/14/postgres-block-error-xyz/image-1-big.png"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5706852622605279650" src="/blog/2012/02/14/postgres-block-error-xyz/image-1.png" style="float:right; margin:10 0 30px 10px;cursor:pointer; cursor:hand;width: 320px; height: 137px;"/></a>

The first number, **X**, indicates which tablespace this relation belongs to. [Tablespaces](https://www.postgresql.org/docs/current/static/manage-ag-tablespaces.html) are physical directories mapped to internal names in the database. Their primary use is to allow you to put tables or indexes on different physical disks. The number here, **1663**, is a very familiar one, as it almost always indicates the default tablespace, known as **pg_default**. If you do not create any additional tablespaces, everything will end up here. On disk, this will be the directory named **base** underneath your *data_directory*.

What if the relation you are tracking is not inside of the default tablespace? The number **X** represents the OID inside the [pg_tablespace](https://www.postgresql.org/docs/9.1/static/catalog-pg-tablespace.html) system table, which will let you know where the tablespace is physically located. To illustrate, let’s create a new tablespace and then view the contents of the **pg_tablespace** table:

```nohighlight
$ mkdir /tmp/pgtest
$ psql -c "CREATE TABLESPACE ttest LOCATION '/tmp/pgtest'"
CREATE TABLESPACE

 $ psql -c 'select oid, * from pg_tablespace'
  oid  |  spcname   | spcowner | spclocation | spcacl | spcoptions
-------+------------+----------+-------------+--------+------------
1663   | pg_default |       10 |             |        |
1664   | pg_global  |       10 |             |        |
78289  | ttest      |       10 | /tmp/pgtest |        |
```

Thus, if **X** were **78289**, it would lead us to the tablespace **ttest**, and we would know that the file we were ultimately looking for will be in the directory indicated by the **spclocation** column, **/tmp/pgtest**. If that column is blank, it means the directory to use is ***data_directory*/base**.

-----------

The second number in our X/Y/Z series, **Y**, indicates which database the relation belongs to. You can look this information up by querying the [pg_database](https://www.postgresql.org/docs/current/static/catalog-pg-database.html) system table like so:

```
$ psql -xc 'select oid, * from pg_database where oid = 18421'
-[ RECORD 1 ]-+-----------
oid           | 18421
datname       | foobar
datdba        | 10
encoding      | 6
datcollate    | en_US.utf8
datctype      | en_US.utf8
datistemplate | f
datallowconn  | t
datconnlimit  | -1
datlastsysoid | 12795
datfrozenxid  | 1792
dattablespace | 1663
datacl        |
```

The columns may look different depending on your version of Postgres—​the important thing here is that the number **Y** maps to a database via the oid column—​in this case the database **foobar**. We need to know which database so we can query the correct **pg_class** table in the next step. We did not have to worry about that in until now as the **pg_tablespace** and **pg_database** tables are two of the very few shared system catalogs.

-----------

The final number in our X/Y/Z series, **Z**, represents a file on disk. You can look up which relation it is by querying the **pg_class** system table of the correct database:

```nohighlight
$ psql -d foobar -c "select relname,relkind from pg_class where relfilenode=31582"
relname | relkind
--------+-------
(0 rows)
```

No rows, so as far as Postgres is concerned that file does not exist! Let’s verify that this is the case by looking on the disk. Recall that X was the default tablespace, which means we start in ***data_directory*/base**. Once we are in that directory, we can look for the subdirectory holding the database we want (Y or 18421)—​it is named after the OID of the database. We can then look for our relfilenode (Z or 31582) inside of that directory:

```nohighlight
$ psql -c 'show data_directory'

      data_directory       
---------------------------------
/var/lib/pgsql/data
(1 row)

$ cd /var/lib/pgsql/data
/var/lib/pgsql/data $ cd base
/var/lib/pgsql/data/base $ cd 18421
/var/lib/pgsql/data/base/18421 $ stat 31582
stat: cannot stat `31582': No such file or directory
```

So in this case, we confirmed that the relfilenode was no longer there! If it *was* there, we can probably surmise that the file on disk is corrupted somehow. If the relation was an index, the solution would be to simply run a [REINDEX INDEX indexname](https://www.postgresql.org/docs/current/static/sql-reindex.html) on it, which will recreate the entire index with a new relfilenode. If it is a table, then things get trickier: we can try a [VACUUM FULL](https://www.postgresql.org/docs/current/static/sql-vacuum.html) on it, which rewrites the entire table, but you will most likely need to go back to your last SQL backup or take a look at your [PITR (Point-In-Time Recovery) server](https://www.postgresql.org/docs/current/static/continuous-archiving.html).

So why would a relfilenode file not exist on disk? There are a few possibilities:

- We are looking in the wrong **pg_class** table (i.e. user error). Each database has its own copy of the **pg_class**, with different relfilenodes. This means that each subdirectory corresponding to the database has its own set of files as well.
- It may be a bug in Postgres. Unlikely, unless we have exhausted the other possibilities.
- Bad RAM or a bad disk may have caused a flipped bit somewhere, for example changing the relfilenode from 12345 to 12340. Possible, but still unlikely.
- The relfilenode file was removed by something. This is the most likely explanation. We’ve already hinted above at one way this could happen: a REINDEX. Since the client in this story was (is!) prudently running with **log_statement = 'all'**, I was able to grep back through the logs and found that a REINDEX of a few system tables, including pg_depend, was kicked off a second before the error popped up. While it’s impossible to know exactly what the missing relfilenode referred to, the REINDEX is as close to a smoking gun as we are going to get. So the query started, a REINDEX removed one of the indexes it was using, and then the error occurred as Postgres tried to access that index.

In this case, we were able to simply rerun the query and it worked as expected. In normal every day usage, this error should not appear, even when reindexing system tables, but should something like this happen to you, at least you will know what those numbers mean. :)
