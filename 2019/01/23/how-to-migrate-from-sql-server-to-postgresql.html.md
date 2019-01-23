---
author: "Selvakumar Arumugam"
title: "How to Migrate from Microsoft SQL Server to PostgreSQL"
tags: pentaho, postgres, database, migration
---


One of our client had Java based applications stack in Linux servers with pretty old version of SQL Server database. We decided to migrate from SQL Server to PostgreSQL database to make the entire application stack more stable with regular updates and serve better with our Postgres experts.

I was experimenting with few approaches for the migration and decided to go with the process of schema migration and then data migration approach which is referred in Postgres wiki page. Let’s walk through the step by step process of migration.

### Schema Migration

SQL Server database tables and views schema need to be exported to perform schema conversion. The following steps will help to export the schema.

#### Export SQL Server Database Schema
In SQL Management Studio, right click on database > Tasks > Generate Scripts.

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/generate-scripts.png" alt='Generate Scripts' />

Choose ‘Select specific database objects’ and check only your application schema Tables [Untick dbo schema objects and others if any].

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/choose-tables.png" alt="Choose tables" />

Ensure that ‘type of the script’ in advanced options is set to ‘Schema Only’.

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/schema-only.png" alt="Schema Only" />

Review and save the database tables schema file(tables.sql).
Use WinSCP and public key auth to transfer the tables.sql file to linux server.

#### Convert Schema from SQL Server to Postgres

The sqlserver2pgsql is a good migration tool which is written in perl to convert SQL Server schema to Postgres schema. sqlserver2pgsql tool is available in github to clone into your database server and execute the following commands to convert the tables schema.

```bash
$ git clone https://github.com/dalibo/sqlserver2pgsql.git
$ cd sqlserver2pgsql
$ perl sqlserver2pgsql.pl -f tables.sql -b tables-before.sql -a tables-after.sql -u tables-unsure.sql
```

The converted schema available in tables-before.sql and constraint kind of queries will be in tables-after.sql to execute after data migration. Just review tables-unsure.sql and do the needful if there is any SQLs not converted by tool. If you want have any different name for schema in Postgres, you can rename the schema at this stage in sql file.
	
```bash
$ sed -i ‘s/sql_server_schema/public/g’ *.sql 
```

#### Setup Postgres Database:
I hope you would have Postgres database ready in database server. If not, Install the latest version of Postgres database in your server. Then create Postgres user and database with permissions granted to user.

```sql
CREATE USER <user_name> WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
  
CREATE DATABASE <database_name>
    WITH 
    OWNER = <user_name>
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
```

Once database and user account is ready, load converted tables-before.sql script into database to create tables. Then we can move forward with data migration.

```bash
psql -Uuser_name -p5432 -hlocalhost -d database_name -f tables-before.sql
	OR
database_name=# \i /path/to/tables-before.sql
```

### Data Migration
The data migration through data dump and restore makes the process cumbersome with huge manual process, data types mismatches, date formats, etc…, It is wise to use existing stable systems instead of investing more time into it.

#### Pentaho Data Integration

Pentaho offers various stable data centric products. The Pentaho Data Integration (PDI) is a ETL tool which provides great support on migrating data between different databases without any manual interventions. The community edition PDI is good enough to perform our task here. It needs to establish connection to both source and destination databases. Then it will do the rest of work on migrating data from SQL server to Postgres database by executing PDI Job. 

Download Pentaho Data Integration Community Edition and extract the tarball in your local environment.
[http://community.pentaho.com](http://community.pentaho.com)
[https://community.hitachivantara.com/docs/DOC-1009931-downloads](https://community.hitachivantara.com/docs/DOC-1009931-downloads)

Start the spoon.sh to open application GUI in local environment.

```bash
$ cd pentaho/data-integration
$ ./spoon.sh
```

Create connections to both SQL Server and Postgres databases in PDI.

1) Create a New Job.

File => New => Job

2) Create Source Database Connection.

Click View in left sidebar > Right Click ‘Database Connections’ > Choose New > Provide SQL Server connection details

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/sqlserver-database-connection.png" alt="SQL Server Database" />

3) Create Destination Database Connection

Click View in left sidebar -> Right Click ‘Database Connections’ -> Choose New -> Provide Postgres connection details

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/postgres-database-connection.png" alt="PostgreSQL Database" />

4) From Wizard menu, choose Copy Tables Wizard…

Tools -> Wizard -> Copy Tables

5) Choose Source and Destination databases

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/source-destination.png" alt="Source and Destination" />

6) Select the list of tables to migrate

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/source-destination.png" alt="Source and Destination" />

7) Move forward to choose the path for job and transformation files

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/create-job.png" alt="Create Job" />

8) The transformations were created to copy data from source to destination database. 

<img src="/blog/2019/01/23/how-to-migrate-from-sql-server-to-postgresql/job-view.png" alt="Job Steps" />

9) Copy the Pentaho Data Integration tar ball and job with transformations to Postgres server to avoid network latency on data migration.

```bash
$ rsync -azP data-integration.zip user@server:
$ tar -cvzf pdi-migration-job.tar.gz pdi-migration-job/
$ scp pdi-migration-job.tar.gz user@server:
```

10) Check Postgres server to SQL Server database access [based on architecture design at your end].
Establish ssh tunneling to connect SQL Server through application server

```bash
$ cat config 
host tunnel-server
    Hostname <application_server>
    Port 22
    User root
    LocalForward 1433 <ipaddress>:1433

$ ssh tunnel-server
$ telnet localhost 1433
```

#### PDI Job Execution
Execute PDI job using Pentaho kitchen utility in Database Server. Add a kettle configuration to avoid Pentaho consider empty as null values which affects not-null constraint

```bash
$ cat .kettle/kettle.properties 
KETTLE_EMPTY_STRING_DIFFERS_FROM_NULL=Y
```

Ensure IP address for database servers connection and execute the job using kitchen.sh which is a command line utility to execute PDI jobs

```bash
$ ./kitchen.sh -file="/path/to/pdi-migration-job.kjb" -level=Basic | tee pdi-migration-job.log

The data migration process took around 30 minutes to copy 10GB of data from SQL Server to Postgres database over network. 
Output
2018/08/23 11:16:52 - SQLServerToPostgres20180823 - Job execution finished
2018/08/23 11:16:52 - Kitchen - Finished!
2018/08/23 11:16:52 - Kitchen - Start=2018/08/23 10:51:00.701, Stop=2018/08/23 11:16:52.951
2018/08/23 11:16:52 - Kitchen - Processing ended after 25 minutes and 52 seconds (1552 seconds total).
```

We ran into a space problem on copying table with huge in size and handled with reducing the number of rows size in corresponding table transformation file
[Kettle-out-of-memory-error-loading-a-large-fact-table](http://forums.pentaho.com/showthread.php?72409-Kettle-out-of-memory-error-loading-a-large-fact-table)

Fix:

```bash
vi **table_name**.ktr
    <size_rowset>100</size_rowset>

sed 's/<size_rowset>10000<\/size_rowset>/<size_rowset>100<\/size_rowset>/' *table_name*
```
Once data migration is completed, execute after schema-migration script to apply constraints.

```bash
psql -Uuser_name -p5432 -hlocalhost -d database_name -f tables-after.sql
	OR
database_name=# \i /path/to/tables-after.sql
```

#### Migrate Views
Follow the same steps to convert views schema. Right Click Database -> Tasks -> Generate Script -> Export only views

```bash
$ perl sqlserver2pgsql.pl -f views.sql -b views-before.sql -a views-after.sql -u views-unsure.sql
$ psql -Uuser_name -p5432 -hlocalhost -d database_name -f views-unsure.sql
	OR
database_name=# \i /path/to/tables-unsure.sql
```

#### Migrate Functions
The functions migration needs skill and syntax awareness in both SQL Server and Postgres database. The functions needs to validated and tested properly after rewriting for Postgres. Place all rewritten functions into postgres-function.sql and load into database as part of migration process.

### Most Common Errors
* ERROR:  syntax error at or near "["  
Square brackets - Remove square brackets around column and table names.  
SELECT [user_id] => SELECT user_id

* ERROR:  operator does not exist: character varying = integer.  
Type casting on comparison  
AND column_name in (1, -1) => AND column_name in ('1', '-1')

* ERROR:  syntax error at or near ","  
Datatype conversion  
convert(varchar(10),column_name) => column_name::text

* ERROR: column "user_id" of relation "user" does not exist  
No double quotes on integer data type columns  
INSERT INTO user ("user_id") VALUES (1) => INSERT INTO user (user_id) VALUES (1)

* ERROR: column "mm" does not exist  
DATEADD -> INTERVAL  
DATEADD(mm,-6,GETDATE()) => CURRENT_DATE + INTERVAL '-6 month'

* ERROR: column "varchar" does not exist  
Convert Date to USA format  
convert(varchar, tc_agreed_dt, 101) => to_char(CURRENT_TIMESTAMP::TIMESTAMP, 'MM/DD/YYY')

### Result
After migration, we have performed extensive testing on the application and optimised the queries at various modules. Also benchmark test on speed and performance has been completed between improved and existing system. Finally, Postgres migration paid off with promising result of 39.67% average gain on overall performance of the application.

The entire migration was automated with script to test multiple times and reduce manual intervention to perform error free process. The automated script is available to customise based on your scenario.

<a href="/blog/2019/01/23/sqlserver-postgres-migartion-automation-script.sh">sqlserver-postgres-migartion-automation-script.sh</a>