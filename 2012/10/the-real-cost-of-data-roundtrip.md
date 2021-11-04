---
author: Szymon Lipiński
title: The Real Cost of Data Roundtrip
github_issue_number: 701
tags:
- database
- optimization
- postgres
date: 2012-10-03
---

Sometimes you need to perform some heavy database operations. I don't know why very often programmers are afraid of using databases for that. They usually have some fancy ORM which performs all the operations, and the only way to change the data is to make some SELECT * from a table, create a bunch of unneeded objects, change one field, convert those changed objects into queries and send that to the database.

Have you ever thought about the cost of the roundtrip of data? The cost of getting all the data from database just to send changed data into the database? Why do that if there would be much faster way of achieving the same results?

Imagine that you have quite a heavy operation. Let's make something which normally databases cannot do, some more complicated operation. Many programmers just don't know that there is any other way than writing this in the application code. Let's change all the HTML entities into real characters.

The HTML entities are a way of writing many different characters in HTML. This way you can write for instance the Euro currency sign "€" in HTML even if you don't have it on your keyboard. You just have to write &euro; or &#8364; instead. I don't have to, as when I use UTF-8 encoding and write this character directly, it should be showed normally. What's more I have this character on my keyboard.

I will convert the text stored in database changing all the htmlentities into real unicode characters. I will do it using three different methods.

- The first will be a simple query run inside PostgreSQL
- The second will be an external program which downloads the text column from database, changes it externally and loads into database.
- The third method will be almost the same as the second, however it will download whole rows.

### Generate Data

So, for this test I need to have some data. Let's write a simple data generator.

First, a simple function for returning a random number within the given range.

```sql
CREATE FUNCTION random(INTEGER, INTEGER) RETURNS INTEGER AS $$
  SELECT floor ( $1 + ($2 - $1 + 1 ) * random())::INTEGER;
$$ LANGUAGE SQL;
```

Now the function for generating random texts of random length filled with the HTML entities.

```sql
CREATE FUNCTION generate_random_string() RETURNS TEXT AS $$
DECLARE
  items TEXT[] =
    ARRAY[
      'AAAA','BBBB','CCCC','DDDD','EEEE','FFFF','GGGG',
      'HHHH','IIII','JJJJ','KKKK','LLLL','MMMM','NNNN',
      'OOOO','PPPP','QQQQ','RRRR','SSSS','TTTT','UUUU',
      'VVVV','WWWW','XXXX','YYYY','ZZZZ',
      '&amp;', '&#34;', '&#39;', '&#38;','&#60;','&#62;',
      '&#162;','&#163;','&#164;','&#165;','&#166;','&#167;',
      '&#168;','&#169;','&#170;','&#171;','&#172;','&#173;',
      '&#174;','&#175;','&#176;','&#177;','&#178;','&#179;',
      '&#180;','&#181;','&#182;','&#183;','&#184;','&#185;',
      '&#186;','&#187;','&#188;','&#189;','&#190;'
    ];
  length INTEGER := random(500, 1500);
  result TEXT := '';
  items_length INTEGER := array_length(items, 1);
BEGIN
  FOR x IN 1..length LOOP
    result := result || items[ random(1, items_length) ];
  END LOOP;

  RETURN result;
END;
$$ LANGUAGE PLPGSQL;
```

The table for storing the data is created with the following query:

```sql
CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    padding TEXT,
    t TEXT
);
```

Then I filled this table using a query generating 50k rows with random data:

```sql
INSERT INTO data(payload, t)
SELECT
    generate_random_string(),
    generate_random_string()
FROM
    generate_series(1, 50*1000);
```

Let's check the table size:

```sql
SELECT pg_size_pretty(pg_relation_size('data'));
 pg_size_pretty
 ----------------
  207 MB
  (1 row)
```

As the table is filled with random data, I need to have two tables with exactly the same data.

```sql
CREATE TABLE query (id SERIAL PRIMARY KEY, payload TEXT, t TEXT);
CREATE TABLE script (id SERIAL PRIMARY KEY, payload TEXT, t TEXT);
CREATE TABLE script_full (id SERIAL PRIMARY KEY, payload TEXT, t TEXT);

INSERT INTO query SELECT * FROM data;
INSERT INTO script SELECT * FROM data;
INSERT INTO script_full SELECT * FROM data;
```

### The Tests

#### SQL

Many programmers think that such operations are not normally available inside a database. However PostgreSQL has quite a nice feature, it can execute functions written in many different languages. For the purpose of this test I will use the language pl/perlu which allows me to use external libraries. I will also use HTML::Entities package for the conversion.

The function I wrote is quite simple:

```sql
CREATE FUNCTION decode_html_entities(text) RETURNS TEXT AS $$
    use HTML::Entities;
    return decode_entities($_[0]);
$$ LANGUAGE plperlu;
```

The update of the data can be done using the following query:

```sql
UPDATE query SET t = decode_html_entities(t);
```

#### Application

In order to have those tests comparable, I will write a simple perl script using exactly the same package for converting html entities.

```perl
#!/usr/bin/env perl

use DBI;
use HTML::Entities;
use Encode;

my $dbh = DBI->connect(
    "DBI:Pg:dbname=test;host=localhost",
    "szymon",
    "",
    {'RaiseError' => 1, 'pg_utf8_strings' => 1});

$dbh->do('BEGIN');

my $upd = $dbh->prepare("UPDATE script SET t = ? WHERE id = ?");

my $sth = $dbh->prepare("SELECT id, t FROM script");
$sth->execute();

while(my $row = $sth->fetchrow_hashref()) {
    my $t = decode_entities( $row->{'t'} );
    $t = encode("UTF-8", $t);
    $upd->execute( $t, $row->{'id'} );
}

$dbh->do('COMMIT');
$dbh->disconnect();
```

#### The Worst Application

There is another terrible idea implemented by programmers too often. Why select only the column you want to change? Let's select all the rows and send them back to database.

This script will look like this (the important changes are in lines 17 and 23)

```perl
#!/usr/bin/env perl

use DBI;
use HTML::Entities;
use Encode;

my $dbh = DBI->connect(
    "DBI:Pg:dbname=test;host=localhost",
    "szymon",
    "",
    {'RaiseError' => 1, 'pg_utf8_strings' => 1});

$dbh->do('BEGIN');

my $upd = $dbh->prepare("UPDATE script_all SET t = ? WHERE id = ?");

my $sth = $dbh->prepare("SELECT id, payload, t FROM script_all");
$sth->execute();

while(my $row = $sth->fetchrow_hashref()) {
    my $t = decode_entities( $row->{'t'} );
    $t = encode("UTF-8", $t);
    $upd->execute( $t, $row->{'payload'}, $row->{'id'} );
}

$dbh->do('COMMIT');
$dbh->disconnect();
```

### Results

The query using **pl/perlu function** executed in **26 seconds**.

The **script** changing data externally execuded in **2 minutes 10 seconds (5 times slower)**

The **worst script** getting and resending whole rows finished in **4 minutes 35 seconds (10 times slower)**.

I used quite a small number of rows. There were just 50k rows (about 200MB). On production servers the numbers are much bigger.

Just imagine that the code you developed for changing data could run 10 times faster if you'd do this in the database.
