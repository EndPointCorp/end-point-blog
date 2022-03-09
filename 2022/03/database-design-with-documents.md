---
author: Emre Hasegeli
title: 'Database Design: Using Documents'
github_issue_number: xxx
tags:
- database
- development
- performance
- postgres
- sql
date: xxx
---

Using documents in relational databases is increasingly popular.  This
technique can be practical and efficient when used in fitting circumstances.

### Example

Let's start with an example.  Imagine we are scraping web sites for external
URLs and store them in a table.  We'll have the web sites table to store
the scrape timestamp and another table to store all of the references.

```sql
CREATE TABLE web_sites (
    web_site_domain text NOT NULL,
    last_scraped_at timestamptz,

    PRIMARY KEY (web_site_domain)
);

CREATE TABLE refs (
    web_site_domain text NOT NULL,
    ref_location text NOT NULL,
    link_url text NOT NULL,

    PRIMARY KEY (web_site_domain, ref_location, link_url),
    FOREIGN KEY (web_site_domain) REFERENCES web_sites
);
```

We do not need to bother adding an id to the `web_sites` table, because we
assume there won't be too many of them.  The domain is small and more
practical to use as an identifier.  If you are curious about advantages
of using natural keys, see [my previous article](/blog/2021/03/database-design-using-natural-keys).

### Normalized Tables

There may be many thousands of unique URLs for a single web site and other
web sites may refer to the same URLs.  To try to minimize the storage,
we can keep the locations and the URLs in separate tables, give them integer
identifiers, and have another table for the many-to-many relations.

```sql
CREATE TABLE locations (
    location_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    web_site_domain text NOT NULL,
    ref_location text NOT NULL,

    PRIMARY KEY (location_id),
    UNIQUE (web_site_domain, ref_location),
    FOREIGN KEY (web_site_domain) REFERENCES web_sites
);

CREATE TABLE links (
    link_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    link_url text NOT NULL,

    PRIMARY KEY (link_id),
    UNIQUE (link_url)
);

CREATE TABLE locations_links (
    location_id bigint NOT NULL,
    link_id bigint NOT NULL,

    PRIMARY KEY (location_id, link_id),
    FOREIGN KEY (location_id) REFERENCES locations,
    FOREIGN KEY (link_id) REFERENCES links
);
```

The idea in here is to keep our biggest table narrow.  It'd pay off to refer
to the `locations` and `links` just with integer identifiers when we'll have
very many of them.

### Table Sizes

We'll have many web sites and many URLs, so our lookup tables would be big
and the relation table would be even bigger.  That is going to be a major
problem because of many reasons, one of them being space efficiency.  Narrow
tables with many rows are not very space efficient especially on Postgres
where there's 24 bytes per-row overhead.  To demonstrate it being significant,
let's add one row to each of the tables to see the sizes compared with
the overhead.

```sql
INSERT INTO web_sites (web_site_domain)
VALUES ('example.com');

INSERT INTO refs (web_site_domain, ref_location, link_url)
VALUES ('example.com', '/source', 'http://example.net/target.html');

INSERT INTO locations (web_site_domain, ref_location)
VALUES ('example.com', '/source');

INSERT INTO links (link_url)
VALUES ('http://example.net/example.html');

INSERT INTO locations_links
VALUES (1, 1);

SELECT table_name, tuple_len, (100.0 * 24 / tuple_len)::int AS overhead_perc
FROM information_schema.tables, LATERAL pgstattuple(table_name)
WHERE table_schema = 'public';

   table_name    | tuple_len | overhead_perc
-----------------+-----------+---------------
 web_sites       |        36 |            67
 refs            |        75 |            32
 locations       |        52 |            46
 links           |        64 |            38
 locations_links |        40 |            60
```

With just one rows and such short domains and URLs, we wouldn't be gaining
anything by having the links on a lookup table.  In fact, it's a lot less
efficient.  Although, the situation may change with with many rows.

### Composite Types

We can combine multiple fields in a column to avoid the overhead of many
rows in narrow tables.  Postgres has good support for composite types and
arrays over them.  They are useful if you need strict data type checking.

```sql
CREATE TYPE web_site_page AS (
    ref_location text,
    link_urls text[]
);

ALTER TABLE web_sites ADD COLUMN pages web_site_page[];

UPDATE web_sites
SET pages = ARRAY[ROW(ref_location, ARRAY[link_url])::web_site_page]
FROM refs;

SELECT pg_column_size(pages) FROM web_sites;

 pg_column_size
----------------
            117
```

As you see, the new column is not exactly small because composite types
and arrays come with their own overheads.  Still it could be much better
when a web site has many references.

### JSON Document Column

The composite types are not very easy to work with.  We can store the pages
in another format.  JSON is the most popular one nowadays.  There are multiple
options to store JSON in a column in Postgres.  Let's start with
the text-based data type.

```sql
ALTER TABLE web_sites ADD COLUMN pages_json json;

UPDATE web_sites SET pages_json = to_json(pages);

SELECT pg_column_size(pages_json) FROM web_sites;

 pg_column_size
----------------
             76
```

What is perhaps also surprising is the JSON being smaller than the array over
composite type.  This is because Postgres data types are a bit wasteful because
of alignment and storing oids of the enclosed data types repeatedly.

### Binary JSON

Another JSON data type, `jsonb` is available in Postgres.  It is a binary
structure that allows faster access to the values inside the document.

```sql
ALTER TABLE web_sites ADD COLUMN pages_jsonb jsonb;

UPDATE web_sites SET pages_jsonb = to_jsonb(pages);

SELECT pg_column_size(pages_jsonb) FROM web_sites;

 pg_column_size
----------------
             98
```

As you see the text-based JSON is still smaller.  This is due to the binary
offsets stored in the binary structure for faster access to the fields.
The text based JSON also compresses better.

### Size Comparison

Very simple single row data shows the text-based `json` as the smallest,
binary `jsonb` a bit larger, and the composite type to be the largest.
However, the differences would be a lot smaller with more realistic sample data
with many items inside the documents.  I generated some data and gathered
these results (the sizes excluding the indexes).

        model         |   size
    ------------------|---------
    single table      |  436 MiB
    normalized tables |  387 MiB
    composite type    |  324 MiB
    json              |  318 MiB
    jsonb             |  320 MiB

You may expect the normalized tables to be the smallest as otherwise
the metadata is stored repeatedly in the columns.  Though, the results reveal
it's the other way around.  This is because of the per-row overhead in
Postgres.  It becomes noticeable in narrow tables as in this example.

It's also useful to notice that the most of the size is occupied by
the TOAST tables when the data is stored in a single column.  TOAST is
a mechanism in Postgres that kicks in when a column is large enough which
would often be the case when you design your tables this way.  In this case,
the table excluding the TOASTed part is pretty small which would help
any query that doesn't touch the large column.

### Usability

What matters more than size is the usability of having it all in a single
column.  It is really practical to send and receive this column as a whole
all the way from the database to the frontend.  Compare this with dealing
with lots of small objects used with the normalized tables.

It's also possible in Postgres to index the document columns to allow
efficient searches in them.  There are many options to do so with advantages
and disadvantages over each other.  Though this post is getting long.  I'll
leave indexing to another one.
