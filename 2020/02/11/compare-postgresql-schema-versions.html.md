---
author: "Selvakumar Arumugam"
title: "A Tool to Compare PostgreSQL Database Schema Versions"
tags: postgres, database
gh_issue_number: 1589
---

<img src="/blog/2020/02/11/compare-postgresql-schema-versions/parcel-sorting.jpg" alt="Parcel sorting" /> [Photo](https://unsplash.com/photos/k6hti1f8WSw) by [@kelvyn](https://unsplash.com/@kelvyn) on [Unsplash](https://unsplash.com/)

The End Point development team has completed a major application migration from one stack to another. Many years ago, the vendor maintaining the old stack abandoned support and development. This led to a stack evolution riddled with independent custom changes and new features in the following years. The new application was developed by a consortium that allowed migration scripts to transfer data to a fresh stack resulting in a completely restructured database schema. While consortium migration scripts cannot be directly applied to our client application, attempting to create migration scripts from scratch would be tedious due to more labor-intensive and time-consuming tasks. Our development team looked to reuse and customize the scripts in order to ensure an exact match of the customized changes to the client’s application.

### Liquibase—Schema Comparison Tool

After an arduous hunt to acquire a suitable solution, the End Point team came across Liquibase, an open-source schema comparison tool that utilizes the `diff` command to assess line items such as missing, changed, and unexpected objects.

#### Installation and Usage

Below is an example of how to use Liquibase as well as review the insights and results offered by the `diff` command. Before beginning, download the latest version of [Liquibase](https://github.com/liquibase/liquibase/releases/). As the default package doesn’t have its own driver, it would be wise to add the PostgreSQL driver to the Liquibase lib folder (you’ll need to do this with any other database types and their necessary libraries and drivers).

```bash
$ wget https://github.com/liquibase/liquibase/releases/download/v3.8.5/liquibase-3.8.5.tar.gz
$ tar -xvzf liquibase-3.8.5.tar.gz
$ wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.5/postgresql-42.2.5.jar -P lib/

$ ./liquibase \
--classpath="/Users/<user>/apps/liquidiff/lib" \
--outputFile=liquibase_output.txt \
--driver=org.postgresql.Driver \
--url=jdbc:postgresql://localhost:5432/schema_two \
--username=postgres \
--password=CHANGEME \
--defaultSchemaName=public \
Diff \
--referenceUrl=jdbc:postgresql://localhost:5432/schema_one \
--referenceUsername=postgres \
--referencePassword=CHANGEME \
--referenceDefaultSchemaName=public
```

#### Comparison Results
The following output shows the list of all sections with missing, changed, and newly added objects to each section.

```bash
$ cat liquibase_output.txt

Reference Database: postgres @ jdbc:postgresql://localhost:5432/schema_one (Default Schema: public)
Comparison Database: postgres @ jdbc:postgresql://localhost:5432/schema_two (Default Schema: public)
Compared Schemas: public
Product Name: EQUAL
Product Version: EQUAL
Missing Catalog(s): NONE
Unexpected Catalog(s): NONE
Changed Catalog(s): 
     schema_one
          name changed from 'schema_one' to 'schema_two'
Missing Column(s): 
     public.users.settings
     ...
Changed Column(s): 
     public.table_one.unique_no
          type changed from 'varchar(20 BYTE)' to 'varchar(255 BYTE)'     
     public.table_two.created_at
          defaultValue changed from 'null' to 'now()'
          nullable changed from 'false' to 'true'
          order changed from '4' to '22'
    ...
Missing Foreign Key(s): 
     one_two_id_fkey(one[two_id] -> two[id])
    ...
Unexpected Foreign Key(s): 
    ...
Changed Foreign Key(s): 
    ...
Missing Index(s): 
    ...
Unexpected Index(s): 
     table_pkey UNIQUE  ON public.table(id)
    ...
Changed Index(s): 
     index_events_on_record_number ON public.table(record_number)
          unique changed from 'false' to 'true'
    ...
Missing Primary Key(s): ...
Unexpected Primary Key(s): ...
Changed Primary Key(s): ...
Missing Schema(s): NONE
Unexpected Schema(s): NONE
Changed Schema(s): NONE
Missing Sequence(s): ...
Unexpected Sequence(s): NONE
Changed Sequence(s): NONE
Missing Stored Procedure(s): NONE
Unexpected Stored Procedure(s): NONE
Changed Stored Procedure(s): NONE
Missing Table(s): ...
Unexpected Table(s): ...
Changed Table(s): NONE
Missing Unique Constraint(s): NONE
Unexpected Unique Constraint(s): NONE
Changed Unique Constraint(s): NONE
Missing View(s): ...
Unexpected View(s): NONE
Changed View(s): NONE
Liquibase command 'Diff' was executed successfully.
```

#### Conclusion
Although comparing and contrasting the 100+ tables from the old application was beneficial, the data migration was challenging due to volume and variety of data. However, with the help of Liquibase, we became more familiarized with differences in the schema (including table level, columns, references, indexes, views, etc.). This led to an increase in accuracy which was very helpful during the migration process. The End Point development team hopes that by sharing its findings, others will also benefit from this tool and all that it offers.
