---
author: Joshua Tolley
gh_issue_number: 799
tags: database, mysql, open-source, postgres, sql, tools
title: Foreign Data Wrappers
---



<a href="/blog/2013/05/13/foreign-data-wrappers/image-0-big.png" imageanchor="1"><img border="0" src="/blog/2013/05/13/foreign-data-wrappers/image-0.png"/></a>

Original images from Flickr user [jenniferwilliams](http://www.flickr.com/photos/jenniferwilliams/)

One of our clients, for various historical reasons, runs both MySQL and PostgreSQL to support their website.  Information for user login lives in one database, but their customer activity lives in the other. The eventual plan is to consolidate these databases, but thus far, other concerns have been more pressing. So when they needed a report combining user account information and customer activity, the involvement of two separate databases became a significant complicating factor.

In similar situations in the past, using earlier versions of PostgreSQL, we've written scripts to pull data from MySQL and dump it into PostgreSQL. This works well enough, but we've updated PostgreSQL fairly recently, and can use the SQL/MED features added in version 9.1. [SQL/MED](http://wiki.postgresql.org/wiki/Foreign_data_wrappers) ("MED" stands for "Management of External Data") is a decade-old standard designed to allow databases to make external data sources, such as text files, web services, and even other databases look like normal database tables, and access them with the usual SQL commands. PostgreSQL has supported some of the SQL/MED standard since version 9.1, with a feature called Foreign Data Wrappers, and among other things, it means we can now access MySQL through PostgreSQL seamlessly.

The first step is to install the right software, called mysql_fdw. It comes to us via Dave Page, PostgreSQL core team member and contributor to many projects.  It's worth noting Dave's warning that he considers this experimental code. For our purposes it works fine, but as will be seen in this post, we didn't push it too hard. We opted to [download the source](https://github.com/dpage/mysql_fdw) and build it, but installing using pgxn works as well:

```nohighlight
$ env USE_PGXS=1 pgxnclient install mysql_fdw
INFO: best version: mysql_fdw 1.0.1
INFO: saving /tmp/tmpjrznTj/mysql_fdw-1.0.1.zip
INFO: unpacking: /tmp/tmpjrznTj/mysql_fdw-1.0.1.zip
INFO: building extension
gcc -O2 -Wall -Wmissing-prototypes -Wpointer-arith -Wdeclaration-after-statement -Wendif-labels -Wformat-security -fno-strict-aliasing -fwrapv -fexcess-precision=standard -g -fpic -I/usr/include/mysql -I. -I. -I/home/josh/devel/pg91/include/postgresql/server -I/home/josh/devel/pg91/include/postgresql/internal -D_GNU_SOURCE -I/usr/include/libxml2   -c -o mysql_fdw.o mysql_fdw.c
mysql_fdw.c: In function ‘mysqlPlanForeignScan’:
mysql_fdw.c:466:8: warning: ‘rows’ may be used uninitialized in this function [-Wmaybe-uninitialized]
gcc -O2 -Wall -Wmissing-prototypes -Wpointer-arith -Wdeclaration-after-statement -Wendif-labels -Wformat-security -fno-strict-aliasing -fwrapv -fexcess-precision=standard -g -fpic -shared -o mysql_fdw.so mysql_fdw.o -L/home/josh/devel/pg91/lib -L/usr/lib  -Wl,--as-needed -Wl,-rpath,'/home/josh/devel/pg91/lib',--enable-new-dtags  -L/usr/lib/x86_64-linux-gnu -lmysqlclient -lpthread -lz -lm -lrt -ldl
INFO: installing extension
&lt; ... snip ... &gt;
```

Here I'll refer to the documentation provided in [mysql_fdw's README](https://github.com/dpage/mysql_fdw/blob/master/README). The first step in using a foreign data wrapper, once the software is installed, is to create the foreign server, and the user mapping. The foreign server tells PostgreSQL how to connect to MySQL, and the user mapping covers what credentials to use. This is an interesting detail; it means the foreign data wrapper system can authenticate with external data sources in different ways depending on the PostgreSQL user involved. You'll note the pattern in creating these objects: each simply takes a series of options that can mean whatever the FDW needs them to mean. This allows the flexibility to support all sorts of different data sources with one interface.

The final step in setting things up is to create a foreign table. In MySQL's case, this is sort of like a view, in that it creates a PostgreSQL table from the results of a MySQL query. For our purposes, we needed access to several thousand structurally identical MySQL tables (I mentioned the goal is to move off of this one day, right?), so I automated the creation of each table with a simple bash script, which I piped into psql:

```nohighlight
for i in `cat mysql_tables`; do
    echo "CREATE FOREIGN TABLE mysql_schema.$i ( ... table definition ...)
        SERVER mysql_server OPTIONS (
            database 'mysqldb',
            query 'SELECT ... some fields ... FROM $i'
        );"
done
```

In a step not shown above, this script also consolidates the data from each table into one, native PostgreSQL table, to simplify later reporting. In our case, pulling the data once and reporting on the results is perfectly acceptable; in other words, data a few seconds old wasn't a concern. We also didn't need to write back to MySQL, which presumably could complicate things somewhat. We did, however, run into the same data validation problems PostgreSQL users habitually complain about when working with MySQL. Here's an example, in my own test database:

```nohighlight
mysql&gt; create table bad_dates (mydate date);
Query OK, 0 rows affected (0.07 sec)

mysql&gt; insert into bad_dates values ('2013-02-30'), ('0000-00-00');
Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

Note that MySQL silently transformed '2013-02-30' into '0000-00-00'. Sigh. Then, in psql we do this:

```nohighlight
josh=# create extension mysql_fdw;
CREATE EXTENSION

josh=# create server mysql_svr foreign data wrapper mysql_fdw options (address '127.0.0.1', port '3306');
CREATE SERVER

josh=# create user mapping for public server mysql_svr options (username 'josh', password '');
CREATE USER MAPPING

josh=# create foreign table bad_dates (mydate date) server mysql_svr options (query 'select * from test.bad_dates');
CREATE FOREIGN TABLE

josh=# select * from bad_dates ;
ERROR:  date/time field value out of range: "0000-00-00"
```

We've told PostgreSQL we'll be feeding it valid dates, but MySQL's idea of a valid date differs from PostgreSQL's, and the latter complains when the dates don't meet its stricter requirements. Several different workarounds exist, including admitting that '0000-00-00' really is wrong and cleaning up MySQL, but in this case, we modified the query underlying the foreign table to fix the dates on the fly:

```sql
SELECT CASE disabled WHEN '0000-00-00' THEN NULL ELSE disabled END,
    -- various other fields
    FROM some_table
```

Fortunately this is the only bit of MySQL / PostgreSQL impedance mismatch that has tripped us up thus far; we'd have to deal with any others we found individually, just as we did this one.


