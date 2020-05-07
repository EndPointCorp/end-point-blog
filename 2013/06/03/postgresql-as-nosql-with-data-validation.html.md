---
author: Szymon Lipiński
gh_issue_number: 810
tags: json, nosql, postgres, couchdb
title: PostgreSQL as NoSQL with Data Validation
---

PostgreSQL is a relational database with many great features. There are also many so called NoSQL databases, some of them, like CouchDB, are document databases. However the document in CouchDB is automatically enhanced with a “_id” field, if it is not present. When you want to get this one document, you can use this “_id” field—​it behaves exactly like the primary key from relational databases. PostgreSQL stores data in tables’ rows while CouchDB stores data as JSON documents. On one hand CouchDB seems like a great solution, as you can have all the different data from different PostgreSQL tables in just one JSON document. This flexibility comes with a cost of no constraints on the data structure, which can be really appealing at the first moment and really frustrating when you have a huge database and some of the documents contain bad values or there are missing some fields.

PostgreSQL 9.3 comes with great features which can turn it into a NoSQL database, with full transaction support, storing JSON documents with constraints on the fields data.

### Simple Example

I will show how to do it using a very simple example of a table with products. Each product has a name, description, some id number, price, currency and number of products we have in stock.

### PostgreSQL Version

The simple table in PostgreSQL can look like:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    price DECIMAL(10,2),
    currency TEXT,
    in_stock INTEGER
);
```

This table allows us to insert products like:

```sql
INSERT INTO products (name, description, price, currency, in_stock) VALUES ('shoes', 'blue shoes', 12.34, 'dollars', 5);
```

Unfortunately the above table also allows for adding rows missing some important information:

```sql
INSERT INTO products (name, description, price, currency, in_stock) VALUES ('', null, -20, 'handa', -42);
```

This should be fixed by adding constraints in the database. Assume that we want to always have unique not empty name, not empty description, non negative price and in_stock, and the currency should always be dollars. The table with such constraints is:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency TEXT NOT NULL,
    in_stock INTEGER NOT NULL,
    CHECK (length(name) > 0),
    CHECK (description IS NOT NULL AND length(description) > 0),
    CHECK (price >= 0.0),
    CHECK (currency = 'dollars'),
    CHECK (in_stock >= 0)
); >
```

Now all the operations, like adding or modifying a row, which violate any of those constraints, just fail. Let’s check:

```sql
postgres=# INSERT INTO products (name, description, price, currency, in_stock) VALUES ('shoes', 'blue shoes', 12.34, 'dollars', 5);
INSERT 0 1
postgres=# INSERT INTO products (name, description, price, currency, in_stock) VALUES ('shoes', 'blue shoes', 12.34, 'dollars', -1);
ERROR:  new row for relation "products" violates check constraint "products_in_stock_check"
DETAIL:  Failing row contains (2, shoes, blue shoes, 12.34, dollars, -1).
```

### NoSQL Version

In CouchDB the inserted row in the above table, would be just a JSON looking like this:

```sql
{
    "id": 1,
    "name": "shoes",
    "description": "blue_shoes",
    "price": 12.34,
    "currency": "dollars",
    "in_stock": 5
}
```

#### The Trivial Solution

In PostgreSQL we can store this JSON as a row in the products table:

```sql
CREATE TABLE products (
    data TEXT
);
```

This works like most of the NoSQL datatabases, no checks, no errors with bad fields. As a result, you can modify the data the way you want, the problem begins when your application expects that the price is a number, and you get a string there, or there is no price at all.

#### Validate JSON

CouchDB validates JSON before saving the document into database. In PostgreSQL 9.2 there is the nice type for that, it is named JSON. The JSON type can store only a proper JSON, there is validation performed before converting into this type.

Let’s change the definition of the table to:

```sql
CREATE TABLE products (
    data JSON
);
```

We can insert correct JSON into this table:

```sql
postgres=# INSERT INTO products(data) VALUES('{
    "id": 1,
    "name": "shoes",
    "description": "blue_shoes",
    "price": 12.34,
    "currency": "dollars",
    "in_stock": 5
}');
INSERT 0 1
postgres=# SELECT * FROM products;
               data
----------------------------------
 {                               +
     "id": 1,                    +
     "name": "shoes",            +
     "description": "blue_shoes",+
     "price": 12.34,             +
     "currency": "dollars",      +
     "in_stock": 5               +
 }
(1 row)
```

This works, but inserting not a valid JSON ends with an error:

```sql
postgres=# INSERT INTO products(data) VALUES('{
    "id": 1,
    "name": "shoes",
    "description": "blue_shoes",
    "price": 12.34,
    "currency": "dollars",
    "in_stock": 5,
}');
ERROR:  invalid input syntax for type json
LINE 1: INSERT INTO products(data) VALUES('{
                                          ^
DETAIL:  Expected string, but found "}".
CONTEXT:  JSON data, line 5: ...,
    "currency": "dollars",
    "in_stock": 5,
}
```

The problem with formatting can be hard to notice (I’ve added comma after the last field, JSON doesn’t like it).

#### Validating Fields

OK, so we have a solution which looks almost like the first native PostgreSQL solution: we have data which validates. It doesn’t mean the data is sensible.

Let’s add checks for validating the data.

In PostgreSQL 9.3, which has not been released yet, there are some new great features for manipulating JSON values. There are defined operators for the JSON type, which give you easy access to the fields and values.

I will use only one operator “->>”, but you can find more information in [PostgreSQL documentation](https://www.postgresql.org/docs/9.3/static/functions-json.html).

I also need to validate the types of the fields, including id field. This is something Postgres just checks because of the types definitions. I am going to use some other syntax for the checks, as I want to name it. It will be easier to look at problem with specific field instead of searching through the whole huge JSON.

The table with the constraints looks like this:

```sql
CREATE TABLE products (
    data JSON,
    CONSTRAINT validate_id CHECK ((data->>'id')::integer >= 1 AND (data->>'id') IS NOT NULL ),
    CONSTRAINT validate_name CHECK (length(data->>'name') > 0 AND (data->>'name') IS NOT NULL ),
    CONSTRAINT validate_description CHECK (length(data->>'description') > 0  AND (data->>'description') IS NOT NULL ),
    CONSTRAINT validate_price CHECK ((data->>'price')::decimal >= 0.0 AND (data->>'price') IS NOT NULL),
    CONSTRAINT validate_currency CHECK (data->>'currency' = 'dollars' AND (data->>'currency') IS NOT NULL),
    CONSTRAINT validate_in_stock CHECK ((data->>'in_stock')::integer >= 0 AND (data->>'in_stock') IS NOT NULL )
}
```

The “->>” operator allows me to get the value of a specific field from JSON, check if it exists and validate it.

Let’s add a JSON without a description:

```sql
postgres=# INSERT INTO products(data) VALUES('{
    "id": 1,
    "name": "d",
    "price": 1.0,
    "currency": "dollars",
    "in_stock": 5
}');
```
```sql
ERROR:  new row for relation "products" violates check constraint "validate_description"
DETAIL:  Failing row contains ({
    "id": 1,
    "name": "d",
    "price": 1.0,
    "currency...). >
```

There is one more validation left. The id and name fields should be unique. This can be easily done with two indexes:

```sql
CREATE UNIQUE INDEX ui_products_id ON products((data->>'id'));
CREATE UNIQUE INDEX ui_products_name ON products((data->>'name'));
```

Now when you try to add a JSON document which id which already exists in database, then you will have an error like:

```sql
ERROR:  duplicate key value violates unique constraint "ui_products_id"
DETAIL:  Key ((data ->> 'id'::text))=(1) already exists.
ERROR:  current transaction is aborted, commands ignored until end of transaction block
```

#### Id Generation

In NoSQL databases the id field is usually some UUID. This is an identifier generated with algorithms with a very small chance of generating the same value, even when you generate them on different machines. So I’m not going to touch it here.

### Searching

You can search the JSON data normally like you were searching columns in a table. Let’s search for the most expensive product we have in stock:

```sql
SELECT * FROM products WHERE in_stock > 0 ORDER BY price DESC LIMIT 1;
```

The JSON version is very similar:

```sql
SELECT * FROM products WHERE (data->>'in_stock')::integer > 0 ORDER BY (data->>'price')::decimal DESC LIMIT 1;
```

This query can be very inefficient. It needs to read all the rows, parse JSON fields and check the in_stock and price fields, convert into proper types and then sort. The plan of such a query, after filling the table with 100k rows, looks like this:

```sql
                                                        QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=9256.48..9256.48 rows=1 width=32) (actual time=412.911..412.912 rows=1 loops=1)
   ->  Sort  (cost=9256.48..9499.05 rows=97027 width=32) (actual time=412.910..412.910 rows=1 loops=1)
         Sort Key: (((data ->> 'price'::text))::numeric)
         Sort Method: top-N heapsort  Memory: 25kB
         ->  Seq Scan on products  (cost=0.00..8771.34 rows=97027 width=32) (actual time=0.022..375.624 rows=100000 loops=1)
               Filter: (((data ->> 'in_stock'::text))::integer > 0)
 Total runtime: 412.939 ms
(7 rows)
```

The “Seq Scan” line means that PostgreSQL needs to read the whole table. The time of 412 ms is not that bad, but can we make it better?

Fortunately PostgreSQL has a great feature: indexes on expressions, also named as functional indexes. It can store in the index sorted values of some expressions, and if the same expressions occur in a query, then the index can be used.

The indexes I need are:

```sql
CREATE INDEX i_products_in_stock ON products(( (data->>'in_stock')::integer ));
CREATE INDEX i_products_price ON products(( (data->>'price')::decimal ));
```

Notice the double parenthesis, they are required because of the non trivial expression.

The plan now looks a little bit different, after creating indexes and running analyze on the products table:

```sql
                                                                    QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.42..0.55 rows=1 width=32) (actual time=0.041..0.041 rows=1 loops=1)
   ->  Index Scan Backward using i_products_price on products  (cost=0.42..13690.06 rows=100000 width=32) (actual time=0.041..0.041 rows=1 loops=1)
         Filter: (((data ->> 'in_stock'::text))::integer > 0)
 Total runtime: 0.062 ms
(4 rows)
```

So it is 664k percent faster.

### The JSON Advantage

The JSON solution has got one nice feature which the native PostgreSQL hasn’t. The application can add its own fields on the fly without altering any table. JSON field is just a text, however with some validation. The new field won’t be checked by the indexes and constraints I’ve shown you above.

What’s more, you can add a constraint for this field later. This way you can have the best from both worlds: easy data model changing and consistent JSON structure across the database.

On the other hand you could of course add a trigger checking the JSON, before saving it to database, to check the list of available fields. This way you could prevent adding new fields by the application.

### Summary

So, I’ve shown you how you can use PostgreSQL as a simple NoSQL database storing JSON blobs of text. The great advantage over the simple NoSQL databases storing blobs is that you can constrain the blobs, so they are always correct and you shouldn’t have any problems with parsing and getting them from the database.

You can also query the database very easily, with huge speed. The ad-hoc queries are really simple, much simpler than the map-reduce queries which are needed in many NoSQL databases.
