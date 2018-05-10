---
author: David Christensen
gh_issue_number: 1061
tags: shell, mysql, perl, postgres
title: MySQL to PostgreSQL Migration Tips
---

I recently was involved in a project to migrate a client’s existing application from MySQL to PostgreSQL, and I wanted to record some of my experiences in doing so in the hopes they would be useful for others.

Note that these issues should not be considered exhaustive, but were taken from my notes of issues encountered and/or things that we had to take into consideration in this migration process.

### Convert the schema

The first step is to convert the equivalent schema in your PostgreSQL system, generated from the original MySQL.

We used `mysqldump --compatible=postgresql --no-data` to get a dump which matched PostgreSQL’s quoting rules. This file still required some manual editing to cleanup some of the issues, such as removing MySQL’s “Engine” specification after a CREATE TABLE statement, but this resulted in a script in which we were able to create a skeleton PostgreSQL database with the correct database objects, names, types, etc.

Some of the considerations here include the database collations/charset. MySQL supports multiple collations/charset per database; in this case we ended up storing everything in UTF-8, which matched the encoding of the PostgreSQL database, so there were no additional changes needed here; otherwise, it would have been necessary to note the original encoding of the individual tables and later convert that to UTF-8 in the next step.

We needed to make the following modifications for datatypes:

<table style="border: 1px;"><tbody><tr>     <th>MySQL Datatype</th>     <th>PostgreSQL Datatype</th>   </tr>
<tr>     <td>tinyint</td>     <td>int</td>   </tr>
<tr>     <td>int(<i>NN</i>)</td>     <td>int</td>   </tr>
<tr>     <td>blob</td>     <td>bytea*</td>   </tr>
<tr>     <td>datetime</td>     <td>timestamp with timezone</td>   </tr>
<tr>     <td>int unsigned</td>     <td>int**</td>   </tr>
<tr>     <td>enum('1')</td>     <td>bool</td>   </tr>
<tr>     <td>longtext</td>     <td>text</td>   </tr>
<tr>     <td>varbinary(<i>NN</i>)</td>     <td>bytea</td>   </tr>
</tbody></table>

*\* Note: we ended up converting these specific fields to text, just given the data that was stored in these fields in actuality, which just goes to show you should review your data.*

*\*\* Note: because PostgreSQL does not have unsigned numeric types, if this feature is an important part of your data model you can/should add a CHECK constraint to the column in question to check that the value is non-negative.*

A few other syntactic changes; MySQL’s UNIQUE KEY in the CREATE TABLE statement needs to just be UNIQUE.

Some of the MySQL indexes were defined as FULLTEXT indexes as well, which was a keyword PostgreSQL did not recognize. We made note of these, then created just normal indexes for the time being, intending to review to what extent these actually needed full text search capabilities.

Some of the AUTO_INCREMENT fields did not get the DEFAULT value set correctly to a sequence, because those types just ended up as integers without being declared a serial field, so we used the following query to correct this:

```sql
-- cleanup missing autoincrement fields

WITH
datasource AS (
    SELECT
        k.table_name,
        k.column_name,
        atttypid::regtype,
        adsrc
    FROM
        information_schema.key_column_usage k
    JOIN
        pg_attribute
    ON
        attrelid = k.table_name :: regclass AND
        attname = k.column_name
    LEFT JOIN
        pg_attrdef
    ON
        adrelid = k.table_name :: regclass AND
        adnum = k.ordinal_position
    WHERE
        table_name IN (
            SELECT table_name::text FROM information_schema.key_column_usage WHERE constraint_name LIKE '%_pkey' GROUP BY table_name HAVING count(table_name) = 1
        ) AND
        adsrc IS NULL AND
        atttypid = 'integer' ::regtype
),
frags AS (
    SELECT
        quote_ident(table_name || '_' || column_name || '_seq') AS q_seqname,
        quote_ident(table_name) as q_table,
        quote_ident(column_name) as q_col
    FROM
        datasource
),
queries AS (
    SELECT
        'CREATE SEQUENCE ' || q_seqname || ';
' ||
        'ALTER TABLE ' || q_table || ' ALTER COLUMN ' || q_col || $$ SET DEFAULT nextval('$$ || q_seqname || $$');
    $$ ||
        $$SELECT setval('$$ || q_seqname || $$',(SELECT max($$ || q_col || ') FROM ' || q_table || '));
' AS query
    FROM frags
)
SELECT
    COALESCE(string_agg(query, E'\n'),$$SELECT 'No autoincrement fixes needed';$$) AS queries FROM queries
\gset

BEGIN;
:queries
COMMIT;
```

Basically the idea is that we look for all table with a defined integer primary key (hand-waving it it by using the _pkey suffix in the constraint name), but without a current default value, then generate the equivalent SQL to create a sequence and set that table’s default value to the nextval() for the sequence in question. We also generate SQL to scan that table and set that sequence value to the next appropriate value for the column in question. (Since this is for a migration and we know we’ll be the only user accessing these tables we can ignore MVCC.)

Another interesting thing about this script is that we utilize psql’s ability to store results in a variable, using the \gset command, then we subsequently execute this SQL by interpolating that corresponding variable in the same script.

### Convert the data

The next step was to prepare the data load from a MySQL data-only dump. Using a similar dump recipe as for the initial import, we used: `mysqldump --compatible=postgresql --no-create-info --extended-insert > data.sql` to save the data in a dump file so we could iteratively tweak our approach to cleaning up the MySQL data.

Using our dump file, we attempted a fresh load into the new PostgreSQL database. This failed initially due to multiple issues, including ones of invalid character encoding and stricter datatype interpretations in PostgreSQL.

What we ended up doing was to create a filter script to handle all of the “fixup” issues needed here. This involved decoding the data and reencoding to ensure we were using proper UTF8, performing some context-sensitive datatype conversions, etc.

### Additional schema modifications

As we were already using a filter script to process the data dump, we decided to take the opportunity to fixup some warts in the current table definitions. This included some fields which were varchar, but should have actually been numeric or integer; as this was a non-trivial schema (100 tables) we were able to use PostgreSQL’s system views to identify a list of columns which should should be numeric and were currently not.

Since this was an ecommerce application, we identified columns that were likely candidates for data type reassignment based on field names *count, *qty, *price, *num.

Once we identified the fields in question, I wrote a script to generate the appropriate ALTER TABLE statements to first drop the default, change the column type, then set the new default. This was done via a mapping between table/column name and desired output type.

### Convert the application

The final (and needless to say most involved step) was to convert the actual application itself to work with PostgreSQL. Despite the fact that these databases both speak SQL, we had to come up for solutions for the following issues:

### Quotation styles

MySQL is more lax with its quoting styles, so some of this migration involved hunting down differences in quoting styles. The codebase contained lots of double-quoted string literals, which PostgreSQL interprets as identifiers, as well as the difference in quoting of column names (backticks for MySQL, double-quotes for PostgreSQL). These had to be identified wherever they appeared and fixed to use a consistent quoting style.

### Specific unsupported syntax differences:

#### INSERT ON DUPLICATE KEY

MySQL supports the INSERT ON DUPLICATE KEY syntax. Modifying these queries involved creating a special UPSERT-style function to support the different options in use in the code base. We isolated and categorized the uses of INSERT ON DUPLICATE KEY UPDATE into several categories: those which did a straight record replace and those which did some sort of modification. I wrote a utility script (detailed later in this article) which served to replicate the logic needed to handle this as the application would expect.

Upcoming versions of PostgreSQL are likely to incorporate an INSERT ... ON CONFLICT UPDATE/IGNORE syntax, which would produce a more direct method of handling migration of these sorts of queries.

#### INSERT IGNORE

MySQL’s INSERT ... IGNORE syntax allows you to insert a row and effectively ignore a primary key violation, assuming that the rest of the row is valid. You can handle this case via creating a similar UPSERT function as in the previous point. Again, this case will be easily resolved if PostgreSQL adopts the INSERT ... ON CONFLICT IGNORE syntax.

#### REPLACE INTO

MySQL’s REPLACE INTO syntax effectively does a DELETE followed by an INSERT; it basically ensures that a specific version of a row exists for the given primary key value. We handle this case by just modifying these queries to do an unconditional DELETE for the Primary Key in question followed by the corresponding INSERT. We ensure these are done within a single transaction so the result is atomic.

#### INTERVAL syntax

Date interval syntax can be slightly different in MySQL; intervals may be unquoted in MySQL, but **must** be quoted in PostgreSQL. This project necessitated hunting down several instances to add quoting of specific literal INTERVAL instances.

### Function considerations

#### last_insert_id()

Many times when you insert a records into a MySQL table, later references to this are found using the last_insert_id() SQL function. These sorts of queries need to be modified to utilize the equivalent functionality using PostgreSQL sequences, such as the currval() function.

#### GROUP_CONCAT()

MySQL has the GROUP_CONCAT function, which serves as a string “join” of sorts. We emulate this behavior in PostgreSQL by using the string_agg aggregate function with the delimiter of choice.

#### CONCAT_WS() —​ expected to be but not an issue; PG has this function

PostgreSQL has included a CONCAT_WS() function since PostgreSQL 9.1, so this was not an issue with the specific migration, but could still be an issue if you are migrating to an older version of PostgreSQL.

#### str_to_date()

This function does not exist directly in PostgreSQL, but can be simulated using to_date(). Note however that the format string argument differs between MySQL and PostgreSQL’s versions.

#### date_format()

MySQL has a date_format() function which transforms a date type to a string with a given format option. PostgreSQL has similar functionality using the to_char() function; the main difference here lies in the format string specifier.

#### DateDiff()

DateDiff() does not exist in PostgreSQL, this is handled by transforming the function call to the equivalent date manipulation operators using the subtraction (-) operator.

#### rand() to random()

This is more-or-less a simple function rename, as the equivalent functionality for returning a random float between 0.0 <= x <= 1.0 exists in PostgreSQL and MySQL, it’s just what the function name itself is. The other difference is that MySQL supports a scale argument so the random number for rand(*N*) will be returned between 0.0 <= x <= N, whereas you’d have to scale the result in PostgreSQL yourself, via random() * N.

#### IF() to CASE WHEN ELSE

MySQL has an IF() function which returns the second argument in the case the first argument evaluates to true otherwise returns the third argument. This can be trivially converted from IF(expression1, arg2, arg3) to the equilvalent PostgreSQL syntax: CASE WHEN expression1 THEN arg2 ELSE arg3.

#### IFNULL() to COALESCE()

MySQL has a function IFNULL() which returns the first argument if it is not NULL, otherwise it returns the second argument. This can effectively be replaced by the PostgreSQL COALESCE() function, which serves the same purpose.

#### split_part()

MySQL has a built-in function called split_part() which allows you to access a specific index of an array delimited by a string. PostgreSQL also has this function, however the split_part() function in MySQL allows the index to be negative, in which case this returns the part from the right-hand side.

in MySQL:

```sql
split_part('a banana boat', ' ', -1) => 'boat'
```
in PostgreSQL:

```sql
split_part('a banana boat', ' ', -1) => // ERROR: field position must be greater than zero
```

I fixed this issue by creating a custom plpgsql function to handle this case. (In my specific case, all of the negative indexes were -1; i.e., the last element in the array, so I created a function to return only the substring occurring after the last instance of the delimiter.)

### Performance considerations

#### You may need to revisit COUNT(*) queries

MySQL MyISAM tables have a very fast COUNT(*) calculation, owing to queries taking a table lock (which means MySQL can cache the COUNT(*) result itself, since there can be no concurrent updates), while PostgreSQL utilizes MVCC in order to calculate table counts which necessitates a full table scan to see which rows are visible to the specific calling snapshot, so this assumption may need to be revisited in order to calculate an equivalent performant query.

#### GROUP BY vs DISTINCT ON

MySQL is much more (*ahem*) flexible when it comes to GROUP BY/aggregate queries, allowing some columns to be excluded in a GROUP BY or an aggregate function. Making the equivalent query in PostgreSQL involves transforming the query from SELECT ... GROUP BY (cols) to a SELECT DISTINCT ON (cols) ... and providing an explicit sort order for the rows.

### More notes

Don’t be afraid to script things; in fact, I would go so far as to suggest that **everything** you do should be scripted. This process was complicated and there were lots of moving parts to ensure moved in tandem. There were changes being made on the site itself concurrently, so we were doing testing against a dump of the original database at a specific point-in-time. Having everything scripted ensured that this process was repeatable and testable, and that we could get to a specific point in the process without having to remember anything I’d done off-the-cuff.

In addition to scripting the actual SQL/migrations, I found it helpful to script the solutions to various classifications of problems. I wrote some scripts which I used to create some of the various scaffolding/boilerplate for the tables involved. This included a script which would create an UPSERT function for a specific table given the table name, which was used when replacing the INSERT ON DUPLICATE KEY UPDATE functions. This generated script could then be tailored to handle more complex logic beyond a simple UPDATE. (One instance here is an INSERT ON DUPLICATE KEY UPDATE which increased the count of a specific field in the table instead of replacing the value.)

```perl
#!/usr/bin/env perl
# -*-cperl-*-

use strict;
use warnings;

use Data::Dumper;

my $table = shift or die "Usage: $0 <table>\n";
my @cols = @ARGV;

my $dbh = DBI->connect(...);

my @raw_cols = @{ $dbh->column_info(undef, 'public', $table, '%')->fetchall_arrayref({}) };
my %raw_cols = map { $_->{COLUMN_NAME} => $_ } @raw_cols;

die "Can't find table $table\n" unless @raw_cols;

my @missing_cols = grep { ! defined $raw_cols{$_} } @cols;

die "Referenced non-existing columns: @missing_cols\n" if @missing_cols;

my %is_pk;

unless (@cols) {
    @cols = map { $_->{COLUMN_NAME} } @raw_cols;
}

my @pk_cols = $dbh->primary_key(undef, 'public', $table);

@is_pk{@pk_cols} = (1)x@pk_cols;

my @data_cols = grep { ! $is_pk{$_} } @cols;

die "Missing PK cols from column list!\n" unless @pk_cols == grep { $is_pk{$_} } @cols;
die "No data columns!\n" unless @data_cols;

print <<EOF
CREATE OR REPLACE FUNCTION
    upsert_$table (@{[
    join ', ' => map {
        "_$_ $raw_cols{ $_ }->{pg_type}"
    } @cols
]})
RETURNS void
LANGUAGE plpgsql
AS \$EOSQL\$
BEGIN
    LOOP
        UPDATE $table SET @{[
    join ', ' => map { "$_ = _$_" } @data_cols
]} WHERE @{[
    join ' AND ' => map { "$_ = _$_" } @pk_cols
]};
        IF FOUND THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO $table (@{[join ',' => @cols]}) VALUES (@{[join ',' => map { "_$_" } @cols]});
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Do nothing, and loop to try the UPDATE again.
        END;
    END LOOP;
END
\$EOSQL\$
;
EOF
;
```

This script created an upsert function from a given table to update all columns by default, also allowing you to create one with a different number of columns upserted.

I also wrote scripts which could handle/validate some of the column datatype changes. Since there were large numbers of columns which were changed, often multiple in the same table, I was able to have this script create a single ALTER TABLE statement with multiple ALTER COLUMN TYPE USING clauses, plus be able to specify the actual method that these column changes were to take place. These included several different approaches, depending on the target data type, but generally were to solve cases where there were fairly legitimate data that was not picked up by PostgreSQL’s input parsers. These included how to interpret blank fields as integers (in some cases we wanted it to be 0, in others we wanted it to be NULL), weird numeric formatting (leaving off numbers before or after the decimal point), etc.

We had to fix up in several locations missing defaults for AUTO_INCREMENT columns. The tables were created with the proper datatype, however we had to find tables which matched a specific naming convention and create/associate a sequence/serial column, set the proper default here, etc. (This was detailed above.)

There was a fair amount of iteration and customization in this process, as there was a fair amount of data which was not of the expected format. The process was iterative, and generally involved attempting to alter the table from within a transaction and finding the next datum which the conversion to the expected type did not work. This would result in a modification of the USING clause of the ALTER TABLE ALTER COLUMN TYPE to accommodate some of the specific issues.

In several cases, there were only a couple records which had bad/bunko data, so I included explicit UPDATE statements to update those data values via primary key. While this felt a bit “impure”, it was a quick and preferred solution to the issue of a few specific records which did not fit general rules.
