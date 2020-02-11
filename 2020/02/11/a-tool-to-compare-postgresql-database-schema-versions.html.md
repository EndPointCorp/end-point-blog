---
author: "Selvakumar Arumugam"
title: "A Tool to Compare PostgreSQL Database Schema Versions"
tags: postgres, database, migration, schema
---


Recently we have completed a major data intensive application migration from one tech stack to another which had completely restructured database schema. The consortium who developed the new application have written migration scripts to transfer data from their old stack to the new one. The old application stack vendor abandoned development and support many years back. So old application stack was evolved with custom changes and new features independently in recent years. 


It is evident that consortium migration scripts can not be directly applied to our client application. But writing migration scripts from scratch will be reinventing the wheel, due to the fact that it’s much more labor-intensive and time-consuming. We were looking to reuse the scripts and customize to make sure it is a 100% match with our client application custom changes.


### Liquibase - Schema Comparison Tool

We have researched for a suitable solution to match with our needs and requirements. The search led us to an awesome open-source schema comparison tool called “Liquibase” with the diff command to figure out following line items. 

* Missing Objects
* Changed Objects
* Unexpected Objects

### Installation and Usage

Let's see how to use Liquibase and collect insights in results offered by the diff command. The liquibase tarball format binary package is available in github. Download the latest version and extract into the installation path. The default package doesn't have a driver, it’s advisable to add PostgreSQL driver to the lib folder. It can be used for other databases with necessary libraries and drivers as well.


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

### Comparison Results
The following output shows the list of all sections[removed details to save the page :)] with missing, changed and newly added objects to the section.

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

### Benefits
It helped us to compare the 100+ tables in the old application stack database schema version between our client and consortium. The data migration part was challenging due to volume and the variety of data but knowing the schema differences through liquibase on table level, columns, references, indexes, views..etc helped in accuracy on the migration process. So it played a wonderful role in our migration work and hope it will be helpful for you.
