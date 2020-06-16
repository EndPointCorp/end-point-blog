---
author: "Árpád Lajos"
title: "Migrating large PostgreSQL databases"
tags: postgres, big-data, database
gh_issue_number: 1613
---

![Migration](/blog/2020/04/21/migrating-large-postgresql-databases/migration.jpg)

Photo by [Harshil Gudka](https://unsplash.com/@hgudka97) on [Unsplash](https://unsplash.com/)

### The challenge

One of our clients has a large and important health-related application. It’s built on an end-of-life Ruby on Rails-based open source framework, heavily customized over the years. They wanted to upgrade to a newer, supported, Java-based open source application a partner organization had developed as a replacement. Both organizations used the old system previously. To do that we would need to migrate all their existing PostgreSQL data from the old system to the new one, retaining important customizations while adapting to the new database schema.

Although there were many similarities between the old system and the new, the differences were significant enough to require careful study of the database schemas and the migration scripts designed to move the data:

- There were schema-level differences between our old database and the partner organization’s old database.
- Even where the two old databases were similar there were differences on the data level, such as different standards, different values in table records, different representation, etc.
- We had different content, so if a script was working well for their data, it was not necessarily correct for us.
- There were dynamically generated tables for both old databases and we had to find out how we can convert our current schema elements along with its records to the planned schema elements along with its records.

We had to understand the differences between our and their old databases. Due to the number of tables and average number of columns, manual comparison between databases was not really an option. We knew that the algorithm of handling the scripts would look like below:

```plain
For each S in Scripts
    Analyze S and understand the intent behind it
    Compute a read-only version of S to avoid write operations
    Execute the read-only version of S
    Analyze the results and find out whether they are different from the expected results
    Convert our read-only version of S to S′, where S′ is compatible with our expectations
    While there are technical issues do
        Fix it
    While end
    Execute S′
For end
```

Understanding these differences was easier said than done. The main problem is that we found it difficult to define our exact expectations. For that purpose we needed a deeper understanding about the databases.

### Entity Relationship Diagram

We first needed to see an Entity Relationship Diagram (ER diagram or ERD). We used [DbVisualizer](https://www.dbvis.com/) for this.

We imported the database into our local RDBMS and then created a database connection by right-clicking Connections in the left menu tree

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvisualizer-connections.png)

then clicking on Create Database Connection and selecting No Wizard

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvisualizer-connection-wizard.png)

and filling in the data. 

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvisualizer-connection-form.png)

After that, we double-clicked on the schema we wanted to generate an ER diagram for and clicked on Open Object.

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvisualizer-open-object.png)

Finally, we clicked on the References tab and a bird’s-eye view of the ER diagram was generated.

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvizualizer-references.png)

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvisualizer-schema-birdview.png)

Then we right-clicked on the diagram and clicked on Export.

![](/blog/2020/04/21/migrating-large-postgresql-databases/dbvisualizer-schema-export.png)

We chose SVG and saved it. After opening the SVG diagram, we saw that the schema was too big to easily analyze, so we dropped the tables we were not specifically interested in in our local copy and generated a new ER diagram. It was super easy and cool. Finally, we were able to see which parts of the other team’s database was old and which was new. We were also able to compare our old database with the new database we were implementing.

### Comparing our databases against their counterparts

Next we needed to understand what the schema differences were between their old database and our old database to determine what selections in the scripts will not work properly and to determine how we needed to modify it to fit our technical nuances.

We used Liquibase for this purpose. See [Selva’s article on comparing PostgreSQL database schema versions](/blog/2020/02/11/compare-postgresql-schema-versions).

The actual command we used was [`diff`](https://www.liquibase.org/documentation/diff.html).

So, we needed to make sure we had a proper setup and then we could run the command. The example output the documentation gives is this:

```plain
Diff Results:
Reference Database: MYSCHEMA2 @ jdbc:oracle:thin:@localhost:1521:ORCL (Default Schema: MYSCHEMA2)
Comparison Database: MYSCHEMA @ jdbc:oracle:thin:@localhost:1521:ORCL (Default Schema: MYSCHEMA)
Compared Schemas: MYSCHEMA2 -> MYSCHEMA
Product Name: EQUAL
Product Version: EQUAL
Missing Catalog(s): NONE
Unexpected Catalog(s): NONE
Changed Catalog(s): NONE
Missing Check Constraint(s): NONE
Unexpected Check Constraint(s): NONE
Changed Check Constraint(s): NONE
Missing Column(s): NONE
Unexpected Column(s):
     MYSCHEMA.DEPARTMENT.ACTIVE
     MYSCHEMA.SERVICETECH.ACTIVE
     MYSCHEMA.SERVICETECH2.ACTIVE
     MYSCHEMA.SERVICETECH3.ACTIVE
     MYSCHEMA.VIEW1.ACTIVE
     MYSCHEMA.DATABASECHANGELOG.AUTHOR
     MYSCHEMA.DATABASECHANGELOG.COMMENTS
     MYSCHEMA.DATABASECHANGELOG.CONTEXTS
     MYSCHEMA.DATABASECHANGELOG.DATEEXECUTED
     MYSCHEMA.DATABASECHANGELOG.DEPLOYMENT_ID
     MYSCHEMA.DATABASECHANGELOG.DESCRIPTION
     MYSCHEMA.DATABASECHANGELOG.EXECTYPE
     MYSCHEMA.DATABASECHANGELOG.FILENAME
     MYSCHEMA.DATABASECHANGELOG.ID
     MYSCHEMA.DATABASECHANGELOGLOCK.ID
     MYSCHEMA.DEPARTMENT.ID
     MYSCHEMA.SERVICETECH.ID
     MYSCHEMA.SERVICETECH2.ID
     MYSCHEMA.SERVICETECH3.ID
     MYSCHEMA.VIEW1.ID
     MYSCHEMA.DATABASECHANGELOG.LABELS
     MYSCHEMA.DATABASECHANGELOG.LIQUIBASE
     MYSCHEMA.DATABASECHANGELOGLOCK.LOCKED
     MYSCHEMA.DATABASECHANGELOGLOCK.LOCKEDBY
     MYSCHEMA.DATABASECHANGELOGLOCK.LOCKGRANTED
     MYSCHEMA.DATABASECHANGELOG.MD5SUM
     MYSCHEMA.DEPARTMENT.NAME
     MYSCHEMA.SERVICETECH.NAME
     MYSCHEMA.SERVICETECH2.NAME
     MYSCHEMA.SERVICETECH3.NAME
     MYSCHEMA.VIEW1.NAME
     MYSCHEMA.DATABASECHANGELOG.ORDEREXECUTED
     MYSCHEMA.DATABASECHANGELOG.TAG
Changed Column(s): NONE
Missing Database Package(s): NONE
Unexpected Database Package(s): NONE
Changed Database Package(s): NONE
Missing Database Package Body(s): NONE
Unexpected Database Package Body(s): NONE
Changed Database Package Body(s): NONE
Missing Foreign Key(s): NONE
Unexpected Foreign Key(s): NONE
Changed Foreign Key(s): NONE
Missing Function(s): NONE
Unexpected Function(s): NONE
Changed Function(s): NONE
Missing Index(s): NONE
Unexpected Index(s):
     PK_DATABASECHANGELOGLOCK UNIQUE  ON MYSCHEMA.DATABASECHANGELOGLOCK(ID)
     PK_DEPARTMENT UNIQUE  ON MYSCHEMA.DEPARTMENT(ID)
     PK_SERVICETECH UNIQUE  ON MYSCHEMA.SERVICETECH(ID)
     PK_SERVICETECH2 UNIQUE  ON MYSCHEMA.SERVICETECH2(ID)
     PK_SERVICETECH3 UNIQUE  ON MYSCHEMA.SERVICETECH3(ID)
Changed Index(s): NONE
Missing Java Class(s): NONE
Unexpected Java Class(s): NONE
Changed Java Class(s): NONE
Missing Java Source(s): NONE
Unexpected Java Source(s): NONE
Changed Java Source(s): NONE
Missing Primary Key(s): NONE
Unexpected Primary Key(s):
     PK_DATABASECHANGELOGLOCK on MYSCHEMA.DATABASECHANGELOGLOCK(ID)
     PK_DEPARTMENT on MYSCHEMA.DEPARTMENT(ID)
     PK_SERVICETECH on MYSCHEMA.SERVICETECH(ID)
     PK_SERVICETECH2 on MYSCHEMA.SERVICETECH2(ID)
     PK_SERVICETECH3 on MYSCHEMA.SERVICETECH3(ID)
Changed Primary Key(s): NONE
Missing Sequence(s): NONE
Unexpected Sequence(s): NONE
Changed Sequence(s): NONE
Missing Stored Procedure(s): NONE
Unexpected Stored Procedure(s): NONE
Changed Stored Procedure(s): NONE
Missing Synonym(s): NONE
Unexpected Synonym(s): NONE
Changed Synonym(s): NONE
Missing Table(s): NONE
Unexpected Table(s):
     DATABASECHANGELOG
     DATABASECHANGELOGLOCK
     DEPARTMENT
     SERVICETECH
     SERVICETECH2
     SERVICETECH3
Changed Table(s): NONE
Missing Trigger(s): NONE
Unexpected Trigger(s): NONE
Changed Trigger(s): NONE
Missing Unique Constraint(s): NONE
Unexpected Unique Constraint(s): NONE
Changed Unique Constraint(s): NONE
Missing View(s): NONE
Unexpected View(s):
     VIEW1
Changed View(s): NONE
Liquibase command 'diff' was executed successfully.
```

Of course, we could do this job manually by listing all the tables with psql’s ```\dt``` and then checking each of them individually with ```\d tablename```, but if there are many tables, this would take forever.

Yes, we can write software for this purpose, implementing an algorithm along the lines of

```plain
tables = <execute \dt>
For each (tables as table) do
    Differences[table] = difference(<execute \d table at db1>, <execute \d table at db2>)
End For
```

however, the algorithm above won’t handle special cases, like tables existing in db1 and not in db2 or vice versa. The algorithm above graciously outsources the arduous task of splitting the rows in both cases by identifying whether a row is a column name, an index, a foreign key, etc. and by identifying the subject of the line (e.g. column name) and finding the matches between the two to a function called difference.

It is of course implementable, but it would add a considerable amount of work. We should also mention that such a newly developed piece of code would not be well tested yet and we would have to watch out for possible bugs, create unit tests, create a nice UI or file export to ensure that we can analyse the results, and so on. All this work is unnecessary due to the availability of Liquibase and we are only talking about a single command compared to the many here.

### Dynamically generated tables

In practical terms this means the data our software must manage does not fit a pre-established schema; users create and update new data collection forms regularly. These forms consist of sets of uniquely named questions and text-based answers to those questions. The [PostgreSQL JSON data type](https://www.postgresql.org/docs/current/datatype-json.html) may seem like a natural fit for such data. However, the original version of the software predates PostgreSQL’s now extensive JSON support. The software version from which we were upgrading stored these data in an [Entity-Attribute-Value schema](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model), a database pattern often maligned (justly) by database designers.

In this version, a single table stored all the answers given for every user-defined question for every case in the system, along with a pointer to the associated question and case. As one might expect, this table grew fairly large, though its principal drawbacks were not its size but rather the large number of joins necessary to process data it contained, and the lack of sufficient data validation. It is possible that the [hstore data type](https://www.postgresql.org/docs/current/hstore.html) would have been a better fit, however, neither programming language support for hstore data nor developer familiarity with it made it an obvious choice at the time. We did use hstore widely in the backend for data manipulation functions that could be contained entirely in SQL.

Fast forward to newer versions, where this schema has been redesigned. We weren’t involved in the design process and can’t comment on the justification behind this design decision, but the new version creates new tables within the database as needed for each data entry form, and text fields for each question on the form. This reduces the number of joins or aggregations necessary to compile all the data for one form for a single case, but it means creating SQL queries dynamically to create, and later to find, the tables and columns containing data of interest.

We’ve run our fingers through the data several times, both during and after the migration, and found neither schema variant satisfies our every wish. Both versions store users’ data as text fields, whatever data type they may represent. Some form of data validation at the database level would be very nice, and in the new version where each field has its own column in the database, this is entirely possible, though of course, it would have required more work in the development process. In particular, many questions expect answers taken from a predefined set, for which [enumerated types](https://www.postgresql.org/docs/current/datatype-enum.html) could be a good fit. Of course, stored procedures could conceivably ensure valid data no matter its data type in the schema, but this doesn’t seem like a plausible option in practice. As a further drawback to the new approach, column and table names derive from user-defined data, meaning we need to sanitize user input to create valid PostgreSQL identifiers. This is a tricky process, and difficult to separate entirely into its own module to avoid reimplementing the same intricate logic multiple times.

JSON data types provide one possible schema alternative, with all entries for one data entry form for a single case stored in a single JSON field, and indeed the [PostgreSQL documentation](https://www.postgresql.org/docs/current/datatype-json.html#JSON-DOC-DESIGN) proposes its use in such situations. It’s not entirely clear, though, that this would be a win. We could define new keys within the JSON structure without needing to modify the database schema itself, and with JSON we’d always know exactly what table and field we needed, to find the data we were after, but we’d still need to write queries dynamically in order to pull the desired fields. We could avoid some of the data sanitization necessary to create field names, as the rules for JSON key names are far more permissive than for column names in a proper database table. But, again barring extensive stored procedures, we would still have very limited ability to validate data within the database itself, as JSON supports only a small set of primitive types.

### Putting it all together

After we acquired the understanding that we needed we were able to work out the migration script according to the algorithm that we outlined at the start of this article.

This was still a long, labor-intensive task which was done by repeated pair-programming sessions but we were able to reach high enough accuracy. So high that to our great surprise we were able to start the application after the migration process was done.

### Release

We were able to do the release on a weekend and the three of us moved on to solving problems submitted by beta testers. We called this process “dragon hunting”.

![](/blog/2020/04/21/migrating-large-postgresql-databases/dragpon.jpg)

-----

(Written with help from [Selvakumar Arumugam](/team/selvakumar_arumugam) and [Joshua Tolley](/team/josh_tolley).)
