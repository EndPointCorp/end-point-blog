---
author: Greg Sabino Mullane
gh_issue_number: 1068
tags: database, dbdpg, json, perl, postgres
title: DBD::Pg escaping placeholders with backslashes
---

<div class="separator" style="clear: both; float: right; margin-bottom: 1em; text-align: center;"><a href="/blog/2015/01/12/dbdpg-escaping-placeholders-with/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-left: 1em;"><img border="0" src="/blog/2015/01/12/dbdpg-escaping-placeholders-with/image-0.jpeg"/></a>
<br/><small><a href="https://flic.kr/p/4vUdLJ">Image</a> by <a href="https://www.flickr.com/photos/spine/">Rick Audet</a></small></div>

The popularity of using JSON and [JSONB](http://www.depesz.com/2014/03/25/waiting-for-9-4-introduce-jsonb-a-structured-format-for-storing-json/) within Postgres has forced a solution to the problem of question mark overload. JSON (as well as hstore) uses the question mark as an operator in its queries, and Perl DBI (esp. DBD::Pg) uses the question mark to indicate a placeholder. [Version 3.5.0 of DBD::Pg](http://search.cpan.org/dist/DBD-Pg/
) has solved this by allowing the use of a backslash character before the question mark, to indicate it is NOT a placeholder. We will see some code samples after establishing a little background.

First, what are placeholders? They are special characters within a SQL statement that allow you to defer adding actual values until a later time. This has a number of advantages. First, it completely removes the need to worry about quoting your values. Second, it allows efficient re-use of queries. Third, it reduces network traffic as you do not need to send the entire query each time it is re-run. Fourth, it can allow for seamless translation of data types from Postgres to your client language and back again (for example, DBD::Pg translates easily between Perl arrays and Postgres arrays). There are three styles of placeholders supported by DBD::Pg - question marks, dollar-signs, and colon-names.

Next, what are Postgres operators? They are special symbols withing a SQL statement that perform some action using as inputs the strings to the left and right side of them. It sounds more complicated than it is. Take this query:

```
SELECT count(*) FROM pg_class WHERE relpages > 24;
```

In this case, the operator is ">" - the greater than sign. It compares the things on its left (in this case, the value of the relpages column) with the things on its right (in this case, the number 24). The operator will return true or false - in this case, it will return true only if the value on its left is larger than the value on its right. Postgres is extremely extensible, which means it is easy to add all types of new things to it. Adding your own operator is fairly easy. Here's an example that duplicates the greater-than operator, but with a ? symbol:

```
CREATE OPERATOR ? (procedure=int4gt, leftarg=integer, rightarg=integer);
```

Now the operator is ready to go. You should be able to run queries like this:

```
SELECT count(*) FROM pg_class WHERE relpages ? 24;
```

The list of characters that can make up an operator is fairly small. The [documentation](http://www.postgresql.org/docs/9.4/static/sql-createoperator.html) has the detailed rules, but the basic list is **+ - * / < > = ~ ! @ # % ^ & | ` ?**. Note that an operator can consist of more than one character, for example, **>=**

A question mark inside a SQL query can be both a placeholder and an operator, and the driver has no real way to figure out which is which. The first real use of a question mark as an operator was with the [geometric operators](http://www.postgresql.org/docs/current/static/functions-geometry.html) and then with the [hstore module](http://www.postgresql.org/docs/current/static/hstore.html), which allows storing and querying of key/value pairs. It uses a lone question mark to determine if a given value appears as a key in a hstore column. For example, if the goal is to find all rows in which an hstore column contains the value foobar, the SQL would be:

```
SELECT * FROM mytable WHERE myhstorecol ? 'foobar';
```

However, if you were to try this via a Perl script using the question-mark placeholder style, DBD::Pg would get confused (and rightly so):

```
$sth = $dbh->prepare('SELECT * FROM mytable WHERE myhstorecol ? ?');
$sth->execute('foobar');
DBD::Pg::st execute failed: called with 1 bind variables when 2 are needed
```

Trying to use another placeholder style still does not work, as DBD::Pg still picks it up as a possible placeholder

```
$sth = $dbh->prepare('SELECT * FROM mytable WHERE myhstorecol ? $1');
$sth->execute('foobar');
Cannot mix placeholder styles "?" and "$1"
```

A few years ago, a solution was developed: by setting the database handle attribute "pg_placeholder_dollaronly" to true, DBD::Pg will ignore the question mark and only treat dollar-sign numbers as placeholders:

```
$dbh->{pg_placeholder_dollaronly} = 1;
$sth = $dbh->prepare('SELECT * FROM mytable WHERE myhstorecol ? $1');
$sth->execute('foobar');
## No error!
```

Then came JSON and JSONB. Just like hstore, they have three operators with question marks in them: ?, ?& and ?| - all of which will prevent the use of question-mark placeholders. However, some frameworks and supporting modules (e.g. SQL::Abstract and DBIx::Class) only support the question mark style of placeholder! Hence, another solution was needed. After some [discussion](http://codeverge.com/perl.dbi.users/escaping-placeholders-take-2/2026098) on the dbi-users list, it was agreed that a backslash before a placeholder character would allow that character to be "escaped" and sent as-is to the database (minus the backslash). Thus, as of version 3.5.0 of DBD::Pg, the above query can be written as:

```
use DBD::Pg 3.5.0;
$SQL = "SELECT * FROM mytable WHERE hstorecol \\? ?");
$sth = $dbh->prepare($SQL);
$sth->execute('foobar');
# No error!
$SQL = "SELECT * FROM mytable2 WHERE jsoncol \\? ?");
$sth = $dbh->prepare($SQL);
$sth->execute('foobar');
# Still no error!
```

So, a fairly elegant solution. The only caveat is to beware of single and double quotes. The latter require two backslashes, of course. I recommend you always use double quotes and get in the habit of consistently using double backslashes. Not only will you thus never have to worry about single-vs-double, but it adds a nice little visual garnish to help that important backslash trick stand out a little more.

Much thanks to Tim Bunce for reporting this issue, herding it through dbi-users, and helping write the final DBD::Pg solution and code!
